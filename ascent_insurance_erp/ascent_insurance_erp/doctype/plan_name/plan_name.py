import frappe
from frappe.model.document import Document

class PlanName(Document):
	def validate(self):
		# Ensure the selected policy type belongs to the selected LOB
		if self.policy_type and self.lob:
			policy_type_lob = frappe.db.get_value("Policy Type", self.policy_type, "lob")
			if policy_type_lob != self.lob:
				frappe.throw(
					"The selected Policy Type '{0}' does not belong to the Line of Business '{1}'. "
					"It belongs to '{2}'.".format(self.policy_type, self.lob, policy_type_lob)
				)
		
		# Ensure at least one active plan option exists before marking active
		if self.is_active:
			active_options = [o for o in self.plan_options if o.is_active]
			if not active_options:
				frappe.msgprint(
					"Warning: This plan has no active Plan Options. "
					"Agents will not be able to select it in quotations.",
					indicator="orange"
				)
