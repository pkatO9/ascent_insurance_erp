frappe.ui.form.on('Lead', {
    refresh: function(frm) {
        // Requirement: policy_type_of_interest should be mandatory ONLY after initial save
        if (!frm.is_new()) {
            frm.set_df_property('policy_type_of_interest', 'reqd', 1);
        } else {
            frm.set_df_property('policy_type_of_interest', 'reqd', 0);
        }
        
        // Ensure status field is read-only for non-System Managers to enforce pipeline
        // (Optional, user didn't ask but it's good practice for pipelines)
        // if (frappe.session.user !== 'Administrator' && !frappe.user_roles.includes('System Manager')) {
        //    frm.set_df_property('status', 'read_only', 1);
        // }
    }
});
