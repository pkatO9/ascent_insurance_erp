frappe.ui.form.on("Policy", {
	refresh: function(frm) {
		frm.trigger("setup_indicators");
		frm.trigger("setup_navigation_buttons");
		frm.trigger("setup_checklist");
		frm.trigger("setup_fetch_commission_button");
	},

	setup_indicators: function(frm) {
		const status_colors = {
			"Draft": "grey",
			"Active": "green",
			"Up for Renewal": "orange",
			"Lapsed": "red",
			"Cancelled": "red",
			"Expired": "red",
			"Renewed": "blue"
		};
		
		if (frm.doc.status) {
			frm.dashboard.add_indicator(__(frm.doc.status), status_colors[frm.doc.status] || "blue");
		}
	},

	setup_navigation_buttons: function(frm) {
		if (frm.doc.proposal) {
			frm.add_custom_button(__("View Proposal"), () => {
				frappe.set_route("Form", "Policy Proposal", frm.doc.proposal);
			}, __("Navigation"));
		}
		if (frm.doc.lead) {
			frm.add_custom_button(__("View Lead"), () => {
				frappe.set_route("Form", "Lead", frm.doc.lead);
			}, __("Navigation"));
		}
		if (frm.doc.customer) {
			frm.add_custom_button(__("View Customer"), () => {
				frappe.set_route("Form", "Customer", frm.doc.customer);
			}, __("Navigation"));
		}
	},

	setup_checklist: function(frm) {
		if (frm.doc.docstatus === 0) {
			let checklist = [];
			
			const check = (val) => val ? '<span style="color: green;">✓</span>' : '<span style="color: red;">✗</span>';
			
			checklist.push(`${check(frm.doc.policy_number)} Policy Number`);
			checklist.push(`${check(frm.doc.members && frm.doc.members.length > 0)} Members`);
			checklist.push(`${check(frm.doc.policy_document)} PDF Attached`);
			checklist.push(`${check(frm.doc.commission_rate > 0)} Commission Rate`);
			
			let html = `<div style="font-weight: bold;">Checklist: ${checklist.join(' | ')}</div>`;
			frm.set_intro(html, "blue");
		}
	},

	setup_fetch_commission_button: function(frm) {
		if (frm.doc.docstatus === 0) {
			frm.set_df_property("commission_rate", "field_helper", {
				label: __("Fetch Commission Rate"),
				onclick: () => {
					if (!frm.doc.insurer || !frm.doc.plan_name) {
						frappe.msgprint(__("Please select Insurer and Plan Name first."));
						return;
					}
					
					frappe.call({
						method: "ascent_insurance_erp.ascent_insurance_erp.doctype.policy.policy.get_commission_rate",
						args: {
							insurer: frm.doc.insurer,
							product_type: frm.doc.product_type
						},
						callback: function(r) {
							if (r.message !== null && r.message !== undefined) {
								frm.set_value("commission_rate", r.message);
								frappe.show_alert(__("Commission rate fetched: {0}%", [r.message]));
							} else {
								frappe.msgprint(__("No commission structure found for this insurer and product for current month."));
							}
						}
					});
				}
			});
		}
	},

	gross_premium: function(frm) {
		frm.trigger("calculate_premiums");
		frm.trigger("calculate_commission");
	},

	commission_rate: function(frm) {
		frm.trigger("calculate_commission");
	},

	calculate_premiums: function(frm) {
		if (frm.doc.gross_premium) {
			let gst = flt(frm.doc.gross_premium) * 0.18;
			frm.set_value("gst_amount", gst);
			frm.set_value("net_premium", flt(frm.doc.gross_premium) - gst);
		}
	},

	calculate_commission: function(frm) {
		if (frm.doc.gross_premium && frm.doc.commission_rate) {
			let amount = flt(frm.doc.gross_premium) * flt(frm.doc.commission_rate) / 100;
			frm.set_value("commission_amount", amount);
		}
	},

	start_date: function(frm) {
		frm.trigger("calculate_dates");
	},

	end_date: function(frm) {
		frm.trigger("calculate_dates");
	},

	calculate_dates: function(frm) {
		if (frm.doc.start_date && frm.doc.end_date) {
			// Policy Term
			let d1 = moment(frm.doc.start_date);
			let d2 = moment(frm.doc.end_date);
			let years = d2.diff(d1, 'years', true);
			frm.set_value("policy_term", Math.round(years));
			
			// Renewal Date
			let renewal_date = frappe.datetime.add_days(frm.doc.end_date, -30);
			frm.set_value("renewal_date", renewal_date);
		}
	},

	validate: function(frm) {
		// Mandatory completeness check before submit
		// The user said "before_save (when docstatus is moving to submit)"
		// In Frappe JS, validate runs before save. We can check frm.doc.docstatus or the intended action.
		// Standard way to catch submission is to use before_submit, but user asked for before_save with checks.
		
		if (frm.doc.docstatus === 1) { // This is triggered during SUBMIT
			let missing = [];
			
			if (!frm.doc.policy_number) missing.push(__("Policy Number"));
			if (!frm.doc.policy_document) missing.push(__("Policy PDF Attachment"));
			if (!frm.doc.members || frm.doc.members.length === 0) missing.push(__("At least one Member"));
			if (!frm.doc.start_date || !frm.doc.end_date) missing.push(__("Policy Dates"));
			if (!(frm.doc.commission_rate > 0)) missing.push(__("Commission Rate"));
			
			if (missing.length > 0) {
				frappe.throw({
					title: __("Missing Mandatory Details for Submission"),
					message: __("Please fill the following before submitting:\n") + "<ul><li>" + missing.join("</li><li>") + "</li></ul>"
				});
			}
		}
	}
});

frappe.ui.form.on("Policy Member Detail", {
	dob: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.dob) {
			let dob = moment(row.dob);
			let today = moment();
			let age = today.diff(dob, 'years');
			frappe.model.set_value(cdt, cdn, "age", age);
		}
	}
});
