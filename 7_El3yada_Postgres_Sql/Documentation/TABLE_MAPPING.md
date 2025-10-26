# Database Table Mapping

## Application Table Names vs. Insertion Script Names

The application uses lowercase table names, while the insertion script uses mixed case. Here's the mapping:

| Application Table Name | Insertion Script Table Name | Description |
|------------------------|----------------------------|-------------|
| `patients` | `Patient_Information` | Patient demographic and contact information |
| `blood_test` | `Blood_Test` | Blood test results (stored as JSON) |
| `hormonal_test` | `Hormonal_Test` | Hormonal test results |
| `tumor_marks` | `Tumor_Marks` | Tumor marker test results |
| `mutation_analysis` | `Mutation_Analysis` | Genetic mutation analysis results |
| `clinical_notes` | N/A (not in script) | Clinical visit notes and observations |
| `projects` | N/A (not in script) | Project management (if used) |

## Important Notes

### Option 1: Modify Database Schema (Recommended)
If you're using the provided insertion script, you should modify it to use lowercase table names to match the application:

```python
# Change from:
CREATE TABLE Patient_Information (...)
# To:
CREATE TABLE patients (...)

# Change from:
CREATE TABLE Blood_Test (...)
# To:
CREATE TABLE blood_test (...)

# And so on...
```

### Option 2: Modify Application Code
Alternatively, you can modify `db_functions.py` to use the mixed-case table names:

```python
# In fetch_data() calls, change:
fetch_data("patients")
# To:
fetch_data("Patient_Information")
```

However, this is **NOT recommended** as it would require changes in multiple places.

## Column Mappings

### patients / Patient_Information
- `patient_id` (SERIAL PRIMARY KEY)
- `name` → `first_name` + `last_name` (combined in app)
- `gender`
- `age`
- `birth_date` → `dob`
- `primary_phone_number` → `contact_info` (stored differently)
- `secondary_phone_number`
- `address`
- `emergency_phone_number` → `emergency_contact` (stored differently)
- `emergency_name`
- `email`
- `marital_status`
- `notes`

### blood_test / Blood_Test
- `blood_test_id` (SERIAL PRIMARY KEY)
- `patient_id` (FOREIGN KEY)
- `test_date`
- `test_name` (not in insertion script)
- `test_results` (JSON) → Individual columns in script

### hormonal_test / Hormonal_Test
- `hormonal_test_id` (SERIAL PRIMARY KEY)
- `patient_id` (FOREIGN KEY)
- `test_date`
- `estrogen_levels` → `hormone_level` (stored differently)
- `progesterone_levels`
- `luteinizing_hormone`
- `follicle_stimulating_hormone`
- `testosterone_levels`
- `thyroid_tsh`
- `thyroid_t3`
- `thyroid_t4`
- `notes` → `interpretation_notes`

### tumor_marks / Tumor_Marks (Not in insertion script)
- `tumor_marks_id` (SERIAL PRIMARY KEY)
- `patient_id` (FOREIGN KEY)
- `test_date`
- `ca_15_3`
- `ca_27_29`
- `carcinoembryonic_antigen`
- `her2_neu`
- `muc1`

### mutation_analysis / Mutation_Analysis
- `mutation_id` (SERIAL PRIMARY KEY)
- `patient_id` (FOREIGN KEY)
- `test_date`
- `bcr_abl_fusion_gene`
- `bcr_abl_transcript_levels`
- `t315i_mutation`
- `f317l_mutation`
- `e255k_mutation`
- `g250e_mutation`
- `m351t_mutation`
- `v299l_mutation`

## Schema Differences to Address

### 1. Patient Name Storage
**Insertion Script**: Stores `first_name` and `last_name` separately
**Application**: Uses single `name` field

**Solution**: Either:
- Modify insertion script to use single `name` column
- Or modify application to use `first_name` and `last_name`

### 2. Contact Information
**Insertion Script**: Stores as plain text string
**Application**: Expects structured phone numbers

**Solution**: Keep as plain text (current implementation works)

### 3. Blood Test Results
**Insertion Script**: Stores individual parameters as columns
**Application**: Stores as JSON in `test_results` column

**Solution**: Application handles JSON conversion automatically

### 4. Missing Tables
The application uses `clinical_notes` and `projects` tables not present in the insertion script.

**Solution**: Create these tables manually:

```sql
CREATE TABLE clinical_notes (
    visit_id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(patient_id),
    date_of_visit DATE,
    disease_type VARCHAR(50),
    has_disease BOOLEAN,
    -- Add other clinical note fields as needed
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);
```

## Recommended Approach

1. **Use lowercase table names** throughout (modify insertion script)
2. **Align column names** between script and application
3. **Add missing tables** (clinical_notes, projects)
4. **Test thoroughly** after schema changes

## Quick Fix SQL Script

```sql
-- Rename tables to lowercase (if they exist with mixed case)
ALTER TABLE IF EXISTS Patient_Information RENAME TO patients;
ALTER TABLE IF EXISTS Blood_Test RENAME TO blood_test;
ALTER TABLE IF EXISTS Hormonal_Test RENAME TO hormonal_test;
ALTER TABLE IF EXISTS Mutation_Analysis RENAME TO mutation_analysis;

-- Add missing tables
CREATE TABLE IF NOT EXISTS clinical_notes (
    visit_id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(patient_id),
    date_of_visit DATE,
    disease_type VARCHAR(50),
    has_disease BOOLEAN,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

-- Add tumor_marks table (not in insertion script)
CREATE TABLE IF NOT EXISTS tumor_marks (
    tumor_marks_id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(patient_id),
    test_date DATE,
    ca_15_3 NUMERIC(10,2),
    ca_27_29 NUMERIC(10,2),
    carcinoembryonic_antigen NUMERIC(10,2),
    her2_neu VARCHAR(20),
    muc1 NUMERIC(10,2)
);
```
