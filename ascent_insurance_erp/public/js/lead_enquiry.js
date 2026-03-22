frappe.ui.form.on("Lead Enquiry", {

    refresh: function(frm) {
        apply_filters(frm);
        show_status_indicator(frm);
        show_action_buttons(frm);
    },

    lob: function(frm) {
        frm.set_value("policy_type", "");
        apply_filters(frm);
    },

    sales_agent: function(frm) {
        if (!frm.doc.sales_agent) return;
        // Auto-fill assigned_ops from sales agent's linked user
        frappe.db.get_value(
            "Sales Agent", frm.doc.sales_agent, "user",
            function(r) {
                if (r && r.user && !frm.doc.assigned_ops) {
                    frm.set_value("assigned_ops", r.user);
                }
            }
        );
    },

    referral_source: function(frm) {
        if (!frm.doc.referral_source) return;
        frappe.db.get_value(
            "Referral Source",
            frm.doc.referral_source,
            "source_type",
            function(r) {
                if (r) frm.set_value("source_type", r.source_type);
            }
        );
    },

});

function apply_filters(frm) {
    frm.set_query("policy_type", function() {
        const filters = { is_active: 1 };
        if (frm.doc.lob) filters["lob"] = frm.doc.lob;
        return { filters };
    });
    frm.set_query("sales_agent", function() {
        return { filters: { is_active: 1 } };
    });
    frm.set_query("client", function() {
        return { filters: { is_active: 1 } };
    });
}

function show_status_indicator(frm) {
    const colors = {
        "New": "grey", "Contacted": "blue",
        "Quotation Sent": "orange",
        "Proposal Submitted": "purple",
        "Converted": "green", "Lost": "red"
    };
    frm.dashboard.add_indicator(
        frm.doc.status,
        colors[frm.doc.status] || "grey"
    );
}

function show_action_buttons(frm) {
    if (frm.is_new()) return;
    if (frm.doc.status === "Converted" || frm.doc.status === "Lost") return;

    if (!frm.doc.insurance_quotation) {
        frm.add_custom_button("Create Quotation", function() {
            frappe.new_doc("Insurance Quotation", {
                lead_enquiry: frm.doc.name,
                client: frm.doc.client,
                lob: frm.doc.lob,
                policy_type: frm.doc.policy_type,
                sales_agent: frm.doc.sales_agent,
                prepared_by: frappe.session.user
            });
        }, "Actions");
    } else {
        frm.add_custom_button("View Quotation", function() {
            frappe.set_route("Form", "Insurance Quotation",
                frm.doc.insurance_quotation);
        }, "Actions");
    }

    frm.add_custom_button("Mark as Lost", function() {
        frappe.prompt({
            label: "Reason for Loss", fieldtype: "Small Text",
            fieldname: "lost_reason", reqd: 1
        }, function(values) {
            frappe.call({
                method: "frappe.client.set_value",
                args: {
                    doctype: "Lead Enquiry",
                    name: frm.doc.name,
                    fieldname: {
                        status: "Lost",
                        lost_reason: values.lost_reason
                    }
                },
                callback: function() {
                    frm.reload_doc();
                    frappe.show_alert("Lead marked as Lost", 5);
                }
            });
        }, "Mark Lead as Lost", "Confirm");
    }, "Actions");
}
