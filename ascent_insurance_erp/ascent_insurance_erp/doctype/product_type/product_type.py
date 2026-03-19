import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class ProductType(Document):
	def validate(self):
		self.validate_uniqueness()
		self.update_last_updated()

	def validate_uniqueness(self):
		# Ensure product_name + insurer is unique
		if frappe.db.exists("Product Type", {
			"product_name": self.product_name,
			"insurer": self.insurer,
			"name": ["!=", self.name]
		}):
			frappe.throw(frappe._("Product '{0}' already exists for insurer '{1}'").format(self.product_name, self.insurer))

	def update_last_updated(self):
		self.last_updated = now_datetime()
