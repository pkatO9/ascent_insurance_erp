frappe.ui.form.on("Plan Name", {
	setup(frm) {
		frm.set_query("policy_type", () => {
			return {
				filters: {
					lob: frm.doc.lob
				}
			};
		});
	},
	lob(frm) {
		// Clear policy_type if LOB changes
		frm.set_value("policy_type", "");
	},

	plan_options_add: function(frm) {
		show_option_summary(frm);
	},

	plan_options_remove: function(frm) {
		show_option_summary(frm);
	}
});

frappe.ui.form.on("Plan Option", {
	is_active: function(frm) {
		show_option_summary(frm);
	}
});

function show_option_summary(frm) {
	// Use dashboard indicator instead of set_intro for reliability
	frm.dashboard.clear_headline();

	const options = frm.doc.plan_options || [];
	const total = options.length;
	const active = options.filter(o => o.is_active).length;

	if (total === 0) {
		frm.set_intro(
			"No plan options added yet. Add at least one option so agents "
			+ "can select this plan in quotations.",
			"red"
		);
		frm.dashboard.add_indicator("No active options", "red");
		return;
	}

	// Clear any previous intro
	frm.set_intro("");

	if (active === 0) {
		frm.dashboard.add_indicator(
			`0 of ${total} options active`, "red"
		);
	} else {
		frm.dashboard.add_indicator(
			`${active} of ${total} option(s) active`, "green"
		);
	}
}

