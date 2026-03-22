frappe.ui.form.on("Client", {

    refresh: function(frm) {
        show_client_badge(frm);

        if (!frm.is_new()) {
            frm.add_custom_button("View Leads", function() {
                frappe.set_route("List", "Lead Enquiry", {"client": frm.doc.name});
            });
            frm.add_custom_button("View Policies", function() {
                frappe.set_route("List", "Policy", {"client": frm.doc.name});
            });
        }
    },

    dob: function(frm) {
        if (frm.doc.dob) {
            const dob = new Date(frm.doc.dob);
            const today = new Date();
            const age = Math.floor(
                (today - dob) / (365.25 * 24 * 60 * 60 * 1000)
            );
            frm.set_value("age", age);
        }
    },

    client_type: function(frm) {
        // Clear type-specific fields when client_type changes
        if (frm.doc.client_type === "Individual" ||
            frm.doc.client_type === "Family") {
            frm.set_value("company_name", "");
            frm.set_value("gstin", "");
        }
    }

});

function show_client_badge(frm) {
    const colors = {
        "Individual": "blue",
        "Family": "green",
        "Corporate": "purple",
        "HUF": "orange"
    };
    if (frm.doc.client_type) {
        frm.dashboard.add_indicator(
            frm.doc.client_type,
            colors[frm.doc.client_type] || "grey"
        );
    }
    if (frm.doc.linked_customer) {
        frm.dashboard.add_indicator("Customer Created", "green");
    }
}
