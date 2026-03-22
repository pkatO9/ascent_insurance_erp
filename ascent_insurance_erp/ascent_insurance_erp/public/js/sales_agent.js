frappe.ui.form.on("Sales Agent", {
    refresh: function(frm) {
        show_indicators(frm);

        if (!frm.is_new()) {
            frm.add_custom_button("View Leads", function() {
                frappe.set_route("List", "Lead Enquiry", {
                    "sales_agent": frm.doc.name
                });
            });
            frm.add_custom_button("View Policies", function() {
                frappe.set_route("List", "Policy", {
                    "sales_agent": frm.doc.name
                });
            });
        }

        // User filter — only enabled users
        frm.set_query("user", function() {
            return { filters: { enabled: 1 } };
        });
    },
});

function show_indicators(frm) {
    if (frm.is_new()) return;

    frm.dashboard.add_indicator("Internal Sales Agent", "blue");

    if (!frm.doc.is_active) {
        frm.dashboard.add_indicator("Inactive", "red");
    }

    if (frm.doc.license_expiry) {
        const expiry = new Date(frm.doc.license_expiry);
        const today = new Date();
        const days = Math.floor((expiry - today) / (1000 * 60 * 60 * 24));
        if (days < 0) {
            frm.dashboard.add_indicator("License Expired", "red");
        } else if (days <= 30) {
            frm.dashboard.add_indicator(
                `License expires in ${days} days`, "orange"
            );
        } else {
            frm.dashboard.add_indicator("License Valid", "green");
        }
    }
}
