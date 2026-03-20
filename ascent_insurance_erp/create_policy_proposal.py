import frappe

def create_doctype():
    frappe.flags.in_test = True  # skip link validations
    
    if not frappe.db.exists("DocType", "Policy"):
        # create a stub Policy doctype
        frappe.get_doc({
            "doctype": "DocType",
            "name": "Policy",
            "module": "Ascent Insurance ERP",
            "custom": 0,
            "fields": [
                {"fieldname": "title", "fieldtype": "Data", "label": "Title"}
            ],
            "permissions": [{"role": "System Manager", "read": 1}]
        }).insert(ignore_permissions=True)
        frappe.db.commit()

    if frappe.db.exists("DocType", "Policy Proposal"):
        print("DocType already exists")
        frappe.delete_doc("DocType", "Policy Proposal")
        frappe.db.commit()

    doc = {
        "doctype": "DocType",
        "name": "Policy Proposal",
        "module": "Ascent Insurance ERP",
        "custom": 0,
        "is_submittable": 1,
        "track_changes": 1,
        "autoname": "naming_series:",
        "fields": [
            # Section: Proposal Details
            {"fieldname": "proposal_details_sec", "fieldtype": "Section Break", "label": "Proposal Details"},
            {"fieldname": "naming_series", "fieldtype": "Select", "label": "Series", "default": "PROP-.YYYY.-", "options": "PROP-.YYYY.-"},
            {"fieldname": "lead", "fieldtype": "Link", "label": "Lead", "options": "Lead", "reqd": 1, "in_list_view": 1},
            {"fieldname": "insurance_quotation", "fieldtype": "Link", "label": "Insurance Quotation", "options": "Insurance Quotation", "reqd": 1},
            {"fieldname": "customer", "fieldtype": "Link", "label": "Customer", "options": "Customer", "reqd": 1},
            {"fieldname": "agent", "fieldtype": "Link", "label": "Agent", "options": "User", "reqd": 1, "default": "frappe.session.user"},
            
            {"fieldname": "col_break_1", "fieldtype": "Column Break"},
            {"fieldname": "insurer", "fieldtype": "Link", "label": "Insurer", "options": "Insurer", "reqd": 1, "in_list_view": 1},
            {"fieldname": "policy_type", "fieldtype": "Link", "label": "Policy Type", "options": "Policy Type", "reqd": 1},
            {"fieldname": "product_type", "fieldtype": "Link", "label": "Product Type", "options": "Product Type", "reqd": 1},
            {"fieldname": "sum_insured", "fieldtype": "Currency", "label": "Sum Insured", "reqd": 1},
            
            # Section: Submission Details
            {"fieldname": "submission_details_sec", "fieldtype": "Section Break", "label": "Submission Details"},
            {"fieldname": "submission_date", "fieldtype": "Date", "label": "Submitted to Insurer On", "reqd": 1},
            {"fieldname": "expected_approval_date", "fieldtype": "Date", "label": "Expected Approval Date"},
            {"fieldname": "proposal_notes", "fieldtype": "Small Text", "label": "Submission Notes / Remarks"},
            
            {"fieldname": "col_break_2", "fieldtype": "Column Break"},
            {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Draft\nSubmitted\nApproved\nRejected", "default": "Draft", "in_list_view": 1},
            {"fieldname": "approval_date", "fieldtype": "Date", "label": "Approval / Rejection Date", "read_only": 0},
            {"fieldname": "rejection_reason", "fieldtype": "Small Text", "label": "Rejection Reason", "depends_on": "eval:doc.status == 'Rejected'"},
            
            # Section: Linked Policy
            {"fieldname": "linked_policy_sec", "fieldtype": "Section Break", "label": "Linked Policy"},
            {"fieldname": "policy", "fieldtype": "Link", "label": "Policy Created", "options": "Policy", "read_only": 1, "description": "Auto-filled when policy is created from this proposal"}
        ],
        "permissions": [
            {
                "role": "System Manager",
                "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1, "amend": 1
            }
        ]
    }
    
    doctype_doc = frappe.get_doc(doc)
    doctype_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print("Policy Proposal doctype created successfully")

