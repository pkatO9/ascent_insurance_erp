frappe.ui.form.on('Insurance Quotation', {
	setup: function(frm) {
		// Attempt to set datepicker options for the whole child table
		frm.set_df_property('members', 'get_datepicker_options', function() {
			return {
				view: 'years',
				startView: 'years',
				firstDay: 1
			};
		});
	},
	onload: function(frm) {
		// Force Quotation Options to NOT be an editable grid
		// This ensures clicking 'Add Row' or a row opens the Dialog
		if (frm.fields_dict.options && frm.fields_dict.options.grid) {
			frm.fields_dict.options.grid.editable_grid = false;
		}
	},
	refresh: function(frm) {
		if (frm.doc.lead) {
			frm.trigger('update_proposer_options');
		}
		// Also pulse the grid to ensure it respects the editable_grid setting
		if (frm.fields_dict.options && frm.fields_dict.options.grid) {
			frm.fields_dict.options.grid.editable_grid = false;
			frm.fields_dict.options.grid.refresh();
		}
	},
	lead: function(frm) {
		if (frm.doc.lead) {
			frm.trigger('update_proposer_options');
			
			frappe.db.get_value('Lead', frm.doc.lead, 'lead_name', (r) => {
				if (r && !frm.doc.proposer_name) {
					frm.set_value('proposer_name', r.lead_name);
				}
			});
		}
	},
	update_proposer_options: function(frm) {
		if (!frm.doc.lead) return;
		
		frappe.db.get_list('Contact', {
			filters: [
				['Dynamic Link', 'link_doctype', '=', 'Lead'],
				['Dynamic Link', 'link_name', '=', frm.doc.lead]
			],
			fields: ['full_name']
		}).then(contacts => {
			let options = [];
			
			frappe.db.get_value('Lead', frm.doc.lead, 'lead_name', (lead_res) => {
				if (lead_res && lead_res.lead_name) {
					options.push(lead_res.lead_name);
				}
				
				if (contacts) {
					contacts.forEach(c => {
						if (c.full_name) options.push(c.full_name);
					});
				}
				
				options = [...new Set(options)];
				frm.set_df_property('proposer_name', 'options', [""].concat(options));
				frm.refresh_field('proposer_name');
			});
		});
	}
});

frappe.ui.form.on('Quotation Member', {
	members_add: function(frm, cdt, cdn) {
		// Configuration for datepicker to start with years
		setTimeout(() => {
			let field = frappe.utils.get_grid_field(frm, 'members', 'dob');
			if (field && field.datepicker) {
				field.datepicker.options.view = 'years';
				field.datepicker.options.startView = 'years';
			}
		}, 100);
	},
	form_render: function(frm, cdt, cdn) {
		// Ensure year view on dialog open
		let field = frappe.utils.get_grid_field(frm, 'members', 'dob');
		if (field && field.datepicker) {
			field.datepicker.options.view = 'years';
			field.datepicker.options.startView = 'years';
		}
	},
	dob: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.dob) {
			let dob = moment(row.dob);
			let age = moment().diff(dob, 'years');
			frappe.model.set_value(cdt, cdn, 'age', age);
		}
	}
});
