import streamlit as st
import pandas as pd
import plotly.express as px

def admin_leaderboard_page(data_processor):
    """Admin Leaderboard Page"""
    st.markdown("<h1 class='main-header'>Patient Leaderboard</h1>", unsafe_allow_html=True)
    
    # Create filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Get unique treatment types
        all_patients = data_processor.get_all_patients()
        treatment_types = ['All'] + sorted(all_patients['treatment_type'].unique().tolist())
        selected_treatment = st.selectbox("Filter by Treatment Type", treatment_types)
    
    with col2:
        # Age group filter
        age_groups = ['All', '<30', '30-45', '46-60', '61-75', '75+']
        selected_age_group = st.selectbox("Filter by Age Group", age_groups)
    
    with col3:
        # Sorting options
        sort_options = {
            'Ranking Percentile': 'ranking_percentile',
            'Total Points': 'total_points',
            'Health Score': 'health_score',
            'Commitment Score': 'commitment_score',
            'Level': 'level'
        }
        selected_sort = st.selectbox("Sort by", list(sort_options.keys()))
        sort_column = sort_options[selected_sort]
    
    # Get leaderboard data
    leaderboard = data_processor.get_leaderboard(sort_by=sort_column, ascending=False)
    
    # Apply filters
    filtered_leaderboard = leaderboard.copy()
    
    if selected_treatment != 'All':
        # Get patient IDs with the selected treatment type
        treatment_patients = all_patients[all_patients['treatment_type'] == selected_treatment]['patient_id'].tolist()
        filtered_leaderboard = filtered_leaderboard[filtered_leaderboard['patient_id'].isin(treatment_patients)]
    
    if selected_age_group != 'All':
        # Get patient IDs in the selected age group
        if selected_age_group == '<30':
            age_patients = all_patients[all_patients['age'] < 30]['patient_id'].tolist()
        elif selected_age_group == '30-45':
            age_patients = all_patients[(all_patients['age'] >= 30) & (all_patients['age'] <= 45)]['patient_id'].tolist()
        elif selected_age_group == '46-60':
            age_patients = all_patients[(all_patients['age'] >= 46) & (all_patients['age'] <= 60)]['patient_id'].tolist()
        elif selected_age_group == '61-75':
            age_patients = all_patients[(all_patients['age'] >= 61) & (all_patients['age'] <= 75)]['patient_id'].tolist()
        elif selected_age_group == '75+':
            age_patients = all_patients[all_patients['age'] > 75]['patient_id'].tolist()
        
        filtered_leaderboard = filtered_leaderboard[filtered_leaderboard['patient_id'].isin(age_patients)]
    
    # Reset index to create rank column
    filtered_leaderboard = filtered_leaderboard.reset_index(drop=True)
    filtered_leaderboard.index = filtered_leaderboard.index + 1  # Start rank from 1
    
    # Display leaderboard
    st.markdown("<div class='subheader'>Patient Rankings</div>", unsafe_allow_html=True)
    
    # Format the dataframe for display
    display_df = filtered_leaderboard.copy()
    display_df = display_df.rename(columns={
        'patient_id': 'Patient ID',
        'name': 'Name',
        'level': 'Level',
        'total_points': 'Total Points',
        'health_score': 'Health Score',
        'commitment_score': 'Commitment Score',
        'badges_count': 'Badges',
        'ranking_percentile': 'Percentile'
    })
    
    # Add rank column
    display_df = display_df.reset_index().rename(columns={'index': 'Rank'})
    
    # Highlight top performers
    def highlight_top_three(row):
        if row['Rank'] <= 3:
            return ['background-color: rgba(144, 224, 239, 0.2)'] * len(row)
        return [''] * len(row)
    
    # Apply styling
    styled_df = display_df.style.apply(highlight_top_three, axis=1)
    
    # Display the table
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Create visualizations
    st.markdown("<div class='subheader'>Leaderboard Visualizations</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 patients by total points
        top_points = display_df.sort_values('Total Points', ascending=False).head(10)
        
        fig = px.bar(
            top_points,
            x='Total Points',
            y='Patient ID',
            color='Total Points',
            color_continuous_scale=['#CAF0F8', '#90E0EF', '#48CAE4', '#00B4D8', '#0096C7', '#0077B6'],
            orientation='h',
            title='Top 10 Patients by Total Points'
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Total Points",
            yaxis_title="",
            coloraxis_showscale=False,
            plot_bgcolor='rgba(240,240,240,0.1)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top 10 patients by health score
        top_health = display_df.sort_values('Health Score', ascending=False).head(10)
        
        fig = px.bar(
            top_health,
            x='Health Score',
            y='Patient ID',
            color='Health Score',
            color_continuous_scale=['#CAF0F8', '#90E0EF', '#48CAE4', '#00B4D8', '#0096C7', '#0077B6'],
            orientation='h',
            title='Top 10 Patients by Health Score'
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Health Score",
            yaxis_title="",
            coloraxis_showscale=False,
            plot_bgcolor='rgba(240,240,240,0.1)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Level distribution
    st.markdown("##### Level Distribution in Current Leaderboard")
    
    level_counts = display_df['Level'].value_counts().sort_index().reset_index()
    level_counts.columns = ['Level', 'Count']
    
    fig = px.pie(
        level_counts,
        values='Count',
        names='Level',
        hole=0.4,
        color_discrete_sequence=['#CAF0F8', '#90E0EF', '#48CAE4', '#00B4D8', '#0096C7', '#0077B6']
    )
    
    fig.update_layout(
        height=400,
        margin=dict(t=0, b=0, l=0, r=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
