import frappe
from frappe import _

def get_or_create_customer(lead_name):
	if not lead_name:
		return None
		
	# Check if a customer is already linked to this lead
	customer = frappe.db.get_value("Customer", {"lead_name": lead_name}, "name")
	if customer:
		return customer
		
	lead = frappe.get_doc("Lead", lead_name)
	
	# Check by email if available
	if lead.get("email_id"):
		customer = frappe.db.get_value("Customer", {"email_id": lead.email_id}, "name")
		if customer:
			return customer
			
	# Create new customer
	new_cust = frappe.new_doc("Customer")
	new_cust.customer_name = lead.lead_name or lead.name
	new_cust.customer_type = "Individual"
	new_cust.customer_group = _("All Customer Groups")
	new_cust.territory = _("All Territories")
	new_cust.lead_name = lead.name
	new_cust.email_id = lead.get("email_id")
	new_cust.mobile_no = lead.get("mobile_no")
	new_cust.insert(ignore_permissions=True)
	
	return new_cust.name
