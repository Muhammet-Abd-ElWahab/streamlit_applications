import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys

# Add the current directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our custom chart library
from new_charts import (
    BarChart, PieChart, ScatterPlot, LinePlot, HistogramPlot, 
    BoxPlot, ViolinPlot, HeatmapPlot, AreaPlot, BubblePlot, RaincloudPlot
)

# Import data generator
from lung_cancer_data_generator import generate_lung_cancer_trial_data

# Set page config
st.set_page_config(
    page_title="Lung Cancer Clinical Trial Dashboard",
    page_icon="ud83eudec1",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Try to import AgGrid, install if not available
try:
    from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
except ImportError:
    st.warning("Installing streamlit-aggrid package...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit-aggrid"])
    from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

# Custom CSS for Power BI-like styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --main-color: #008080; /* Teal */
        --secondary-color: #4682B4; /* Light Blue */
        --background-color: #F5F5F5; /* Light Gray */
        --text-color: #333333; /* Dark Gray */
        --accent-color: #20B2AA; /* Light Sea Green */
        --card-bg-color: rgba(255, 255, 255, 0.9);
        --section-bg-color: rgba(245, 245, 245, 0.7);
    }
    
    /* Dark mode adjustments */
    @media (prefers-color-scheme: dark) {
        :root {
            --main-color: #20B2AA; /* Lighter Teal for dark mode */
            --secondary-color: #87CEEB; /* Lighter Blue for dark mode */
            --background-color: #2F2F2F; /* Darker Gray */
            --text-color: #E0E0E0; /* Light Gray for better contrast */
            --accent-color: #48D1CC; /* Medium Turquoise */
            --card-bg-color: rgba(60, 60, 60, 0.7);
            --section-bg-color: rgba(50, 50, 50, 0.5);
        }
        .metric-card {
            background-color: rgba(60, 60, 60, 0.7) !important;
            border: 1px solid rgba(100, 100, 100, 0.5) !important;
        }
        .metric-label {
            color: #E0E0E0 !important;
        }
        .section-header {
            color: var(--secondary-color) !important;
        }
    }
    
    /* Dashboard title */
    .dashboard-title {
        color: var(--main-color);
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--main-color);
    }
    
    /* Section headers */
    .section-header {
        color: var(--secondary-color);
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        background-color: var(--card-bg-color);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Section container */
    .section-container {
        border: 1px solid rgba(200, 200, 200, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        background-color: var(--section-bg-color);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Card styling */
    .metric-card {
        background-color: var(--card-bg-color);
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(200, 200, 200, 0.3);
        height: 100%;
    }
    
    /* Metric value */
    .metric-value {
        color: var(--main-color);
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Metric label */
    .metric-label {
        color: var(--text-color);
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Filter panel */
    .filter-container {
        background-color: var(--card-bg-color);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(200, 200, 200, 0.3);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: var(--background-color);
    }
    
    /* Custom button */
    .stButton>button {
        background-color: var(--main-color);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        background-color: var(--accent-color);
    }
    
    /* Make charts background transparent */
    .js-plotly-plot .plotly .main-svg {
        background-color: transparent !important;
    }
    
    .js-plotly-plot .plotly .bg {
        fill: transparent !important;
    }
    
    /* Analysis options box */
    .analysis-options {
        background-color: var(--card-bg-color);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(200, 200, 200, 0.3);
    }
</style>

<div class="dashboard-title">Lung Cancer Clinical Trial Dashboard</div>
""", unsafe_allow_html=True)

# Function to load or generate data
@st.cache_data
def load_data():
    # Check if data file exists
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lung_cancer_trial_data.csv')
    
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
    else:
        # Generate data
        df = generate_lung_cancer_trial_data()
        # Save data
        df.to_csv(data_path, index=False)
    
    # Convert date columns
    df['VisitDate'] = pd.to_datetime(df['VisitDate'])
    
    return df

# Load data
df = load_data()

# Sidebar for filters
st.sidebar.markdown('<div class="section-header">Filters</div>', unsafe_allow_html=True)

# Treatment group filter
treatment_options = ['All'] + sorted(df['TreatmentGroup'].unique().tolist())
selected_treatment = st.sidebar.selectbox('Treatment Group', treatment_options)

# Visit filter
visit_options = ['All'] + sorted(df['Visit'].unique().tolist())
selected_visit = st.sidebar.selectbox('Visit', visit_options)

# Cancer stage filter
stage_options = ['All'] + sorted(df['CancerStage'].unique().tolist())
selected_stage = st.sidebar.selectbox('Cancer Stage', stage_options)

# Age range filter
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider('Age Range', min_age, max_age, (min_age, max_age))

# Gender filter
gender_options = ['All'] + sorted(df['Gender'].unique().tolist())
selected_gender = st.sidebar.selectbox('Gender', gender_options)

# Smoking status filter
smoking_options = ['All'] + sorted(df['SmokingStatus'].unique().tolist())
selected_smoking = st.sidebar.selectbox('Smoking Status', smoking_options)

# Apply filters
filtered_df = df.copy()

if selected_treatment != 'All':
    filtered_df = filtered_df[filtered_df['TreatmentGroup'] == selected_treatment]
    
if selected_visit != 'All':
    filtered_df = filtered_df[filtered_df['Visit'] == selected_visit]
    
if selected_stage != 'All':
    filtered_df = filtered_df[filtered_df['CancerStage'] == selected_stage]
    
filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1])]

if selected_gender != 'All':
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
if selected_smoking != 'All':
    filtered_df = filtered_df[filtered_df['SmokingStatus'] == selected_smoking]

# Main dashboard content
# Top metrics row
st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
st.markdown('<div class="section-container">', unsafe_allow_html=True)

# Get metrics for the selected visit or the latest visit if 'All' is selected
metrics_df = filtered_df.copy()
if selected_visit == 'All':
    # Get the latest visit for each patient
    latest_visits = metrics_df.sort_values('VisitNumber').groupby('PatientID').last().reset_index()
    metrics_df = latest_visits

# Calculate key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Number of patients
    num_patients = len(metrics_df['PatientID'].unique())
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{num_patients}</div>
        <div class="metric-label">Patients</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Average tumor size
    avg_tumor_size = metrics_df['TumorSize'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_tumor_size:.1f} mm</div>
        <div class="metric-label">Avg. Tumor Size</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # Average lung function
    avg_lung_function = metrics_df['LungFunction'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_lung_function:.1f}%</div>
        <div class="metric-label">Avg. Lung Function</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    # Response rate (if not baseline)
    if 'Response' in metrics_df.columns and 'Not Applicable' not in metrics_df['Response'].unique():
        response_rate = (metrics_df['Response'] == 'Responder').mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{response_rate:.1f}%</div>
            <div class="metric-label">Response Rate</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">N/A</div>
            <div class="metric-label">Response Rate</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Main charts section with analysis options
st.markdown('<div class="section-header">Treatment Outcomes</div>', unsafe_allow_html=True)
st.markdown('<div class="section-container">', unsafe_allow_html=True)

# Analysis options moved from sidebar to main content
st.markdown('<div class="analysis-options">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    analysis_metric = st.selectbox(
        'Primary Analysis Metric', 
        ['TumorSize', 'TumorSizePercentChange', 'LungFunction', 'QualityOfLife', 'PainScore', 'Biomarker']
    )
with col2:
    show_individual_patients = st.checkbox('Show Individual Patient Data', value=False)
st.markdown('</div>', unsafe_allow_html=True)

# Prepare data for treatment comparison
if selected_visit == 'All':
    # For comparing across visits, we need data from all visits
    comparison_df = filtered_df
    
    # Create a chart showing the trend of the selected metric across visits
    visit_trend_df = comparison_df.groupby(['Visit', 'TreatmentGroup'])[analysis_metric].mean().reset_index()
    
    # Line chart for metric over time by treatment group
    line_chart = LinePlot(
        df=visit_trend_df,
        x='Visit',
        y=analysis_metric,
        color='TreatmentGroup',
        title=f'{analysis_metric} by Visit and Treatment Group',
        height=400,
        width=800,
        x_title='Visit',
        y_title=analysis_metric,
        legend_title='Treatment Group',
        color_sequence=['#20B2AA', '#4682B4'],  # Teal and Light Blue
        markers=True
    )
    line_chart.create().display(use_streamlit=True)
    
    # Box plots to show distribution
    st.markdown('<div class="section-header">Distribution Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    
    box_chart = BoxPlot(
        df=comparison_df,
        x='Visit',
        y=analysis_metric,
        color='TreatmentGroup',
        title=f'Distribution of {analysis_metric} by Visit and Treatment Group',
        height=500,
        width=800,
        x_title='Visit',
        y_title=analysis_metric,
        legend_title='Treatment Group',
        color_sequence=['#20B2AA', '#4682B4'],  # Teal and Light Blue
        points='outliers'
    )
    box_chart.create().display(use_streamlit=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # If showing individual patients is enabled
    if show_individual_patients:
        st.markdown('<div class="section-header">Individual Patient Trajectories</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        
        # Select a sample of patients for visualization (too many makes the chart unreadable)
        sample_size = min(20, len(filtered_df['PatientID'].unique()))
        sample_patients = np.random.choice(filtered_df['PatientID'].unique(), sample_size, replace=False)
        sample_df = filtered_df[filtered_df['PatientID'].isin(sample_patients)]
        
        # Line chart for individual patients
        patient_line_chart = LinePlot(
            df=sample_df,
            x='Visit',
            y=analysis_metric,
            color='PatientID',
            line_dash='TreatmentGroup',  # Differentiate treatment groups by line style
            title=f'Individual Patient {analysis_metric} Trajectories',
            height=600,
            width=800,
            x_title='Visit',
            y_title=analysis_metric,
            legend_title='Patient ID',
            markers=True
        )
        patient_line_chart.create().display(use_streamlit=True)
        
        st.markdown(f"*Note: Showing a random sample of {sample_size} patients. Solid lines are Treatment group, dashed lines are Placebo group.*")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # For a specific visit, show comparison between treatment groups
    comparison_df = filtered_df
    
    # Bar chart comparing treatment groups
    treatment_comparison = comparison_df.groupby('TreatmentGroup')[analysis_metric].mean().reset_index()
    
    bar_chart = BarChart(
        df=treatment_comparison,
        x='TreatmentGroup',
        y=analysis_metric,
        title=f'{analysis_metric} by Treatment Group at {selected_visit}',
        height=400,
        width=800,
        x_title='Treatment Group',
        y_title=analysis_metric,
        color_sequence=['#20B2AA', '#4682B4'],  # Teal and Light Blue
        text=analysis_metric,
        text_location='outside',
        text_percentage=False  # Use raw values instead of percentages
    )
    bar_chart.create().display(use_streamlit=True)
    
    # Show distribution with violin plots
    st.markdown('<div class="section-header">Distribution Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    
    violin_chart = ViolinPlot(
        df=comparison_df,
        x='TreatmentGroup',
        y=analysis_metric,
        title=f'Distribution of {analysis_metric} by Treatment Group at {selected_visit}',
        height=500,
        width=800,
        x_title='Treatment Group',
        y_title=analysis_metric,
        color='TreatmentGroup',
        color_sequence=['#20B2AA', '#4682B4'],  # Teal and Light Blue
        box=True,
        points='all'
    )
    violin_chart.create().display(use_streamlit=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # If it's not baseline, show response rate
    if selected_visit != 'Baseline' and 'Response' in comparison_df.columns:
        st.markdown('<div class="section-header">Response Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        
        # Calculate response rates by treatment group
        response_df = comparison_df.groupby(['TreatmentGroup', 'Response']).size().reset_index(name='Count')
        
        # Create a pie chart for each treatment group
        col1, col2 = st.columns(2)
        
        with col1:
            # Placebo group
            placebo_df = response_df[response_df['TreatmentGroup'] == 'Placebo']
            if not placebo_df.empty:
                pie_placebo = PieChart(
                    df=placebo_df,
                    values='Count',
                    names='Response',
                    title='Response Rate - Placebo Group',
                    height=400,
                    width=400,
                    color_sequence=['#FF6B6B', '#4ECDC4'],  # Red for Non-Responder, Teal for Responder
                    hole=0.4  # Donut chart
                )
                pie_placebo.create().display(use_streamlit=True)
        
        with col2:
            # Treatment group
            treatment_df = response_df[response_df['TreatmentGroup'] == 'Treatment']
            if not treatment_df.empty:
                pie_treatment = PieChart(
                    df=treatment_df,
                    values='Count',
                    names='Response',
                    title='Response Rate - Treatment Group',
                    height=400,
                    width=400,
                    color_sequence=['#FF6B6B', '#4ECDC4'],  # Red for Non-Responder, Teal for Responder
                    hole=0.4  # Donut chart
                )
                pie_treatment.create().display(use_streamlit=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close the Treatment Outcomes section container

# Patient Demographics Section
st.markdown('<div class="section-header">Patient Demographics</div>', unsafe_allow_html=True)
st.markdown('<div class="section-container">', unsafe_allow_html=True)

# Get unique patients from filtered data
unique_patients = filtered_df.drop_duplicates('PatientID')

col1, col2 = st.columns(2)

with col1:
    # Age distribution
    age_hist = HistogramPlot(
        df=unique_patients,
        x='Age',
        color='TreatmentGroup',
        title='Age Distribution',
        height=400,
        width=400,
        x_title='Age',
        y_title='Count',
        legend_title='Treatment Group',
        color_sequence=['#20B2AA', '#4682B4'],  # Teal and Light Blue
        nbins=10
    )
    age_hist.create().display(use_streamlit=True)

with col2:
    # Gender distribution
    gender_df = unique_patients.groupby(['Gender', 'TreatmentGroup']).size().reset_index(name='Count')
    
    gender_bar = BarChart(
        df=gender_df,
        x='Gender',
        y='Count',
        color='TreatmentGroup',
        title='Gender Distribution',
        height=400,
        width=400,
        x_title='Gender',
        y_title='Count',
        legend_title='Treatment Group',
        color_sequence=['#20B2AA', '#4682B4'],  # Teal and Light Blue
        text='Count',
        text_location='outside',
        text_percentage=False  # Use raw values instead of percentages
    )
    gender_bar.create().display(use_streamlit=True)

col1, col2 = st.columns(2)

with col1:
    # Smoking status
    smoking_df = unique_patients.groupby(['SmokingStatus', 'TreatmentGroup']).size().reset_index(name='Count')
    
    smoking_bar = BarChart(
        df=smoking_df,
        x='SmokingStatus',
        y='Count',
        color='TreatmentGroup',
        title='Smoking Status Distribution',
        height=400,
        width=400,
        x_title='Smoking Status',
        y_title='Count',
        legend_title='Treatment Group',
        color_sequence=['#20B2AA', '#4682B4'],  # Teal and Light Blue
        text='Count',
        text_location='outside',
        text_percentage=False  # Use raw values instead of percentages
    )
    smoking_bar.create().display(use_streamlit=True)

with col2:
    # Cancer stage
    stage_df = unique_patients.groupby(['CancerStage', 'TreatmentGroup']).size().reset_index(name='Count')
    
    stage_bar = BarChart(
        df=stage_df,
        x='CancerStage',
        y='Count',
        color='TreatmentGroup',
        title='Cancer Stage Distribution',
        height=400,
        width=400,
        x_title='Cancer Stage',
        y_title='Count',
        legend_title='Treatment Group',
        color_sequence=['#20B2AA', '#4682B4'],  # Teal and Light Blue
        text='Count',
        text_location='outside',
        text_percentage=False  # Use raw values instead of percentages
    )
    stage_bar.create().display(use_streamlit=True)

st.markdown('</div>', unsafe_allow_html=True)

# Advanced Analysis Section
st.markdown('<div class="section-header">Advanced Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-container">', unsafe_allow_html=True)

# Correlation heatmap
if selected_visit != 'All':
    # Select numerical columns for correlation
    num_cols = ['Age', 'PackYears', 'ECOGStatus', 'TumorSize', 'LungFunction', 
                'QualityOfLife', 'PainScore', 'Biomarker']
    
    # Calculate correlation matrix
    corr_df = filtered_df[num_cols].corr().reset_index()
    corr_df = pd.melt(corr_df, id_vars='index', value_vars=num_cols)
    corr_df.columns = ['Variable1', 'Variable2', 'Correlation']
    
    # Create heatmap
    heatmap = HeatmapPlot(
        df=corr_df,
        x='Variable1',
        y='Variable2',
        z='Correlation',
        title='Correlation Matrix of Key Metrics',
        height=600,
        width=800,
        color_continuous_scale='Teal',
        text_auto=True
    )
    heatmap.create().display(use_streamlit=True)

st.markdown('</div>', unsafe_allow_html=True)

# Scatter plot to explore relationships
st.markdown('<div class="section-header">Relationship Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-container">', unsafe_allow_html=True)

# Let user select variables to compare
col1, col2 = st.columns(2)

with col1:
    x_var = st.selectbox(
        'X-axis Variable', 
        ['Age', 'PackYears', 'ECOGStatus', 'TumorSize', 'LungFunction', 'QualityOfLife', 'PainScore', 'Biomarker'],
        index=3  # Default to TumorSize
    )

with col2:
    y_var = st.selectbox(
        'Y-axis Variable', 
        ['Age', 'PackYears', 'ECOGStatus', 'TumorSize', 'LungFunction', 'QualityOfLife', 'PainScore', 'Biomarker'],
        index=4  # Default to LungFunction
    )

# Create scatter plot
scatter = ScatterPlot(
    df=filtered_df,
    x=x_var,
    y=y_var,
    color='TreatmentGroup',
    size='ECOGStatus',  # Size points by ECOG status
    title=f'Relationship between {x_var} and {y_var}',
    height=600,
    width=800,
    x_title=x_var,
    y_title=y_var,
    legend_title='Treatment Group',
    color_sequence=['#20B2AA', '#4682B4'],  # Teal and Light Blue
    trendline='ols'  # Add trend line
)
scatter.create().display(use_streamlit=True)

st.markdown('</div>', unsafe_allow_html=True)

# Patient Data Table (expandable) using AgGrid
st.markdown('<div class="section-header">Patient Data</div>', unsafe_allow_html=True)

show_data = st.expander("Click to view patient data table")
with show_data:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    # Format the data for display
    display_df = filtered_df.copy()
    
    # Round numerical columns
    numeric_cols = ['Age', 'PackYears', 'ECOGStatus', 'TumorSize', 'LungFunction', 
                   'QualityOfLife', 'PainScore', 'Biomarker']
    
    for col in numeric_cols:
        if col in display_df.columns:
            display_df[col] = display_df[col].round(1)
    
    # Format date
    if 'VisitDate' in display_df.columns:
        display_df['VisitDate'] = display_df['VisitDate'].dt.strftime('%Y-%m-%d')
    
    # Configure AgGrid
    gb = GridOptionsBuilder.from_dataframe(display_df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
    gb.configure_default_column(min_column_width=100, resizable=True, sortable=True, filterable=True)
    
    # Center align all columns
    cell_style_jscode = JsCode("""
    function(params) {
        return {
            'textAlign': 'center'
        };
    }
    """)
    
    # Apply center alignment to all columns
    for col in display_df.columns:
        gb.configure_column(col, cellStyle=cell_style_jscode, headerClass="ag-header-cell-center")
    
    grid_options = gb.build()
    
    # Add custom CSS for header centering
    st.markdown("""
    <style>
    .ag-header-cell-center { text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the grid
    AgGrid(
        display_df,
        gridOptions=grid_options,
        theme='streamlit',
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        height=400
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 40px; padding: 20px; color: gray; font-size: 0.8em;">
    Lung Cancer Clinical Trial Dashboard | Created with Streamlit and Plotly | Data is synthetic for demonstration purposes
</div>
""", unsafe_allow_html=True)
