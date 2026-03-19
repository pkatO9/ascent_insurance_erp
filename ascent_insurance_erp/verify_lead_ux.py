import frappe
from frappe import _

def test_lead_ux_optimization():
    print("Testing Lead UX Optimization...")
    
    # 1. Verify Defaults
    meta = frappe.get_meta("Lead")
    fields_to_check = {
        "status": "New",
        "ascent_lead_source": "WhatsApp",
        "lead_priority": "Warm"
    }
    
    for field, expected in fields_to_check.items():
        actual = next((f.default for f in meta.fields if f.fieldname == field), None)
        if actual == expected:
            print(f"PASSED: Default for {field} is '{actual}'")
        else:
            print(f"FAILED: Default for {field} is '{actual}', expected '{expected}'")
            
    # 2. Verify Quick Entry
    if meta.quick_entry:
        print("PASSED: Quick Entry is enabled for Lead")
    else:
        print("FAILED: Quick Entry is NOT enabled for Lead")
        
    # 3. Test Auto-Assignment and Mandatory Field Logic
    # (policy_type_of_interest should be optional during initial creation)
    lead = frappe.get_doc({
        "doctype": "Lead",
        "first_name": "UX",
        "last_name": "Test",
        # Not setting lead_owner, policy_type_of_interest, status, source, priority
    })
    
    lead.insert()
    print(f"Created Lead: {lead.name}")
    
    # Check auto-assignment
    if lead.lead_owner == frappe.session.user:
        print(f"PASSED: lead_owner auto-assigned to '{lead.lead_owner}'")
    else:
        print(f"FAILED: lead_owner '{lead.lead_owner}', expected '{frappe.session.user}'")
        
    # Check defaults on the record
    if lead.status == "New" and lead.ascent_lead_source == "WhatsApp" and lead.lead_priority == "Warm":
        print("PASSED: Record defaults applied correctly")
    else:
        print(f"FAILED: Record defaults - status:{lead.status}, source:{lead.ascent_lead_source}, priority:{lead.lead_priority}")

    # Check mandatory field after save
    lead = frappe.get_doc("Lead", lead.name)
    lead.first_name = "UX Updated"
    try:
        lead.save()
        print("FAILED: Allowed saving existing record without policy_type_of_interest")
    except frappe.MandatoryError:
        print("PASSED: Blocked saving existing record without policy_type_of_interest")

    # Cleanup
    frappe.db.rollback()
    print("Test Completed (Transaction Rolled Back)")

if __name__ == "__main__":
    test_lead_ux_optimization()

