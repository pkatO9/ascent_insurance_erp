import frappe
from frappe import _, ValidationError
from frappe.model.document import Document
from frappe.utils import today

from ascent_insurance_erp.ascent_insurance_erp.utils.customer_utils import get_or_create_customer

class PolicyProposal(Document):
	def validate(self):
		# Fetch customer silently
		if self.lead:
			self.customer = get_or_create_customer(self.lead)

		if self.status == "Approved" and not self.approval_date:
			frappe.throw(_("Please set the Approval Date before marking as Approved."), frappe.ValidationError)
		
		if self.status == "Rejected" and not self.rejection_reason:
			frappe.throw(_("Please provide a Rejection Reason."), frappe.ValidationError)
		
		if self.status == "Rejected":
			old_doc = self.get_doc_before_save()
			if old_doc and old_doc.status != "Rejected":
				if self.lead:
					frappe.db.set_value("Lead", self.lead, "status", "Quotation Sent")
					
		if self.has_value_changed("status"):
			old_doc = self.get_doc_before_save()
			if old_doc and old_doc.status == "Approved" and self.status in ["Draft", "Submitted"]:
				frappe.throw(_("A proposal cannot move from Approved back to Draft or Submitted"), frappe.ValidationError)

	def on_submit(self):
		if self.status not in ("Approved", "Rejected"):
			frappe.throw(_("Status must be either Approved or Rejected before submitting."))
			
		if self.status == "Approved":
			self.create_policy()

	def on_update(self):
		if self.status == "Submitted" and not self.submission_date:
			self.db_set("submission_date", today())

	@frappe.whitelist()
	def create_policy(self):
		if self.policy:
			frappe.msgprint(_("Policy {0} is already created for this proposal.").format(self.policy))
			return
			
		new_policy = frappe.new_doc("Policy")
		new_policy.proposal = self.name
		new_policy.lead = self.lead
		new_policy.customer = self.customer
		new_policy.insurer = self.insurer
		new_policy.policy_type = self.policy_type
		new_policy.product_type = self.product_type
		new_policy.sum_insured = self.sum_insured
		new_policy.agent = self.agent
		new_policy.insurance_quotation = self.insurance_quotation
		new_policy.status = "Draft"
		
		if self.insurance_quotation:
			iq = frappe.get_doc("Insurance Quotation", self.insurance_quotation)
			if iq.get("members"):
				for m in iq.members:
					new_policy.append("members", {
						k: v for k, v in m.as_dict().items() 
						if k not in ('name', 'parent', 'parenttype', 'parentfield', 'creation', 'modified', 'modified_by', 'owner', 'idx', 'docstatus')
					})

		new_policy.insert(ignore_permissions=True)
		
		self.db_set("policy", new_policy.name)
		self.policy = new_policy.name
		
		frappe.msgprint(_("Policy {0} created. Please complete the policy details.").format(new_policy.name))

# Hook wrappers for doc_events registration
def validate_hook(doc, method=None):
	pass

def on_submit_hook(doc, method=None):
	pass

def on_update_hook(doc, method=None):
	pass
