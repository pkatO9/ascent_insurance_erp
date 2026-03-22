import frappe
from frappe.model.document import Document

class PolicyType(Document):
	def validate(self):
		if not self.lob:
			frappe.throw("Line of Business (LOB) is mandatory for Policy Type.")
