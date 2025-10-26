# New Database Setup Guide

## Overview

This guide explains how to set up and populate your new PostgreSQL database with the updated schema.

## Database Schema Changes

### Key Changes from Old Schema:

1. **Patient ID Type**: Changed from `INTEGER` to `TEXT` (format: P001, P002, etc.)
2. **Test ID Types**: Changed to `SERIAL` or `BIGSERIAL` for auto-increment
3. **JSONB Support**: Blood test results stored as JSONB for flexibility
4. **Additional Tables**: Added support for more medical data types

## Step-by-Step Setup

### Step 1: Create the Database

Run the database creation script:

```bash
bash Documentation/Create_DB.sh
```

This will:
- Create a new PostgreSQL database
- Create a new user with appropriate permissions
- Create all required tables with proper schema
- Set up indexes for performance

**Tables Created:**
- `patients` - Main patient information (TEXT patient_id)
- `patients_infor` - Alternative patient structure (UUID)
- `patient_summary` - Disease summaries
- `medical_history` - Patient medical history
- `medication_profile` - Medication tracking
- `documentation` - Document management
- `diagnostic_reports` - Test report summaries
- `biopsy` - Biopsy results
- `genetic_test` - Genetic testing results
- `radiology` - Imaging results
- `blood_test` - Blood test results (JSONB)
- `hormonal_test` - Hormonal test results
- `mutation_analysis` - CML mutation analysis
- `tumor_marks` - Breast cancer tumor markers
- `clinical_notes` - Clinical visit notes

### Step 2: Update Database Credentials

Edit `.streamlit/secrets.toml` with your database credentials:

```toml
dbname = 'your_database_name'
dbusername = 'your_username'
password = "your_password"
host = "your_host_ip"
port = '5432'
```

### Step 3: Insert Sample Data

Run the data insertion script:

```bash
python insert_sample_data.py
```

**What it does:**
- Prompts if you want to truncate existing data
- Inserts sample data into all tables:
  - ✅ 50 patients
  - ✅ 100 blood tests
  - ✅ 80 hormonal tests
  - ✅ 60 tumor marker tests
  - ✅ 40 mutation analyses
  - ✅ 150 clinical notes

**Sample Data Details:**

| Table | Records | Description |
|-------|---------|-------------|
| patients | 50 | Patient demographics with TEXT IDs (P001-P050) |
| blood_test | 100 | Blood test results with JSONB data |
| hormonal_test | 80 | Hormone level measurements |
| tumor_marks | 60 | Breast cancer tumor markers |
| mutation_analysis | 40 | CML genetic mutations |
| clinical_notes | 150 | Clinical visit records |

### Step 4: Run the Application

```bash
streamlit run 1_⛪Home.py
```

## Application Updates

### Changes Made to Application Code:

1. **db_functions.py**
   - ✅ Already uses parameterized queries (works with TEXT patient_id)
   - ✅ Connection pooling maintained
   - ✅ All CRUD operations compatible

2. **Lab Profile Page**
   - ✅ Updated selectboxes to handle TEXT patient_ids
   - ✅ Added debug panel to show table status
   - ✅ Added safety checks for empty dataframes

3. **Clinical Notes Page**
   - ✅ Updated patient_id handling
   - ✅ Added validation checks

4. **Dashboard Page**
   - ✅ Added empty dataframe checks
   - ✅ Safe column access

5. **Patients Page**
   - ✅ Updated header styling
   - ✅ Fixed grid configurations

## Data Insertion Script Features

### Truncate Option

When running `insert_sample_data.py`, you'll be asked:

```
⚠️  Do you want to TRUNCATE all tables before inserting? (yes/no):
```

- **yes**: Clears all existing data before inserting new data
- **no**: Appends new data to existing data (may cause duplicates)

### Customizing Data Volume

Edit `insert_sample_data.py` to change the number of records:

```python
# At the top of the file
NUM_PATIENTS = 50              # Change this
NUM_BLOOD_TESTS = 100          # Change this
NUM_HORMONAL_TESTS = 80        # Change this
NUM_TUMOR_MARKS = 60           # Change this
NUM_MUTATION_ANALYSIS = 40     # Change this
NUM_CLINICAL_NOTES = 150       # Change this
```

## Patient ID Format

### New Format: TEXT

Patient IDs are now TEXT strings in format: **P001, P002, P003**, etc.

**Benefits:**
- More readable and user-friendly
- Easier to reference in conversations
- Can include prefixes for different patient types
- No integer overflow concerns

**Example Patient IDs:**
- P001 - First patient
- P025 - Twenty-fifth patient
- P050 - Fiftieth patient

## Blood Test Results (JSONB)

Blood test results are stored as JSONB for flexibility:

```json
{
  "WBC": 7.5,
  "RBC": 4.8,
  "Hemoglobin": 14.2,
  "Platelets": 250,
  "Glucose": 95
}
```

**Advantages:**
- Flexible schema
- Can add new test parameters without schema changes
- Easy to query specific values
- Compact storage

## Verification Steps

### 1. Check Database Connection

```bash
streamlit run test_db_connection.py
```

This shows:
- All tables in your database
- Column names for each table
- Row counts

### 2. Check Application Debug Panel

1. Open **Lab Profile** page
2. Click **"🔍 Debug: Database Connection Info"**
3. Verify:
   - ✅ All tables show data
   - ✅ Correct column names
   - ✅ Expected row counts

### 3. Test Each Page

- **Home**: Should display patient list
- **Patients**: Should show all patients with P001-P050 IDs
- **Lab Profile**: Should show test results
- **Clinical Notes**: Should show visit records
- **Dashboard**: Should show statistics and charts

## Common Issues

### Issue 1: "No data available to display"

**Cause**: Tables are empty

**Solution**: Run `insert_sample_data.py`

### Issue 2: Connection errors

**Cause**: Wrong credentials in secrets.toml

**Solution**: Verify database credentials match those used in Create_DB.sh

### Issue 3: Column name errors

**Cause**: Schema mismatch

**Solution**: Drop and recreate database using Create_DB.sh

## SQL Queries for Verification

```sql
-- Check patient count
SELECT COUNT(*) FROM patients;

-- View sample patients
SELECT patient_id, name, gender, age FROM patients LIMIT 10;

-- Check blood tests
SELECT COUNT(*) FROM blood_test;

-- View sample blood test with JSONB
SELECT patient_id, test_date, test_name, test_results 
FROM blood_test LIMIT 5;

-- Check clinical notes
SELECT COUNT(*) FROM clinical_notes;

-- View recent clinical notes
SELECT patient_id, date_of_visit, disease_type, has_disease 
FROM clinical_notes 
ORDER BY date_of_visit DESC 
LIMIT 10;
```

## Backup and Restore

### Backup Database

```bash
pg_dump -U your_username -d your_database > backup.sql
```

### Restore Database

```bash
psql -U your_username -d your_database < backup.sql
```

## Next Steps

1. ✅ Create database using Create_DB.sh
2. ✅ Update secrets.toml with credentials
3. ✅ Run insert_sample_data.py to populate data
4. ✅ Run application: `streamlit run 1_⛪Home.py`
5. ✅ Verify all pages work correctly
6. ✅ Add your own real patient data

## Support Files Created

- `insert_sample_data.py` - Data insertion script
- `test_db_connection.py` - Database connection tester
- `TROUBLESHOOTING.md` - Detailed troubleshooting guide
- `TABLE_MAPPING.md` - Schema mapping reference
- `NEW_DATABASE_SETUP.md` - This file

## Summary

Your application is now fully configured to work with the new database schema:
- ✅ TEXT patient IDs (P001, P002, etc.)
- ✅ JSONB blood test results
- ✅ All tables properly indexed
- ✅ Sample data ready to insert
- ✅ Application code updated
- ✅ Debug tools available

Everything is ready to go! 🎉
