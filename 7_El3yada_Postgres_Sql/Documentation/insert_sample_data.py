#!/usr/bin/env python3
"""
Sample Data Insertion Script for El3yada Medical Database
Inserts realistic sample data into all tables
"""

import psycopg2
from psycopg2.extras import execute_values
import json
from datetime import datetime, timedelta
import random
import streamlit as st

# Database configuration
DB_CONFIG = {
    'dbname': st.secrets['dbname'],
    'user': st.secrets['dbusername'],
    'password': st.secrets['password'],
    'host': st.secrets['host'],
    'port': st.secrets['port']
}

# Sample data counts
NUM_PATIENTS = 50
NUM_BLOOD_TESTS = 100
NUM_HORMONAL_TESTS = 80
NUM_TUMOR_MARKS = 60
NUM_MUTATION_ANALYSIS = 40
NUM_CLINICAL_NOTES = 150

def truncate_all_tables(conn):
    """Truncate all tables before inserting new data"""
    print("\n🗑️  Truncating all tables...")
    cur = conn.cursor()
    
    tables = [
        'clinical_notes',
        'tumor_marks',
        'mutation_analysis',
        'hormonal_test',
        'blood_test',
        'radiology',
        'genetic_test',
        'biopsy',
        'diagnostic_reports',
        'documentation',
        'medication_profile',
        'medical_history',
        'patient_summary',
        'patients_infor',
        'patients'
    ]
    
    for table in tables:
        try:
            cur.execute(f"TRUNCATE TABLE {table} CASCADE;")
            print(f"  ✓ Truncated {table}")
        except Exception as e:
            print(f"  ⚠️  Could not truncate {table}: {e}")
    
    conn.commit()
    cur.close()
    print("✅ All tables truncated\n")

def generate_patient_id(index):
    """Generate patient ID in format P001, P002, etc."""
    return f"P{str(index).zfill(3)}"

def random_date(start_year=2020, end_year=2024):
    """Generate random date"""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def insert_patients(conn):
    """Insert sample patients"""
    print(f"📝 Inserting {NUM_PATIENTS} patients...")
    cur = conn.cursor()
    
    first_names = ['Ahmed', 'Mohamed', 'Fatma', 'Aisha', 'Ali', 'Sara', 'Omar', 'Nour', 
                   'Hassan', 'Mona', 'Youssef', 'Layla', 'Karim', 'Huda', 'Mahmoud']
    last_names = ['Ibrahim', 'Hassan', 'Ali', 'Mahmoud', 'Ahmed', 'Salem', 'Khalil', 
                  'Farouk', 'Nasser', 'Gamal', 'Zaki', 'Rashid']
    
    patients_data = []
    for i in range(1, NUM_PATIENTS + 1):
        patient_id = generate_patient_id(i)
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        gender = random.choice(['Male', 'Female'])
        birth_year = random.randint(1950, 2005)
        birth_date = datetime(birth_year, random.randint(1, 12), random.randint(1, 28))
        age = 2024 - birth_year
        
        patients_data.append((
            patient_id,
            name,
            gender,
            birth_date,
            age,
            f"+20{random.randint(1000000000, 1999999999)}",
            f"+20{random.randint(1000000000, 1999999999)}" if random.random() > 0.3 else None,
            f"{random.choice(first_names)} {random.choice(last_names)}",
            f"+20{random.randint(1000000000, 1999999999)}",
            f"{first_name.lower()}.{last_name.lower()}@email.com",
            f"{random.randint(1, 100)} {random.choice(['Tahrir', 'Nasr', 'Heliopolis', 'Maadi', 'Zamalek'])} St, Cairo",
            random.choice(['Single', 'Married', 'Divorced', 'Widowed']),
            f"Patient notes for {name}"
        ))
    
    execute_values(cur, """
        INSERT INTO patients (patient_id, name, gender, birth_date, age, primary_phone_number,
                             secondary_phone_number, emergency_name, emergency_phone_number,
                             email, address, marital_status, notes)
        VALUES %s
    """, patients_data)
    
    conn.commit()
    cur.close()
    print(f"✅ Inserted {NUM_PATIENTS} patients\n")

def insert_blood_tests(conn):
    """Insert sample blood tests"""
    print(f"🩸 Inserting {NUM_BLOOD_TESTS} blood tests...")
    cur = conn.cursor()
    
    test_names = ['Complete Blood Count', 'Lipid Panel', 'Metabolic Panel', 'Liver Function', 'Kidney Function']
    
    blood_tests_data = []
    for i in range(NUM_BLOOD_TESTS):
        patient_id = generate_patient_id(random.randint(1, NUM_PATIENTS))
        test_date = random_date(2022, 2024)
        test_name = random.choice(test_names)
        
        # Generate random test results as JSON
        test_results = {
            'WBC': round(random.uniform(4.0, 11.0), 2),
            'RBC': round(random.uniform(4.0, 6.0), 2),
            'Hemoglobin': round(random.uniform(12.0, 17.0), 2),
            'Platelets': random.randint(150, 400),
            'Glucose': random.randint(70, 140)
        }
        
        blood_tests_data.append((
            patient_id,
            test_date,
            test_name,
            json.dumps(test_results)
        ))
    
    execute_values(cur, """
        INSERT INTO blood_test (patient_id, test_date, test_name, test_results)
        VALUES %s
    """, blood_tests_data)
    
    conn.commit()
    cur.close()
    print(f"✅ Inserted {NUM_BLOOD_TESTS} blood tests\n")

def insert_hormonal_tests(conn):
    """Insert sample hormonal tests"""
    print(f"💉 Inserting {NUM_HORMONAL_TESTS} hormonal tests...")
    cur = conn.cursor()
    
    hormonal_tests_data = []
    for i in range(NUM_HORMONAL_TESTS):
        patient_id = generate_patient_id(random.randint(1, NUM_PATIENTS))
        test_date = random_date(2022, 2024)
        
        hormonal_tests_data.append((
            patient_id,
            test_date,
            round(random.uniform(20.0, 400.0), 2),  # estrogen
            round(random.uniform(0.1, 25.0), 2),    # progesterone
            round(random.uniform(250.0, 1100.0), 2), # testosterone
            round(random.uniform(1.5, 12.0), 2),    # FSH
            round(random.uniform(1.0, 10.0), 2),    # LH
            round(random.uniform(0.4, 4.5), 2),     # TSH
            round(random.uniform(80.0, 200.0), 2),  # T3
            round(random.uniform(4.5, 12.0), 2),    # T4
            f"Normal hormonal levels for patient"
        ))
    
    execute_values(cur, """
        INSERT INTO hormonal_test (patient_id, test_date, estrogen_levels, progesterone_levels,
                                   testosterone_levels, follicle_stimulating_hormone, luteinizing_hormone,
                                   thyroid_tsh, thyroid_t3, thyroid_t4, notes)
        VALUES %s
    """, hormonal_tests_data)
    
    conn.commit()
    cur.close()
    print(f"✅ Inserted {NUM_HORMONAL_TESTS} hormonal tests\n")

def insert_tumor_marks(conn):
    """Insert sample tumor markers"""
    print(f"🎗️  Inserting {NUM_TUMOR_MARKS} tumor marker tests...")
    cur = conn.cursor()
    
    tumor_marks_data = []
    for i in range(NUM_TUMOR_MARKS):
        patient_id = generate_patient_id(random.randint(1, NUM_PATIENTS))
        test_date = random_date(2022, 2024)
        
        tumor_marks_data.append((
            patient_id,
            test_date,
            round(random.uniform(0.0, 40.0), 2),    # CA 15-3
            round(random.uniform(0.0, 38.0), 2),    # CA 27-29
            round(random.uniform(0.0, 5.0), 2),     # CEA
            random.choice(['Negative', 'Positive', '1+', '2+', '3+']),  # HER2
            round(random.uniform(0.0, 100.0), 2)    # MUC1
        ))
    
    execute_values(cur, """
        INSERT INTO tumor_marks (patient_id, test_date, ca_15_3, ca_27_29,
                                carcinoembryonic_antigen, her2_neu, muc1)
        VALUES %s
    """, tumor_marks_data)
    
    conn.commit()
    cur.close()
    print(f"✅ Inserted {NUM_TUMOR_MARKS} tumor marker tests\n")

def insert_mutation_analysis(conn):
    """Insert sample mutation analysis"""
    print(f"🧬 Inserting {NUM_MUTATION_ANALYSIS} mutation analyses...")
    cur = conn.cursor()
    
    mutation_data = []
    for i in range(NUM_MUTATION_ANALYSIS):
        patient_id = generate_patient_id(random.randint(1, NUM_PATIENTS))
        test_date = random_date(2022, 2024)
        
        mutation_data.append((
            patient_id,
            test_date,
            random.choice(['Positive', 'Negative']),
            round(random.uniform(0.0, 100.0), 2),
            random.choice(['Detected', 'Not Detected']),
            random.choice(['Detected', 'Not Detected']),
            random.choice(['Detected', 'Not Detected']),
            random.choice(['Detected', 'Not Detected']),
            random.choice(['Detected', 'Not Detected']),
            random.choice(['Detected', 'Not Detected'])
        ))
    
    execute_values(cur, """
        INSERT INTO mutation_analysis (patient_id, test_date, bcr_abl_fusion_gene,
                                      bcr_abl_transcript_levels, t315i_mutation, e255k_mutation,
                                      f317l_mutation, g250e_mutation, m351t_mutation, v299l_mutation)
        VALUES %s
    """, mutation_data)
    
    conn.commit()
    cur.close()
    print(f"✅ Inserted {NUM_MUTATION_ANALYSIS} mutation analyses\n")

def insert_clinical_notes(conn):
    """Insert sample clinical notes"""
    print(f"📋 Inserting {NUM_CLINICAL_NOTES} clinical notes...")
    cur = conn.cursor()
    
    disease_types = ['CML', 'Breast Cancer']
    diagnoses = [
        'Patient showing improvement',
        'Stable condition',
        'Requires follow-up',
        'Treatment responding well',
        'Side effects managed'
    ]
    prescriptions = [
        'Imatinib 400mg daily',
        'Tamoxifen 20mg daily',
        'Dasatinib 100mg daily',
        'Letrozole 2.5mg daily'
    ]
    
    clinical_notes_data = []
    for i in range(NUM_CLINICAL_NOTES):
        patient_id = generate_patient_id(random.randint(1, NUM_PATIENTS))
        visit_date = random_date(2022, 2024)
        disease_type = random.choice(disease_types)
        has_disease = random.choice([True, False])
        
        clinical_notes_data.append((
            patient_id,
            visit_date,
            disease_type,
            has_disease,
            random.choice(diagnoses),
            random.choice(prescriptions) if has_disease else None,
            'No known allergies' if random.random() > 0.2 else 'Penicillin allergy',
            visit_date + timedelta(days=random.randint(30, 90))
        ))
    
    execute_values(cur, """
        INSERT INTO clinical_notes (patient_id, date_of_visit, disease_type, has_disease,
                                   doctor_diagnosis, prescriptions, allergy, next_visit_date)
        VALUES %s
    """, clinical_notes_data)
    
    conn.commit()
    cur.close()
    print(f"✅ Inserted {NUM_CLINICAL_NOTES} clinical notes\n")

def main():
    """Main execution function"""
    print("=" * 70)
    print("  El3yada Medical Database - Sample Data Insertion")
    print("=" * 70)
    print(f"\nConnecting to database: {DB_CONFIG['dbname']}@{DB_CONFIG['host']}")
    
    try:
        # Connect to database
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected successfully\n")
        
        # Ask user if they want to truncate tables
        response = input("⚠️  Do you want to TRUNCATE all tables before inserting? (yes/no): ").lower()
        if response in ['yes', 'y']:
            truncate_all_tables(conn)
        
        # Insert data into all tables
        insert_patients(conn)
        insert_blood_tests(conn)
        insert_hormonal_tests(conn)
        insert_tumor_marks(conn)
        insert_mutation_analysis(conn)
        insert_clinical_notes(conn)
        
        # Close connection
        conn.close()
        
        print("=" * 70)
        print("  ✅ DATA INSERTION COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print(f"\n📊 Summary:")
        print(f"  • {NUM_PATIENTS} patients")
        print(f"  • {NUM_BLOOD_TESTS} blood tests")
        print(f"  • {NUM_HORMONAL_TESTS} hormonal tests")
        print(f"  • {NUM_TUMOR_MARKS} tumor marker tests")
        print(f"  • {NUM_MUTATION_ANALYSIS} mutation analyses")
        print(f"  • {NUM_CLINICAL_NOTES} clinical notes")
        print(f"\n  Total: {NUM_PATIENTS + NUM_BLOOD_TESTS + NUM_HORMONAL_TESTS + NUM_TUMOR_MARKS + NUM_MUTATION_ANALYSIS + NUM_CLINICAL_NOTES} records inserted")
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
