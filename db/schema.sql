CREATE DATABASE IF NOT EXISTS crop_fertilizer_db;
USE crop_fertilizer_db;

CREATE TABLE User (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    contact_number VARCHAR(15),
    role ENUM('Admin', 'Farmer', 'Lab_Technician') NOT NULL
);

-- 2. Admin Table
CREATE TABLE Admin (
    user_id INT PRIMARY KEY,
    hire_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 3. Soil Test Lab Table
CREATE TABLE Soil_Test_Lab (
    lab_id INT PRIMARY KEY AUTO_INCREMENT,
    lab_name VARCHAR(100) NOT NULL,
    address TEXT,
    contact VARCHAR(15),
    admin_id INT,
    FOREIGN KEY (admin_id) REFERENCES Admin(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- 4. Lab Technician Table
CREATE TABLE Lab_Technician (
    user_id INT PRIMARY KEY,
    certification TEXT,
    specialization VARCHAR(50),
    hire_date DATE NOT NULL,
    lab_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (lab_id) REFERENCES Soil_Test_Lab(lab_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 5. Farmer Table
CREATE TABLE Farmer (
    user_id INT PRIMARY KEY,
    farm_size DECIMAL(6,2),
    no_of_crops_grown INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 6. Farm Location Table
CREATE TABLE Farm_Location (
    region_name VARCHAR(100),
    street VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    zipcode VARCHAR(10),
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (latitude, longitude),
    FOREIGN KEY (user_id) REFERENCES Farmer(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 7. Fertility Class Table
CREATE TABLE Fertility_Class (
    fertility_class_id INT PRIMARY KEY AUTO_INCREMENT,
    class_name ENUM('Low', 'Moderate', 'High', 'Very High') NOT NULL,
    description TEXT,
    min_nitrogen DECIMAL(5,2),
    max_nitrogen DECIMAL(5,2),
    min_phosphorus DECIMAL(5,2),
    max_phosphorus DECIMAL(5,2),
    min_potassium DECIMAL(5,2),
    max_potassium DECIMAL(5,2),
    min_calcium DECIMAL(5,2),
    max_calcium DECIMAL(5,2),
    min_carbon DECIMAL(5,2),
    max_carbon DECIMAL(5,2),
    min_lime DECIMAL(5,2),
    max_lime DECIMAL(5,2),
    min_sulfur DECIMAL(5,2),
    max_sulfur DECIMAL(5,2),
    min_moisture DECIMAL(5,2),
    max_moisture DECIMAL(5,2)
);

-- 8. Crop Table (each crop belongs to a fertility class)
CREATE TABLE Crop (
    crop_id INT PRIMARY KEY AUTO_INCREMENT,
    crop_name VARCHAR(100) NOT NULL UNIQUE,
    fertility_class_id INT NOT NULL,
    FOREIGN KEY (fertility_class_id) REFERENCES Fertility_Class(fertility_class_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 9. Fertilizer Table (each fertilizer belongs to a fertility class)
CREATE TABLE Fertilizer (
    fertilizer_id INT PRIMARY KEY AUTO_INCREMENT,
    fertilizer_name VARCHAR(100) NOT NULL UNIQUE,
    npk_ratio VARCHAR(20),
    fertility_class_id INT NOT NULL,
    FOREIGN KEY (fertility_class_id) REFERENCES Fertility_Class(fertility_class_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 10. Soil Sample
CREATE TABLE Soil_Sample (
    soil_id INT PRIMARY KEY AUTO_INCREMENT,
    farmer_id INT NOT NULL,
    lab_id INT NOT NULL,
    nitrogen DECIMAL(5,2),
    phosphorus DECIMAL(5,2),
    potassium DECIMAL(5,2),
    calcium DECIMAL(5,2),
    magnesium DECIMAL(5,2),
    sulfur DECIMAL(5,2),
    lime DECIMAL(5,2),
    carbon DECIMAL(5,2),
    moisture DECIMAL(5,2),
    test_date TIMESTAMP NOT NULL,
    farm_latitude DECIMAL(9,6) NOT NULL,
    farm_longitude DECIMAL(9,6) NOT NULL,
    fertility_class_id INT,
    sample_status ENUM('waiting', 'tested') DEFAULT 'waiting',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (farmer_id) REFERENCES Farmer(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (lab_id) REFERENCES Soil_Test_Lab(lab_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (farm_latitude, farm_longitude) REFERENCES Farm_Location(latitude, longitude)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (fertility_class_id) REFERENCES Fertility_Class(fertility_class_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);


-- 11. Crop Growth Table
CREATE TABLE Crop_Growth (
    growth_id INT PRIMARY KEY AUTO_INCREMENT,
    farmer_id INT NOT NULL,
    crop_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    status ENUM('Planted', 'Growing', 'Harvested') DEFAULT 'Planted',
    yield_quantity DECIMAL(6,2),
    FOREIGN KEY (farmer_id) REFERENCES Farmer(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (crop_id) REFERENCES Crop(crop_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 12. Farm-Crop Mapping Table
CREATE TABLE Farm_Crop (
    farm_latitude DECIMAL(9,6),
    farm_longitude DECIMAL(9,6),
    crop_id INT,
    PRIMARY KEY (farm_latitude, farm_longitude, crop_id),
    FOREIGN KEY (farm_latitude, farm_longitude) REFERENCES Farm_Location(latitude, longitude)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (crop_id) REFERENCES Crop(crop_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Crop_Fertilizer (
    crop_id INT,
    fertilizer_id INT,
    PRIMARY KEY (crop_id, fertilizer_id),
    FOREIGN KEY (crop_id) REFERENCES Crop(crop_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (fertilizer_id) REFERENCES Fertilizer(fertilizer_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Sample_Testing (
    technician_id INT NOT NULL,
    lab_id INT NOT NULL,
    soil_id INT NOT NULL,
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (technician_id, lab_id, soil_id),

    FOREIGN KEY (technician_id) REFERENCES Lab_Technician(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,

    FOREIGN KEY (lab_id) REFERENCES Soil_Test_Lab(lab_id)
        ON DELETE CASCADE ON UPDATE CASCADE,

    FOREIGN KEY (soil_id) REFERENCES Soil_Sample(soil_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
