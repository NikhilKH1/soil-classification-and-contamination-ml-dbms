# Soil Classification and Contamination Analysis using Machine Learning and DBMS

## 📌 Overview
This project implements a **machine-learning–based soil classification and contamination analysis system** backed by a **relational database (DBMS)**. The design and methodology are inspired by the following research paper:

**Soil Classification and Contamination Prediction Using Machine Learning Techniques**  
Springer – Advances in Intelligent Systems and Computing  
https://link.springer.com/chapter/10.1007/978-981-16-3342-3_3

The system integrates **ML models** with **database-driven storage, validation, and querying** to enable efficient, scalable, and automated soil analysis for environmental and agricultural use cases.

---

## 🎯 Problem Statement
Conventional soil testing methods are manual, slow, and difficult to scale. This project aims to:
- Classify soil types using physicochemical properties
- Identify contamination patterns using machine learning
- Store and manage soil data efficiently using a DBMS
- Reduce manual intervention through automation

---

## 🧠 Solution Approach
The project combines:
- **Machine Learning** for soil classification and contamination prediction
- **Database Management Systems (DBMS)** for structured storage and querying
- **Stored Procedures** for efficient backend data processing

### Workflow
1. Soil data ingestion
2. Data preprocessing and normalization
3. ML-based prediction
4. Database storage using relational schema
5. Query-driven analysis via stored procedures

---

## 📊 Dataset Description
The dataset consists of soil physicochemical properties commonly used in agricultural and environmental studies.

### Sample Features
- pH value
- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Moisture content
- Organic carbon

### Target
- Soil classification / contamination category

Data is validated and normalized before being passed into the ML pipeline.

---

## 🏗️ System Architecture
User / Input Data
→
Python Application
→
ML Model (Prediction & Classification)
→
MySQL Database
→
Stored Procedures & Queries


---

## 🤖 Machine Learning Component
- Supervised learning models for soil classification
- Feature engineering based on soil chemistry
- Model evaluation using accuracy and error-based metrics
- ML workflow inspired by methodologies described in the referenced Springer paper

---

## 🗄️ Database Design (DBMS)
- Relational schema for soil samples and predictions
- Indexed columns for efficient querying
- Stored procedures used for:
  - Data insertion
  - Validation
  - Aggregated analysis
  - Result retrieval

---

## 📁 Project Structure
.
- main.py # Entry point for ML + DBMS workflow

- connection.py # Database connection configuration

─ stored_procedures.py # SQL stored procedures and queries

─ README.md # Project documentation


---

## 🛠️ Tech Stack
- **Programming Language:** Python
- **Machine Learning:** Scikit-learn
- **Database:** MySQL
- **Backend Logic:** SQL Stored Procedures
- **Libraries:** NumPy, Pandas

---

## 🚀 How to Run the Project

### 1️⃣ Clone the repository
```bash
git clone https://github.com/NikhilKH1/soil-classification-and-contamination-ml-dbms.git
cd soil-classification-and-contamination-ml-dbms
```
2️⃣ Configure Database
Update database credentials in:
```bash
connection.py
```
Ensure MySQL is running and required tables/stored procedures are created.

3️⃣ Run the application
```bash
python main.py
```
📈 Results and Outcomes
Accurate soil classification using ML models

Efficient contamination detection

Structured and queryable soil data storage

Reduced manual analysis through automation

🔮 Future Enhancements
Introduce deep learning models for higher accuracy

Integrate real-time IoT soil sensor data

Build a web-based dashboard for visualization

Deploy using cloud-based ML and DB services

📚 Reference
Springer Research Paper:
```bash
https://link.springer.com/chapter/10.1007/978-981-16-3342-3_3
```
