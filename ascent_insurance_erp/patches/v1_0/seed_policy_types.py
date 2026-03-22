import frappe

# ─────────────────────────────────────────────────────────────
# EDIT THIS LIST to add or change policy types.
# Format: ("Policy Type Name", "LOB")
# LOB must be one of: "Life", "General", "Health"
# ─────────────────────────────────────────────────────────────
POLICY_TYPES = [
    # Health
    ("Health - Individual",        "Health"),
    ("Health - Family Floater",    "Health"),
    ("Health - Senior Citizen",    "Health"),
    ("Health - Group",             "Health"),
    ("Personal Accident - Individual", "General"),
    ("Personal Accident - Group",  "General"),
    # Life
    ("Term Life",                  "Life"),
    ("Whole Life",                 "Life"),
    ("ULIP",                       "Life"),
    ("Endowment",                  "Life"),
    # General
    ("Motor - Private Car",        "General"),
    ("Motor - Two Wheeler",        "General"),
    ("Motor - Commercial Vehicle", "General"),
    ("Travel - Individual",        "General"),
    ("Travel - Group",             "General"),
    ("Fire & Property",            "General"),
    ("Marine",                     "General"),
    ("Liability",                  "General"),
]

def execute():
    for policy_type_name, lob_name in POLICY_TYPES:
        if frappe.db.exists("Policy Type", policy_type_name):
            # Record exists — just ensure LOB is linked
            existing_lob = frappe.db.get_value(
                "Policy Type", policy_type_name, "lob"
            )
            if not existing_lob:
                frappe.db.set_value(
                    "Policy Type", policy_type_name, "lob", lob_name
                )
        else:
            # Create fresh
            doc = frappe.new_doc("Policy Type")
            doc.policy_type_name = policy_type_name  # adjust field name
            # If Policy Type uses autoname field:lob_name pattern, set name:
            doc.name = policy_type_name
            doc.lob = lob_name
            doc.active = 1  # Fixed: Field name is 'active', not 'is_active'
            doc.insert(ignore_permissions=True)

    frappe.db.commit()
    print(f"Seeded {len(POLICY_TYPES)} policy types successfully.")
