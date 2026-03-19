import frappe
from frappe import _

def test_lead_extension():
    print("Testing Lead Extension...")
    
    # 1. Create a new lead
    lead = frappe.get_doc({
        "doctype": "Lead",
        "first_name": "Test",
        "last_name": "Lead",
        "status": "New",
        "ascent_lead_source": "WhatsApp"
    })
    lead.insert()
    lead_name = lead.name
    print(f"Created Lead: {lead_name}")
    
    # Fetch fresh object
    lead = frappe.get_doc("Lead", lead_name)
    
    # 2. Check initial status
    if lead.status != "New":
        print("FAILED: New lead status is not 'New'")
    else:
        print("PASSED: New lead status is 'New'")
        
    # 3. Try to skip status to 'Quotation Sent' (Should fail)
    lead.status = "Quotation Sent"
    try:
        # Manually call our validation function which is hooked to doc_events
        from ascent_insurance_erp.ascent_insurance_erp.lead import validate as validate_lead
        validate_lead(lead, "validate")
        print("FAILED: Allowed skipping status transition")
    except frappe.ValidationError as e:
        print(f"PASSED: Blocked invalid transition: {e}")

    # 4. Correct transition to 'Contacted'
    lead.status = "Contacted"
    lead.policy_type_of_interest = "Health"
    from ascent_insurance_erp.ascent_insurance_erp.lead import validate as validate_lead
    validate_lead(lead, "validate")
    print(f"PASSED: Allowed transition to 'Contacted' with Policy Type")
    
    # 5. Try to valid without policy_type_of_interest
    lead.policy_type_of_interest = None
    try:
        validate_lead(lead, "validate")
        print("FAILED: Allowed missing Policy Type of Interest after initial save")
    except frappe.MandatoryError:
        print("PASSED: Blocked missing Policy Type of Interest")

    # Cleanup
    frappe.db.rollback()
    print("Test Completed (Transaction Rolled Back)")


if __name__ == "__main__":
    test_lead_extension()
