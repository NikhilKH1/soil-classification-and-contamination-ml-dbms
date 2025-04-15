USE crop_fertlizer_db;

-- Insert Users with Roles
INSERT INTO User (first_name, last_name, email, password, contact_number, role) VALUES
('Ramesh', 'Patel', 'ramesh.patel@example.com', 'pass123', '9876543210', 'Admin'),
('Sita', 'Sharma', 'sita.sharma@example.com', 'sita456', '9123456780', 'Farmer'),
('Aman', 'Verma', 'aman.verma@example.com', 'aman789', '9988776655', 'Lab_Technician'),
('Sunita', 'Rao', 'sunita.rao@example.com', 'sunita101', '9090909090', 'Farmer'),
('Vijay', 'Kumar', 'vijay.kumar@example.com', 'vijay202', '9000001111', 'Admin'),
('Meena', 'Joshi', 'meena.joshi@example.com', 'meena303', '9123487610', 'Farmer'),
('Anil', 'Mehta', 'anil.mehta@example.com', 'anil404', '8899776655', 'Lab_Technician'),
('Kavita', 'Shah', 'kavita.shah@example.com', 'kavita505', '8989898989', 'Farmer'),
('Deepak', 'Singh', 'deepak.singh@example.com', 'deepak606', '9111112222', 'Lab_Technician'),
('Rekha', 'Gupta', 'rekha.gupta@example.com', 'rekha707', '9223344556', 'Farmer');

-- Admins
INSERT INTO Admin (user_id, hire_date) VALUES
(1, '2020-01-15'),
(5, '2021-06-10');

-- Soil Test Labs
INSERT INTO Soil_Test_Lab (lab_name, address, contact, admin_id) VALUES
('AgriSoil Labs', '123 Green St, Jaipur', '9823456780', 1),
('SoilCheck Center', '456 Farm Rd, Pune', '9876543212', 5);

-- Lab Technicians
INSERT INTO Lab_Technician (user_id, certification, specialization, hire_date, lab_id) VALUES
(3, 'Certified Soil Analyst', 'pH & Nutrients', '2022-02-01', 1),
(7, 'Agritech Certified', 'Minerals', '2023-01-10', 1),
(9, 'Certified Soil Analyst' , 'pH & Nutrients, Minerals', '2024-02-09', 2);

-- Farmers
INSERT INTO Farmer (user_id, farm_size, no_of_crops_grown) VALUES
(2, 3.5, 2), (4, 1.8, 1), (6, 5.0, 3), (8, 2.2, 2), (10, 4.5, 3);

-- Farm Locations
INSERT INTO Farm_Location (region_name, street, city, state, country, zipcode, latitude, longitude, user_id) VALUES
('North Region', '78 A St', 'Jaipur', 'Rajasthan', 'India', '302001', 26.9124, 75.7873, 2),
('South Zone', '90 Green Rd', 'Pune', 'Maharashtra', 'India', '411001', 18.5204, 73.8567, 4);

-- Fertility Classes
INSERT INTO Fertility_Class (
    class_name, description,
    min_nitrogen, max_nitrogen, min_phosphorus, max_phosphorus,
    min_potassium, max_potassium, min_calcium, max_calcium,
    min_carbon, max_carbon, min_lime, max_lime,
    min_sulfur, max_sulfur, min_moisture, max_moisture
) VALUES
('Very High', 'Ideal for most crops', 70, 100, 45, 60, 50, 80, 30, 50, 3, 5, 1.5, 3, 8, 12, 25, 35),
('High', 'Fertile with slight supplementation', 50, 69, 30, 44, 40, 49, 20, 29, 2, 2.9, 1, 1.4, 5, 7.9, 15, 24.9),
('Moderate', 'Can support crops with supplements', 30, 49, 20, 29, 25, 39, 15, 19, 1, 1.9, 0.5, 0.9, 3, 4.9, 10, 14.9),
('Low', 'Needs heavy supplementation', 10, 29, 10, 19, 10, 24, 10, 14, 0.5, 0.9, 0.2, 0.4, 1, 2.9, 5, 9.9);

-- Crops
INSERT INTO Crop (crop_name, fertility_class_id) VALUES
('Wheat', 1), ('Rice', 1), ('Corn', 2), ('Soybean', 3), ('Tomato', 2);

-- Fertilizers
INSERT INTO Fertilizer (fertilizer_name, npk_ratio, fertility_class_id) VALUES
('Urea', '46-0-0', 1),
('DAP', '18-46-0', 2),
('Compost', '2-1-1', 4);

-- Soil Samples
INSERT INTO Soil_Sample (
    farmer_id, lab_id, nitrogen, phosphorus, potassium,
    calcium, magnesium, sulfur, lime, carbon, moisture,
    test_date, farm_latitude, farm_longitude, fertility_class_id
) VALUES
(2, 1, 75, 50, 65, 40, 20, 10, 2, 4, 30, NOW(), 26.9124, 75.7873, 1),
(4, 2, 35, 25, 30, 20, 12, 4, 0.9, 1.5, 12, NOW(), 18.5204, 73.8567, 3);

-- Crop Growth
INSERT INTO Crop_Growth (farmer_id, crop_id, start_date, end_date, status, yield_quantity) VALUES
(2, 1, '2023-01-10', '2023-05-15', 'Harvested', 2.3),
(4, 3, '2023-02-05', NULL, 'Growing', NULL);

-- Farm-Crop Mapping
INSERT INTO Farm_Crop (farm_latitude, farm_longitude, crop_id) VALUES
(26.9124, 75.7873, 1),
(18.5204, 73.8567, 3);

INSERT INTO Crop_Fertilizer (crop_id, fertilizer_id) VALUES
(1, 1), -- Wheat → Urea
(1, 2), -- Wheat → DAP
(2, 1), -- Rice → Urea
(3, 2), -- Corn → DAP
(3, 3), -- Corn → Compost
(4, 3), -- Soybean → Compost
(5, 2); -- Tomato → DAP

INSERT INTO Sample_Testing (technician_id, lab_id, soil_id)
VALUES
(3, 1, 1),  -- Technician 3 tested Soil Sample 1 at Lab 1
(7, 1, 2);  -- Technician 7 tested Soil Sample 2 at Lab 1


