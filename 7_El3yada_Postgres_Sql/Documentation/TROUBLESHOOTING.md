# Troubleshooting Guide

## Issue: "No data available to display" despite having data in database

### Diagnostic Steps

#### Step 1: Run the Database Connection Test

```bash
streamlit run test_db_connection.py
```

This will show you:
- ✅ If connection is successful
- 📋 All tables in your database
- 📊 Column names for each table
- 🔢 Row counts

#### Step 2: Check Debug Panel in Lab Profile Page

1. Go to **Lab Profile** page
2. Click on **"🔍 Debug: Database Connection Info"** expander at the top
3. This will show:
   - Which tables have data
   - What columns exist in each table
   - How many rows are in each table

### Common Issues and Solutions

#### Issue 1: Table Names Don't Match

**Problem:** Your database uses different table names than the application expects.

**Example:**
- Database has: `Patient_Information`
- App expects: `patients`

**Solution:** Rename your database tables to lowercase:

```sql
-- Run these SQL commands in your PostgreSQL database
ALTER TABLE Patient_Information RENAME TO patients;
ALTER TABLE Blood_Test RENAME TO blood_test;
ALTER TABLE Hormonal_Test RENAME TO hormonal_test;
ALTER TABLE Mutation_Analysis RENAME TO mutation_analysis;
-- Add tumor_marks table if it doesn't exist
```

#### Issue 2: Column Names Don't Match

**Problem:** Your database columns have different names.

**Example:**
- Database has: `first_name`, `last_name`
- App expects: `name`

**Solutions:**

**Option A:** Modify database schema (Recommended)
```sql
-- Combine first_name and last_name into name
ALTER TABLE patients ADD COLUMN name VARCHAR(200);
UPDATE patients SET name = first_name || ' ' || last_name;
ALTER TABLE patients DROP COLUMN first_name;
ALTER TABLE patients DROP COLUMN last_name;
```

**Option B:** Modify application code
Edit `db_functions.py` to map column names after fetching data.

#### Issue 3: Missing Tables

**Problem:** Some tables don't exist in your database.

**Tables required by the application:**
- `patients`
- `blood_test`
- `hormonal_test`
- `tumor_marks` (not in your insertion script)
- `mutation_analysis`
- `clinical_notes` (not in your insertion script)

**Solution:** Create missing tables:

```sql
-- Create tumor_marks table
CREATE TABLE tumor_marks (
    tumor_marks_id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(patient_id),
    test_date DATE,
    ca_15_3 NUMERIC(10,2),
    ca_27_29 NUMERIC(10,2),
    carcinoembryonic_antigen NUMERIC(10,2),
    her2_neu VARCHAR(20),
    muc1 NUMERIC(10,2)
);

-- Create clinical_notes table
CREATE TABLE clinical_notes (
    visit_id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(patient_id),
    date_of_visit DATE,
    disease_type VARCHAR(50),
    has_disease BOOLEAN,
    notes TEXT
);
```

#### Issue 4: Connection Pool Issues

**Problem:** Connection pool not created or exhausted.

**Symptoms:**
- "Connection pool is None" errors
- Slow performance
- Connection timeouts

**Solution:** Check `db_functions.py` connection pool initialization:

```python
# Should see this message in terminal when app starts:
# ✅ Connection pool created successfully

# If you see:
# ❌ Error creating connection pool: ...
# Then check your database credentials in secrets.toml
```

### Quick Fix Checklist

- [ ] Database is running and accessible
- [ ] Credentials in `.streamlit/secrets.toml` are correct
- [ ] Table names are lowercase (`patients`, not `Patient_Information`)
- [ ] Required tables exist (patients, blood_test, hormonal_test, etc.)
- [ ] Tables have data (run `SELECT COUNT(*) FROM patients;`)
- [ ] Column `patient_id` exists in all tables
- [ ] Connection pool initialized successfully

### Verify Your Setup

Run these SQL queries to verify your database:

```sql
-- Check if tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Check patients table
SELECT COUNT(*) FROM patients;
SELECT * FROM patients LIMIT 1;

-- Check blood_test table
SELECT COUNT(*) FROM blood_test;
SELECT * FROM blood_test LIMIT 1;

-- Check column names
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'patients';
```

### Expected Database Schema

The application expects these exact table and column names:

**patients table:**
- patient_id (PRIMARY KEY)
- name
- gender
- age
- birth_date
- primary_phone_number
- secondary_phone_number
- address
- emergency_phone_number
- emergency_name
- email
- marital_status
- notes

**blood_test table:**
- blood_test_id (PRIMARY KEY)
- patient_id (FOREIGN KEY)
- test_date
- test_name
- test_results (JSON or TEXT)

**hormonal_test table:**
- hormonal_test_id (PRIMARY KEY)
- patient_id (FOREIGN KEY)
- test_date
- estrogen_levels
- progesterone_levels
- luteinizing_hormone
- follicle_stimulating_hormone
- testosterone_levels
- thyroid_tsh
- thyroid_t3
- thyroid_t4
- notes

**tumor_marks table:**
- tumor_marks_id (PRIMARY KEY)
- patient_id (FOREIGN KEY)
- test_date
- ca_15_3
- ca_27_29
- carcinoembryonic_antigen
- her2_neu
- muc1

**mutation_analysis table:**
- mutation_id (PRIMARY KEY)
- patient_id (FOREIGN KEY)
- test_date
- bcr_abl_fusion_gene
- bcr_abl_transcript_levels
- t315i_mutation
- f317l_mutation
- e255k_mutation
- g250e_mutation
- m351t_mutation
- v299l_mutation

### Still Having Issues?

1. **Check the Debug Panel** in Lab Profile page - it will tell you exactly what's wrong
2. **Run the test script**: `streamlit run test_db_connection.py`
3. **Check terminal output** for connection pool messages
4. **Verify table names** match exactly (case-sensitive in some systems)
5. **Check PostgreSQL logs** for any errors

### Contact Information

If you continue to have issues, provide:
1. Screenshot of Debug Panel from Lab Profile page
2. Output from `test_db_connection.py`
3. Result of `SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';`
