import frappe
from frappe import _

def test_quotation_validations():
    print("Testing Insurance Quotation Validations...")
    
    # Setup: Create a temporary lead
    lead = frappe.get_doc({
        "doctype": "Lead",
        "first_name": "Quotation Tester",
        "mobile_no": "9999999999",
        "status": "New"
    }).insert(ignore_permissions=True)
    
    # Real records from database
    POLICY_TYPE = "Health"
    PRODUCT_TYPE = "Standard Health-LIC Corp"
    INSURER = "LIC Corp"

    # 1. Test: No members
    print("1. Testing No Members...")
    q1 = frappe.new_doc("Insurance Quotation")
    q1.lead = lead.name
    q1.policy_type = POLICY_TYPE
    q1.members = []
    try:
        q1.insert(ignore_permissions=True)
        print("Fail: No members validation failed.")
    except Exception as e:
        if "At least 1 member is required" in str(e):
            print(f"Success: Caught expected error: {e}")
        else:
            print(f"Error: Caught unexpected error: {e}")

    # 2. Test: Status 'Sent' with < 3 options
    print("2. Testing Status 'Sent' with < 3 options...")
    q2 = frappe.new_doc("Insurance Quotation")
    q2.lead = lead.name
    q2.policy_type = POLICY_TYPE
    q2.status = "Sent"
    q2.append("members", {"relation": "Self", "member_name": "Test User", "dob": "1990-01-01"})
    q2.append("options", {"insurer": INSURER, "product_type": PRODUCT_TYPE, "sum_insured": 500000, "premium": 15000})
    try:
        q2.insert(ignore_permissions=True)
        print("Fail: Status Sent with < 3 options validation failed.")
    except Exception as e:
        if "At least 3 quotation options are required" in str(e):
            print(f"Success: Caught expected error: {e}")
        else:
            print(f"Error: Caught unexpected error: {e}")

    # 3. Test: Premium = 0
    print("3. Testing Premium > 0...")
    q3 = frappe.new_doc("Insurance Quotation")
    q3.lead = lead.name
    q3.policy_type = POLICY_TYPE
    q3.status = "Draft"
    q3.append("members", {"relation": "Self", "member_name": "Test User", "dob": "1990-01-01"})
    q3.append("options", {"insurer": INSURER, "product_type": PRODUCT_TYPE, "sum_insured": 500000, "premium": 0})
    try:
        q3.insert(ignore_permissions=True)
        print("Fail: Premium > 0 validation failed.")
    except Exception as e:
        if "Premium must be greater than 0" in str(e):
            print(f"Success: Caught expected error: {e}")
        else:
            print(f"Error: Caught unexpected error: {e}")

    # Cleanup
    frappe.db.rollback()
    print("Verification Completed (Transaction Rolled Back).")

if __name__ == "__main__":
    test_quotation_validations()
