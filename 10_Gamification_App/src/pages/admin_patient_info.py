import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

def admin_patient_info_page(data_processor):
    """Admin Patient Information Page"""
    st.markdown("<h1 class='main-header'>Patient Information</h1>", unsafe_allow_html=True)
    
    # Get all patients
    patients = data_processor.get_all_patients()
    
    # Create patient selector
    patient_options = patients['patient_id'].tolist()
    patient_names = patients['name'].tolist()
    patient_display = [f"{id} - {name}" for id, name in zip(patient_options, patient_names)]
    
    selected_patient_display = st.selectbox(
        "Select Patient",
        options=patient_display,
        index=0
    )
    
    # Extract patient ID from selection
    selected_patient_id = selected_patient_display.split(' - ')[0]
    
    # Get patient data
    patient_data = patients[patients['patient_id'] == selected_patient_id].iloc[0]
    patient_visits = data_processor.get_patient_data(selected_patient_id)
    
    # Display patient information in a card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    # Header with patient info
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader(f"{patient_data['name']} ({patient_data['patient_id']})")
        st.write(f"Age: {patient_data['age']}")
        st.write(f"Treatment Type: {patient_data['treatment_type']}")
        st.write(f"Initial Diagnosis: {patient_data['initial_diagnosis_date'].strftime('%Y-%m-%d')}")
    
    with col2:
        st.markdown("<div class='subheader'>Next Appointment</div>", unsafe_allow_html=True)
        next_appointment = patient_data['next_appointment'].strftime('%Y-%m-%d')
        st.markdown(f"<div style='font-size:1.5rem; color:#4527A0; font-weight:bold;'>{next_appointment}</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='subheader'>Current Level</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:1.5rem; color:#4527A0; font-weight:bold;'>Level {patient_data['level']}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Gamification Metrics", "Medical History", "Comparative Analysis", "Medication Adherence"])
    
    # Tab 1: Gamification Metrics
    with tab1:
        st.markdown("<div class='subheader'>Gamification Metrics</div>", unsafe_allow_html=True)
        
        # Points and Level
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Points Progress")
            total_points = patient_data['total_points']
            next_level_points = total_points + 100  # Simplified calculation
            progress = total_points / next_level_points
            
            st.progress(progress)
            st.write(f"Total Points: {total_points} / {next_level_points} for next level")
        
        with col2:
            st.markdown("##### Medication Streak")
            current_streak = patient_data['medication_streak']
            max_streak = patient_data['max_streak']
            streak_progress = current_streak / max_streak if max_streak > 0 else 0
            
            st.progress(streak_progress)
            st.write(f"Current Streak: {current_streak} / Max Streak: {max_streak}")
        
        # Attendance Rate
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Attendance Rate")
            attendance_rate = patient_data['attendance_rate'] / 100  # Convert to decimal
            
            st.progress(attendance_rate)
            st.write(f"Attendance Rate: {patient_data['attendance_rate']}%")
        
        with col2:
            st.markdown("##### Ranking Percentile")
            percentile = patient_data['ranking_percentile'] / 100  # Convert to decimal
            
            st.progress(percentile)
            st.write(f"Ranking Percentile: {patient_data['ranking_percentile']}%")
        
        # Badges
        st.markdown("##### Badges Earned")
        
        badges = patient_data['badges'].split('|') if '|' in patient_data['badges'] else [patient_data['badges']]
        
        badge_html = ""
        for badge in badges:
            badge_html += f"<div class='badge'>{badge}</div>"
        
        st.markdown(f"<div>{badge_html}</div>", unsafe_allow_html=True)
    
    # Tab 2: Medical History
    with tab2:
        st.markdown("<div class='subheader'>Medical History Timeline</div>", unsafe_allow_html=True)
        
        # Create timeline of visits
        timeline = data_processor.get_patient_visits_timeline(selected_patient_id)
        
        # Display each visit as a card
        for visit in timeline:
            with st.expander(f"Visit #{visit['visit_number']} - {visit['visit_date']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("##### Medical Metrics")
                    st.write(f"Tumor Size: {visit['tumor_size_cm']} cm")
                    st.write(f"Side Effect Severity: {visit['side_effect_severity']}/10")
                    st.write(f"Quality of Life: {visit['quality_of_life']}/10")
                    st.write(f"Treatment Adherence: {visit['treatment_adherence']}%")
                
                with col2:
                    st.markdown("##### Notes")
                    st.write(visit['notes'])
                    
                    st.markdown("##### Points Earned")
                    st.write(f"Points: {visit['points_earned']}")
        
        # Create a line chart for tumor size over time
        visit_numbers = [visit['visit_number'] for visit in timeline]
        tumor_sizes = [visit['tumor_size_cm'] for visit in timeline]
        side_effects = [visit['side_effect_severity'] for visit in timeline]
        quality_of_life = [visit['quality_of_life'] for visit in timeline]
        
        # Create dataframe for plotting
        plot_df = pd.DataFrame({
            'Visit Number': visit_numbers,
            'Tumor Size (cm)': tumor_sizes,
            'Side Effect Severity': side_effects,
            'Quality of Life': quality_of_life
        })
        
        # Plot tumor size over time
        st.markdown("##### Tumor Size Over Time")
        fig = px.line(
            plot_df, 
            x='Visit Number', 
            y='Tumor Size (cm)',
            markers=True,
            line_shape='linear'
        )
        
        fig.update_layout(
            xaxis=dict(tickmode='linear', dtick=1),
            height=300,
            margin=dict(t=0, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Plot side effects and quality of life
        st.markdown("##### Side Effects & Quality of Life")
        fig = px.line(
            plot_df, 
            x='Visit Number', 
            y=['Side Effect Severity', 'Quality of Life'],
            markers=True,
            line_shape='linear'
        )
        
        fig.update_layout(
            xaxis=dict(tickmode='linear', dtick=1),
            height=300,
            margin=dict(t=0, b=0, l=0, r=0),
            legend_title_text=''
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Comparative Analysis
    with tab3:
        st.markdown("<div class='subheader'>Comparative Analysis</div>", unsafe_allow_html=True)
        
        # Get comparison data
        comparison = data_processor.get_patient_comparison(selected_patient_id)
        
        # Create radar chart for comparison
        categories = list(comparison.keys())
        patient_values = [comparison[metric]['patient'] for metric in categories]
        average_values = [comparison[metric]['average'] for metric in categories]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=patient_values,
            theta=categories,
            fill='toself',
            name=f'{patient_data["name"]}'  
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=average_values,
            theta=categories,
            fill='toself',
            name='Average Patient'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                )
            ),
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display percentile ranking
        st.markdown("##### Percentile Ranking")
        st.write(f"This patient is in the **{patient_data['ranking_percentile']}th percentile** compared to other patients.")
        
        # Create a gauge chart for percentile
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=patient_data['ranking_percentile'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Percentile Ranking"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#4527A0"},
                'steps': [
                    {'range': [0, 25], 'color': "#EDE7F6"},
                    {'range': [25, 50], 'color': "#D1C4E9"},
                    {'range': [50, 75], 'color': "#B39DDB"},
                    {'range': [75, 100], 'color': "#9575CD"}
                ]
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(t=0, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: Medication Adherence
    with tab4:
        st.markdown("<div class='subheader'>Medication Adherence</div>", unsafe_allow_html=True)
        
        # Get medication calendar data
        med_calendar = data_processor.get_medication_calendar(selected_patient_id)
        
        # Create a weekly calendar visualization
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Create a dataframe for the calendar
        calendar_df = pd.DataFrame({
            'Day': days,
            'Taken': med_calendar
        })
        
        # Create a bar chart for the calendar
        fig = px.bar(
            calendar_df,
            x='Day',
            y='Taken',
            color='Taken',
            color_discrete_map={0: '#EF5350', 1: '#66BB6A'},
            labels={'Taken': 'Medication Taken'},
            height=300
        )
        
        fig.update_layout(
            xaxis_title="",
            yaxis_title="",
            yaxis=dict(tickmode='linear', dtick=1, range=[0, 1.1]),
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate adherence rate
        adherence_rate = sum(med_calendar) / len(med_calendar) * 100
        
        # Display adherence rate
        st.markdown(f"##### 7-Day Adherence Rate: {adherence_rate:.1f}%")
        
        # Display medication streak information
        st.markdown(f"##### Current Medication Streak: {patient_data['medication_streak']} days")
        st.markdown(f"##### Maximum Streak: {patient_data['max_streak']} days")
