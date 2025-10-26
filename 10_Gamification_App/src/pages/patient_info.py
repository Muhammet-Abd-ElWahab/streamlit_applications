import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

def patient_info_page(data_processor, patient_id):
    """Patient Information Page"""
    st.markdown("<h1 class='main-header'>My Information</h1>", unsafe_allow_html=True)
    
    # Get patient data
    patients = data_processor.get_all_patients()
    patient_data = patients[patients['patient_id'] == patient_id].iloc[0]
    patient_visits = data_processor.get_patient_data(patient_id)
    
    # Display patient information in a card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    # Header with patient info
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader(f"Welcome, {patient_data['name']}")
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
    tab1, tab2, tab3, tab4 = st.tabs(["My Progress", "Medical History", "How Do I Compare?", "Medication Tracking"])
    
    # Tab 1: Gamification Metrics
    with tab1:
        st.markdown("<div class='subheader'>My Progress</div>", unsafe_allow_html=True)
        
        # Points and Level
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Points Progress")
            total_points = patient_data['total_points']
            next_level_points = total_points + 100  # Simplified calculation
            progress = total_points / next_level_points
            
            st.progress(progress)
            st.write(f"Total Points: {total_points} / {next_level_points} for next level")
            
            # Add some encouragement
            points_needed = next_level_points - total_points
            st.info(f"💪 You need {points_needed} more points to reach Level {patient_data['level'] + 1}!")
        
        with col2:
            st.markdown("##### Medication Streak")
            current_streak = patient_data['medication_streak']
            max_streak = patient_data['max_streak']
            streak_progress = current_streak / max_streak if max_streak > 0 else 0
            
            st.progress(streak_progress)
            st.write(f"Current Streak: {current_streak} / Max Streak: {max_streak}")
            
            # Add some encouragement
            if current_streak < max_streak:
                streak_diff = max_streak - current_streak
                st.info(f"🔥 Keep going! You're {streak_diff} days away from beating your record!")
            else:
                st.success(f"🏆 Amazing! You're on your best streak ever!")
        
        # Attendance Rate
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Attendance Rate")
            attendance_rate = patient_data['attendance_rate'] / 100  # Convert to decimal
            
            st.progress(attendance_rate)
            st.write(f"Attendance Rate: {patient_data['attendance_rate']}%")
            
            # Add some encouragement
            if patient_data['attendance_rate'] >= 90:
                st.success("🌟 Excellent attendance! Keep it up!")
            elif patient_data['attendance_rate'] >= 75:
                st.info("👍 Good attendance! Try to make every appointment.")
            else:
                st.warning("⚠️ Try to improve your attendance to get better results.")
        
        with col2:
            st.markdown("##### Ranking Percentile")
            percentile = patient_data['ranking_percentile'] / 100  # Convert to decimal
            
            st.progress(percentile)
            st.write(f"Ranking Percentile: {patient_data['ranking_percentile']}%")
            
            # Add some context
            if patient_data['ranking_percentile'] >= 90:
                st.success("🏅 You're among the top performers!")
            elif patient_data['ranking_percentile'] >= 75:
                st.info("🌟 You're doing better than most patients!")
            elif patient_data['ranking_percentile'] >= 50:
                st.info("👍 You're above average!")
            else:
                st.warning("💪 Keep working to improve your ranking!")
        
        # Badges
        st.markdown("##### My Badges")
        
        badges = patient_data['badges'].split('|') if '|' in patient_data['badges'] else [patient_data['badges']]
        
        badge_html = ""
        for badge in badges:
            badge_html += f"<div class='badge'>{badge}</div>"
        
        st.markdown(f"<div>{badge_html}</div>", unsafe_allow_html=True)
        
        # Add some context about badges
        st.markdown("""  
        Earn badges by completing specific health goals:  
        - **Medication Master**: Perfect medication adherence  
        - **Lab Test Warrior**: Completing all lab tests  
        - **Exercise Champion**: Meeting exercise goals  
        - **Nutrition Expert**: Following dietary guidelines  
        - **Hydration Hero**: Meeting hydration goals  
        - **Sleep Tracker**: Maintaining healthy sleep patterns  
        """)
    
    # Tab 2: Medical History
    with tab2:
        st.markdown("<div class='subheader'>My Medical History</div>", unsafe_allow_html=True)
        
        # Create timeline of visits
        timeline = data_processor.get_patient_visits_timeline(patient_id)
        
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
        
        # Create dataframe for plotting
        plot_df = pd.DataFrame({
            'Visit Number': visit_numbers,
            'Tumor Size (cm)': tumor_sizes
        })
        
        # Plot tumor size over time
        st.markdown("##### My Treatment Progress")
        fig = px.line(
            plot_df, 
            x='Visit Number', 
            y='Tumor Size (cm)',
            markers=True,
            line_shape='linear',
            title='Tumor Size Over Time'
        )
        
        fig.update_layout(
            xaxis=dict(tickmode='linear', dtick=1),
            height=300
        )
        
        # Add annotations for progress
        if len(tumor_sizes) > 1:
            initial_size = tumor_sizes[0]
            current_size = tumor_sizes[-1]
            percent_reduction = ((initial_size - current_size) / initial_size) * 100
            
            fig.add_annotation(
                x=visit_numbers[-1],
                y=tumor_sizes[-1],
                text=f"{percent_reduction:.1f}% reduction",
                showarrow=True,
                arrowhead=1
            )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add encouragement based on progress
        if len(tumor_sizes) > 1:
            if percent_reduction > 0:
                st.success(f"🎉 Great progress! Your tumor has reduced by {percent_reduction:.1f}% since your first visit.")
            elif percent_reduction == 0:
                st.info("Your tumor size has remained stable. Continue with your treatment plan.")
            else:
                st.warning("Your tumor size has increased. Please discuss with your doctor at your next appointment.")
    
    # Tab 3: Comparative Analysis
    with tab3:
        st.markdown("<div class='subheader'>How Do I Compare?</div>", unsafe_allow_html=True)
        
        # Get comparison data
        comparison = data_processor.get_patient_comparison(patient_id)
        
        # Create radar chart for comparison
        categories = list(comparison.keys())
        patient_values = [comparison[metric]['patient'] for metric in categories]
        average_values = [comparison[metric]['average'] for metric in categories]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=patient_values,
            theta=categories,
            fill='toself',
            name='You'
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
        st.markdown("##### Your Ranking")
        st.write(f"You are in the **{patient_data['ranking_percentile']}th percentile** compared to other patients.")
        
        # Create a gauge chart for percentile
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=patient_data['ranking_percentile'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Your Percentile Ranking"},
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
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add tips for improvement
        st.markdown("##### Tips to Improve Your Ranking")
        
        tips = [
            "Take your medication consistently to increase your streak",
            "Attend all scheduled appointments",
            "Follow your treatment plan closely",
            "Track your symptoms and side effects",
            "Stay hydrated and maintain a healthy diet",
            "Get regular exercise as recommended by your doctor",
            "Get enough sleep and manage stress"
        ]
        
        for tip in tips:
            st.markdown(f"- {tip}")
    
    # Tab 4: Medication Adherence
    with tab4:
        st.markdown("<div class='subheader'>My Medication Tracking</div>", unsafe_allow_html=True)
        
        # Get medication calendar data
        med_calendar = data_processor.get_medication_calendar(patient_id)
        
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
            height=300,
            title='Last 7 Days Medication Tracking'
        )
        
        fig.update_layout(
            xaxis_title="",
            yaxis_title="",
            yaxis=dict(tickmode='linear', dtick=1, range=[0, 1.1]),
            showlegend=False
        )
        
        # Add text annotations
        for i, val in enumerate(med_calendar):
            text = "✓" if val == 1 else "✗"
            color = "green" if val == 1 else "red"
            
            fig.add_annotation(
                x=days[i],
                y=val,
                text=text,
                showarrow=False,
                font=dict(size=20, color=color)
            )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate adherence rate
        adherence_rate = sum(med_calendar) / len(med_calendar) * 100
        
        # Display adherence rate
        st.markdown(f"##### 7-Day Adherence Rate: {adherence_rate:.1f}%")
        
        # Display medication streak information
        st.markdown(f"##### Current Medication Streak: {patient_data['medication_streak']} days")
        st.markdown(f"##### Maximum Streak: {patient_data['max_streak']} days")
        
        # Add tips for medication adherence
        st.markdown("##### Tips for Medication Adherence")
        st.markdown("""
        - Set daily reminders on your phone
        - Use a pill organizer
        - Take medication at the same time each day
        - Keep a medication journal
        - Ask a family member to help remind you
        - Use a medication tracking app
        """)

