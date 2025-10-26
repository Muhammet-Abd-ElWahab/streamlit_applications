import pandas as pd
import numpy as np
from datetime import datetime
import os

class DataProcessor:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load data from CSV file"""
        self.df = pd.read_csv(self.csv_path)
        
        # Convert date columns to datetime
        date_columns = ['initial_diagnosis_date', 'visit_date', 'next_appointment']
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        
        # Process badges column (split by pipe character)
        self.df['badges_list'] = self.df['badges'].apply(lambda x: x.split('|') if isinstance(x, str) and '|' in x else [x] if isinstance(x, str) else [])
        self.df['badges_count'] = self.df['badges_list'].apply(len)
        
        # Create unique patients dataframe
        self.unique_patients = self.df.sort_values('visit_number').groupby('patient_id').last().reset_index()
        
    def get_all_patients(self):
        """Return all unique patients"""
        return self.unique_patients
    
    def get_patient_data(self, patient_id):
        """Get all data for a specific patient"""
        return self.df[self.df['patient_id'] == patient_id].sort_values('visit_number')
    
    def get_dashboard_stats(self):
        """Get statistics for dashboard"""
        stats = {
            'total_patients': self.unique_patients.shape[0],
            'total_visits': self.df.shape[0],
            'avg_age': round(self.unique_patients['age'].mean(), 1),
            'avg_health_score': round(self.unique_patients['health_score'].mean(), 1),
            'avg_commitment_score': round(self.unique_patients['commitment_score'].mean(), 1),
            'treatment_types': self.unique_patients['treatment_type'].value_counts().to_dict(),
            'age_groups': self.get_age_groups(),
            'badges_distribution': self.get_badges_distribution(),
            'level_distribution': self.unique_patients['level'].value_counts().sort_index().to_dict()
        }
        return stats
    
    def get_age_groups(self):
        """Group patients by age range"""
        bins = [0, 30, 45, 60, 75, 100]
        labels = ['<30', '30-45', '46-60', '61-75', '75+']
        self.unique_patients['age_group'] = pd.cut(self.unique_patients['age'], bins=bins, labels=labels, right=False)
        return self.unique_patients['age_group'].value_counts().sort_index().to_dict()
    
    def get_badges_distribution(self):
        """Get distribution of badges across all patients"""
        all_badges = []
        for badges in self.df['badges_list']:
            all_badges.extend(badges)
        
        badge_counts = {}
        for badge in all_badges:
            if badge in badge_counts:
                badge_counts[badge] += 1
            else:
                badge_counts[badge] = 1
        
        # Sort by count (descending)
        return dict(sorted(badge_counts.items(), key=lambda x: x[1], reverse=True))
    
    def get_leaderboard(self, sort_by='ranking_percentile', ascending=False):
        """Get leaderboard data sorted by specified column"""
        leaderboard_columns = ['patient_id', 'name', 'level', 'total_points', 'health_score', 
                               'commitment_score', 'badges_count', 'ranking_percentile']
        
        leaderboard = self.unique_patients[leaderboard_columns].sort_values(sort_by, ascending=ascending)
        leaderboard = leaderboard.reset_index(drop=True)
        leaderboard.index = leaderboard.index + 1  # Start rank from 1 instead of 0
        return leaderboard
    
    def get_patient_comparison(self, patient_id):
        """Compare patient metrics with average metrics"""
        patient_data = self.unique_patients[self.unique_patients['patient_id'] == patient_id].iloc[0]
        
        comparison_metrics = ['health_score', 'commitment_score', 'total_points', 'level', 
                             'medication_streak', 'attendance_rate']
        
        comparison = {}
        for metric in comparison_metrics:
            comparison[metric] = {
                'patient': patient_data[metric],
                'average': round(self.unique_patients[metric].mean(), 1),
                'percentile': round(patient_data['ranking_percentile'], 0)
            }
        
        return comparison
    
    def get_patient_visits_timeline(self, patient_id):
        """Get timeline of patient visits"""
        patient_visits = self.df[self.df['patient_id'] == patient_id].sort_values('visit_number')
        
        timeline = []
        for _, visit in patient_visits.iterrows():
            timeline.append({
                'visit_number': visit['visit_number'],
                'visit_date': visit['visit_date'].strftime('%Y-%m-%d'),
                'tumor_size_cm': visit['tumor_size_cm'],
                'side_effect_severity': visit['side_effect_severity'],
                'quality_of_life': visit['quality_of_life'],
                'treatment_adherence': visit['treatment_adherence'],
                'points_earned': visit['points_earned'],
                'notes': visit['notes']
            })
        
        return timeline
    
    def get_medication_calendar(self, patient_id):
        """Get medication adherence calendar based on med_tracking_7days"""
        patient_data = self.unique_patients[self.unique_patients['patient_id'] == patient_id].iloc[0]
        med_tracking = patient_data['med_tracking_7days']
        
        if not isinstance(med_tracking, str):
            return [0] * 7  # Default to all zeros if data is missing
        
        # Convert string of 0s and 1s to list of integers
        calendar = [int(day) for day in med_tracking]
        
        # Ensure we have exactly 7 days (pad with zeros if needed)
        calendar = (calendar + [0] * 7)[:7]
        
        return calendar
