import frappe
from frappe import _
from frappe.model.document import Document

class Agent(Document):
    def validate(self):
        self.validate_license_for_type()
        self.validate_linked_user()
        self.validate_commission_rate()

    def validate_license_for_type(self):
        licensed_types = ["POSP", "Individual Agent", "DSA / Corporate Agent", "Broker"]
        if self.agent_type in licensed_types:
            if not self.irdai_license_no:
                frappe.msgprint(
                    _("IRDAI License No. is recommended for agent type '{0}'.").format(self.agent_type),
                    indicator="orange",
                    title=_("License Missing")
                )
            if self.license_expiry:
                from frappe.utils import getdate, today
                if getdate(self.license_expiry) < getdate(today()):
                    frappe.msgprint(
                        _("IRDAI License for {0} has expired on {1}. Please renew.").format(
                            self.agent_name, self.license_expiry
                        ),
                        indicator="red",
                        title=_("License Expired")
                    )

    def validate_linked_user(self):
        # Only Internal Staff should have a linked user
        if self.linked_user and self.agent_type != "Internal Staff":
            frappe.msgprint(
                _("Linked User (ERP login) is typically only for Internal Staff. "
                "External agents are tracked without a login."),
                indicator="orange",
                title=_("Note")
            )
        # Ensure no two agents share the same linked_user
        if self.linked_user:
            existing = frappe.db.get_value(
                "Agent",
                {"linked_user": self.linked_user, "name": ("!=", self.name)},
                "name"
            )
            if existing:
                frappe.throw(
                    _("User '{0}' is already linked to agent '{1}'. "
                    "Each ERP user can only be linked to one Agent record.").format(
                        self.linked_user, existing
                    )
                )

    def validate_commission_rate(self):
        if self.commission_rate and (self.commission_rate < 0 or self.commission_rate > 100):
            frappe.throw(_("Commission rate must be between 0 and 100."))
