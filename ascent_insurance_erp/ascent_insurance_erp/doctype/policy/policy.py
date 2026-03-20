import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import date_diff, add_days, getdate, nowdate, flt
from dateutil.relativedelta import relativedelta

class Policy(Document):
	def validate(self):
		self.calculate_member_ages()
		self.calculate_premiums()
		self.calculate_dates()
		self.validate_dates()
		self.validate_members()
		self.fetch_commission_rate()
		self.calculate_commission()

	def calculate_member_ages(self):
		"""AUTO-CALCULATE AGE for each member using frappe.utils.date_diff"""
		today = getdate(nowdate())
		for member in self.members:
			if member.dob:
				dob = getdate(member.dob)
				# Simple age calculation in years
				diff = date_diff(today, dob)
				member.age = int(diff / 365.25)

	def calculate_premiums(self):
		"""AUTO-CALCULATE GST and Net Premium"""
		if self.gross_premium:
			# Standard GST for insurance is 18%
			# gross_premium is inclusive of GST? 
			# User says: gst_amount = gross_premium * 0.18, net_premium = gross_premium - gst_amount
			# This implies gross_premium is the total amount paid by user.
			self.gst_amount = flt(self.gross_premium) * 0.18
			self.net_premium = flt(self.gross_premium) - self.gst_amount

	def calculate_dates(self):
		"""AUTO-CALCULATE policy_term and renewal_date"""
		if self.start_date and self.end_date:
			# policy_term = year difference between start_date and end_date (rounded)
			d1 = getdate(self.start_date)
			d2 = getdate(self.end_date)
			diff = relativedelta(d2, d1)
			self.policy_term = diff.years
			
			# renewal_date = end_date minus 30 days
			self.renewal_date = add_days(self.end_date, -30)

	def validate_dates(self):
		"""VALIDATE dates: end_date must be after start_date"""
		if self.start_date and self.end_date:
			if getdate(self.end_date) <= getdate(self.start_date):
				frappe.throw(_("Policy End Date must be after Policy Start Date"))

	def validate_members(self):
		"""VALIDATE members: at least one member required for health insurance policies"""
		if self.policy_type:
			policy_type_name = frappe.db.get_value("Policy Type", self.policy_type, "name")
			if policy_type_name and "Health" in policy_type_name:
				if not self.members:
					frappe.throw(_("At least one member is required for Health Insurance policies"))

	def fetch_commission_rate(self):
		"""FETCH COMMISSION RATE if commission_rate is 0 or empty"""
		if not self.commission_rate:
			rate = get_commission_rate(self.insurer, self.product_type)
			if rate:
				self.commission_rate = rate
			else:
				frappe.msgprint(_("No active commission structure found for this insurer/product. Please set commission rate manually."), indicator="orange")

	def calculate_commission(self):
		"""AUTO-CALCULATE: commission_amount = gross_premium * commission_rate / 100"""
		if self.gross_premium and self.commission_rate:
			self.commission_amount = flt(self.gross_premium) * flt(self.commission_rate) / 100

	def on_submit(self):
		"""On Submit hooks"""
		self.db_set("status", "Active")
		
		# Update linked Lead status to "Converted"
		if self.lead:
			frappe.db.set_value("Lead", self.lead, "status", "Converted")
		
		frappe.msgprint(_("Policy activated successfully."))

	def on_cancel(self):
		"""On Cancel hooks"""
		self.db_set("status", "Cancelled")
		
		# Commission validation
		if self.commission_status in ["Invoiced", "Settled"]:
			frappe.throw(_("Cannot cancel a policy with invoiced or settled commission. Contact accounts."))

@frappe.whitelist()
def get_commission_rate(insurer, product_type):
	"""Query Commission Structure child table for matching insurer + product_type + current month"""
	if not insurer or not product_type:
		return None
		
	# Check if Commission Structure DocType exists first to avoid errors
	if not frappe.db.exists("DocType", "Commission Structure"):
		return None

	# User says: "Query active Commission Structure for self.insurer, self.product_type, current month/year"
	# Assuming a DocType named "Commission Structure" with a child table or fields.
	# Since it doesn't exist yet, I'll provide a generic implementation that returns None for now.
	# The logic would be:
	# structures = frappe.get_all("Commission Structure", filters={"insurer": insurer, "is_active": 1})
	# for s in structures:
	#     # find matching row for product_type...
	return None
