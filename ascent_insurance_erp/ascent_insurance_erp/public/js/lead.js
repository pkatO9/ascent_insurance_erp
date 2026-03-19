frappe.ui.form.on('Lead', {
    refresh: function(frm) {
        // Requirement: policy_type_of_interest should be mandatory ONLY after initial save
        if (!frm.is_new()) {
            frm.set_df_property('policy_type_of_interest', 'reqd', 1);
        } else {
            frm.set_df_property('policy_type_of_interest', 'reqd', 0);
        }
    },
    
    policy_type_of_interest: function(frm) {
        if (frm.doc.policy_type_of_interest) {
            frappe.show_alert({
                message: __("Selected Policy Type: {0}", [frm.doc.policy_type_of_interest]),
                indicator: 'green'
            });
        }
    },
    
    mobile_no: function(frm) {
        // Optional formatting for mobile number (basic check)
        if (frm.doc.mobile_no && !/^[0-9+]{10,15}$/.test(frm.doc.mobile_no)) {
            frappe.msgprint(__("Please enter a valid mobile number (10-15 digits)"));
        }
    }
});
