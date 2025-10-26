import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def admin_dashboard_page(data_processor):
    """Admin Dashboard Page"""
    st.markdown("<h1 class='main-header'>Admin Dashboard</h1>", unsafe_allow_html=True)
    
    # Get dashboard statistics
    stats = data_processor.get_dashboard_stats()
    
    # Display key metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='metric-card'>"
                    f"<div class='metric-value'>{stats['total_patients']}</div>"
                    "<div class='metric-label'>Total Patients</div>"
                    "</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>"
                    f"<div class='metric-value'>{stats['total_visits']}</div>"
                    "<div class='metric-label'>Total Visits</div>"
                    "</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='metric-card'>"
                    f"<div class='metric-value'>{stats['avg_health_score']}</div>"
                    "<div class='metric-label'>Avg Health Score</div>"
                    "</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div class='metric-card'>"
                    f"<div class='metric-value'>{stats['avg_commitment_score']}</div>"
                    "<div class='metric-label'>Avg Commitment Score</div>"
                    "</div>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Create two rows of visualizations
    row1_col1, row1_col2 = st.columns(2)
    
    # Treatment Types Distribution
    with row1_col1:
        st.markdown("<div class='subheader'>Treatment Types Distribution</div>", unsafe_allow_html=True)
        
        treatment_df = pd.DataFrame({
            'Treatment': list(stats['treatment_types'].keys()),
            'Count': list(stats['treatment_types'].values())
        })
        
        fig = px.pie(
            treatment_df, 
            values='Count', 
            names='Treatment',
            color_discrete_sequence=['#0077B6', '#00B4D8', '#90E0EF', '#48CAE4', '#0096C7'],
            hole=0.4
        )
        
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            height=350,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Age Group Distribution
    with row1_col2:
        st.markdown("<div class='subheader'>Age Group Distribution</div>", unsafe_allow_html=True)
        
        age_df = pd.DataFrame({
            'Age Group': list(stats['age_groups'].keys()),
            'Count': list(stats['age_groups'].values())
        })
        
        fig = px.bar(
            age_df, 
            x='Age Group', 
            y='Count',
            color='Count',
            color_continuous_scale=['#CAF0F8', '#90E0EF', '#48CAE4', '#00B4D8', '#0096C7', '#0077B6'],
            text='Count'
        )
        
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            height=350,
            xaxis_title="",
            yaxis_title="",
            coloraxis_showscale=False,
            plot_bgcolor='rgba(240,240,240,0.1)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)
    
    row2_col1, row2_col2 = st.columns(2)
    
    # Badge Distribution
    with row2_col1:
        st.markdown("<div class='subheader'>Top Badges Distribution</div>", unsafe_allow_html=True)
        
        # Get top 10 badges
        top_badges = dict(list(stats['badges_distribution'].items())[:10])
        
        badge_df = pd.DataFrame({
            'Badge': list(top_badges.keys()),
            'Count': list(top_badges.values())
        })
        
        fig = px.bar(
            badge_df, 
            y='Badge', 
            x='Count',
            color='Count',
            color_continuous_scale=['#CAF0F8', '#90E0EF', '#48CAE4', '#00B4D8', '#0096C7', '#0077B6'],
            orientation='h',
            text='Count'
        )
        
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            height=350,
            xaxis_title="",
            yaxis_title="",
            coloraxis_showscale=False,
            plot_bgcolor='rgba(240,240,240,0.1)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Level Distribution
    with row2_col2:
        st.markdown("<div class='subheader'>Level Distribution</div>", unsafe_allow_html=True)
        
        level_df = pd.DataFrame({
            'Level': list(stats['level_distribution'].keys()),
            'Count': list(stats['level_distribution'].values())
        })
        
        # Convert level to string for better display
        level_df['Level'] = level_df['Level'].astype(str)
        
        fig = px.bar(
            level_df, 
            x='Level', 
            y='Count',
            color='Count',
            color_continuous_scale=['#CAF0F8', '#90E0EF', '#48CAE4', '#00B4D8', '#0096C7', '#0077B6'],
            text='Count'
        )
        
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            height=350,
            xaxis_title="",
            yaxis_title="",
            coloraxis_showscale=False,
            plot_bgcolor='rgba(240,240,240,0.1)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tumor Size Reduction Analysis
    st.markdown("<div class='subheader'>Tumor Size Reduction Analysis</div>", unsafe_allow_html=True)
    # Get all patients with multiple visits
    patients = data_processor.df['patient_id'].unique()
    selected_patient = st.selectbox("Select Patient", patients, key="patient_id")
    patients = patients[patients == selected_patient]
    # Prepare data for visualization
    tumor_data = []
    
    for patient_id in patients:
        patient_visits = data_processor.get_patient_data(patient_id)
        
        if len(patient_visits) > 1:  # Only include patients with multiple visits
            for _, visit in patient_visits.iterrows():
                tumor_data.append({
                    'patient_id': visit['patient_id'],
                    'visit_number': visit['visit_number'],
                    'tumor_size_cm': visit['tumor_size_cm']
                })
    
    tumor_df = pd.DataFrame(tumor_data)
    
    # Create line chart for tumor size reduction
    fig = px.line(
        tumor_df, 
        x='visit_number', 
        y='tumor_size_cm',
        color='patient_id',
        markers=True,
        title='Tumor Size Reduction Over Visits',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig.update_layout(
        xaxis_title="Visit Number",
        yaxis_title="Tumor Size (cm)",
        legend_title="Patient ID",
        height=500,
        plot_bgcolor='rgba(240,240,240,0.1)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
