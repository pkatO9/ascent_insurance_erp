import frappe
from frappe import _
from frappe.model.document import Document

class InsuranceQuotation(Document):
	def validate(self):
		self.validate_members()
		self.validate_options()
		self.validate_premiums()

	def validate_members(self):
		"""At least 1 member required"""
		if not self.members:
			frappe.throw(_("At least 1 member required in the quotation."))

	def validate_options(self):
		"""At least 3 options required before status = 'Sent'"""
		if self.status == "Sent" and len(self.options) < 3:
			frappe.throw(_("At least 3 quotation options are required before status can be set to 'Sent'."))

	def validate_premiums(self):
		"""Premium must be > 0 and mandatory fields for options"""
		for d in self.options:
			if not d.insurer or not d.plan_name:
				frappe.throw(_("Insurer and Plan Name are mandatory for all options in Row #{0}").format(d.idx))
			if d.premium <= 0:
				frappe.throw(_("Premium must be greater than 0 for option from {0} in Row #{1}").format(d.insurer, d.idx))

@frappe.whitelist()
def email_quotation(docname, to_email, message=None):
	doc = frappe.get_doc("Insurance Quotation", docname)
	
	if not message:
		message = _("Please find attached the health insurance premium comparison for {0}.").format(doc.proposer_name)
	
	# Generate PDF
	print_format = "Health Insurance Quotation"
	pdf_content = frappe.get_print("Insurance Quotation", docname, print_format, as_pdf=True)
	
	filename = _("Quotation_{0}.pdf").format(docname)
	
	# Send Email
	frappe.sendmail(
		recipients=[to_email],
		subject=_("Insurance Quotation: {0}").format(docname),
		message=message,
		attachments=[{
			"fname": filename,
			"fcontent": pdf_content
		}],
		reference_doctype="Insurance Quotation",
		reference_name=docname,
		delayed=False
	)
	
	# Update status if Draft
	if doc.status == "Draft":
		doc.status = "Sent"
		doc.save()
	
	return True
