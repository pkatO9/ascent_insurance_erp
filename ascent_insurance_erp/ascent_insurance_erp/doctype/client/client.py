import frappe
from frappe.model.document import Document

class Client(Document):
	def validate(self):
		self.calculate_age()
		self.validate_pan()
		self.validate_gstin()

	def calculate_age(self):
		if self.dob:
			from frappe.utils import date_diff, getdate, today
			age_days = date_diff(today(), self.dob)
			self.age = int(age_days / 365.25)

	def validate_pan(self):
		if self.pan_number:
			import re
			pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
			if not re.match(pan_pattern, self.pan_number.upper()):
				frappe.throw("PAN Number format is invalid. Expected format: ABCDE1234F")
			self.pan_number = self.pan_number.upper()

	def validate_gstin(self):
		if self.gstin:
			import re
			gstin_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
			if not re.match(gstin_pattern, self.gstin.upper()):
				frappe.throw("GSTIN format is invalid. Please check and re-enter.")
			self.gstin = self.gstin.upper()

@frappe.whitelist()
def get_or_create_customer(client_name):
	"""
	Called when a policy is first issued for this client.
	Creates an ERPNext Customer and links it back to the Client record.
	Returns the Customer name.
	"""
	client = frappe.get_doc("Client", client_name)

	if client.linked_customer:
		return client.linked_customer

	customer = frappe.new_doc("Customer")
	customer.customer_name = (
		client.company_name if client.client_type in ["Corporate", "HUF"]
		else client.full_name
	)
	customer.customer_type = (
		"Company" if client.client_type in ["Corporate", "HUF"]
		else "Individual"
	)
	customer.customer_group = "Individual"
	customer.territory = "All Territories"
	customer.mobile_no = client.mobile
	customer.email_id = client.email
	customer.insert(ignore_permissions=True)

	frappe.db.set_value("Client", client_name, "linked_customer", customer.name)
	frappe.db.commit()

	return customer.name
