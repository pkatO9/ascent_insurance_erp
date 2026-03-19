import frappe
from frappe import _

def validate(doc, method):
    """
    Called via hooks.py doc_events on Lead validate
    """
    validate_status_transition(doc)
    validate_insurance_fields(doc)
    validate_owner(doc)
    track_assignment_history(doc)

def before_insert(doc, method):
    """
    Auto-assign lead_owner to the current logged-in user if not set
    """
    if not doc.get("lead_owner"):
        doc.lead_owner = frappe.session.user

def validate_owner(doc):
    """
    Ensure lead_owner is always set
    """
    if not doc.get("lead_owner"):
        # If it's still empty (e.g. cleared manually), force current user or throw error
        if frappe.session.user != "Guest":
            doc.lead_owner = frappe.session.user
        else:
            frappe.throw(_("Lead Owner is mandatory"), frappe.MandatoryError)

def track_assignment_history(doc):
    """
    Detect lead_owner change and log to Lead Assignment History child table
    """
    if doc.is_new():
        # Optional: log initial assignment
        add_history_row(doc, None, doc.lead_owner)
        return

    old_owner = frappe.db.get_value("Lead", doc.name, "lead_owner")
    
    if old_owner and old_owner != doc.lead_owner:
        add_history_row(doc, old_owner, doc.lead_owner)
        notify_new_owner(doc, doc.lead_owner)

def add_history_row(doc, previous_owner, new_owner):
    doc.append("ascent_assignment_history", {
        "previous_owner": previous_owner,
        "new_owner": new_owner,
        "changed_by": frappe.session.user,
        "changed_on": frappe.utils.now_datetime()
    })

def notify_new_owner(doc, new_owner):
    """
    Notify the new owner about the assignment
    """
    if not new_owner or new_owner == "Guest":
        return
        
    subject = _("New Lead Assigned: {0}").format(doc.lead_name or doc.name)
    message = _("A new lead has been assigned to you: {0}").format(frappe.bold(doc.lead_name or doc.name))
    
    # Send internal notification using Notification Log if available, or just email
    try:
        if frappe.db.exists("DocType", "Notification Log"):
            from frappe.desk.doctype.notification_log.notification_log import enqueue_create_notification
            enqueue_create_notification(new_owner, {
                "subject": subject,
                "email_content": message,
                "document_type": "Lead",
                "document_name": doc.name,
                "from_user": frappe.session.user
            })
    except Exception:
        # Fallback to email
        frappe.sendmail(
            recipients=[new_owner],
            subject=subject,
            message=message,
            reference_doctype="Lead",
            reference_name=doc.name
        )

def validate_status_transition(doc):
    if doc.is_new():
        if doc.status != "New":
            doc.status = "New"
        return

    if not doc.has_value_changed("status"):
        return

    # Use _doc_before_save if available, fallback to DB
    old_status = getattr(doc, "_doc_before_save", None)
    if old_status:
        old_status = old_status.status
    else:
        old_status = frappe.db.get_value("Lead", doc.name, "status")
    
    if not old_status or old_status == doc.status:
        return

    # Valid transitions mapping
    valid_transitions = {
        "New": ["Contacted", "Lost"],
        "Contacted": ["Quotation Sent", "Lost"],
        "Quotation Sent": ["Policy Proposal", "Lost"],
        "Policy Proposal": ["Converted", "Lost"]
    }

    allowed_next = valid_transitions.get(old_status, [])
    
    if doc.status not in allowed_next:
        frappe.throw(
            _("Invalid Status Transition: {0} cannot move to {1}. Expected next stage: {2}").format(
                frappe.bold(old_status), 
                frappe.bold(doc.status), 
                ", ".join([frappe.bold(s) for s in allowed_next]) if allowed_next else _("None")
            )
        )


def validate_insurance_fields(doc):
    if not doc.is_new():
        if not doc.get("policy_type_of_interest"):
            frappe.throw(
                _("Field {0} is mandatory after initial lead creation").format(
                    frappe.bold(_("Policy Type of Interest"))
                ),
                frappe.MandatoryError
            )

