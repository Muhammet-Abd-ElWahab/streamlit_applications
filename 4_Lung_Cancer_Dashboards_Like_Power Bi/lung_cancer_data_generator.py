import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_lung_cancer_trial_data(n_patients=500, seed=42):
    """
    Generate synthetic lung cancer clinical trial data for 500 patients.
    
    Data includes measurements across 3 visits for patients in two groups:
    - Placebo
    - Treatment (medication)
    
    Returns a pandas DataFrame with the trial data.
    """
    np.random.seed(seed)
    
    # Patient IDs
    patient_ids = [f'P{i:03d}' for i in range(1, n_patients + 1)]
    
    # Demographics
    ages = np.random.normal(65, 10, n_patients).astype(int)
    ages = np.clip(ages, 40, 90)  # Clip to realistic range
    
    genders = np.random.choice(['Male', 'Female'], n_patients, p=[0.6, 0.4])
    
    # Smoking status (higher prevalence in lung cancer patients)
    smoking_status = np.random.choice(
        ['Never Smoker', 'Former Smoker', 'Current Smoker'],
        n_patients,
        p=[0.15, 0.45, 0.4]
    )
    
    # Pack years for smokers (0 for never smokers)
    pack_years = np.zeros(n_patients)
    for i in range(n_patients):
        if smoking_status[i] == 'Former Smoker':
            pack_years[i] = np.random.normal(25, 10)
        elif smoking_status[i] == 'Current Smoker':
            pack_years[i] = np.random.normal(30, 15)
    pack_years = np.clip(pack_years, 0, 100).round(1)
    
    # Cancer stage
    cancer_stages = np.random.choice(
        ['Stage I', 'Stage II', 'Stage III', 'Stage IV'],
        n_patients,
        p=[0.2, 0.3, 0.3, 0.2]
    )
    
    # Treatment group (balanced randomization)
    treatment_groups = np.random.choice(['Placebo', 'Treatment'], n_patients, p=[0.5, 0.5])
    
    # ECOG Performance Status (0-5 scale, lower is better)
    ecog_status = np.random.choice([0, 1, 2, 3], n_patients, p=[0.3, 0.4, 0.2, 0.1])
    
    # Create base dataframe with patient information
    base_df = pd.DataFrame({
        'PatientID': patient_ids,
        'Age': ages,
        'Gender': genders,
        'SmokingStatus': smoking_status,
        'PackYears': pack_years,
        'CancerStage': cancer_stages,
        'TreatmentGroup': treatment_groups,
        'ECOGStatus': ecog_status
    })
    
    # Visits data
    visits = ['Baseline', 'Visit 1 (Week 4)', 'Visit 2 (Week 8)']
    
    # Function to generate measurements with treatment effect
    def generate_measurements(patient_row, visit_num):
        # Base tumor size (mm) - dependent on cancer stage
        stage_to_size = {
            'Stage I': np.random.normal(15, 5),
            'Stage II': np.random.normal(30, 8),
            'Stage III': np.random.normal(45, 10),
            'Stage IV': np.random.normal(60, 15)
        }
        
        base_tumor_size = stage_to_size[patient_row['CancerStage']]
        
        # Treatment effect increases with visits
        treatment_effect = 0
        if visit_num > 0:  # After baseline
            if patient_row['TreatmentGroup'] == 'Treatment':
                # Treatment reduces tumor size by 5-15% per visit
                treatment_effect = base_tumor_size * (0.05 + 0.1 * visit_num) * np.random.normal(1, 0.3)
            else:  # Placebo
                # Placebo has minimal effect, sometimes tumor grows
                treatment_effect = -base_tumor_size * 0.02 * visit_num * np.random.normal(1, 0.5)
        
        # Final tumor size with some random variation
        tumor_size = max(0, base_tumor_size - treatment_effect + np.random.normal(0, 2))
        
        # Lung function (FEV1) - percent of predicted value
        # Baseline depends on cancer stage and smoking
        base_fev1 = 85 - 5 * ecog_status[patient_row.name]
        if patient_row['SmokingStatus'] == 'Current Smoker':
            base_fev1 -= 15
        elif patient_row['SmokingStatus'] == 'Former Smoker':
            base_fev1 -= 8
            
        # Adjust based on cancer stage
        stage_penalty = {
            'Stage I': 0,
            'Stage II': 5,
            'Stage III': 10,
            'Stage IV': 15
        }
        base_fev1 -= stage_penalty[patient_row['CancerStage']]
        
        # Treatment effect on lung function
        fev1_effect = 0
        if visit_num > 0:
            if patient_row['TreatmentGroup'] == 'Treatment':
                # Treatment improves lung function slightly
                fev1_effect = 2 * visit_num * np.random.normal(1, 0.3)
            else:  # Placebo
                # Placebo has minimal effect
                fev1_effect = 0.5 * visit_num * np.random.normal(1, 0.5)
        
        fev1 = min(100, max(20, base_fev1 + fev1_effect + np.random.normal(0, 3)))
        
        # Quality of Life score (0-100)
        base_qol = 70 - 5 * ecog_status[patient_row.name] - stage_penalty[patient_row['CancerStage']]
        
        qol_effect = 0
        if visit_num > 0:
            if patient_row['TreatmentGroup'] == 'Treatment':
                # Treatment improves QoL
                qol_effect = 3 * visit_num * np.random.normal(1, 0.4)
            else:  # Placebo
                # Placebo has minimal effect
                qol_effect = 1 * visit_num * np.random.normal(1, 0.5)
        
        qol = min(100, max(10, base_qol + qol_effect + np.random.normal(0, 5)))
        
        # Adverse events (0-5 scale, higher is worse)
        if patient_row['TreatmentGroup'] == 'Treatment':
            adverse_events = np.random.choice([0, 1, 2, 3, 4], p=[0.5, 0.25, 0.15, 0.07, 0.03])
        else:  # Placebo has fewer adverse events
            adverse_events = np.random.choice([0, 1, 2], p=[0.8, 0.15, 0.05])
        
        # Pain score (0-10 scale)
        base_pain = min(10, max(0, 3 + stage_penalty[patient_row['CancerStage']]/3 + np.random.normal(0, 1)))
        
        pain_effect = 0
        if visit_num > 0:
            if patient_row['TreatmentGroup'] == 'Treatment':
                # Treatment reduces pain
                pain_effect = 0.5 * visit_num * np.random.normal(1, 0.3)
            else:  # Placebo
                # Placebo has minimal effect
                pain_effect = 0.1 * visit_num * np.random.normal(1, 0.5)
        
        pain_score = max(0, base_pain - pain_effect + np.random.normal(0, 0.5))
        
        # Biomarker levels (normalized 0-100)
        biomarker = 50 + 10 * (4 - ecog_status[patient_row.name])
        if patient_row['TreatmentGroup'] == 'Treatment' and visit_num > 0:
            # Treatment normalizes biomarker
            biomarker = biomarker - 5 * visit_num * np.random.normal(1, 0.3)
        
        biomarker = min(100, max(0, biomarker + np.random.normal(0, 5)))
        
        return {
            'TumorSize': round(tumor_size, 1),
            'LungFunction': round(fev1, 1),
            'QualityOfLife': round(qol, 1),
            'AdverseEvents': adverse_events,
            'PainScore': round(pain_score, 1),
            'Biomarker': round(biomarker, 1)
        }
    
    # Create a list to hold all records
    all_records = []
    
    # Generate data for each patient and visit
    for idx, row in base_df.iterrows():
        for visit_idx, visit in enumerate(visits):
            # Get measurements for this patient and visit
            measurements = generate_measurements(row, visit_idx)
            
            # Create a record
            record = {
                'PatientID': row['PatientID'],
                'Visit': visit,
                'VisitNumber': visit_idx,
                'VisitDate': (datetime(2024, 1, 1) + timedelta(days=28*visit_idx) + 
                             timedelta(days=np.random.randint(-3, 4))).strftime('%Y-%m-%d'),
                'Age': row['Age'],
                'Gender': row['Gender'],
                'SmokingStatus': row['SmokingStatus'],
                'PackYears': row['PackYears'],
                'CancerStage': row['CancerStage'],
                'TreatmentGroup': row['TreatmentGroup'],
                'ECOGStatus': row['ECOGStatus']
            }
            
            # Add measurements
            record.update(measurements)
            
            # Add to records list
            all_records.append(record)
    
    # Create final dataframe
    df = pd.DataFrame(all_records)
    
    # Calculate response rate (>30% reduction in tumor size from baseline)
    baseline_sizes = df[df['Visit'] == 'Baseline'].set_index('PatientID')['TumorSize']
    
    # For visits after baseline
    for visit in visits[1:]:
        visit_data = df[df['Visit'] == visit]
        response_list = []
        
        for _, row in visit_data.iterrows():
            patient_id = row['PatientID']
            baseline_size = baseline_sizes.loc[patient_id]
            current_size = row['TumorSize']
            
            # Calculate percent change
            percent_change = (current_size - baseline_size) / baseline_size * 100
            
            # Determine response
            if percent_change <= -30:
                response = 'Responder'
            else:
                response = 'Non-Responder'
            
            response_list.append(response)
        
        # Add response to dataframe
        df.loc[df['Visit'] == visit, 'Response'] = response_list
    
    # Fill NaN values for baseline visits
    df.loc[df['Visit'] == 'Baseline', 'Response'] = 'Not Applicable'
    
    # Add percent change from baseline for non-baseline visits
    for visit in visits[1:]:
        visit_data = df[df['Visit'] == visit]
        percent_changes = []
        
        for _, row in visit_data.iterrows():
            patient_id = row['PatientID']
            baseline_size = baseline_sizes.loc[patient_id]
            current_size = row['TumorSize']
            
            # Calculate percent change
            percent_change = (current_size - baseline_size) / baseline_size * 100
            percent_changes.append(round(percent_change, 1))
        
        # Add percent change to dataframe
        df.loc[df['Visit'] == visit, 'TumorSizePercentChange'] = percent_changes
    
    # Fill NaN values for baseline visits
    df.loc[df['Visit'] == 'Baseline', 'TumorSizePercentChange'] = 0.0
    
    return df

# Generate the data
if __name__ == "__main__":
    df = generate_lung_cancer_trial_data()
    df.to_csv('lung_cancer_trial_data.csv', index=False)
    print(f"Generated data for {len(df)//3} patients across 3 visits.")
    print(f"Total records: {len(df)}")
