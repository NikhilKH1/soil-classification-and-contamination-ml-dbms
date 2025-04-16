from .connection import get_connection

# ============================
# 1. USER MANAGEMENT
# ============================

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


# ============================
# 2. FARM / SOIL MANAGEMENT
# ============================

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

def request_soil_sample(farmer_id, lab_id, n, p, k, ca, mg, s, lime, carbon, moisture,
                        latitude, longitude):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_request_soil_sample", [
                farmer_id, lab_id, n, p, k, ca, mg, s, lime, carbon, moisture,
                latitude, longitude
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


# ============================
# 3. RECOMMENDATIONS
# ============================

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


# ============================
# 4. CROP GROWTH TRACKING
# ============================

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


# ============================
# 5. ADMIN / REPORTS
# ============================

def get_regional_fertility_reports(region_name):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_regional_fertility_reports", [region_name])
            result = cursor.fetchall()
            return result
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
        with conn.cursor() as cursor:
            cursor.callproc("sp_get_latest_classified_soil_sample", [farmer_id])
            return cursor.fetchone()
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


