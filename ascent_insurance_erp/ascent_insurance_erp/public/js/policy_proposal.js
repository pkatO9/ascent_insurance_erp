frappe.ui.form.on("Policy Proposal", {
	refresh: function(frm) {
		frm.trigger("setup_visibility");
		frm.trigger("add_custom_buttons");
	},
	
	status: function(frm) {
		frm.trigger("setup_visibility");
	},
	
	setup_visibility: function(frm) {
		frm.toggle_display("rejection_reason", frm.doc.status === "Rejected");
		frm.toggle_display("approval_date", ["Approved", "Rejected"].includes(frm.doc.status));
		frm.toggle_display("policy", frm.doc.status === "Approved" && frm.doc.policy);
		
		if (frm.doc.docstatus === 1) {
			frm.disable_save();
		}
	},
	
	add_custom_buttons: function(frm) {
		if (frm.doc.status === "Approved" && !frm.doc.policy && frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Create Policy"), () => {
				frappe.confirm(__("This will create a Policy record from this proposal. Continue?"), () => {
					frappe.call({
						method: "create_policy",
						doc: frm.doc,
						callback: function(r) {
							if (!r.exc) {
								frappe.show_alert(__("Policy created successfully"), 5);
								frm.reload_doc();
							}
						}
					});
				});
			}, __("Actions"));
			frm.change_custom_button_type(__("Create Policy"), __("Actions"), "primary");
		}
		
		if (frm.doc.policy) {
			frm.add_custom_button(__("View Policy"), () => {
				frappe.set_route("Form", "Policy", frm.doc.policy);
			}, __("Actions"));
		}
	},
	
	lead: function(frm) {
		if (frm.doc.lead) {
			frappe.db.get_value("Lead", frm.doc.lead, ["customer", "lead_name"], (r) => {
				if (r) {
					if (r.customer) {
						frm.set_value("customer", r.customer);
						frm.set_df_property("customer", "read_only", 1);
						frm.set_intro(__("Linked Customer found: {0}", [r.customer]), "blue");
					} else {
						frm.set_value("customer", "");
						frm.set_df_property("customer", "read_only", 0);
						frm.set_intro(__("Note: Customer will be auto-created for '{0}' on proposal approval.", [r.lead_name]), "orange");
					}
				}
			});
		} else {
			frm.set_intro(null);
			frm.set_df_property("customer", "read_only", 0);
		}
	},
	
	insurance_quotation: function(frm) {
		if (frm.doc.insurance_quotation) {
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Insurance Quotation",
					name: frm.doc.insurance_quotation
				},
				callback: function(r) {
					if (r.message) {
						let iq = r.message;
						
						// 1. Auto-fill parent fields
						frm.set_value("lead", iq.lead);
						frm.set_value("customer", iq.customer);
						frm.set_value("policy_type", iq.policy_type);
						
						let options = iq.options || [];
						if (options.length === 1) {
							frm.events.apply_option(frm, options[0]);
						} else if (options.length > 1) {
                            let option_list = options.map(opt => {
                                return {
                                    label: `${opt.insurer} - ${opt.plan_name || 'Plan'} (SI: ${opt.sum_insured}, Prem: ${opt.premium})`,
                                    value: opt.name
                                };
                            });
                            
							frappe.prompt([
								{
									label: __("Select Quotation Option"),
									fieldname: "quotation_option",
									fieldtype: "Select",
									options: option_list,
									reqd: 1
								}
							], (values) => {
								let selected_opt = options.find(o => o.name === values.quotation_option);
								frm.events.apply_option(frm, selected_opt);
							}, __("Select Option"), __("Apply"));
						}
					}
				}
			});
		}
	},
	
	apply_option: function(frm, opt) {
		if (opt) {
			frm.doc.insurer = opt.insurer;
			frm.doc.product_type = opt.product_type;
			frm.doc.sum_insured = opt.sum_insured;
			frm.doc.premium = opt.premium;
			frm.refresh_fields(["insurer", "product_type", "sum_insured", "premium"]);
		}
	}
});
