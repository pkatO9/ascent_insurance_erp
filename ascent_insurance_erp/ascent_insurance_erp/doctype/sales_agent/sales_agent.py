import frappe
from frappe import _
from frappe.model.document import Document

class SalesAgent(Document):
    def validate(self):
        self.validate_user_unique()
        self.validate_commission_rate()
        self.validate_license()

    def validate_user_unique(self):
        existing = frappe.db.get_value(
            "Sales Agent",
            {"user": self.user, "name": ("!=", self.name)},
            "name"
        )
        if existing:
            frappe.throw(
                _("User '{0}' is already linked to Sales Agent '{1}'. Each user can only be one Sales Agent.").format(
                    self.user, existing
                )
            )

    def validate_commission_rate(self):
        if not self.commission_rate or self.commission_rate <= 0:
            frappe.throw(
                _("Commission Rate is mandatory for Sales Agents. Please enter the negotiated commission percentage.")
            )
        if self.commission_rate > 100:
            frappe.throw(_("Commission rate cannot exceed 100%."))

    def validate_license(self):
        if self.license_expiry:
            from frappe.utils import getdate, today
            if getdate(self.license_expiry) < getdate(today()):
                frappe.msgprint(
                    _("IRDAI License for {0} expired on {1}. Please renew.").format(
                        self.sales_agent_name, self.license_expiry
                    ),
                    indicator="red",
                    title=_("License Expired")
                )
