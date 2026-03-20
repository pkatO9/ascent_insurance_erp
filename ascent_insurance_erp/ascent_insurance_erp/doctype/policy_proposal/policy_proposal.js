frappe.ui.form.on("Policy Proposal", {
	lead: function(frm) {
		if (frm.doc.lead) {
			frappe.db.get_value("Insurance Quotation", 
				{ "lead": frm.doc.lead, "status": "Accepted" }, 
				["name", "insurer", "policy_type", "product_type", "sum_insured"], 
				(r) => {
					if (r && r.name) {
						frm.set_value("insurance_quotation", r.name);
						frm.set_value("insurer", r.insurer);
						frm.set_value("policy_type", r.policy_type);
						frm.set_value("product_type", r.product_type);
						frm.set_value("sum_insured", r.sum_insured);
					}
				}
			);
		}
	}
});
