import frappe

def execute():
    lobs = ["Life", "General", "Health"]
    for lob_name in lobs:
        if not frappe.db.exists("LOB", lob_name):
            doc = frappe.new_doc("LOB")
            doc.lob_name = lob_name
            doc.is_active = 1
            doc.insert(ignore_permissions=True)
    frappe.db.commit()
