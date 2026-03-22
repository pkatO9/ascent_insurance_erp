import frappe
from frappe.model.document import Document
from frappe.utils import today

class LeadEnquiry(Document):

    def validate(self):
        self.validate_status_transition()
        self.auto_set_converted_on()

    def validate_status_transition(self):
        if not self.is_new():
            old_status = frappe.db.get_value(
                "Lead Enquiry", self.name, "status"
            )
            if old_status in ["Converted", "Lost"] \
                    and self.status != old_status:
                frappe.throw(
                    f"Cannot change status from '{old_status}'. "
                    f"Create a new Lead Enquiry for this client if needed."
                )

    def auto_set_converted_on(self):
        if self.status == "Converted" and not self.converted_on:
            self.converted_on = today()

    def on_update(self):
        self.share_with_ops_person()
        self.auto_fill_ops_from_agent()

    def auto_fill_ops_from_agent(self):
        """
        If assigned_ops is empty and the Sales Agent has an ERP user,
        auto-fill assigned_ops with that user.
        """
        if self.sales_agent and not self.assigned_ops:
            agent_user = frappe.db.get_value(
                "Sales Agent", self.sales_agent, "user"
            )
            if agent_user:
                self.db_set("assigned_ops", agent_user)

    def share_with_ops_person(self):
        """
        When assigned_ops is set, give read access via DocShare.
        Skip if ops person is already the sales agent's own user
        (same person — they already have access as owner).
        """
        if not self.assigned_ops:
            return

        # Check if this user is the sales agent themselves
        agent_user = frappe.db.get_value(
            "Sales Agent", self.sales_agent, "user"
        ) if self.sales_agent else None

        if agent_user and agent_user == self.assigned_ops:
            return  # Same person — no need to add share

        existing = frappe.db.exists("DocShare", {
            "share_doctype": "Lead Enquiry",
            "share_name": self.name,
            "user": self.assigned_ops
        })
        if not existing:
            frappe.share.add(
                "Lead Enquiry",
                self.name,
                user=self.assigned_ops,
                read=1,
                write=0,
                share=0,
                notify=1
            )
