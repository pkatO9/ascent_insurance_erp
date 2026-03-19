import frappe

def check_lead_fields():
    meta = frappe.get_meta('Lead')
    print("Lead Field Properties:")
    target_fields = ['lead_name', 'first_name', 'last_name', 'mobile_no', 'policy_type_of_interest', 'status']
    for f in meta.fields:
        if f.fieldname in target_fields:
            print(f"{f.fieldname}: label={f.label}, reqd={f.reqd}, quick={f.allow_in_quick_entry}")
    print(f"DocType Quick Entry: {meta.quick_entry}")
    print(f"DocType Quick Entry Fields: {meta.quick_entry_fields}")



if __name__ == "__main__":
    check_lead_fields()
