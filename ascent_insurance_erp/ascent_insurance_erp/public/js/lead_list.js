frappe.listview_settings['Lead'] = {
	onload: function(listview) {
		// Set default filter for lead_owner to current user
		if (!listview.filter_area.get_filter_value('lead_owner')) {
			listview.filter_area.add_filter('Lead', 'lead_owner', '=', frappe.session.user);
			listview.refresh();
		}
	},
	get_indicator: function(doc) {
		// Define indicator colors based on status
		const status_colors = {
			"New": "grey",
			"Contacted": "blue",
			"Quotation Sent": "orange",
			"Policy Proposal": "purple",
			"Converted": "green",
			"Lost": "red"
		};
		return [__(doc.status), status_colors[doc.status] || "grey", "status,=," + doc.status];
	}
};

frappe.kanban_settings['Lead'] = {
	get_indicator: function(doc) {
		const status_colors = {
			"New": "grey",
			"Contacted": "blue",
			"Quotation Sent": "orange",
			"Policy Proposal": "purple",
			"Converted": "green",
			"Lost": "red"
		};
		return [__(doc.status), status_colors[doc.status] || "grey", "status,=," + doc.status];
	}
};


