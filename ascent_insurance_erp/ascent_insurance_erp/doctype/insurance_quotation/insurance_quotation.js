frappe.ui.form.on('Insurance Quotation', {

    refresh: function(frm) {
        if (frm.doc.lead && !frm.is_new()) {
            frm.trigger('update_proposer_options');
        }
    },

    lead: function(frm) {
        if (!frm.doc.lead) return;

        frm.trigger('update_proposer_options');

        frappe.db.get_value('Lead', frm.doc.lead, 'lead_name')
            .then(r => {
                if (r.message && !frm.doc.proposer_name) {
                    frm.set_value('proposer_name', r.message.lead_name);
                }
            });
    },

    update_proposer_options: function(frm) {
        if (!frm.doc.lead) return;

        Promise.all([
            frappe.db.get_list('Contact', {
                filters: [
                    ['Dynamic Link', 'link_doctype', '=', 'Lead'],
                    ['Dynamic Link', 'link_name', '=', frm.doc.lead]
                ],
                fields: ['full_name']
            }),
            frappe.db.get_value('Lead', frm.doc.lead, 'lead_name')
        ]).then(([contacts, lead_res]) => {

            let options = [];

            if (lead_res.message?.lead_name) {
                options.push(lead_res.message.lead_name);
            }

            (contacts || []).forEach(c => {
                if (c.full_name) options.push(c.full_name);
            });

            options = [...new Set(options)].filter(Boolean);

            frm.set_df_property('proposer_name', 'options', ["", ...options]);
            frm.refresh_field('proposer_name');
        });
    }
});


frappe.ui.form.on('Quotation Member', {

    form_render: function(frm) {
        frm.fields_dict.members.grid.update_docfield_property('dob', 'datepicker_options', {
            view: 'years',
            startView: 'years'
        });
    },

    dob: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (row.dob && moment(row.dob).isValid()) {
            let dob = moment(row.dob);

            if (dob.isAfter(moment())) {
                frappe.msgprint("DOB cannot be in the future");
                return;
            }

            let age = moment().diff(dob, 'years');
            frappe.model.set_value(cdt, cdn, 'age', age);
        }
    }
});