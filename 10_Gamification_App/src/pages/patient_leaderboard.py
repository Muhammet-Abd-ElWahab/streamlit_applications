import streamlit as st
import pandas as pd
import plotly.express as px

def patient_leaderboard_page(data_processor, patient_id):
    """Patient Leaderboard Page"""
    st.markdown("<h1 class='main-header'>Leaderboard</h1>", unsafe_allow_html=True)
    
    # Create filters
    col1, col2 = st.columns(2)
    
    with col1:
        # Get unique treatment types
        all_patients = data_processor.get_all_patients()
        treatment_types = ['All'] + sorted(all_patients['treatment_type'].unique().tolist())
        selected_treatment = st.selectbox("Filter by Treatment Type", treatment_types)
    
    with col2:
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
    
    # Reset index to create rank column
    filtered_leaderboard = filtered_leaderboard.reset_index(drop=True)
    filtered_leaderboard.index = filtered_leaderboard.index + 1  # Start rank from 1
    
    # Display leaderboard
    st.markdown("<div class='subheader'>Patient Rankings</div>", unsafe_allow_html=True)
    
    # Format the dataframe for display
    display_df = filtered_leaderboard.copy()
    
    # Anonymize patient names except for the current patient
    display_df['name'] = display_df.apply(
        lambda row: row['name'] if row['patient_id'] == patient_id else f"Patient {row['patient_id']}", 
        axis=1
    )
    
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
    
    # Check if the patient is in the filtered leaderboard
    patient_in_leaderboard = len(display_df[display_df['Patient ID'] == patient_id]) > 0
    
    if not patient_in_leaderboard:
        st.warning(f"You are not visible in the current filtered leaderboard. Try changing the filter settings.")
        
        # Display the table without highlighting
        st.dataframe(display_df, use_container_width=True, height=400)
    else:
        # Find the current patient's row
        patient_row = display_df[display_df['Patient ID'] == patient_id].index[0]
        
        # Highlight the current patient and top performers
        def highlight_rows(row):
            if row.name == patient_row:
                return ['background-color: #0077B6'] * len(row)
            elif 'Rank' in row and row['Rank'] <= 3:
                return ['background-color: #90E0EF'] * len(row)
            return [''] * len(row)
        
        # Apply styling
        styled_df = display_df.style.apply(highlight_rows, axis=0)
        
        # Display the table
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        # Get current patient's rank
        patient_rank = display_df[display_df['Patient ID'] == patient_id]['Rank'].values[0]
        total_patients = len(display_df)
        
        # Display patient's rank
        st.markdown(f"##### Your current rank: {patient_rank} out of {total_patients} patients")
        
        # Calculate how many points needed to reach next rank
        if patient_rank > 1:
            next_rank_points = display_df[display_df['Rank'] == patient_rank - 1]['Total Points'].values[0]
            patient_points = display_df[display_df['Patient ID'] == patient_id]['Total Points'].values[0]
            points_needed = next_rank_points - patient_points
            
            st.info(f"🏋️ You need {points_needed} more points to move up to rank {patient_rank - 1}!")
        else:
            st.success("🏆 Congratulations! You're at the top of the leaderboard!")
    
    # Create visualizations
    st.markdown("<div class='subheader'>Leaderboard Visualizations</div>", unsafe_allow_html=True)
    
    # Create a copy of display_df for visualization
    viz_df = display_df.copy()
    
    # Mark the current patient for visualization
    viz_df['Is You'] = viz_df['Patient ID'] == patient_id
    
    # Top 10 patients by total points (or all if less than 10)
    top_count = min(10, len(viz_df))
    top_points = viz_df.sort_values('Total Points', ascending=False).head(top_count)
    
    if top_count > 0:
        fig = px.bar(
            top_points,
            x='Total Points',
            y='Patient ID',
            color='Is You',
            color_discrete_map={True: '#0077B6', False: '#90E0EF'},
            orientation='h',
            title='Top Patients by Total Points',
            labels={'Is You': ''}
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Total Points",
            yaxis_title="Patient ID",
            yaxis=dict(autorange="reversed"),  # Reverse y-axis to show rank 1 at the top
            plot_bgcolor='rgba(240,240,240,0.1)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Level distribution
    st.markdown("##### Level Distribution")
    
    if len(viz_df) > 0:
        level_counts = viz_df['Level'].value_counts().sort_index().reset_index()
        level_counts.columns = ['Level', 'Count']
        
        # Get the current patient's level if patient is in the leaderboard
        if patient_in_leaderboard:
            patient_level = viz_df[viz_df['Patient ID'] == patient_id]['Level'].values[0]
            # Add a column to highlight the patient's level
            level_counts['Is Your Level'] = level_counts['Level'] == patient_level
        else:
            # If patient is not in the filtered view, don't highlight any level
            level_counts['Is Your Level'] = False
        
        fig = px.bar(
            level_counts,
            x='Level',
            y='Count',
            color='Is Your Level',
            color_discrete_map={True: '#0077B6', False: '#90E0EF'},
            title='Level Distribution',
            labels={'Is Your Level': ''}
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Level",
            yaxis_title="Number of Patients",
            plot_bgcolor='rgba(240,240,240,0.1)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Add motivational message
    st.markdown("##### Keep Going!")
    st.markdown("""
    Remember, the leaderboard is updated after each visit. Here are some ways to improve your ranking:
    - Take your medication consistently
    - Attend all scheduled appointments
    - Follow your treatment plan
    - Complete health challenges to earn badges
    - Track your symptoms and side effects
    
    Every small step counts towards your health journey! 💪
    """)
