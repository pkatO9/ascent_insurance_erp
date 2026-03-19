import frappe
from frappe import _

def test_lead_assignment_tracking():
    print("Testing Lead Assignment and Tracking...")
    
    # 1. Create a new lead (Auto-assignment)
    lead = frappe.get_doc({
        "doctype": "Lead",
        "first_name": "Assignment",
        "last_name": "Test",
        "ascent_lead_source": "WhatsApp",
        "status": "New",
        "policy_type_of_interest": "Health"
    })

    lead.insert()
    print(f"Created Lead: {lead.name}")
    
    # Check auto-assignment
    if lead.lead_owner == frappe.session.user:
        print(f"PASSED: lead_owner auto-assigned to '{lead.lead_owner}'")
    else:
        print(f"FAILED: lead_owner '{lead.lead_owner}', expected '{frappe.session.user}'")
        
    # Check initial history row
    if len(lead.ascent_assignment_history) == 1:
        row = lead.ascent_assignment_history[0]
        if row.new_owner == frappe.session.user:
            print("PASSED: Initial assignment logged to history")
        else:
            print(f"FAILED: Initial assignment history row invalid: {row.new_owner}")
    else:
        print(f"FAILED: Assignment history rows: {len(lead.ascent_assignment_history)}, expected 1")

    # 2. Reassign to another user
    lead.reload()
    
    # Try to find another user to reassign to
    other_user = frappe.db.get_value("User", {"name": ["not in", [frappe.session.user, "Guest", "Administrator"]], "enabled": 1}, "name")
    if not other_user:
        # Fallback if no other user exists
        other_user = "Administrator" if frappe.session.user != "Administrator" else "Guest"
        
    lead.lead_owner = other_user
    lead.save()
    print(f"Reassigned Lead to: {lead.lead_owner}")
    
    # Check history logging
    lead.reload()
    if len(lead.ascent_assignment_history) == 2:
        row = lead.ascent_assignment_history[1]
        if row.new_owner == other_user:
            print(f"PASSED: Reassignment to {other_user} logged to history correctly")
        else:
            print(f"FAILED: Reassignment history row invalid: {row.previous_owner} -> {row.new_owner}")
    else:
        print(f"FAILED: Assignment history rows: {len(lead.ascent_assignment_history)}, expected 2")


    # 3. Mandatory Owner Validation
    lead.lead_owner = None
    try:
        lead.save()
        # In our logic, it forces current user if empty, or throws. 
        # Since I'm Administrator, it might re-set it.
        if not lead.lead_owner:
            print("FAILED: Allowed empty lead_owner")
        else:
            print(f"PASSED: Prevented empty lead_owner (re-set to {lead.lead_owner})")
    except frappe.MandatoryError:
        print("PASSED: Blocked empty lead_owner with MandatoryError")

    # Cleanup
    frappe.db.rollback()
    print("Test Completed (Transaction Rolled Back)")

if __name__ == "__main__":
    test_lead_assignment_tracking()
