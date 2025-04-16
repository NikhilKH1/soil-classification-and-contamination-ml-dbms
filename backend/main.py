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
    update_user_contact,
    set_fertility_thresholds,
    get_regional_fertility_reports
)


def main():
    try:
        conn = get_connection()
        print("\nConnected to Crop & Fertilizer Database successfully!")
    except pymysql.err.OperationalError as e:
        print(f"Database connection error: {e}")
        return

    while True:
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
        role = input("Enter Role (Farmer/Lab_Technician/Admin): ")

        admin_date = farm_size = crop_count = None
        cert = specialization = hire_date = lab_id = None

        if role == 'Admin':
            admin_date = input("Enter Admin Hire Date (YYYY-MM-DD): ") or None
        elif role == 'Farmer':
            farm_size = float(input("Enter Farm Size (in acres): "))
            crop_count = int(input("Enter Crop Count: "))
        elif role == 'Lab_Technician':
            cert = input("Enter Certification: ")
            specialization = input("Enter Specialization: ")
            hire_date = input("Enter Hire Date (YYYY-MM-DD): ") or None
            lab_id = int(input("Enter Lab ID: "))

        user = create_user(
            first_name, last_name, email, password,
            contact, role, admin_date, farm_size, crop_count,
            cert, specialization, hire_date, lab_id
        )

        print(f"\nUser registered successfully: {user}")

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
        print("4: View Recommended Crops for the Soil Test Result ")
        print("5: View Recommended Fertilizers for the Soil Test Result")
        print("6: Record Crop Growth")
        print("7: Update Crop Growth Status")
        print("8: View Crop Growth")
        print("9: Map Crop to My Farm")
        print("10: Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_farm_location_flow(conn, farmer_id)
        elif choice == "2":
            request_soil_sample_flow(conn, farmer_id)
        elif choice == "3":
            view_farmer_soil_results_flow(conn, farmer_id)
        elif choice == "4":
            view_crop_recommendations_flow(conn, farmer_id)
        elif choice == "5":
            view_fertilizer_recommendations_flow(conn, farmer_id)
        elif choice == "6":
            record_crop_growth_flow(conn, farmer_id)
        elif choice == "7":
            update_crop_growth_flow(conn, farmer_id)
        elif choice == "8":
            view_crop_growth_flow(conn, farmer_id)
        elif choice == "9":
            map_crop_to_farm_flow(conn, farmer_id)
        elif choice == "10":
            break
        else:
            print("Invalid choice. Please enter 1 to 10.")

def map_crop_to_farm_flow(conn, farmer_id):
    print("\n-- Map Crop to Farm --")
    try:
        coords = get_farm_coordinates(farmer_id)
        if not coords:
            print("No farm location found. Please add one first.")
            return

        lat, lon = coords["latitude"], coords["longitude"]

        with conn.cursor() as cursor:
            cursor.execute("SELECT crop_id, crop_name FROM Crop")
            crops = cursor.fetchall()

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
            print(f"ID: {c['growth_id']} | Crop: {c['crop_name']} | Status: {c['status']} | "
                  f"Start: {c['start_date']} | End: {c['end_date']} | Yield: {c['yield_quantity']} kg")
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

        print("\n📋 Choose a Crop:")
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


        # Shared variables
        n = p = k = ca = mg = s = lime = c = moisture = None

        if mode == "1":
            print("\nEnter Soil Nutrient Details:")
            n = float(input("Nitrogen (N): "))
            p = float(input("Phosphorus (P): "))
            k = float(input("Potassium (K): "))
            ca = float(input("Calcium (Ca): "))
            mg = float(input("Magnesium (Mg): "))
            s = float(input("Sulfur (S): "))
            lime = float(input("Lime: "))
            c = float(input("Carbon (C): "))
            moisture = float(input("Moisture %: "))

        request_soil_sample(
            farmer_id, lab_id, n, p, k, ca, mg, s, lime, c, moisture, lat, lon
        )

        print("\n Soil sample request submitted successfully!")

    except Exception as e:
        print(f"\n Error requesting soil sample: {e}")

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
            class_name = result["class_name"]
            description = result["description"]
            print(f"Fertility Class: {class_name} - {description}")
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

def view_assigned_samples(conn, technician_id):
    try:
        samples = get_assigned_samples(technician_id)
        if not samples:
            print("No soil samples assigned to you yet.")
        else:
            print("\nAssigned Soil Samples:")
            for s in samples:
                print(f"  - Soil ID: {s['soil_id']} | Date: {s['test_date']}")
    except Exception as e:
        print(f"Error: {e}")


def lab_technician_dashboard(conn, user):
    technician_id = user['user_id']

    while True:
        print("\nLab Technician Dashboard")
        print("1: View Assigned Soil Samples")
        print("2: Submit Soil Test Results")
        print("3: View Soil Sample Results")
        print("4: Classify Soil Sample (Manual)")
        print("5: Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_assigned_samples(conn, technician_id)
        elif choice == "2":
            submit_test_results(conn)
        elif choice == "3":
            view_soil_sample_results_flow(conn)
        elif choice == "4":
            classify_soil_sample_flow(conn)
        elif choice == "5":
            break
        else:
            print("Invalid input. Choose 1-5.")

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
            region_name = input("Enter region name to view reports: ")
            reports = display_regional_fertility_reports(conn, region_name)

            export_option = input("Do you want to export the report to CSV? (y/n): ")
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
        print("2: Update User Contact")
        print("3: Back to Admin Menu")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            try:
                # This function calls the stored procedure 'sp_get_all_users'
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
                user_id = int(input("Enter the User ID to update contact information: "))
                new_contact = input("Enter the new contact number: ")
                # Calls the stored procedure function from stored_procedures.py
                update_user_contact(user_id, new_contact)
                print("User contact updated successfully.")
            except Exception as e:
                print(f"Error updating user contact: {e}")
                
        elif choice == "3":
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
                    print(lab)
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
        # Take user input for fertility class ID
        class_id = int(input("Enter Fertility Class ID to update: "))

        # Ask the user which thresholds they want to update
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

        # Create a dictionary to hold the new values for the updated fields
        updated_values = {}

        if threshold_choices.lower() == 'all':
            # If the user wants to update all fields, prompt for values for all fields
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
            # If the user wants to update specific fields, ask for values for those fields
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

        # Call the set_fertility_thresholds function
        set_fertility_thresholds(class_id, updated_values)

    except Exception as e:
        print(f"Error updating threshold: {e}")

def display_regional_fertility_reports(conn, region_name):
    reports = get_regional_fertility_reports(conn, region_name)
    
    if not reports:
        return

    # Print headers
    print(f"\n-- Regional Fertility Reports for {region_name} --")
    print(f"{'Region':<20}{'Total Samples':<15}{'Avg Nitrogen':<15}{'Avg Phosphorus':<15}{'Avg Potassium':<15}{'Avg Moisture':<15}")
    print("-" * 95)

    # Print data
    for row in reports:
        print(f"{row['region_name']:<20}{row['total_samples']:<15}{row['avg_nitrogen']:<15.2f}"
              f"{row['avg_phosphorus']:<15.2f}{row['avg_potassium']:<15.2f}{row['avg_moisture']:<15.2f}")
    return reports

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
