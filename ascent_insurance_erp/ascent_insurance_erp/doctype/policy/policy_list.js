frappe.listview_settings["Policy"] = {
    add_fields: ["status", "insurer", "agent", "end_date", "gross_premium", "commission_status"],
    
    get_indicator: function(doc) {
        // Return [label, color, filter_field:filter_value] for each status
        if (doc.status === "Active") return ["Active", "green", "status,=,Active"];
        if (doc.status === "Draft") return ["Draft", "grey", "status,=,Draft"];
        if (doc.status === "Up for Renewal") return ["Up for Renewal", "orange", "status,=,Up for Renewal"];
        if (doc.status === "Lapsed") return ["Lapsed", "red", "status,=,Lapsed"];
        if (doc.status === "Cancelled") return ["Cancelled", "red", "status,=,Cancelled"];
        if (doc.status === "Renewed") return ["Renewed", "blue", "status,=,Renewed"];
        if (doc.status === "Expired") return ["Expired", "darkgrey", "status,=,Expired"];
    },
    
    onload: function(listview) {
        // Add filter buttons at top of list
        listview.page.add_inner_button("Active Policies", function() {
            listview.filter_area.add("Policy", "status", "=", "Active");
        });
        listview.page.add_inner_button("Up for Renewal", function() {
            listview.filter_area.add("Policy", "status", "=", "Up for Renewal");
        });
        listview.page.add_inner_button("My Policies", function() {
            listview.filter_area.add("Policy", "agent", "=", frappe.session.user);
        });
    }
};
