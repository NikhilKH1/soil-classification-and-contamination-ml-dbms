USE crop_fertilizer_db;
-- **************************************************************
-- Crop Fertilizer Recommendation System Setup File
-- Includes Stored Procedures, Functions, Triggers, and Verification Queries
-- **************************************************************

/* ===============================
   1. User Management Stored Procedures
   =============================== */

DELIMITER //
CREATE PROCEDURE sp_create_user(
    IN in_first_name VARCHAR(50),
    IN in_last_name VARCHAR(50),
    IN in_email VARCHAR(100),
    IN in_password VARCHAR(100),
    IN in_contact_number VARCHAR(15),
    IN in_role ENUM('Admin', 'Farmer', 'Lab_Technician'),
    -- Role-specific parameters; for non-applicable roles, pass NULL
    IN in_admin_hire_date DATE,
    IN in_farm_size DECIMAL(6,2),
    IN in_no_of_crops_grown INT,
    IN in_lab_certification TEXT,
    IN in_lab_specialization VARCHAR(50),
    IN in_lab_hire_date DATE,
    IN in_lab_id INT
)
BEGIN
    DECLARE last_id INT;
    
    -- Insert into User table
    INSERT INTO User(first_name, last_name, email, password, contact_number, role)
    VALUES (in_first_name, in_last_name, in_email, in_password, in_contact_number, in_role);
    
    SET last_id = LAST_INSERT_ID();
    
    -- Depending on role, insert into the corresponding table
    IF in_role = 'Admin' THEN
       INSERT INTO Admin(user_id, hire_date)
       VALUES (last_id, in_admin_hire_date);
    ELSEIF in_role = 'Farmer' THEN
       INSERT INTO Farmer(user_id, farm_size, no_of_crops_grown)
       VALUES (last_id, in_farm_size, in_no_of_crops_grown);
    ELSEIF in_role = 'Lab_Technician' THEN
       INSERT INTO Lab_Technician(user_id, certification, specialization, hire_date, lab_id)
       VALUES (last_id, in_lab_certification, in_lab_specialization, in_lab_hire_date, in_lab_id);
    END IF;
    
    SELECT last_id AS user_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_get_farm_coordinates(
    IN in_farmer_id INT
)
BEGIN
    SELECT latitude, longitude
    FROM Farm_Location
    WHERE user_id = in_farmer_id
    LIMIT 1;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_authenticate_user;
DELIMITER //
CREATE PROCEDURE sp_authenticate_user(
    IN in_email VARCHAR(100),
    IN in_password VARCHAR(100)
)
BEGIN
    DECLARE userRole ENUM('Admin', 'Farmer', 'Lab_Technician');

    -- Get role of the user
    SELECT role INTO userRole
    FROM User
    WHERE email = in_email AND password = in_password;

    -- Return appropriate fields based on role
    IF userRole = 'Lab_Technician' THEN
        SELECT u.user_id, u.role, lt.lab_id
        FROM User u
        JOIN Lab_Technician lt ON u.user_id = lt.user_id
        WHERE u.email = in_email AND u.password = in_password;

    ELSE
        SELECT user_id, role
        FROM User
        WHERE email = in_email AND password = in_password;
    END IF;
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_update_user_role(
    IN in_user_id INT,
    IN in_new_role ENUM('Admin','Farmer','Lab_Technician'),
    -- New role-specific parameters (use NULL for inapplicable ones)
    IN in_admin_hire_date DATE,
    IN in_farm_size DECIMAL(6,2),
    IN in_no_of_crops_grown INT,
    IN in_lab_certification TEXT,
    IN in_lab_specialization VARCHAR(50),
    IN in_lab_hire_date DATE,
    IN in_lab_id INT
)
BEGIN
    DECLARE current_role ENUM('Admin','Farmer','Lab_Technician');
    
    SELECT role INTO current_role 
    FROM User 
    WHERE user_id = in_user_id;
    
    IF current_role = in_new_role THEN
        UPDATE User SET role = in_new_role WHERE user_id = in_user_id;
    ELSE
        UPDATE User SET role = in_new_role WHERE user_id = in_user_id;
        
        IF current_role = 'Admin' THEN
            DELETE FROM Admin WHERE user_id = in_user_id;
        ELSEIF current_role = 'Farmer' THEN
            DELETE FROM Farmer WHERE user_id = in_user_id;
        ELSEIF current_role = 'Lab_Technician' THEN
            DELETE FROM Lab_Technician WHERE user_id = in_user_id;
        END IF;
        
        IF in_new_role = 'Admin' THEN
           INSERT INTO Admin(user_id, hire_date)
           VALUES (in_user_id, in_admin_hire_date);
        ELSEIF in_new_role = 'Farmer' THEN
           INSERT INTO Farmer(user_id, farm_size, no_of_crops_grown)
           VALUES (in_user_id, in_farm_size, in_no_of_crops_grown);
        ELSEIF in_new_role = 'Lab_Technician' THEN
           INSERT INTO Lab_Technician(user_id, certification, specialization, hire_date, lab_id)
           VALUES (in_user_id, in_lab_certification, in_lab_specialization, in_lab_hire_date, in_lab_id);
        END IF;
    END IF;
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_manage_users(
    IN in_user_id INT,
    IN in_new_contact VARCHAR(15)
)
BEGIN
    UPDATE User SET contact_number = in_new_contact WHERE user_id = in_user_id;
END //
DELIMITER ;



/* ===============================
   2. Farm & Soil Sample Management Stored Procedures
   =============================== */

DELIMITER //
CREATE PROCEDURE sp_add_farm_location(
    IN in_region_name VARCHAR(100),
    IN in_street VARCHAR(50),
    IN in_city VARCHAR(50),
    IN in_state VARCHAR(50),
    IN in_country VARCHAR(50),
    IN in_zipcode VARCHAR(10),
    IN in_latitude DECIMAL(9,6),
    IN in_longitude DECIMAL(9,6),
    IN in_user_id INT
)
BEGIN
    INSERT INTO Farm_Location(region_name, street, city, state, country, zipcode, latitude, longitude, user_id)
    VALUES(in_region_name, in_street, in_city, in_state, in_country, in_zipcode, in_latitude, in_longitude, in_user_id);
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_request_soil_sample(
    IN in_farmer_id INT,
    IN in_lab_id INT,
    IN in_nitrogen DECIMAL(5,2),
    IN in_phosphorus DECIMAL(5,2),
    IN in_potassium DECIMAL(5,2),
    IN in_calcium DECIMAL(5,2),
    IN in_magnesium DECIMAL(5,2),
    IN in_sulfur DECIMAL(5,2),
    IN in_lime DECIMAL(5,2),
    IN in_carbon DECIMAL(5,2),
    IN in_moisture DECIMAL(5,2),
    IN in_farm_latitude DECIMAL(9,6),
    IN in_farm_longitude DECIMAL(9,6)
)
BEGIN
    INSERT INTO Soil_Sample(
        farmer_id, lab_id, nitrogen, phosphorus, potassium,
        calcium, magnesium, sulfur, lime, carbon, moisture,
        test_date, farm_latitude, farm_longitude, sample_status
    ) VALUES (
        in_farmer_id, in_lab_id, in_nitrogen, in_phosphorus, in_potassium,
        in_calcium, in_magnesium, in_sulfur, in_lime, in_carbon, in_moisture,
        NOW(), in_farm_latitude, in_farm_longitude, 'waiting'
    );
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_assign_sample_to_technician(
    IN in_soil_id INT,
    IN in_technician_id INT,
    IN in_lab_id INT
)
BEGIN
    INSERT INTO Sample_Testing (technician_id, lab_id, soil_id)
    VALUES (in_technician_id, in_lab_id, in_soil_id);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_submit_soil_test_results(
    IN in_soil_id INT,
    IN in_nitrogen DECIMAL(5,2),
    IN in_phosphorus DECIMAL(5,2),
    IN in_potassium DECIMAL(5,2),
    IN in_calcium DECIMAL(5,2),
    IN in_magnesium DECIMAL(5,2),
    IN in_sulfur DECIMAL(5,2),
    IN in_lime DECIMAL(5,2),
    IN in_carbon DECIMAL(5,2),
    IN in_moisture DECIMAL(5,2)
)
BEGIN
    UPDATE Soil_Sample
    SET 
        nitrogen = in_nitrogen,
        phosphorus = in_phosphorus,
        potassium = in_potassium,
        calcium = in_calcium,
        magnesium = in_magnesium,
        sulfur = in_sulfur,
        lime = in_lime,
        carbon = in_carbon,
        moisture = in_moisture,
        test_date = NOW(),
        sample_status = 'tested'
    WHERE soil_id = in_soil_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_get_soil_sample_results(
    IN in_soil_id INT
)
BEGIN
    SELECT ss.*, fc.class_name, fc.description
    FROM Soil_Sample ss
    LEFT JOIN Fertility_Class fc ON ss.fertility_class_id = fc.fertility_class_id
    WHERE ss.soil_id = in_soil_id;
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_classify_soil_sample(
    IN in_soil_id INT
)
BEGIN
    DECLARE calc_class INT;
    DECLARE n_val DECIMAL(5,2);
    DECLARE p_val DECIMAL(5,2);
    DECLARE k_val DECIMAL(5,2);
    DECLARE ca_val DECIMAL(5,2);
    DECLARE mg_val DECIMAL(5,2);
    DECLARE s_val DECIMAL(5,2);
    DECLARE lime_val DECIMAL(5,2);
    DECLARE c_val DECIMAL(5,2);
    DECLARE moisture_val DECIMAL(5,2);
    
    SELECT nitrogen, phosphorus, potassium, calcium, magnesium, sulfur, lime, carbon, moisture
    INTO n_val, p_val, k_val, ca_val, mg_val, s_val, lime_val, c_val, moisture_val
    FROM Soil_Sample 
    WHERE soil_id = in_soil_id;
    
    SET calc_class = fn_calculate_fertility_class(n_val, p_val, k_val, ca_val, mg_val, s_val, lime_val, c_val, moisture_val);
    
    UPDATE Soil_Sample 
    SET fertility_class_id = calc_class 
    WHERE soil_id = in_soil_id;
    
    SELECT calc_class AS Fertility_Class_ID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_get_crop_recommendations(
    IN in_fert_class_id INT
)
BEGIN
    SELECT * 
    FROM Crop 
    WHERE fertility_class_id = in_fert_class_id;
END //
DELIMITER ;




DELIMITER //
CREATE PROCEDURE sp_get_fertilizer_recommendations(
    IN in_crop_id INT
)
BEGIN
    SELECT f.*
    FROM Fertilizer f
    JOIN Crop_Fertilizer cf ON f.fertilizer_id = cf.fertilizer_id
    WHERE cf.crop_id = in_crop_id;
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_get_combined_recommendations(
    IN in_soil_id INT
)
BEGIN
    DECLARE fert_class INT;

    CALL sp_classify_soil_sample(in_soil_id);

    SELECT fertility_class_id INTO fert_class 
    FROM Soil_Sample 
    WHERE soil_id = in_soil_id;

    SELECT c.crop_id, c.crop_name
    FROM Crop c
    WHERE c.fertility_class_id = fert_class;

    SELECT c.crop_name, f.fertilizer_name, f.npk_ratio
    FROM Crop c
    JOIN Crop_Fertilizer cf ON c.crop_id = cf.crop_id
    JOIN Fertilizer f ON cf.fertilizer_id = f.fertilizer_id
    WHERE c.fertility_class_id = fert_class;
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_record_crop_growth(
    IN in_farmer_id INT,
    IN in_crop_id INT,
    IN in_start_date DATE,
    IN in_end_date DATE,
    IN in_status ENUM('Planted','Growing','Harvested'),
    IN in_yield_quantity DECIMAL(6,2)
)
BEGIN
    INSERT INTO Crop_Growth(farmer_id, crop_id, start_date, end_date, status, yield_quantity)
    VALUES(in_farmer_id, in_crop_id, in_start_date, in_end_date, in_status, in_yield_quantity);
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_update_crop_growth(
    IN in_growth_id INT,
    IN in_new_status ENUM('Planted','Growing','Harvested'),
    IN in_end_date DATE,
    IN in_yield_quantity DECIMAL(6,2)
)
BEGIN
    UPDATE Crop_Growth
    SET status = in_new_status,
        end_date = in_end_date,
        yield_quantity = in_yield_quantity
    WHERE growth_id = in_growth_id;
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_get_crop_growth(
    IN in_farmer_id INT
)
BEGIN
    SELECT cg.*, c.crop_name
    FROM Crop_Growth cg
    JOIN Crop c ON cg.crop_id = c.crop_id
    WHERE cg.farmer_id = in_farmer_id;
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_map_farm_crop(
    IN in_farm_latitude DECIMAL(9,6),
    IN in_farm_longitude DECIMAL(9,6),
    IN in_crop_id INT
)
BEGIN
    INSERT INTO Farm_Crop(farm_latitude, farm_longitude, crop_id)
    VALUES(in_farm_latitude, in_farm_longitude, in_crop_id);
END //
DELIMITER ;



/* ===============================
   3. Administrative / Reporting Stored Procedures
   =============================== */

DELIMITER //
CREATE PROCEDURE sp_get_regional_fertility_reports(
    IN in_region_name VARCHAR(100)
)
BEGIN
    SELECT fl.region_name,
           COUNT(ss.soil_id) AS total_samples,
           AVG(ss.nitrogen) AS avg_nitrogen,
           AVG(ss.phosphorus) AS avg_phosphorus,
           AVG(ss.potassium) AS avg_potassium,
           AVG(ss.moisture) AS avg_moisture
    FROM Soil_Sample ss
    JOIN Farm_Location fl 
         ON ss.farm_latitude = fl.latitude AND ss.farm_longitude = fl.longitude
    WHERE fl.region_name = in_region_name
    GROUP BY fl.region_name;
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_set_fertility_thresholds(
    IN in_fertility_class_id INT,
    IN in_min_nitrogen DECIMAL(5,2),
    IN in_max_nitrogen DECIMAL(5,2),
    IN in_min_phosphorus DECIMAL(5,2),
    IN in_max_phosphorus DECIMAL(5,2),
    IN in_min_potassium DECIMAL(5,2),
    IN in_max_potassium DECIMAL(5,2),
    IN in_min_calcium DECIMAL(5,2),
    IN in_max_calcium DECIMAL(5,2),
    IN in_min_carbon DECIMAL(5,2),
    IN in_max_carbon DECIMAL(5,2),
    IN in_min_lime DECIMAL(5,2),
    IN in_max_lime DECIMAL(5,2),
    IN in_min_sulfur DECIMAL(5,2),
    IN in_max_sulfur DECIMAL(5,2),
    IN in_min_moisture DECIMAL(5,2),
    IN in_max_moisture DECIMAL(5,2)
)
BEGIN
    UPDATE Fertility_Class
    SET 
        min_nitrogen = IFNULL(in_min_nitrogen, min_nitrogen),
        max_nitrogen = IFNULL(in_max_nitrogen, max_nitrogen),
        min_phosphorus = IFNULL(in_min_phosphorus, min_phosphorus),
        max_phosphorus = IFNULL(in_max_phosphorus, max_phosphorus),
        min_potassium = IFNULL(in_min_potassium, min_potassium),
        max_potassium = IFNULL(in_max_potassium, max_potassium),
        min_calcium = IFNULL(in_min_calcium, min_calcium),
        max_calcium = IFNULL(in_max_calcium, max_calcium),
        min_carbon = IFNULL(in_min_carbon, min_carbon),
        max_carbon = IFNULL(in_max_carbon, max_carbon),
        min_lime = IFNULL(in_min_lime, min_lime),
        max_lime = IFNULL(in_max_lime, max_lime),
        min_sulfur = IFNULL(in_min_sulfur, min_sulfur),
        max_sulfur = IFNULL(in_max_sulfur, max_sulfur),
        min_moisture = IFNULL(in_min_moisture, min_moisture),
        max_moisture = IFNULL(in_max_moisture, max_moisture)
    WHERE fertility_class_id = in_fertility_class_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_create_soil_test_lab(
    IN in_lab_name VARCHAR(100),
    IN in_address TEXT,
    IN in_contact VARCHAR(15),
    IN in_admin_id INT
)
BEGIN
    INSERT INTO Soil_Test_Lab(lab_name, address, contact, admin_id)
    VALUES(in_lab_name, in_address, in_contact, in_admin_id);
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_create_lab_technician(
    IN in_first_name VARCHAR(50),
    IN in_last_name VARCHAR(50),
    IN in_email VARCHAR(100),
    IN in_password VARCHAR(100),
    IN in_contact_number VARCHAR(15),
    IN in_certification TEXT,
    IN in_specialization VARCHAR(50),
    IN in_hire_date DATE,
    IN in_lab_id INT
)
BEGIN
    DECLARE last_id INT;
    
    INSERT INTO User(first_name, last_name, email, password, contact_number, role)
    VALUES(in_first_name, in_last_name, in_email, in_password, in_contact_number, 'Lab_Technician');
    
    SET last_id = LAST_INSERT_ID();
    
    INSERT INTO Lab_Technician(user_id, certification, specialization, hire_date, lab_id)
    VALUES(last_id, in_certification, in_specialization, in_hire_date, in_lab_id);
    
    SELECT last_id AS user_id;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_get_assigned_samples_for_technician;
DELIMITER //

CREATE PROCEDURE sp_get_assigned_samples_for_technician(
    IN in_technician_id INT
)
BEGIN
    SELECT ss.soil_id, ss.test_date, ss.nitrogen, ss.phosphorus, ss.potassium
    FROM Soil_Sample ss
    JOIN Sample_Testing st ON ss.soil_id = st.soil_id
    WHERE st.technician_id = in_technician_id
      AND ss.sample_status = 'waiting';
END //

DELIMITER ;




/* ===============================
   4. Triggers
   =============================== */

DELIMITER //
CREATE TRIGGER trg_auto_set_fertility_class
BEFORE INSERT ON Soil_Sample
FOR EACH ROW
BEGIN
    IF NEW.nitrogen IS NOT NULL 
       AND NEW.phosphorus IS NOT NULL 
       AND NEW.potassium IS NOT NULL THEN
       SET NEW.fertility_class_id = fn_calculate_fertility_class(
            NEW.nitrogen, 
            NEW.phosphorus, 
            NEW.potassium, 
            NEW.calcium, 
            NEW.magnesium, 
            NEW.sulfur, 
            NEW.lime, 
            NEW.carbon, 
            NEW.moisture
       );
    END IF;
END //
DELIMITER ;



DELIMITER //
CREATE TRIGGER trg_soil_sample_before_update
BEFORE UPDATE ON Soil_Sample
FOR EACH ROW
BEGIN
    IF (NEW.nitrogen <> OLD.nitrogen 
        OR NEW.phosphorus <> OLD.phosphorus 
        OR NEW.potassium <> OLD.potassium
        OR NEW.calcium <> OLD.calcium 
        OR NEW.magnesium <> OLD.magnesium 
        OR NEW.sulfur <> OLD.sulfur
        OR NEW.lime <> OLD.lime 
        OR NEW.carbon <> OLD.carbon 
        OR NEW.moisture <> OLD.moisture)
    THEN
         SET NEW.fertility_class_id = fn_calculate_fertility_class(
              NEW.nitrogen, 
              NEW.phosphorus, 
              NEW.potassium, 
              NEW.calcium, 
              NEW.magnesium, 
              NEW.sulfur, 
              NEW.lime, 
              NEW.carbon, 
              NEW.moisture
         );
    END IF;
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER trg_increment_crop_count
AFTER INSERT ON Crop_Growth
FOR EACH ROW
BEGIN
    UPDATE Farmer 
    SET no_of_crops_grown = no_of_crops_grown + 1 
    WHERE user_id = NEW.farmer_id;
END //
DELIMITER ;



DELIMITER //
CREATE TRIGGER trg_decrement_crop_count
AFTER DELETE ON Crop_Growth
FOR EACH ROW
BEGIN
    UPDATE Farmer 
    SET no_of_crops_grown = no_of_crops_grown - 1 
    WHERE user_id = OLD.farmer_id;
END //
DELIMITER ;


/* ===============================
   5. Functions
   =============================== */

DELIMITER //
CREATE FUNCTION fn_get_user_role(in_user_id INT)
RETURNS ENUM('Admin', 'Farmer', 'Lab_Technician')
DETERMINISTIC
BEGIN
    DECLARE u_role ENUM('Admin','Farmer','Lab_Technician');
    SELECT role INTO u_role FROM User WHERE user_id = in_user_id;
    RETURN u_role;
END //
DELIMITER ;

DELIMITER //
CREATE FUNCTION fn_calculate_yield_estimate(in_growth_id INT)
RETURNS DECIMAL(6,2)
DETERMINISTIC
BEGIN
    DECLARE yield_est DECIMAL(6,2);
    SELECT COALESCE(yield_quantity, 0) * 1.1 INTO yield_est
    FROM Crop_Growth
    WHERE growth_id = in_growth_id;
    RETURN yield_est;
END //
DELIMITER ;

DELIMITER //
CREATE FUNCTION fn_calculate_fertility_class(
    n_val DECIMAL(5,2), 
    p_val DECIMAL(5,2), 
    k_val DECIMAL(5,2), 
    ca_val DECIMAL(5,2), 
    mg_val DECIMAL(5,2), 
    s_val DECIMAL(5,2), 
    lime_val DECIMAL(5,2), 
    c_val DECIMAL(5,2), 
    moisture_val DECIMAL(5,2)
) RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE fert_class INT;
    IF n_val >= 70 AND p_val >= 45 AND k_val >= 50 THEN
        SET fert_class = 1;
    ELSEIF n_val >= 50 THEN
        SET fert_class = 2;
    ELSEIF n_val >= 30 THEN
        SET fert_class = 3;
    ELSE
        SET fert_class = 4;
    END IF;
    RETURN fert_class;
END //
DELIMITER ;


DELIMITER //
CREATE FUNCTION fn_years_experience(hire_date DATE)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN TIMESTAMPDIFF(YEAR, hire_date, CURDATE());
END //
DELIMITER ;

CREATE VIEW view_soil_sample_results_pending AS
SELECT ss.soil_id, ss.farmer_id, ss.lab_id, ss.test_date,
       ss.nitrogen, ss.phosphorus, ss.potassium,
       ss.fertility_class_id, ss.sample_status,
       fl.region_name, fl.city, fl.state
FROM Soil_Sample ss
JOIN Farm_Location fl 
  ON ss.farm_latitude = fl.latitude AND ss.farm_longitude = fl.longitude
WHERE ss.sample_status = 'waiting';


DELIMITER //
CREATE PROCEDURE sp_get_latest_classified_soil_sample(IN in_farmer_id INT)
BEGIN
    SELECT ss.soil_id, ss.fertility_class_id, fc.class_name, fc.description
    FROM Soil_Sample ss
    JOIN Fertility_Class fc ON ss.fertility_class_id = fc.fertility_class_id
    WHERE ss.farmer_id = in_farmer_id
      AND ss.fertility_class_id IS NOT NULL
    ORDER BY ss.test_date DESC
    LIMIT 1;
END //
DELIMITER ;

CALL sp_get_latest_classified_soil_sample(2);


DELIMITER //
CREATE PROCEDURE sp_get_all_labs()
BEGIN
    SELECT lab_id, lab_name FROM soil_test_lab;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_get_all_users()
BEGIN
    SELECT user_id, first_name, last_name, email, contact_number, role
    FROM User;
END //

DELIMITER ;

DELIMITER //

-- NEW Additions 

-- DROP PROCEDURE IF EXISTS sp_get_all_soil_labs;
DELIMITER //
CREATE PROCEDURE sp_get_all_soil_labs()
BEGIN
    SELECT lab_id, lab_name, address, contact
    FROM Soil_Test_Lab;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE sp_add_soil_lab(
    IN lab_name VARCHAR(255),
    IN location TEXT,
    IN contact VARCHAR(100)
)
BEGIN
    INSERT INTO Soil_Test_Lab (lab_name, address, contact)
    VALUES (lab_name, address, contact);
END //

DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_remove_soil_lab(
    IN labId INT
)
BEGIN
    DELETE FROM Soil_Test_Lab WHERE lab_id = labId;
END //

DELIMITER ;

-- Lab Technician Additions


DELIMITER //
CREATE PROCEDURE sp_mark_sample_as_tested(
    IN in_soil_id INT
)
BEGIN
    UPDATE Soil_Sample
    SET sample_status = 'tested'
    WHERE soil_id = in_soil_id;
END //
DELIMITER ;

-- DROP PROCEDURE IF EXISTS sp_get_lab_pending_samples;
DELIMITER //

CREATE PROCEDURE sp_get_lab_pending_samples(
    IN in_lab_id INT
)
BEGIN
    SELECT 
        soil_id,
        farmer_id,
        test_date,
        farm_latitude,
        farm_longitude
    FROM Soil_Sample
    WHERE lab_id = in_lab_id
      AND sample_status = 'waiting';
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE sp_request_soil_sample_tested(
    IN in_farmer_id INT,
    IN in_lab_id INT,
    IN in_nitrogen DECIMAL(5,2),
    IN in_phosphorus DECIMAL(5,2),
    IN in_potassium DECIMAL(5,2),
    IN in_calcium DECIMAL(5,2),
    IN in_magnesium DECIMAL(5,2),
    IN in_sulfur DECIMAL(5,2),
    IN in_lime DECIMAL(5,2),
    IN in_carbon DECIMAL(5,2),
    IN in_moisture DECIMAL(5,2),
    IN in_farm_latitude DECIMAL(9,6),
    IN in_farm_longitude DECIMAL(9,6)
)
BEGIN
    DECLARE fert_class_id INT;

    -- Calculate fertility class
    SET fert_class_id = fn_calculate_fertility_class(
        in_nitrogen, in_phosphorus, in_potassium, in_calcium,
        in_magnesium, in_sulfur, in_lime, in_carbon, in_moisture
    );

    -- Insert soil sample as tested with fertility class
    INSERT INTO Soil_Sample (
        farmer_id, lab_id, nitrogen, phosphorus, potassium,
        calcium, magnesium, sulfur, lime, carbon, moisture,
        test_date, farm_latitude, farm_longitude, sample_status, fertility_class_id
    ) VALUES (
        in_farmer_id, in_lab_id, in_nitrogen, in_phosphorus, in_potassium,
        in_calcium, in_magnesium, in_sulfur, in_lime, in_carbon, in_moisture,
        NOW(), in_farm_latitude, in_farm_longitude, 'tested', fert_class_id
    );

    -- Return the inserted row's ID and class
    SELECT LAST_INSERT_ID() AS soil_id, fert_class_id AS fertility_class_id;
END //

DELIMITER ;
