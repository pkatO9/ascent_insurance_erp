import frappe
from frappe import _

def get_or_create_customer(lead_name):
	"""
	Given a Lead name, check if a linked Customer already exists.
	If yes, return the customer name.
	If no, create a new ERPNext Customer from the Lead data and return it.
	"""
	if not lead_name:
		return None

	# Check if Lead already has a linked customer
	existing = frappe.db.get_value("Customer", {"lead_name": lead_name}, "name")
	if existing:
		return existing

	try:
		lead = frappe.get_doc("Lead", lead_name)
		
		# Create Customer
		customer = frappe.new_doc("Customer")
		customer.customer_name = lead.lead_name
		customer.customer_type = "Individual"
		customer.customer_group = "Individual"
		customer.territory = "All Territories"
		customer.lead_name = lead_name
		customer.mobile_no = lead.mobile_no
		customer.email_id = lead.email_id
		customer.insert(ignore_permissions=True)
		
		# Also update the Lead to link to this customer
		frappe.db.set_value("Lead", lead_name, "customer", customer.name)
		
		return customer.name
	except frappe.DuplicateEntryError:
		# Handle duplicate entry gracefully by trying to find the existing one again
		existing = frappe.db.get_value("Customer", {"lead_name": lead_name}, "name")
		if existing:
			return existing
		raise
