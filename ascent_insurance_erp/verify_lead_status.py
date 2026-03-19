import frappe
from frappe import _

def test_status_transitions():
    print("Testing Lead Status Transitions...")
    
    # Setup: Create a new lead
    lead = frappe.get_doc({
        "doctype": "Lead",
        "first_name": "Transition",
        "last_name": "Test",
        "ascent_lead_source": "WhatsApp",
        "status": "New",
        "policy_type_of_interest": "Health"
    })
    lead.insert()
    print(f"Initial Status: {lead.status}")

    def try_transition(to_status, expected_success=True):
        lead.reload()
        old_status = lead.status
        lead.status = to_status
        try:
            lead.save()
            if expected_success:
                print(f"PASSED: Transition {old_status} -> {to_status} Success")
            else:
                print(f"FAILED: Transition {old_status} -> {to_status} should have failed")
        except frappe.ValidationError as e:
            if not expected_success:
                print(f"PASSED: Transition {old_status} -> {to_status} Blocked as expected")
            else:
                print(f"FAILED: Transition {old_status} -> {to_status} failed unexpectedly: {e}")

    # 1. Valid: New -> Contacted
    try_transition("Contacted", True)

    # 2. Invalid: Contacted -> New (Backward)
    try_transition("New", False)

    # 3. Invalid: Contacted -> Policy Proposal (Skip Quotation Sent)
    try_transition("Policy Proposal", False)

    # 4. Valid: Contacted -> Quotation Sent
    try_transition("Quotation Sent", True)

    # 5. Valid: Quotation Sent -> Lost (Exception)
    try_transition("Lost", True)

    # 6. Reset to New (via DB for next test set)
    frappe.db.set_value("Lead", lead.name, "status", "New")
    lead.reload()
    
    # 7. Valid: New -> Lost (Exception)
    try_transition("Lost", True)

    # Check Kanban Board existence
    if frappe.db.exists("Kanban Board", "Lead Pipeline"):
        print("PASSED: Kanban Board 'Lead Pipeline' exists")
    else:
        print("FAILED: Kanban Board 'Lead Pipeline' missing")

    # Cleanup
    frappe.db.rollback()
    print("Test Completed (Transaction Rolled Back)")

if __name__ == "__main__":
    test_status_transitions()

