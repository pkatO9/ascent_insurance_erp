import frappe

def run_seed():
    frappe.logger().info("Starting Insurance ERP Seed Script...")
    
    # 1. Create Insurers
    insurers = [
        {"insurer_name": "HDFC Ergo", "short_code": "HE", "active": 1},
        {"insurer_name": "ICICI Lombard", "short_code": "IL", "active": 1},
        {"insurer_name": "Tata AIG", "short_code": "TA", "active": 1},
        {"insurer_name": "Bajaj Allianz", "short_code": "BA", "active": 1},
        {"insurer_name": "Star Health", "short_code": "SH", "active": 1},
    ]
    
    for ins in insurers:
        if not frappe.db.exists("Insurer", ins["insurer_name"]):
            doc = frappe.get_doc({
                "doctype": "Insurer",
                "insurer_name": ins["insurer_name"],
                "short_code": ins["short_code"],
                "active": ins["active"]
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Insurer: {ins['insurer_name']}")
    
    # 2. Create Policy Types
    policy_types = [
        {"policy_type_name": "Health", "description": "Health and Medical Insurance Policies"},
        {"policy_type_name": "Motor", "description": "Two-wheeler, Car, and Commercial Vehicle Insurance"},
        {"policy_type_name": "Life", "description": "Term, Endowment, and ULIP Life Insurance"},
        {"policy_type_name": "Travel", "description": "Domestic and International Travel Insurance"},
    ]
    
    for pt in policy_types:
        if not frappe.db.exists("Policy Type", pt["policy_type_name"]):
            doc = frappe.get_doc({
                "doctype": "Policy Type",
                "policy_type_name": pt["policy_type_name"],
                "description": pt["description"],
                "active": 1
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Policy Type: {pt['policy_type_name']}")

    frappe.db.commit()

    # 3. Create realistic Products (3 per insurer per policy type)
    # 5 Insurers * 4 Policy Types * 3 Products = 60 Products
    products = [
        # --- HEALTH ---
        # HDFC Ergo
        {"name": "Optima Secure", "ins": "HDFC Ergo", "pt": "Health", "bp": 12000, "p_min": 8000, "p_max": 25000, "sir": "5L - 2Cr", "freq": "Yearly", "csr": 97.5, "kf": "2X Coverage from day 1, Plus Benefit", "tc": "Families, Individuals"},
        {"name": "My:Health Suraksha", "ins": "HDFC Ergo", "pt": "Health", "bp": 10000, "p_min": 6000, "p_max": 20000, "sir": "3L - 75L", "freq": "Yearly", "csr": 97.5, "kf": "Comprehensive cover, No room rent capping", "tc": "Individuals"},
        {"name": "Medisure Classic", "ins": "HDFC Ergo", "pt": "Health", "bp": 8500, "p_min": 5000, "p_max": 15000, "sir": "1L - 10L", "freq": "Yearly", "csr": 97.5, "kf": "Basic coverage for budget conscious", "tc": "Budget segmented"},
        # ICICI Lombard
        {"name": "Elevate", "ins": "ICICI Lombard", "pt": "Health", "bp": 14000, "p_min": 9500, "p_max": 30000, "sir": "10L - Infinite", "freq": "Yearly", "csr": 98.6, "kf": "Infinite restoration, Day 1 pre-existing coverage", "tc": "High Net Worth"},
        {"name": "Health AdvantEdge", "ins": "ICICI Lombard", "pt": "Health", "bp": 11000, "p_min": 7500, "p_max": 22000, "sir": "5L - 50L", "freq": "Yearly", "csr": 98.6, "kf": "Wellness benefits, Bariatric surgery cover", "tc": "Families"},
        {"name": "Health Shield", "ins": "ICICI Lombard", "pt": "Health", "bp": 9000, "p_min": 5500, "p_max": 18000, "sir": "3L - 25L", "freq": "Yearly", "csr": 98.6, "kf": "Affordable family floater", "tc": "Individuals, Small Families"},
        # Tata AIG
        {"name": "Medicare", "ins": "Tata AIG", "pt": "Health", "bp": 13000, "p_min": 8500, "p_max": 28000, "sir": "5L - 1Cr", "freq": "Yearly", "csr": 96.4, "kf": "Global cover, Consumables covered", "tc": "Premium Customers"},
        {"name": "Medicare Premier", "ins": "Tata AIG", "pt": "Health", "bp": 16000, "p_min": 11000, "p_max": 35000, "sir": "50L - 3Cr", "freq": "Yearly", "csr": 96.4, "kf": "High sum insured, Maternity cover", "tc": "High Net Worth"},
        {"name": "Medicare Protect", "ins": "Tata AIG", "pt": "Health", "bp": 8000, "p_min": 5000, "p_max": 15000, "sir": "2L - 15L", "freq": "Yearly", "csr": 96.4, "kf": "Standard hospitalization, Basic protect", "tc": "Budget Buyers"},
        # Bajaj Allianz
        {"name": "Health Guard", "ins": "Bajaj Allianz", "pt": "Health", "bp": 11500, "p_min": 7000, "p_max": 24000, "sir": "5L - 50L", "freq": "Yearly", "csr": 98.2, "kf": "Ayush treatments, Convalescence benefit", "tc": "Families"},
        {"name": "Care Health", "ins": "Bajaj Allianz", "pt": "Health", "bp": 10500, "p_min": 6000, "p_max": 22000, "sir": "3L - 25L", "freq": "Yearly", "csr": 98.2, "kf": "Annual health checkups, No claim bonus", "tc": "Individuals"},
        {"name": "Health Ensure", "ins": "Bajaj Allianz", "pt": "Health", "bp": 7500, "p_min": 4500, "p_max": 14000, "sir": "1L - 10L", "freq": "Yearly", "csr": 98.2, "kf": "Basic illness coverage", "tc": "Rural/Tier 3 Customers"},
        # Star Health
        {"name": "Comprehensive Health", "ins": "Star Health", "pt": "Health", "bp": 15000, "p_min": 9000, "p_max": 32000, "sir": "5L - 1Cr", "freq": "Yearly", "csr": 99.1, "kf": "No sub-limits, Outpatient dental & ophthalmic", "tc": "Complete Families"},
        {"name": "Family Health Optima", "ins": "Star Health", "pt": "Health", "bp": 12500, "p_min": 7500, "p_max": 26000, "sir": "3L - 25L", "freq": "Yearly", "csr": 99.1, "kf": "Super restoration, Assisted reproduction", "tc": "Couples, Families"},
        {"name": "Young Star", "ins": "Star Health", "pt": "Health", "bp": 9500, "p_min": 5000, "p_max": 18000, "sir": "5L - 15L", "freq": "Yearly", "csr": 99.1, "kf": "No waiting period for early buyers, Mid-term inclusion", "tc": "Millennials, People under 40"},
        
        # --- MOTOR ---
        # HDFC Ergo
        {"name": "Motor Shield Two Wheeler", "ins": "HDFC Ergo", "pt": "Motor", "bp": 1500, "p_min": 800, "p_max": 3500, "sir": "IDV", "freq": "Yearly", "csr": 99.5, "kf": "Zero Dep, Engine Protect", "tc": "Bike Owners"},
        {"name": "Motor Shield Private Car", "ins": "HDFC Ergo", "pt": "Motor", "bp": 12000, "p_min": 6000, "p_max": 45000, "sir": "IDV", "freq": "Yearly", "csr": 99.5, "kf": "Consumables, Return to Invoice", "tc": "Car Owners"},
        {"name": "Commercial Vehicle Protect", "ins": "HDFC Ergo", "pt": "Motor", "bp": 25000, "p_min": 15000, "p_max": 80000, "sir": "IDV", "freq": "Yearly", "csr": 99.5, "kf": "Payload protection, Downtime allowance", "tc": "Fleet Owners"},
        # ICICI Lombard
        {"name": "Two Wheeler comprehensive", "ins": "ICICI Lombard", "pt": "Motor", "bp": 1400, "p_min": 750, "p_max": 3000, "sir": "IDV", "freq": "Yearly", "csr": 98.8, "kf": "Instant OD, Multi-year discount", "tc": "Bike Owners"},
        {"name": "Private Car Protect", "ins": "ICICI Lombard", "pt": "Motor", "bp": 11500, "p_min": 5500, "p_max": 42000, "sir": "IDV", "freq": "Yearly", "csr": 98.8, "kf": "Cashless garages, Telematics integration", "tc": "Car Owners"},
        {"name": "Pay As You Drive", "ins": "ICICI Lombard", "pt": "Motor", "bp": 8000, "p_min": 3500, "p_max": 20000, "sir": "IDV", "freq": "Yearly", "csr": 98.8, "kf": "Usage based premium, Low mileage discounts", "tc": "Infrequent drivers"},
        # Tata AIG
        {"name": "Auto Secure - Two Wheeler", "ins": "Tata AIG", "pt": "Motor", "bp": 1600, "p_min": 900, "p_max": 4000, "sir": "IDV", "freq": "Yearly", "csr": 99.2, "kf": "Key replacement, Personal accident cover", "tc": "Bike Owners"},
        {"name": "Auto Secure - Private Car", "ins": "Tata AIG", "pt": "Motor", "bp": 13000, "p_min": 6500, "p_max": 50000, "sir": "IDV", "freq": "Yearly", "csr": 99.2, "kf": "Quick claim settlement, Depreciation reimbursement", "tc": "Car Owners"},
        {"name": "Auto Secure - Fleet", "ins": "Tata AIG", "pt": "Motor", "bp": 35000, "p_min": 20000, "p_max": 150000, "sir": "IDV", "freq": "Yearly", "csr": 99.2, "kf": "Bulk discount, Towing assistance", "tc": "Fleet Operators"},
        # Bajaj Allianz
        {"name": "Motor Protect 2W", "ins": "Bajaj Allianz", "pt": "Motor", "bp": 1350, "p_min": 700, "p_max": 2800, "sir": "IDV", "freq": "Yearly", "csr": 98.5, "kf": "Digital policy, quick renewal", "tc": "Bike Owners"},
        {"name": "Motor Protect 4W", "ins": "Bajaj Allianz", "pt": "Motor", "bp": 11000, "p_min": 5000, "p_max": 40000, "sir": "IDV", "freq": "Yearly", "csr": 98.5, "kf": "24x7 spot assistance, Lock and key replacement", "tc": "Car Owners"},
        {"name": "EV Protect", "ins": "Bajaj Allianz", "pt": "Motor", "bp": 14000, "p_min": 7000, "p_max": 45000, "sir": "IDV", "freq": "Yearly", "csr": 98.5, "kf": "Battery replacement cover, Charger protection", "tc": "EV Owners"},
        # Star Health
        {"name": "Star Motor Basic Two Wheeler", "ins": "Star Health", "pt": "Motor", "bp": 1200, "p_min": 600, "p_max": 2500, "sir": "IDV", "freq": "Yearly", "csr": 95.0, "kf": "Third Party + Basic OD", "tc": "Bike Owners"},
        {"name": "Star Motor Basic Car", "ins": "Star Health", "pt": "Motor", "bp": 10000, "p_min": 4500, "p_max": 35000, "sir": "IDV", "freq": "Yearly", "csr": 95.0, "kf": "Third Party + Basic OD", "tc": "Car Owners"},
        {"name": "Star Motor Comprehensive", "ins": "Star Health", "pt": "Motor", "bp": 12500, "p_min": 5500, "p_max": 45000, "sir": "IDV", "freq": "Yearly", "csr": 95.0, "kf": "Full comprehensive", "tc": "Car Owners"},

        # --- LIFE ---
        # HDFC Ergo
        {"name": "Click 2 Protect", "ins": "HDFC Ergo", "pt": "Life", "bp": 15000, "p_min": 8000, "p_max": 80000, "sir": "50L - 5Cr", "freq": "Yearly", "csr": 99.3, "kf": "Pure Term, Waiver of Premium", "tc": "Breadwinners"},
        {"name": "Sanchay Plus", "ins": "HDFC Ergo", "pt": "Life", "bp": 100000, "p_min": 50000, "p_max": 500000, "sir": "Guaranteed Returns", "freq": "Yearly", "csr": 99.3, "kf": "Guaranteed income, Tax free maturity", "tc": "High Net Worth, Planners"},
        {"name": "Click 2 Invest", "ins": "HDFC Ergo", "pt": "Life", "bp": 60000, "p_min": 30000, "p_max": 200000, "sir": "Fund Value", "freq": "Yearly", "csr": 99.3, "kf": "ULIP, Market linked returns", "tc": "Investors"},
        # ICICI Lombard 
        {"name": "iProtect Smart", "ins": "ICICI Lombard", "pt": "Life", "bp": 14000, "p_min": 7500, "p_max": 75000, "sir": "50L - 5Cr", "freq": "Monthly", "csr": 99.1, "kf": "Critical Illness benefit, Terminal illness cover", "tc": "Breadwinners"},
        {"name": "Gift Long Term", "ins": "ICICI Lombard", "pt": "Life", "bp": 12000, "p_min": 6000, "p_max": 60000, "sir": "Guaranteed Returns", "freq": "Monthly", "csr": 99.1, "kf": "Lifelong income, wealth creation", "tc": "Retirement planning"},
        {"name": "Signature ULIP", "ins": "ICICI Lombard", "pt": "Life", "bp": 10000, "p_min": 5000, "p_max": 50000, "sir": "Fund Value", "freq": "Monthly", "csr": 99.1, "kf": "Return of mortality charges, dynamic asset allocation", "tc": "Investors"},
        # Tata AIG
        {"name": "Sampoorna Raksha", "ins": "Tata AIG", "pt": "Life", "bp": 16000, "p_min": 9000, "p_max": 85000, "sir": "50L - 5Cr", "freq": "Yearly", "csr": 99.0, "kf": "Return of premium option, Whole life cover", "tc": "Breadwinners"},
        {"name": "Fortune Guarantee", "ins": "Tata AIG", "pt": "Life", "bp": 90000, "p_min": 45000, "p_max": 400000, "sir": "Guaranteed Returns", "freq": "Yearly", "csr": 99.0, "kf": "Regular income, high returns", "tc": "Conservative Investors"},
        {"name": "Param Rakshak", "ins": "Tata AIG", "pt": "Life", "bp": 85000, "p_min": 40000, "p_max": 350000, "sir": "Fund Value", "freq": "Yearly", "csr": 99.0, "kf": "ULIP with term cover", "tc": "Aggressive Investors"},
        # Bajaj Allianz
        {"name": "eTouch Online Term", "ins": "Bajaj Allianz", "pt": "Life", "bp": 13500, "p_min": 7000, "p_max": 70000, "sir": "50L - 5Cr", "freq": "Yearly", "csr": 99.0, "kf": "Accidental death benefit, low cost", "tc": "Young earners"},
        {"name": "Guaranteed Income Goal", "ins": "Bajaj Allianz", "pt": "Life", "bp": 75000, "p_min": 35000, "p_max": 300000, "sir": "Guaranteed Returns", "freq": "Yearly", "csr": 99.0, "kf": "Lump sum + regular income", "tc": "Retirement segment"},
        {"name": "Future Wealth Gain", "ins": "Bajaj Allianz", "pt": "Life", "bp": 60000, "p_min": 30000, "p_max": 250000, "sir": "Fund Value", "freq": "Yearly", "csr": 99.0, "kf": "Fund boosters, loyalty additions", "tc": "Investors"},
        # Star Health 
        {"name": "Star Term Protect", "ins": "Star Health", "pt": "Life", "bp": 15000, "p_min": 8500, "p_max": 75000, "sir": "50L - 2Cr", "freq": "Yearly", "csr": 95.5, "kf": "Basic term insurance", "tc": "Breadwinners"},
        {"name": "Star Endowment", "ins": "Star Health", "pt": "Life", "bp": 45000, "p_min": 25000, "p_max": 150000, "sir": "Sum Assured + Bonus", "freq": "Yearly", "csr": 95.5, "kf": "Savings with protection", "tc": "Conservative"},
        {"name": "Star Child Plan", "ins": "Star Health", "pt": "Life", "bp": 50000, "p_min": 25000, "p_max": 200000, "sir": "Milestone payout", "freq": "Yearly", "csr": 95.5, "kf": "Education funding, premium waiver", "tc": "Parents"},

        # --- TRAVEL ---
        # HDFC Ergo
        {"name": "Travel Suraksha Sublimit", "ins": "HDFC Ergo", "pt": "Travel", "bp": 1200, "p_min": 500, "p_max": 5000, "sir": "$50k - $500k", "freq": "Single Premium", "csr": 98.0, "kf": "Medical evacuation, baggage loss", "tc": "International Travelers"},
        {"name": "Travel Suraksha Comprehensive", "ins": "HDFC Ergo", "pt": "Travel", "bp": 2500, "p_min": 1000, "p_max": 10000, "sir": "$100k - $1M", "freq": "Single Premium", "csr": 98.0, "kf": "Flight delay, trip cancellation", "tc": "Frequent Flyers"},
        {"name": "Student Suraksha", "ins": "HDFC Ergo", "pt": "Travel", "bp": 5000, "p_min": 2500, "p_max": 15000, "sir": "$50k - $500k", "freq": "Single Premium", "csr": 98.0, "kf": "Study interruption, sponsor protection", "tc": "Students going abroad"},
        # ICICI Lombard
        {"name": "International Travel Insurance", "ins": "ICICI Lombard", "pt": "Travel", "bp": 1500, "p_min": 600, "p_max": 6000, "sir": "$50k - $500k", "freq": "Single Premium", "csr": 98.5, "kf": "Covid-19 covered, zero deductible", "tc": "Tourists"},
        {"name": "Gold Multi-trip", "ins": "ICICI Lombard", "pt": "Travel", "bp": 4000, "p_min": 2000, "p_max": 12000, "sir": "$100k - $500k", "freq": "Yearly", "csr": 98.5, "kf": "Unlimited trips, seamless renewals", "tc": "Business Travelers"},
        {"name": "Domestic Travel Protect", "ins": "ICICI Lombard", "pt": "Travel", "bp": 300, "p_min": 100, "p_max": 1000, "sir": "10L - 50L", "freq": "Single Premium", "csr": 98.5, "kf": "Train/flight cancellation, hotel stay", "tc": "Domestic Travelers"},
        # Tata AIG
        {"name": "Travel Guard", "ins": "Tata AIG", "pt": "Travel", "bp": 1800, "p_min": 700, "p_max": 7500, "sir": "$50k - $500k", "freq": "Single Premium", "csr": 97.8, "kf": "Hijack allowance, missed connection", "tc": "International Tourists"},
        {"name": "Travel Guard Silver", "ins": "Tata AIG", "pt": "Travel", "bp": 1000, "p_min": 400, "p_max": 4000, "sir": "$50k", "freq": "Single Premium", "csr": 97.8, "kf": "Basic medical cover", "tc": "Budget Travelers"},
        {"name": "Student Guard", "ins": "Tata AIG", "pt": "Travel", "bp": 5500, "p_min": 3000, "p_max": 18000, "sir": "$100k - $500k", "freq": "Single Premium", "csr": 97.8, "kf": "Bail bond, compassionate visit", "tc": "International Students"},
        # Bajaj Allianz
        {"name": "Travel Ace", "ins": "Bajaj Allianz", "pt": "Travel", "bp": 1600, "p_min": 650, "p_max": 6500, "sir": "$50k - $500k", "freq": "Single Premium", "csr": 98.1, "kf": "Loss of passport, pre-existing acute illness", "tc": "Tourists"},
        {"name": "Travel Companion", "ins": "Bajaj Allianz", "pt": "Travel", "bp": 1300, "p_min": 500, "p_max": 5000, "sir": "$50k", "freq": "Single Premium", "csr": 98.1, "kf": "Customizable, affordable", "tc": "Budget Travelers"},
        {"name": "Corporate Travel", "ins": "Bajaj Allianz", "pt": "Travel", "bp": 5000, "p_min": 2500, "p_max": 15000, "sir": "$100k - $500k", "freq": "Yearly", "csr": 98.1, "kf": "Blanket cover for employees", "tc": "Corporates"},
        # Star Health
        {"name": "Star Travel Protect", "ins": "Star Health", "pt": "Travel", "bp": 1400, "p_min": 600, "p_max": 5500, "sir": "$50k - $250k", "freq": "Single Premium", "csr": 96.0, "kf": "Medical expenses, repatriation", "tc": "International Tourists"},
        {"name": "Star Corporate Travel", "ins": "Star Health", "pt": "Travel", "bp": 4500, "p_min": 2000, "p_max": 12000, "sir": "$100k - $500k", "freq": "Yearly", "csr": 96.0, "kf": "Business trip cover", "tc": "Corporates"},
        {"name": "Star Student Travel", "ins": "Star Health", "pt": "Travel", "bp": 4800, "p_min": 2500, "p_max": 14000, "sir": "$100k", "freq": "Single Premium", "csr": 96.0, "kf": "Medical and tuition protection", "tc": "Students"}
    ]
    
    products_created = 0
    for p in products:
        # Avoid duplicate validation error and re-creating existing records
        if not frappe.db.get_list("Product Type", filters={"product_name": p["name"], "insurer": p["ins"]}):
            
            # The sum_insured fields min and max are mandatory and numeric, 
            # I will assign some arbitrary realistic numeric bounds.
            try:
                si_min = 100000 # 1L
                si_max = 10000000 # 1Cr
                if "5L" in p["sir"]: si_min = 500000
                if "10L" in p["sir"]: si_min = 1000000
                if "50L" in p["sir"]: si_min = 5000000
                if "1Cr" in p["sir"]: si_max = 10000000
                if "5Cr" in p["sir"]: si_max = 50000000
            except:
                si_min = 100000
                si_max = 1000000
                
            doc = frappe.get_doc({
                "doctype": "Product Type",
                "product_name": p["name"],
                "insurer": p["ins"],
                "policy_type": p["pt"],
                "base_premium": p["bp"],
                "premium_min": p["p_min"],
                "premium_max": p["p_max"],
                "sum_insured_range": p["sir"],
                "sum_insured_min": si_min,
                "sum_insured_max": si_max,
                "premium_frequency": p["freq"],
                "claim_settlement_ratio": p["csr"],
                "key_features": p["kf"],
                "target_customer": p["tc"],
                "active": 1
            })
            if p["pt"] == "Health":
                doc.network_hospitals = "Cashless facility available in 5,000+ top network hospitals."
            
            doc.insert(ignore_permissions=True)
            products_created += 1
            print(f"Created Product: {p['name']} ({p['ins']})")
            
    frappe.db.commit()
    frappe.logger().info(f"Seed Success: Created {products_created} new Product Types.")
    print(f"\\n--- Seed Complete --- \\nCreated {products_created} Product Types across 5 Insurers and 4 Policy Types.")
