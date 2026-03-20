import frappe
from frappe import _
from frappe.model.document import Document

class Policy(Document):
	def validate(self):
		self.calculate_gst()
		self.validate_payment_details()
		self.sync_dates()

	def calculate_gst(self):
		gst_percent = self.gst_percent or 18
		basic_od = self.basic_od or 0
		net_premium = self.net_premium or 0
		
		gst_amount = (basic_od + net_premium) * gst_percent / 100
		self.gst_amount = gst_amount
		self.net_gst_amount = gst_amount

	def validate_payment_details(self):
		if self.payment_mode == "Cheque" and not self.chq_no:
			frappe.throw(_("Please enter Cheque No. for cheque payments"))

	def sync_dates(self):
		if self.risk_date and not self.start_date:
			self.start_date = self.risk_date
