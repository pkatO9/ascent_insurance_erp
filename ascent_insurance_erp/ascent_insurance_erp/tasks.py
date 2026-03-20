import frappe
from frappe.utils import today, add_days

def update_policy_statuses():
	"""Run daily. Updates policy status based on dates."""
	try:
		current_today = today()
		thirty_days_later = add_days(current_today, 30)
		
		# 1. MARK AS UP FOR RENEWAL:
		# Find all Active policies where end_date is within 30 days from today AND status == "Active"
		renewed_policies = frappe.get_all("Policy", filters={
			"status": "Active",
			"end_date": ["<=", thirty_days_later],
			"end_date": [">=", current_today]
		}, fields=["name"])
		
		renewed_count = 0
		for d in renewed_policies:
			frappe.db.set_value("Policy", d.name, "status", "Up for Renewal")
			renewed_count += 1
		
		# 2. MARK AS EXPIRED:
		# Find all policies where end_date < today AND status in ["Active", "Up for Renewal"]
		expired_policies = frappe.get_all("Policy", filters={
			"status": ["in", ["Active", "Up for Renewal"]],
			"end_date": ["<", current_today]
		}, fields=["name"])
		
		expired_count = 0
		for d in expired_policies:
			frappe.db.set_value("Policy", d.name, "status", "Expired")
			expired_count += 1
			
		# 3. Commit after batch updates
		frappe.db.commit()
		
		# 4. Log summary
		frappe.logger().info(f"Policy status update: {renewed_count} marked Up for Renewal, {expired_count} marked Expired")
		
	except Exception:
		frappe.db.rollback()
		frappe.log_error("Policy Status Update Task Failed")
