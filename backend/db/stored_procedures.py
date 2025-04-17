from .connection import get_connection
import pymysql

def create_user(first_name, last_name, email, password, contact, role,
                admin_date=None, farm_size=None, crop_count=None,
                cert=None, specialization=None, hire_date=None, lab_id=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_create_user", [
                first_name, last_name, email, password, contact, role,
                admin_date, farm_size, crop_count,
                cert, specialization, hire_date, lab_id
            ])
            result = cursor.fetchone()
            conn.commit()
            return result
    finally:
        conn.close()

def map_crop_to_farm(lat, lon, crop_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_map_farm_crop", [lat, lon, crop_id])
            conn.commit()
    finally:
        conn.close()

def authenticate_user(email, password):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_authenticate_user", [email, password])
            result = cursor.fetchone()
            return result
    finally:
        conn.close()

def update_user_role(user_id, new_role,
                     admin_date=None, farm_size=None, crop_count=None,
                     cert=None, specialization=None, hire_date=None, lab_id=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_update_user_role", [
                user_id, new_role,
                admin_date, farm_size, crop_count,
                cert, specialization, hire_date, lab_id
            ])
            conn.commit()
    finally:
        conn.close()

def update_user_contact(user_id, new_contact):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_manage_users", [user_id, new_contact])
            conn.commit()
    finally:
        conn.close()



def add_farm_location(region_name, street, city, state, country, zipcode,
                      latitude, longitude, user_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_add_farm_location", [
                region_name, street, city, state, country, zipcode,
                latitude, longitude, user_id
            ])
            conn.commit()
    finally:
        conn.close()

def request_soil_sample(
    farmer_id, lab_id, n, p, k, ca, mg, s, lime, c, moisture,
    lat, lon, sample_name
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_request_soil_sample", [
                farmer_id, lab_id, n, p, k, ca, mg, s, lime, c, moisture,
                lat, lon, sample_name
            ])
            conn.commit()
    finally:
        conn.close()

def assign_sample_to_technician(soil_id, technician_id, lab_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_assign_sample_to_technician", [soil_id, technician_id, lab_id])
            conn.commit()
    finally:
        conn.close()

def submit_soil_test_results(soil_id, n, p, k, ca, mg, s, lime, carbon, moisture):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_submit_soil_test_results", [
                soil_id, n, p, k, ca, mg, s, lime, carbon, moisture
            ])
            conn.commit()
    finally:
        conn.close()

def get_soil_sample_results(soil_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_soil_sample_results", [soil_id])
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def classify_soil_sample(soil_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_classify_soil_sample", [soil_id])
            result = cursor.fetchone()
            conn.commit()
            return result
    finally:
        conn.close()


def get_crop_recommendations(soil_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_crop_recommendations", [soil_id])
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def get_fertilizer_recommendations(crop_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_fertilizer_recommendations", [crop_id])
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def get_combined_recommendations(soil_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_combined_recommendations", [soil_id])
            results = []
            while True:
                result = cursor.fetchall()
                if result:
                    results.append(result)
                if not cursor.nextset():
                    break
            return results
    finally:
        conn.close()

def record_crop_growth(farmer_id, crop_id, start_date, end_date, status, yield_qty):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_record_crop_growth", [
                farmer_id, crop_id, start_date, end_date, status, yield_qty
            ])
            conn.commit()
    finally:
        conn.close()

def update_crop_growth(growth_id, new_status, end_date, yield_qty):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_update_crop_growth", [
                growth_id, new_status, end_date, yield_qty
            ])
            conn.commit()
    finally:
        conn.close()

def get_crop_growth(farmer_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_crop_growth", [farmer_id])
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def map_farm_crop(latitude, longitude, crop_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_map_farm_crop", [latitude, longitude, crop_id])
            conn.commit()
    finally:
        conn.close()


def set_fertility_thresholds(fert_class_id, min_n, max_n, min_p, max_p,
                             min_k, max_k, min_ca, max_ca, min_c, max_c,
                             min_lime, max_lime, min_s, max_s, min_moist, max_moist):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_set_fertility_thresholds", [
                fert_class_id, min_n, max_n, min_p, max_p,
                min_k, max_k, min_ca, max_ca, min_c, max_c,
                min_lime, max_lime, min_s, max_s, min_moist, max_moist
            ])
            conn.commit()
    finally:
        conn.close()

def create_soil_test_lab(name, address, contact, admin_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_create_soil_test_lab", [
                name, address, contact, admin_id
            ])
            conn.commit()
    finally:
        conn.close()

def create_lab_technician(first_name, last_name, email, password, contact,
                          certification, specialization, hire_date, lab_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_create_lab_technician", [
                first_name, last_name, email, password, contact,
                certification, specialization, hire_date, lab_id
            ])
            result = cursor.fetchone()
            conn.commit()
            return result
    finally:
        conn.close()

def get_assigned_samples(technician_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_assigned_samples_for_technician", [technician_id])
            results = cursor.fetchall()
            return results
    finally:
        conn.close()

def get_farm_coordinates(farmer_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_farm_coordinates", [farmer_id])
            result = cursor.fetchone()
            return result
    finally:
        conn.close()

def request_soil_sample(
    farmer_id, lab_id, nitrogen, phosphorus, potassium,
    calcium, magnesium, sulfur, lime, carbon, moisture,
    latitude, longitude
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_request_soil_sample", [
                farmer_id, lab_id, nitrogen, phosphorus, potassium,
                calcium, magnesium, sulfur, lime, carbon, moisture,
                latitude, longitude
            ])
            conn.commit()
    finally:
        conn.close()

def get_soil_sample_results(soil_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_soil_sample_results", [soil_id])
            result = cursor.fetchone()
            return result
    finally:
        conn.close()

def get_latest_classified_soil_sample(farmer_id):
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.callproc("sp_get_latest_classified_soil_sample", (farmer_id,))
            result = cursor.fetchone()
            return result
    finally:
        conn.close()

def get_farm_location_by_farmer(conn, farmer_id):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.callproc("sp_get_farm_location_by_farmer", (farmer_id,))
        return cursor.fetchone()



def record_crop_growth(farmer_id, crop_id, start_date, end_date, status, yield_qty):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_record_crop_growth", [
                farmer_id, crop_id, start_date, end_date, status, yield_qty
            ])
            conn.commit()
    finally:
        conn.close()

def update_crop_growth(growth_id, new_status, end_date, yield_qty):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_update_crop_growth", [
                growth_id, new_status, end_date, yield_qty
            ])
            conn.commit()
    finally:
        conn.close()

def get_crop_growth_records(farmer_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_crop_growth", [farmer_id])
            return cursor.fetchall()
    finally:
        conn.close()



def get_crop_recommendations(fert_class_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_crop_recommendations", [fert_class_id])
            return cursor.fetchall()
    finally:
        conn.close()

def get_fertilizer_recommendations(crop_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_fertilizer_recommendations", [crop_id])
            return cursor.fetchall()
    finally:
        conn.close()

def get_all_labs():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_all_labs")
            return cursor.fetchall()
    finally:
        conn.close()

def get_all_users():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_all_users")
            result = cursor.fetchall()
            return result
    finally:
        conn.close()


def get_all_soil_labs():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_all_soil_labs")
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def add_soil_lab(lab_name, address, contact):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_add_soil_lab", [lab_name, address, contact])
            conn.commit()
    finally:
        conn.close()

def remove_soil_lab(lab_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_remove_soil_lab", [lab_id])
            conn.commit()
    finally:
        conn.close()


def set_fertility_thresholds(fertility_class_id, threshold_values):
    try:
        params = {
            'in_fertility_class_id': fertility_class_id,
            'in_min_nitrogen': threshold_values.get('min_nitrogen', None),
            'in_max_nitrogen': threshold_values.get('max_nitrogen', None),
            'in_min_phosphorus': threshold_values.get('min_phosphorus', None),
            'in_max_phosphorus': threshold_values.get('max_phosphorus', None),
            'in_min_potassium': threshold_values.get('min_potassium', None),
            'in_max_potassium': threshold_values.get('max_potassium', None),
            'in_min_calcium': threshold_values.get('min_calcium', None),
            'in_max_calcium': threshold_values.get('max_calcium', None),
            'in_min_carbon': threshold_values.get('min_carbon', None),
            'in_max_carbon': threshold_values.get('max_carbon', None),
            'in_min_lime': threshold_values.get('min_lime', None),
            'in_max_lime': threshold_values.get('max_lime', None),
            'in_min_sulfur': threshold_values.get('min_sulfur', None),
            'in_max_sulfur': threshold_values.get('max_sulfur', None),
            'in_min_moisture': threshold_values.get('min_moisture', None),
            'in_max_moisture': threshold_values.get('max_moisture', None)
        }
        
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.callproc("sp_set_fertility_thresholds", list(params.values()))
            conn.commit()
        print("Fertility thresholds updated successfully.")
    except Exception as e:
        print(f"Error in set_fertility_thresholds: {e}")
    finally:
        conn.close()


def get_regional_fertility_reports(conn, region_name):
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_get_regional_fertility_reports', (region_name,))
            
            result = cursor.fetchall()
            
            if not result:
                print(f"No fertility data found for region: {region_name}")
                return []
            
            return result
    except Exception as e:
        print(f"Error retrieving regional fertility data: {e}")
        return []

def submit_soil_test_results(soil_id, n, p, k, ca, mg, s, lime, c, moisture):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_submit_soil_test_results", [soil_id, n, p, k, ca, mg, s, lime, c, moisture])
            conn.commit()
    finally:
        conn.close()


def classify_soil_sample(soil_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_classify_soil_sample", [soil_id])
            result = cursor.fetchone()
            conn.commit()
            return result 
    finally:
        conn.close()

def get_lab_pending_samples(lab_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_lab_pending_samples", [lab_id])
            return cursor.fetchall()
    finally:
        conn.close()

def request_soil_sample_tested(
    farmer_id, lab_id, n, p, k, ca, mg, s, lime, c, moisture,
    lat, lon, sample_name
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_request_soil_sample_tested", [
                farmer_id, lab_id, n, p, k, ca, mg, s, lime, c, moisture,
                lat, lon, sample_name
            ])
            result = cursor.fetchall()
            return result[0] if result else None
    finally:
        conn.close()



def get_all_classified_soil_samples(farmer_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_all_classified_soil_samples", [farmer_id])
            return cursor.fetchall()
    finally:
        conn.close()

def get_all_fertility_classes():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_all_fertility_classes")
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def get_fertility_class_by_id(class_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_fertility_class_by_id", [class_id])
            result = cursor.fetchone()
            if not result:
                return None
            return result
    finally:
        conn.close()

def get_all_regions(conn):
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_all_regions")
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error fetching regions: {e}")
        return []

def get_tested_samples_by_lab(lab_id):
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.callproc("sp_get_tested_samples_by_lab", (lab_id,))
            return cursor.fetchall()
    finally:
        conn.close()

def get_all_crops(conn):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.callproc("sp_get_all_crops")
        return cursor.fetchall()
