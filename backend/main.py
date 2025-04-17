import pymysql
import csv
import random
from getpass import getpass
from db.connection import get_connection
from db.stored_procedures import (
    create_user, authenticate_user,
    add_farm_location,
    request_soil_sample,
    get_assigned_samples,
    request_soil_sample,
    get_farm_coordinates,
    get_latest_classified_soil_sample,
    get_crop_recommendations,
    get_all_labs,
    record_crop_growth,
    get_fertilizer_recommendations,
    update_crop_growth,
    record_crop_growth,
    get_crop_growth,
    get_crop_growth_records,
    map_crop_to_farm,
    get_all_users,
    get_all_soil_labs,
    add_soil_lab,
    remove_soil_lab,
    set_fertility_thresholds,
    get_regional_fertility_reports,
    submit_soil_test_results,
    classify_soil_sample,
    get_lab_pending_samples,
    request_soil_sample_tested,
    get_all_classified_soil_samples,
    get_tested_samples_by_lab,
    get_soil_sample_results,
    get_all_crops,
    get_all_fertility_classes,
    get_fertility_class_by_id,
    get_all_regions,
    get_yield_estimate,
    get_years_experience,
    get_all_lab_technicians_with_experience,
    delete_crop_growth_record,
    update_user_details
)


def main():
    try:
        conn = get_connection()
        print("\nConnected to Crop & Fertilizer Database successfully!")
    except pymysql.err.OperationalError as e:
        print(f"Database connection error: {e}")
        return

    while True:
        print("\n🌾 Welcome to Crop & Fertilizer Recommendation System 🌾")
        print("----------------------------------------------------------")
        print("\nMain Menu:")
        print("1: Register a New User")
        print("2: Login Existing User")
        print("3: Disconnect and Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user(conn)
        elif choice == "2":
            login_user(conn)
        elif choice == "3":
            print("Disconnecting from Database...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    conn.close()
    print("Disconnected successfully.")

def view_crop_recommendations_flow(conn, farmer_id):
    print("\n-- Recommended Crops Based on Soil Fertility --")
    try:
        latest_sample = get_latest_classified_soil_sample(farmer_id)

        if not latest_sample:
            print("No classified soil sample found. Please submit a complete test first.")
            return

        fert_class_id = latest_sample["fertility_class_id"]
        crops = get_crop_recommendations(fert_class_id)

        if not crops:
            print("No crop recommendations found for your soil.")
            return

        print("\n Suitable Crops Based on Your Soil:")
        for crop in crops:
            print(f" - {crop['crop_name']}")
    except Exception as e:
        print(f"Error: {e}")


def register_user(conn):
    print("\n-- User Registration --")
    try:
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        email = input("Enter Email: ")
        password = getpass("Enter Password: ")
        contact = input("Enter Contact: ")
        roles = ['Farmer', 'Lab_Technician', 'Admin']

        print(f"Available Roles: {', '.join(roles)}")
        while True:
            role = input("Enter Role: ")
            if role in roles:
                break
            print("Invalid role selected. Please choose from the listed options.")

        admin_date = farm_size = crop_count = None
        cert = specialization = hire_date = lab_id = None

        if role == 'Admin':
            admin_date = input("Enter Admin Hire Date (YYYY-MM-DD): ") or None
        elif role == 'Farmer':
            farm_size = float(input("Enter Farm Size (in acres): "))
            crop_count = int(input("Enter Crop Count: "))
        elif role == 'Lab_Technician':
            cert = input("Enter Certification (e.g., Soil Analyst, Agronomist, Lab Expert): ")
            specialization = input("Enter Specialization (e.g., Nitrogen Analysis, Mineral Testing, pH Monitoring, Organic Content): ")
            hire_date = input("Enter Hire Date (YYYY-MM-DD): ") or None
            labs = get_all_labs()
            print("\nAvailable Labs:")
            for lab in labs:
                print(f"{lab['lab_id']}: {lab['lab_name']}")
            lab_id = int(input("Enter Lab ID: "))

        user = create_user(
            first_name, last_name, email, password,
            contact, role, admin_date, farm_size, crop_count,
            cert, specialization, hire_date, lab_id
        )

        print(f"\nUser registered successfully")
        print(f"Welcome {first_name} ({role})")

    except Exception as e:
        print(f"\nRegistration error: {e}")


def login_user(conn):
    print("\n-- User Login --")
    email = input("Enter Email: ")
    password = getpass("Enter Password: ")

    user = authenticate_user(email, password)
    if user:
        print(f"\nLogin successful! ")
        user_dashboard(conn, user)
    else:
        print("\nInvalid email or password. Please try again.")


def user_dashboard(conn, user):
    role = user['role']
    print(f"\nLogged in as {role}")

    if role == "Farmer":
        farmer_dashboard(conn, user)
    elif role == "Lab_Technician":
        lab_technician_dashboard(conn, user)
    elif role == "Admin":
        admin_dashboard(conn, user)



def farmer_dashboard(conn, user):
    farmer_id = user['user_id']

    while True:
        print("\n Farmer Dashboard")
        print("1: Add Farm Location")
        print("2: Request Soil Sample Test")
        print("3: View My Soil Test Results")
        print("4: View All Test Results")
        print("5: View Recommended Crops for the Soil Test Result ")
        print("6: View Recommended Fertilizers for the Soil Test Result")
        print("7: Record Crop Growth")
        print("8: Update Crop Growth Status")
        print("9: View Crop Growth")
        print("10: Delete Crop Growth Record")
        print("11: Map Crop to My Farm")
        print("12: Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_farm_location_flow(conn, farmer_id)
        elif choice == "2":
            request_soil_sample_flow(conn, farmer_id)
        elif choice == "3":
            view_farmer_soil_results_flow(conn, farmer_id)
        elif choice == "4":
            view_all_soil_results(conn, farmer_id)
        elif choice == "5":
            view_crop_recommendations_flow(conn, farmer_id)
        elif choice == "6":
            view_fertilizer_recommendations_flow(conn, farmer_id)
        elif choice == "7":
            record_crop_growth_flow(conn, farmer_id)
        elif choice == "8":
            update_crop_growth_flow(conn, farmer_id)
        elif choice == "9":
            view_crop_growth_flow(conn, farmer_id)
        elif choice == "10":
            delete_crop_growth_flow(conn, farmer_id)
        elif choice == "11":  
            map_crop_to_farm_flow(conn, farmer_id)
        elif choice == "12":
            break
        else:
            print("Invalid choice. Please enter 1 to 12.")

def delete_crop_growth_flow(conn, farmer_id):
    print("\n-- Delete Crop Growth Record --")
    try:
        crops = get_crop_growth_records(farmer_id)

        if not crops:
            print("You have no crop growth records.")
            return

        print("\n🌾 Your Crop Growth Records:")
        for c in crops:
            print(f"ID: {c['growth_id']} | Crop: {c['crop_name']} | Status: {c['status']}")

        growth_id = int(input("Enter Growth ID to delete: "))

        valid_ids = [c['growth_id'] for c in crops]
        if growth_id not in valid_ids:
            print("Invalid Growth ID.")
            return

        confirm = input("Are you sure you want to delete this record? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Deletion cancelled.")
            return

        delete_crop_growth_record(growth_id)
        print("Crop growth record deleted. Crop count updated automatically.")

    except Exception as e:
        print(f"Error deleting crop growth record: {e}")


def view_all_soil_results(conn, farmer_id):
    print("\n-- All Soil Test Results --")
    try:
        results = get_all_classified_soil_samples(farmer_id)
        if not results:
            print("No soil results found.")
            return

        for res in results:
            print(f"Sample ID: {res['soil_id']} | Date: {res['test_date']} | "
                  f"Fertility: {res['class_name']} - {res['description']}")
    except Exception as e:
        print(f"Error: {e}")



def map_crop_to_farm_flow(conn, farmer_id):
    print("\n-- Map Crop to Farm --")
    try:
        coords = get_farm_coordinates(farmer_id)
        if not coords:
            print("No farm location found. Please add one first.")
            return

        lat, lon = coords["latitude"], coords["longitude"]

        crops = get_all_crops(conn)

        if not crops:
            print("No crops available. Ask Admin to add crops first.")
            return

        print("\nAvailable Crops:")
        for crop in crops:
            print(f"{crop['crop_id']}: {crop['crop_name']}")

        crop_id = int(input("Enter the Crop ID to map to your farm: "))
        crop_ids = [crop['crop_id'] for crop in crops]
        if crop_id not in crop_ids:
            print("Invalid Crop ID.")
            return

        map_crop_to_farm(lat, lon, crop_id)
        print("Crop mapped to your farm successfully!")

    except Exception as e:
        print(f" Error mapping crop to farm: {e}")



def view_crop_growth_flow(conn, farmer_id):
    print("\n-- View Crop Growth --")
    try:
        crops = get_crop_growth(farmer_id)
        if not crops:
            print("You have no crop growth records.")
            return

        print("\n🌱 Your Crop Growth Records:")
        for c in crops:
            est_yield = get_yield_estimate(c['growth_id']) or "N/A"
            print(f"ID: {c['growth_id']} | Crop: {c['crop_name']} | Status: {c['status']} | "
                  f"Start: {c['start_date']} | End: {c['end_date']} | "
                  f"Yield: {c['yield_quantity']} kg | Est. Yield: {est_yield} kg")

    except Exception as e:
        print(f" Error viewing crop growth: {e}")



def update_crop_growth_flow(conn, farmer_id):
    print("\n-- Update Crop Growth --")
    try:
        crops = get_crop_growth_records(farmer_id)

        if not crops:
            print("You have no crop growth records.")
            return

        print("\n🌾 Your Crop Records:")
        for c in crops:
            print(f"ID: {c['growth_id']} | Crop: {c['crop_name']} | Status: {c['status']} | "
                  f"Start: {c['start_date']} | End: {c['end_date']}")

        growth_id = int(input("\nEnter the Growth ID to update: "))
        new_status = input("New Status (Planted/Growing/Harvested): ").strip()
        end_date = input("Enter End Date (YYYY-MM-DD): ").strip()
        yield_qty = float(input("Enter Yield Quantity (kg): "))

        update_crop_growth(growth_id, new_status, end_date, yield_qty)
        print(" Crop growth updated successfully!")

    except Exception as e:
        print(f" Error updating crop growth: {e}")


def record_crop_growth_flow(conn, farmer_id):
    print("\n-- Record Crop Growth --")
    try:
        latest_sample = get_latest_classified_soil_sample(farmer_id)
        if not latest_sample:
            print("You need a classified soil sample to proceed.")
            return

        fert_class_id = latest_sample["fertility_class_id"]
        crops = get_crop_recommendations(fert_class_id)
        if not crops:
            print("No crops available for your soil.")
            return

        print("\n Choose a Crop:")
        for i, crop in enumerate(crops):
            print(f"{i + 1}. {crop['crop_name']}")
        idx = int(input("Enter crop number: ")) - 1

        selected_crop = crops[idx]
        crop_id = selected_crop["crop_id"]

        start_date = input("Start Date (YYYY-MM-DD): ")
        end_date = input("End Date (YYYY-MM-DD): ")
        status = input("Status (Planted/Growing/Harvested): ")
        yield_qty = float(input("Yield Quantity (in kg): "))

        record_crop_growth(farmer_id, crop_id, start_date, end_date, status, yield_qty)
        print("Crop growth record submitted!")

    except Exception as e:
        print(f"Error: {e}")


def request_soil_sample_flow(conn, farmer_id):
    print("\n-- Request Soil Sample Test --")
    try:
        print("Select the type of soil sample submission:")
        print("1. Submit complete nutrient details for immediate processing")
        print("2. Submit only basic request; lab technician will complete nutrient testing")

        mode = input("Choice (1 or 2): ").strip()

        if mode not in ["1", "2"]:
            print("Invalid choice.")
            return

        coords = get_farm_coordinates(farmer_id)
        if not coords:
            print("No farm location found. Please add a farm location first.")
            return
        lat, lon = coords["latitude"], coords["longitude"]

        labs = get_all_labs()
        print("\nAvailable Labs:")
        for lab in labs:
            print(f"{lab['lab_id']}: {lab['lab_name']}")
        lab_id = int(input("Enter the Lab ID to send your soil sample to: "))
        if lab_id not in [lab['lab_id'] for lab in labs]:
            print("\n Invalid Lab ID. Please select from the list above.")
            return

        raw_input = input("\nEnter a name to identify this sample (e.g., 'North Plot - Morning'): ").strip()

        if not (raw_input.startswith('"') and raw_input.endswith('"')):
            sample_name = f'"{raw_input}"'
        else:
            sample_name = raw_input

        n = p = k = ca = mg = s = lime = c = moisture = None

        if mode == "1":
            print("\nEnter Soil Nutrient Details:")
            n = get_valid_nutrient("Nitrogen (N)")
            p = get_valid_nutrient("Phosphorus (P)")
            k = get_valid_nutrient("Potassium (K)")
            ca = get_valid_nutrient("Calcium (Ca)")
            mg = get_valid_nutrient("Magnesium (Mg)")
            s = get_valid_nutrient("Sulfur (S)")
            lime = get_valid_nutrient("Lime")
            c = get_valid_nutrient("Carbon (C)")
            moisture = get_valid_nutrient("Moisture %")

            result = request_soil_sample_tested(
                farmer_id, lab_id, n, p, k, ca, mg, s, lime, c, moisture, lat, lon, sample_name
            )
            print("\nSoil sample request submitted and classified successfully!")

        elif mode == "2":
            request_soil_sample(
                farmer_id, lab_id, n, p, k, ca, mg, s, lime, c, moisture, lat, lon, sample_name
            )
            print("\nSoil sample request submitted successfully! (pending lab technician input)")

    except Exception as e:
        print(f"\n Error requesting soil sample: {e}")


def get_valid_nutrient(field_name):
    while True:
        try:
            value = float(input(f"{field_name}: "))
            if 0 <= value <= 999.99:
                return value
            else:
                print("Invalid Input. Please enter a number between 0 and 999.99.")
        except ValueError:
            print("\nInvalid input. Please enter a numeric value.")


def view_fertilizer_recommendations_flow(conn, farmer_id):
    print("\n-- Recommended Fertilizers Based on Soil Fertility --")
    try:
        latest_sample = get_latest_classified_soil_sample(farmer_id)
        if not latest_sample:
            print("No classified soil sample found.")
            return

        fert_class_id = latest_sample["fertility_class_id"]
        crops = get_crop_recommendations(fert_class_id)

        if not crops:
            print("No crop recommendations found.")
            return

        print("\n Select a Crop to Get Fertilizer Suggestions:")
        for idx, crop in enumerate(crops):
            print(f"{idx + 1}. {crop['crop_name']}")

        choice = int(input("Enter your choice: "))
        if choice < 1 or choice > len(crops):
            print("Invalid choice.")
            return

        selected_crop = crops[choice - 1]
        fertilizers = get_fertilizer_recommendations(selected_crop["crop_id"])

        print(f"\n Recommended Fertilizers for {selected_crop['crop_name']}:")
        for fert in fertilizers:
            print(f" - {fert['fertilizer_name']} (NPK: {fert['npk_ratio']})")

    except Exception as e:
        print(f"Error: {e}")


def view_farmer_soil_results_flow(conn, farmer_id):
    print("\n-- View Soil Test Results --")
    try:
        result = get_latest_classified_soil_sample(farmer_id) 

        if result:
            sample_name = result.get("sample_name")
            if sample_name is None:
                sample_name = "Unnamed Sample"
            print(f"\nSample Name: {sample_name}")
            print(f"Fertility Class: {result['class_name']} - {result['description']}")
        else:
            print("No classified soil sample found. Try submitting a test with complete details.")
    except Exception as e:
        print(f"Error: {e}")


def add_farm_location_flow(conn, farmer_id):
    print("\n-- Add Farm Location --")
    try:
        region = input("Region Name: ")
        street = input("Street: ")
        city = input("City: ")
        state = input("State: ")
        country = input("Country: ")
        zipcode = input("Zip Code: ")
        lat = round(random.uniform(10.0, 40.0), 6)
        lon = round(random.uniform(60.0, 90.0), 6)

        add_farm_location(region, street, city, state, country, zipcode, lat, lon, farmer_id)
        print("Farm location added successfully!")

    except Exception as e:
        print(f"Error adding farm location: {e}")

def view_lab_pending_samples(conn, lab_id):
    print("\n-- Pending Soil Samples in Your Lab --")
    try:
        samples = get_lab_pending_samples(lab_id)
        if not samples:
            print("No pending soil samples for your lab.")
            return

        for s in samples:
            print(f"  - Soil ID: {s['soil_id']} | Farmer ID: {s['farmer_id']} | Date: {s['test_date']}")

    except Exception as e:
        print(f"Error fetching lab samples: {e}")



def lab_technician_dashboard(conn, user):
    technician_id = user['user_id']

    while True:
        print("\nLab Technician Dashboard")
        print("1: View Assigned Soil Samples")
        print("2: Submit Soil Test Results")
        print("3: View Soil Sample Results")
        print("4: Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_lab_pending_samples(conn, user['lab_id'])
        elif choice == "2":
            submit_test_results(conn, user)
        elif choice == "3":
            view_soil_sample_results_flow(conn, user)
        elif choice == "4":
            break
        else:
            print("Invalid input. Choose 1-4.")

def view_soil_sample_results_flow(conn, user):
    print("\n-- View Soil Sample Results --")
    try:
        lab_id = user.get("lab_id")
        if lab_id is None:
            print("Lab ID not found for this technician.")
            return

        samples = get_tested_samples_by_lab(lab_id)

        if not samples:
            print("No tested soil samples found for your lab.")
            return

        print("\n Tested Samples in Your Lab:")
        for s in samples:
            sample_name = s["sample_name"] or "Unnamed Sample"
            print(f"  - Soil ID: {s['soil_id']} | Sample: {sample_name} | Fertility: {s['class_name']} | Date: {s['test_date'].strftime('%Y-%m-%d')} | Farmer ID: {s['farmer_id']}")

        soil_id_input = input("\nEnter Soil Sample ID to view full details (or press Enter to skip): ").strip()
        if not soil_id_input:
            return

        try:
            soil_id = int(soil_id_input)
        except ValueError:
            print("Invalid Soil ID. Please enter a valid number.")
            return
        
        result = get_soil_sample_results(soil_id)

        if result:
            print("\n Full Soil Sample Details:")
            print(f"Sample ID     : {result['soil_id']}")
            print(f"Sample Name   : {result['sample_name'] or 'Unnamed Sample'}")
            print(f"Farmer ID     : {result['farmer_id']}")
            print(f"Date          : {result['test_date']}")
            print(f"Fertility     : {result['class_name']} - {result['description']}")
            print(f"Nitrogen (N)  : {result['nitrogen']}")
            print(f"Phosphorus (P): {result['phosphorus']}")
            print(f"Potassium (K) : {result['potassium']}")
            print(f"Calcium (Ca)  : {result['calcium']}")
            print(f"Magnesium (Mg): {result['magnesium']}")
            print(f"Sulfur (S)    : {result['sulfur']}")
            print(f"Lime          : {result['lime']}")
            print(f"Carbon (C)    : {result['carbon']}")
            print(f"Moisture %    : {result['moisture']}")
        else:
            print("No detailed result found for that Soil ID.")

    except Exception as e:
        print(f"Error viewing sample results: {e}")


def submit_test_results(conn, technician):
    print("\n-- Submit Soil Test Results --")
    try:
        lab_id = technician['lab_id']
        pending_samples = get_lab_pending_samples(lab_id)

        if not pending_samples:
            print("No pending soil samples to update.")
            return

        print("\nPending Samples in Your Lab:")
        for s in pending_samples:
            print(f"  - Soil ID: {s['soil_id']} | Farmer ID: {s['farmer_id']} | Date: {s['test_date']}")

        valid_ids = [s['soil_id'] for s in pending_samples]
        soil_id = int(input("\nEnter the Soil Sample ID to update: "))
        if soil_id not in valid_ids:
            print("Invalid selection. Please choose a Soil ID from the list.")
            return

        print("Enter updated nutrient values:")
        n = float(input("Nitrogen (N): "))
        p = float(input("Phosphorus (P): "))
        k = float(input("Potassium (K): "))
        ca = float(input("Calcium (Ca): "))
        mg = float(input("Magnesium (Mg): "))
        s = float(input("Sulfur (S): "))
        lime = float(input("Lime: "))
        c = float(input("Carbon (C): "))
        moisture = float(input("Moisture %: "))

        submit_soil_test_results(soil_id, n, p, k, ca, mg, s, lime, c, moisture)
        result = classify_soil_sample(soil_id)

        print(f"\nSoil sample {soil_id} classified as Fertility Class ID: {result['Fertility_Class_ID']}")
        print("Test results submitted.")

    except Exception as e:
        print(f"Error submitting test results: {e}")



def admin_dashboard(conn, user):
    """Admin Dashboard offering multiple administrative functionalities."""
    print("\n--- Admin Dashboard ---")

    while True:
        print("\nAdmin Options:")
        print("1: Manage Users")
        print("2: Manage Soil Test Labs")
        print("3: Update Soil Fertility Threshold Values")
        print("4: Monitor Regional Fertility Reports")
        print("5: Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            admin_manage_users_flow(conn)
        elif choice == "2":
            manage_soil_test_labs_flow(conn)
        elif choice == "3":
            update_soil_thresholds_flow(conn)
        elif choice == "4":
            region_name, reports = display_regional_fertility_reports(conn)

            if reports:
                export_option = input("\nDo you want to export the report to CSV? (y/n): ")
                if export_option.lower() == 'y':
                    export_report_to_csv(reports, f"{region_name}_regional_fertility_report.csv")

        elif choice == "5":
                break
        else:
            print("Invalid choice. Please select 1-5.")

def admin_manage_users_flow(conn):
    """
    Admin flow to manage users.
    Provides options for listing users and updating user details.
    All database interactions are done via stored procedure calls from stored_procedures.py.
    """
    while True:
        print("\n--- Manage Users ---")
        print("1: List All Users")
        print("2: Update User Details")
        print("3: View Lab Technicians with Experience")
        print("4: Back to Admin Menu")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            try:
                users = get_all_users()
                if users:
                    print("\n--- List of Users ---")
                    for user in users:
                        print(f"ID: {user['user_id']} | Name: {user['first_name']} {user['last_name']} | Email: {user['email']} | Contact: {user['contact_number']} | Role: {user['role']}")
                else:
                    print("No users found.")
            except Exception as e:
                print(f"Error listing users: {e}")
        
        elif choice == "2":
            try:
                user_id = int(input("Enter the User ID to update: "))
                first_name = input("New First Name (leave blank to keep current): ") or None
                last_name = input("New Last Name (leave blank to keep current): ") or None
                email = input("New Email (leave blank to keep current): ") or None
                contact = input("New Contact Number (leave blank to keep current): ") or None

                update_user_details(user_id, first_name, last_name, email, contact)
                print("User details updated successfully.")
            except Exception as e:
                print(f"Error updating user contact: {e}")
        
        elif choice == "3":
            try:
                technicians = get_all_lab_technicians_with_experience()
                print("\n--- Lab Technicians & Experience ---")
                for tech in technicians:
                    print(f"ID: {tech['user_id']} | Name: {tech['first_name']} {tech['last_name']} | "
                    f"Email: {tech['email']} | Hire Date: {tech['hire_date']} | "
                    f"Experience: {tech['experience']} years")
            except Exception as e:
                print(f"Error fetching technicians: {e}")

                
        elif choice == "4":
            print("Returning to Admin Menu.")
            break
        
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

def manage_soil_test_labs_flow(conn):
    while True:
        print("\n-- Manage Soil Test Labs --")
        print("1: View All Soil Test Labs")
        print("2: Add New Soil Test Lab")
        print("3: Remove Soil Test Lab")
        print("4: Back to Admin Dashboard")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            labs = get_all_soil_labs()
            if not labs:
                print("No soil test labs found.")
            else:
                print("\n-- Soil Test Labs --")
                for lab in labs:
                    print(f"ID: {lab.get('lab_id')}, Name: {lab.get('lab_name')}, Location: {lab.get('address')}, Contact: {lab.get('contact')}")

        elif choice == "2":
            print("\n-- Add New Soil Test Lab --")
            lab_name = input("Lab Name: ")
            address = input("Location: ")
            contact = input("Contact: ")
            add_soil_lab(lab_name, address, contact)
            print("Soil test lab added successfully!")

        elif choice == "3":
            lab_id = input("Enter Lab ID to remove: ")
            remove_soil_lab(lab_id)
            print("Soil test lab removed successfully!")

        elif choice == "4":
            break
        else:
            print("Invalid choice. Please select 1 to 4.")

def update_soil_thresholds_flow(conn):
    print("\n-- Update Soil Fertility Thresholds --")
    try:
        classes = get_all_fertility_classes()
        if not classes:
            print("No fertility classes found.")
            return
        
        print("\nAvailable Fertility Classes:")
        for cls in classes:
            print(f"ID: {cls['fertility_class_id']}, Name: {cls['class_name']}")
        
        class_id = int(input("Enter Fertility Class ID to update: "))

        current = get_fertility_class_by_id(class_id)
        if not current:
            print("Invalid class ID.")
            return

        print("\nCurrent Threshold Values:")
        for key, value in current.items():
            if key not in ['fertility_class_id', 'class_name']:
                print(f"{key.replace('_', ' ').title()}: {value}")

        print("Which fertility thresholds would you like to update?")
        print("You can update multiple fields by entering the corresponding numbers separated by commas.")
        print("1: Min Nitrogen")
        print("2: Max Nitrogen")
        print("3: Min Phosphorus")
        print("4: Max Phosphorus")
        print("5: Min Potassium")
        print("6: Max Potassium")
        print("7: Min Calcium")
        print("8: Max Calcium")
        print("9: Min Carbon")
        print("10: Max Carbon")
        print("11: Min Lime")
        print("12: Max Lime")
        print("13: Min Sulfur")
        print("14: Max Sulfur")
        print("15: Min Moisture")
        print("16: Max Moisture")
        print("To update all fields, enter 'all'.")

        threshold_choices = input("Enter your choices (e.g., 1, 2, 3 or 'all'): ").strip()


        updated_values = {}

        if threshold_choices.lower() == 'all':
            updated_values["min_nitrogen"] = float(input("Enter new Min Nitrogen: "))
            updated_values["max_nitrogen"] = float(input("Enter new Max Nitrogen: "))
            updated_values["min_phosphorus"] = float(input("Enter new Min Phosphorus: "))
            updated_values["max_phosphorus"] = float(input("Enter new Max Phosphorus: "))
            updated_values["min_potassium"] = float(input("Enter new Min Potassium: "))
            updated_values["max_potassium"] = float(input("Enter new Max Potassium: "))
            updated_values["min_calcium"] = float(input("Enter new Min Calcium: "))
            updated_values["max_calcium"] = float(input("Enter new Max Calcium: "))
            updated_values["min_carbon"] = float(input("Enter new Min Carbon: "))
            updated_values["max_carbon"] = float(input("Enter new Max Carbon: "))
            updated_values["min_lime"] = float(input("Enter new Min Lime: "))
            updated_values["max_lime"] = float(input("Enter new Max Lime: "))
            updated_values["min_sulfur"] = float(input("Enter new Min Sulfur: "))
            updated_values["max_sulfur"] = float(input("Enter new Max Sulfur: "))
            updated_values["min_moisture"] = float(input("Enter new Min Moisture: "))
            updated_values["max_moisture"] = float(input("Enter new Max Moisture: "))
        else:
            threshold_choices_list = threshold_choices.split(',')
            for choice in threshold_choices_list:
                choice = choice.strip()
                if choice == "1":
                    updated_values["min_nitrogen"] = float(input("Enter new Min Nitrogen: "))
                elif choice == "2":
                    updated_values["max_nitrogen"] = float(input("Enter new Max Nitrogen: "))
                elif choice == "3":
                    updated_values["min_phosphorus"] = float(input("Enter new Min Phosphorus: "))
                elif choice == "4":
                    updated_values["max_phosphorus"] = float(input("Enter new Max Phosphorus: "))
                elif choice == "5":
                    updated_values["min_potassium"] = float(input("Enter new Min Potassium: "))
                elif choice == "6":
                    updated_values["max_potassium"] = float(input("Enter new Max Potassium: "))
                elif choice == "7":
                    updated_values["min_calcium"] = float(input("Enter new Min Calcium: "))
                elif choice == "8":
                    updated_values["max_calcium"] = float(input("Enter new Max Calcium: "))
                elif choice == "9":
                    updated_values["min_carbon"] = float(input("Enter new Min Carbon: "))
                elif choice == "10":
                    updated_values["max_carbon"] = float(input("Enter new Max Carbon: "))
                elif choice == "11":
                    updated_values["min_lime"] = float(input("Enter new Min Lime: "))
                elif choice == "12":
                    updated_values["max_lime"] = float(input("Enter new Max Lime: "))
                elif choice == "13":
                    updated_values["min_sulfur"] = float(input("Enter new Min Sulfur: "))
                elif choice == "14":
                    updated_values["max_sulfur"] = float(input("Enter new Max Sulfur: "))
                elif choice == "15":
                    updated_values["min_moisture"] = float(input("Enter new Min Moisture: "))
                elif choice == "16":
                    updated_values["max_moisture"] = float(input("Enter new Max Moisture: "))
                else:
                    print(f"Invalid choice: {choice}")
                    return

        set_fertility_thresholds(class_id, updated_values)

    except Exception as e:
        print(f"Error updating threshold: {e}")

def display_regional_fertility_reports(conn):


    regions = get_all_regions(conn)
    if not regions:
        print("No regions found.")
        return None, []
    
    print("\nAvailable Regions:")
    for idx, region in enumerate(regions, start=1):
        print(f"{idx}. {region['region_name']}")

    # Step 2: Prompt user to choose
    try:
        choice = int(input("\nSelect a region by number: "))
        if choice < 1 or choice > len(regions):
            print("Invalid selection.")
            return None, []
        selected_region = regions[choice - 1]['region_name']
    except ValueError:
        print("Invalid input.")
        return None, []
    
    reports = get_regional_fertility_reports(conn, selected_region)
    
    if not reports:
        return selected_region, []

    # Print headers
    print(f"\n-- Regional Fertility Reports for {selected_region} --")
    print(f"{'Region':<20}{'Total Samples':<15}{'Avg Nitrogen':<15}{'Avg Phosphorus':<15}{'Avg Potassium':<15}{'Avg Moisture':<15}")
    print("-" * 95)

    # Print data
    for row in reports:
        print(f"{row['region_name']:<20}{row['total_samples']:<15}{row['avg_nitrogen']:<15.2f}"
              f"{row['avg_phosphorus']:<15.2f}{row['avg_potassium']:<15.2f}{row['avg_moisture']:<15.2f}")
    return selected_region, reports


def export_report_to_csv(report_data, filename="regional_fertility_report.csv"):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=report_data[0].keys())
            writer.writeheader()
            writer.writerows(report_data)
            print(f"Report exported to {filename}")
    except Exception as e:
        print(f"Error exporting report: {e}")
        


if __name__ == "__main__":
    main()