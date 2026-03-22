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
	}
});
