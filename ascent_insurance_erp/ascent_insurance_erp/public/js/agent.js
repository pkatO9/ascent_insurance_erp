frappe.ui.form.on("Agent", {
    refresh: function(frm) {
        show_agent_summary(frm);
        set_linked_user_filter(frm);

        // Show license expiry warning on form load
        if (frm.doc.license_expiry) {
            const expiry = frappe.datetime.str_to_obj(frm.doc.license_expiry);
            const today = new Date();
            const days_left = Math.floor((expiry - today) / (1000 * 60 * 60 * 24));
            if (days_left < 0) {
                frm.dashboard.add_indicator("License Expired", "red");
            } else if (days_left <= 30) {
                frm.dashboard.add_indicator(
                    `License expires in ${days_left} days`, "orange"
                );
            } else {
                frm.dashboard.add_indicator("License Valid", "green");
            }
        }

        // Quick navigation buttons
        if (!frm.is_new()) {
            frm.add_custom_button("View Leads", function() {
                frappe.set_route("List", "Lead Enquiry", {
                    "agent": frm.doc.name
                });
            });
            frm.add_custom_button("View Policies", function() {
                frappe.set_route("List", "Policy", {
                    "agent": frm.doc.name
                });
            });
        }
    },

    agent_type: function(frm) {
        // Clear linked_user if type changed away from Internal Staff
        if (frm.doc.agent_type !== "Internal Staff" && frm.doc.linked_user) {
            frm.set_value("linked_user", "");
            frappe.show_alert({
                message: "Linked user cleared — only Internal Staff can have ERP login.",
                indicator: "orange"
            }, 5);
        }
    },
});

function set_linked_user_filter(frm) {
    frm.set_query("linked_user", function() {
        return {
            filters: { enabled: 1 }
        };
    });
}

function show_agent_summary(frm) {
    if (frm.is_new()) return;
    const type_colors = {
        "Internal Staff": "blue",
        "POSP": "green",
        "Individual Agent": "green",
        "Sub-agent": "orange",
        "DSA / Corporate Agent": "purple",
        "Broker": "purple"
    };
    const color = type_colors[frm.doc.agent_type] || "grey";
    frm.dashboard.add_indicator(frm.doc.agent_type, color);
    if (!frm.doc.is_active) {
        frm.dashboard.add_indicator("Inactive", "red");
    }
}
