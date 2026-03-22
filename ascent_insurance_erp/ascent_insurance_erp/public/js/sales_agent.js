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

    user: function(frm) {
        if (frm.doc.user) {
            frappe.db.get_value("User", frm.doc.user, ["full_name", "email", "mobile_no"], (r) => {
                if (r) {
                    frm.set_value("sales_agent_name", r.full_name);
                    frm.set_value("email", r.email);
                    if (r.mobile_no) {
                        frm.set_value("mobile", r.mobile_no);
                    }
                }
            });
        }
    }
});

function show_indicators(frm) {
//     if (frm.is_new()) return;

//     // Show Lead Status Stats
//     const statuses = ["New", "Contacted", "Quotation Sent", "Proposal Submitted", "Converted", "Lost"];
//     const colors = {
//         "New": "grey", "Contacted": "blue",
//         "Quotation Sent": "orange",
//         "Proposal Submitted": "purple",
//         "Converted": "green", "Lost": "red"
//     };

//     statuses.forEach(status => {
//         frappe.db.count("Lead Enquiry", {
//             sales_agent: frm.doc.name,
//             status: status
//         }).then(count => {
//             if (count > 0) {
//                 frm.dashboard.add_indicator(
//                     __("{0} {1}", [count, status]),
//                     colors[status] || "blue",
//                     () => frappe.set_route("List", "Lead Enquiry", {
//                         sales_agent: frm.doc.name,
//                         status: status
//                     })
//                 );
//             }
//         });
//     });

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
