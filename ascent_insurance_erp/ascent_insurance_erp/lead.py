import frappe
from frappe import _

def validate(doc, method):
    """
    Called via hooks.py doc_events on Lead validate
    """
    validate_status_transition(doc)
    validate_insurance_fields(doc)

def validate_status_transition(doc):
    if doc.is_new():
        if doc.status != "New":
            doc.status = "New" # Force New for new records
        return

    # Get the value from DB to compare
    old_status = frappe.db.get_value("Lead", doc.name, "status")
    
    if not old_status or old_status == doc.status:
        return

    # Define logical transitions: New → Contacted → Quotation Sent → Policy Proposal → Converted/Lost
    transitions = {
        "New": ["Contacted"],
        "Contacted": ["Quotation Sent"],
        "Quotation Sent": ["Policy Proposal"],
        "Policy Proposal": ["Converted", "Lost"],
        "Converted": [], # Terminal state
        "Lost": [] # Terminal state
    }

    allowed_next = transitions.get(old_status, [])
    
    if doc.status not in allowed_next:
        frappe.throw(
            _("Invalid Status Transition: {0} cannot move to {1}. Expected next stage: {2}").format(
                frappe.bold(old_status), 
                frappe.bold(doc.status), 
                ", ".join([frappe.bold(s) for s in allowed_next]) if allowed_next else _("None (Terminal State)")
            )
        )

def validate_insurance_fields(doc):
    # Requirement: policy_type_of_interest should be mandatory ONLY after initial save
    if not doc.is_new():
        if not doc.get("policy_type_of_interest"):
            frappe.throw(
                _("Field {0} is mandatory after initial lead creation").format(
                    frappe.bold(_("Policy Type of Interest"))
                ),
                frappe.MandatoryError
            )
