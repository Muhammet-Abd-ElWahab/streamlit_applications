#!/bin/bash
# --------------------------------------------
# Script to create PostgreSQL Database matching Supabase schema
# --------------------------------------------

echo "==============================================="
echo "   PostgreSQL Database Setup - Supabase Schema"
echo "==============================================="

# Prompt user for PostgreSQL superuser (usually 'postgres')
read -p "Enter PostgreSQL superuser (default: postgres): " SUPERUSER
SUPERUSER=${SUPERUSER:-postgres}

# Prompt for new database name, username, and password
read -p "Enter the name for the new database: " DBNAME
read -p "Enter the username to create: " USERNAME
read -s -p "Enter the password for user $USERNAME: " PASSWORD
echo ""
read -p "Enter the port (default 5432): " PORT
PORT=${PORT:-5432}

# Confirm details
echo ""
echo "Creating database '$DBNAME' and user '$USERNAME'..."
echo ""

# Create user, database, and grant privileges
sudo -u $SUPERUSER psql -p $PORT <<EOF
CREATE USER $USERNAME WITH PASSWORD '$PASSWORD';
CREATE DATABASE $DBNAME OWNER $USERNAME;
GRANT ALL PRIVILEGES ON DATABASE $DBNAME TO $USERNAME;
EOF

echo "Database and user created successfully."

# Create tables inside the new database
sudo -u $SUPERUSER psql -d $DBNAME -p $PORT <<'SQL'

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Drop tables if they exist (in correct order respecting foreign keys)
DROP TABLE IF EXISTS clinical_notes CASCADE;
DROP TABLE IF EXISTS tumor_marks CASCADE;
DROP TABLE IF EXISTS mutation_analysis CASCADE;
DROP TABLE IF EXISTS hormonal_test CASCADE;
DROP TABLE IF EXISTS blood_test CASCADE;
DROP TABLE IF EXISTS radiology CASCADE;
DROP TABLE IF EXISTS genetic_test CASCADE;
DROP TABLE IF EXISTS biopsy CASCADE;
DROP TABLE IF EXISTS diagnostic_reports CASCADE;
DROP TABLE IF EXISTS documentation CASCADE;
DROP TABLE IF EXISTS medication_profile CASCADE;
DROP TABLE IF EXISTS medical_history CASCADE;
DROP TABLE IF EXISTS patient_summary CASCADE;
DROP TABLE IF EXISTS patients_infor CASCADE;
DROP TABLE IF EXISTS patients CASCADE;

-- ============================================
-- Primary Patient Table
-- ============================================
CREATE TABLE patients (
    patient_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT NOT NULL,
    birth_date DATE,
    age INTEGER,
    primary_phone_number TEXT UNIQUE,
    secondary_phone_number TEXT,
    emergency_name TEXT,
    emergency_phone_number TEXT,
    email TEXT,
    address TEXT,
    marital_status TEXT,
    notes TEXT
);

-- ============================================
-- Patient Information Table (Alternative structure)
-- ============================================
CREATE TABLE patients_infor (
    patient_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    gender VARCHAR(10),
    dob DATE,
    contact_info JSONB,
    address TEXT,
    emergency_contact JSONB,
    insurance_details TEXT
);

-- ============================================
-- Patient Summary
-- ============================================
CREATE TABLE patient_summary (
    summary_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID,
    disease_type VARCHAR(20) CHECK (disease_type IN ('CML', 'Breast Cancer')),
    diagnosis_date DATE,
    current_status VARCHAR(50),
    summary_notes TEXT
);

-- ============================================
-- Medical History
-- ============================================
CREATE TABLE medical_history (
    history_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID,
    disease_type VARCHAR(20) CHECK (disease_type IN ('CML', 'Breast Cancer')),
    previous_conditions TEXT,
    family_history TEXT,
    allergies TEXT,
    other_relevant_info TEXT
);

-- ============================================
-- Medication Profile
-- ============================================
CREATE TABLE medication_profile (
    medication_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID,
    medication_name VARCHAR(100),
    dosage VARCHAR(50),
    start_date DATE,
    end_date DATE,
    side_effects TEXT,
    compliance_notes TEXT
);

-- ============================================
-- Documentation
-- ============================================
CREATE TABLE documentation (
    doc_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID,
    doc_type VARCHAR(50) CHECK (doc_type IN ('Consent', 'Insurance', 'Other')),
    upload_date DATE,
    file_link TEXT
);

-- ============================================
-- Diagnostic Reports
-- ============================================
CREATE TABLE diagnostic_reports (
    report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID,
    disease_type VARCHAR(20) CHECK (disease_type IN ('CML', 'Breast Cancer')),
    test_type VARCHAR(50) CHECK (test_type IN ('Blood Test', 'Biopsy', 'Genetic Test', 'Radiology', 'Mutation Analysis', 'Hormonal Test')),
    report_date DATE,
    test_result_summary TEXT,
    full_report_link TEXT
);

-- ============================================
-- Biopsy
-- ============================================
CREATE TABLE biopsy (
    biopsy_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID,
    biopsy_date DATE,
    sample_site TEXT,
    pathology_report TEXT,
    report_link TEXT
);

-- ============================================
-- Genetic Test
-- ============================================
CREATE TABLE genetic_test (
    genetic_test_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID,
    test_date DATE,
    genes_tested TEXT,
    mutation_found TEXT,
    interpretation_notes TEXT
);

-- ============================================
-- Radiology
-- ============================================
CREATE TABLE radiology (
    radiology_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID,
    imaging_type VARCHAR(50) CHECK (imaging_type IN ('MRI', 'CT', 'Ultrasound', 'X-ray')),
    imaging_date DATE,
    radiologist_notes TEXT,
    report_link TEXT
);

-- ============================================
-- Blood Test (Updated Schema)
-- ============================================
CREATE TABLE blood_test (
    test_id BIGSERIAL PRIMARY KEY,
    patient_id VARCHAR(50),
    test_date DATE NOT NULL,
    test_name VARCHAR(100) NOT NULL,
    test_results JSONB NOT NULL
);

-- ============================================
-- Hormonal Test (Detailed)
-- ============================================
CREATE TABLE hormonal_test (
    test_id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) NOT NULL,
    test_date DATE NOT NULL,
    estrogen_levels DOUBLE PRECISION,
    progesterone_levels DOUBLE PRECISION,
    testosterone_levels DOUBLE PRECISION,
    follicle_stimulating_hormone DOUBLE PRECISION,
    luteinizing_hormone DOUBLE PRECISION,
    thyroid_tsh DOUBLE PRECISION,
    thyroid_t3 DOUBLE PRECISION,
    thyroid_t4 DOUBLE PRECISION,
    notes TEXT
);

-- ============================================
-- Mutation Analysis (CML Specific)
-- ============================================
CREATE TABLE mutation_analysis (
    test_id SERIAL PRIMARY KEY,
    patient_id TEXT NOT NULL,
    test_date DATE NOT NULL,
    bcr_abl_fusion_gene TEXT,
    bcr_abl_transcript_levels DOUBLE PRECISION,
    t315i_mutation TEXT,
    e255k_mutation TEXT,
    f317l_mutation TEXT,
    g250e_mutation TEXT,
    m351t_mutation TEXT,
    v299l_mutation TEXT
);

-- ============================================
-- Tumor Markers (Breast Cancer Specific)
-- ============================================
CREATE TABLE tumor_marks (
    test_id SERIAL PRIMARY KEY,
    patient_id TEXT NOT NULL,
    test_date DATE NOT NULL,
    ca_15_3 NUMERIC,
    ca_27_29 NUMERIC,
    carcinoembryonic_antigen NUMERIC,
    her2_neu VARCHAR(10),
    muc1 NUMERIC
);

-- ============================================
-- Clinical Notes
-- ============================================
CREATE TABLE clinical_notes (
    visit_id SERIAL PRIMARY KEY,
    patient_id TEXT,
    date_of_visit DATE NOT NULL,
    disease_type TEXT NOT NULL,
    has_disease BOOLEAN NOT NULL,
    doctor_diagnosis TEXT NOT NULL,
    prescriptions TEXT,
    allergy TEXT,
    next_visit_date DATE
);

-- ============================================
-- Create Indexes
-- ============================================
CREATE UNIQUE INDEX IF NOT EXISTS patients_primary_phone_number_key ON patients(primary_phone_number);
CREATE INDEX IF NOT EXISTS idx_patient_summary_patient_id ON patient_summary(patient_id);
CREATE INDEX IF NOT EXISTS idx_medical_history_patient_id ON medical_history(patient_id);
CREATE INDEX IF NOT EXISTS idx_medication_profile_patient_id ON medication_profile(patient_id);
CREATE INDEX IF NOT EXISTS idx_blood_test_patient_id ON blood_test(patient_id);
CREATE INDEX IF NOT EXISTS idx_hormonal_test_patient_id ON hormonal_test(patient_id);
CREATE INDEX IF NOT EXISTS idx_mutation_analysis_patient_id ON mutation_analysis(patient_id);
CREATE INDEX IF NOT EXISTS idx_tumor_marks_patient_id ON tumor_marks(patient_id);
CREATE INDEX IF NOT EXISTS idx_clinical_notes_patient_id ON clinical_notes(patient_id);

SQL

echo "✅ All tables created successfully in database '$DBNAME'."
echo ""
echo "📋 Tables created:"
echo "   • patients (main patient table with TEXT IDs)"
echo "   • patients_infor (alternative patient table with UUID)"
echo "   • patient_summary"
echo "   • medical_history"
echo "   • medication_profile"
echo "   • documentation"
echo "   • diagnostic_reports"
echo "   • biopsy"
echo "   • genetic_test"
echo "   • radiology"
echo "   • blood_test (with JSONB results)"
echo "   • hormonal_test (detailed hormone levels)"
echo "   • mutation_analysis (CML specific mutations)"
echo "   • tumor_marks (breast cancer markers)"
echo "   • clinical_notes (visit records)"
echo ""