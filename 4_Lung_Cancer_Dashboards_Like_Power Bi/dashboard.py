import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys
import warnings

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Add the current directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our custom chart library
from new_charts import (
    BarChart, PieChart, ScatterPlot, LinePlot, HistogramPlot, 
    BoxPlot, ViolinPlot, HeatmapPlot, AreaPlot, BubblePlot, RaincloudPlot
)

# Import data generator
from lung_cancer_data_generator import generate_lung_cancer_trial_data

# Function to create a semicircle progress chart
def create_semicircle_progress(value, max_value=100, title="", color="#20B2AA"):
    # Calculate the percentage
    percentage = (value / max_value) * 100
    
    # Create the figure
    fig = go.Figure()
    
    # Add the gauge/semicircle
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24, 'color': color}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': color},
            'bar': {'color': color},
            'bgcolor': 'white',
            'borderwidth': 2,
            'bordercolor': color,
            'steps': [
                {'range': [0, 100], 'color': 'rgba(240, 240, 240, 0.5)'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 100}
        },
        number={'suffix': "%", 'font': {'size': 30}}
    ))
    
    # Update the layout to make it a semicircle
    fig.update_layout(
        height=300,
        margin=dict(t=40, b=0, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': color, 'family': "Arial"},
    )
    
    # Remove the polar axis settings that were causing the error
    # The indicator gauge already creates a semicircle by default
    
    return fig

# Function to display styled warning/error messages
def show_message(message, message_type="info"):
    if message_type == "warning":
        st.markdown(f"""
        <div class="warning-message">
            <div class="warning-title">⚠️ Warning</div>
            <div>{message}</div>
        </div>
        """, unsafe_allow_html=True)
    elif message_type == "error":
        st.markdown(f"""
        <div class="error-message">
            <div class="error-title">❌ Error</div>
            <div>{message}</div>
        </div>
        """, unsafe_allow_html=True)
    elif message_type == "success":
        st.markdown(f"""
        <div class="success-message">
            <div class="success-title">✅ Success</div>
            <div>{message}</div>
        </div>
        """, unsafe_allow_html=True)
    else:  # info
        st.info(message)

# Progress semicircle charts for individual patients
def create_patient_progress_charts(patient_id):
    # Check if patient exists and has data for multiple visits
    patient_data = df[df['PatientID'] == patient_id]
    
    if len(patient_data) < 2:
        show_message(f"Patient {patient_id} doesn't have data for multiple visits.", "warning")
        return
    
    # Get baseline data
    baseline_data = patient_data[patient_data['Visit'] == 'Baseline']
    
    if len(baseline_data) == 0:
        show_message(f"Patient {patient_id} doesn't have baseline data.", "warning")
        return
    
    # Get the latest non-baseline visit
    non_baseline_visits = patient_data[patient_data['Visit'] != 'Baseline']
    
    if len(non_baseline_visits) == 0:
        show_message(f"Patient {patient_id} only has baseline data.", "warning")
        return
    
    latest_visit = non_baseline_visits.sort_values('VisitNumber').iloc[-1]
    visit_name = latest_visit['Visit']
    
    # Get baseline values
    baseline_tumor = baseline_data['TumorSize'].values[0]
    baseline_lung = baseline_data['LungFunction'].values[0]
    baseline_qol = baseline_data['QualityOfLife'].values[0]
    
    # Get current values
    current_tumor = latest_visit['TumorSize']
    current_lung = latest_visit['LungFunction']
    current_qol = latest_visit['QualityOfLife']
    
    # Calculate changes
    tumor_reduction = max(0, (baseline_tumor - current_tumor) / baseline_tumor * 100)
    lung_improvement = max(0, (current_lung - baseline_lung) / baseline_lung * 100)
    qol_improvement = max(0, (current_qol - baseline_qol) / baseline_qol * 100)
    
    # Create columns for the charts
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"<div class='section-header'>Tumor Reduction</div>", unsafe_allow_html=True)
        fig = create_semicircle_progress(
            value=tumor_reduction,
            max_value=100,
            title=f"{visit_name} vs Baseline",
            color="#3F7CAC"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"<div class='section-header'>Lung Function Improvement</div>", unsafe_allow_html=True)
        fig = create_semicircle_progress(
            value=lung_improvement,
            max_value=50,
            title=f"{visit_name} vs Baseline",
            color="#5B9BD5"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.markdown(f"<div class='section-header'>Quality of Life Improvement</div>", unsafe_allow_html=True)
        fig = create_semicircle_progress(
            value=qol_improvement,
            max_value=50,
            title=f"{visit_name} vs Baseline",
            color="#81C784"
        )
        st.plotly_chart(fig, use_container_width=True)

# Set page config
st.set_page_config(
    page_title="Lung Cancer Clinical Trial Dashboard",
    page_icon="ud83eudec1",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Try to import AgGrid, install if not available
try:
    from streamlit_aggrid import AgGrid, GridOptionsBuilder, JsCode
except ImportError:
    st.warning("Installing streamlit-aggrid package...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit-aggrid"])
    from streamlit_aggrid import AgGrid, GridOptionsBuilder, JsCode

# Custom CSS for Power BI-like styling
st.markdown("""
<style>
    /* Main theme colors - simplified color palette */
    :root {
        --main-color: #3F7CAC; /* Soft Blue - main color */
        --secondary-color: #5B9BD5; /* Lighter Blue - secondary color */
        --text-color: #444444; /* Soft Dark Gray - text */
        --accent-color: #6CA6C1; /* Muted Teal-Blue - accent */
        --card-bg-color: rgba(255, 255, 255, 0.92);
        --warning-color: #E9B872; /* Soft Gold - warning */
        --error-color: #E57373; /* Soft Red - error */
        --success-color: #81C784; /* Soft Green - success */
    }
    
    /* Metric card styling */
    .metric-card {
        background-color: var(--card-bg-color);
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(200, 210, 220, 0.3);
        height: 100%;
    }
    
    /* Dashboard title */
    .dashboard-title {
        color: var(--main-color);
        font-size: 2.2rem;
        font-weight: 600;
        text-align: center;
        padding: 0.8rem 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(63, 124, 172, 0.3);
    }
    
    /* Section headers */
    .section-header {
        color: var(--secondary-color);
        font-size: 1.4rem;
        font-weight: 500;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        padding: 0.8rem;
        border-radius: 8px;
        text-align: center;
        background-color: var(--card-bg-color);
        border: 1px solid rgba(200, 210, 220, 0.3);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
    }
    
   
    
    /* Metric value */
    .metric-value {
        color: var(--main-color);
        font-size: 1.8rem;
        font-weight: 600;
    }
    
    /* Metric label */
    .metric-label {
        color: var(--text-color);
        font-size: 0.95rem;
        font-weight: 400;
    }
    
    /* Warning message styling */
    .warning-message {
        background-color: rgba(233, 184, 114, 0.1);
        border-left: 4px solid var(--warning-color);
        padding: 0.8rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .warning-title {
        color: var(--warning-color);
        font-weight: 500;
        margin-bottom: 0.4rem;
    }
    
    /* Error message styling */
    .error-message {
        background-color: rgba(229, 115, 115, 0.1);
        border-left: 4px solid var(--error-color);
        padding: 0.8rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .error-title {
        color: var(--error-color);
        font-weight: 500;
        margin-bottom: 0.4rem;
    }
    
    /* Success message styling */
    .success-message {
        background-color: rgba(129, 199, 132, 0.1);
        border-left: 4px solid var(--success-color);
        padding: 0.8rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .success-title {
        color: var(--success-color);
        font-weight: 500;
        margin-bottom: 0.4rem;
    }
    
    /* Filter panel */
    .filter-container {
        background-color: var(--card-bg-color);
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(200, 210, 220, 0.3);
    }
    
    /* Custom button */
    .stButton>button {
        background-color: var(--main-color);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.4rem 0.8rem;
        font-weight: 500;
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
    
    /* Progress semicircle styling */
    .progress-semicircle {
        margin: 0 auto;
        text-align: center;
    }
</style>

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
# Dashboard title at the top
st.markdown('<div class="dashboard-title">Lung Cancer Clinical Trial Dashboard</div>', unsafe_allow_html=True)

# Key metrics row - always visible at the top
st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)

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


# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Treatment Outcomes", "Patient Demographics", "Correlation Matrics", "Relationship Analysis","Treatment Progress", "Patient Data"])

# Tab 1: Treatment Outcomes
with tab2:
    st.markdown('<div class="section-header">Treatment Outcomes Over Time</div>', unsafe_allow_html=True)
    
    # Add aggregation method selection
    aggregation_method = st.radio(
        "Select Aggregation Method",
        ("Mean", "Median"),
        horizontal=True
    )
    
    # Line charts for key metrics over time
    line_metrics = ['TumorSize', 'LungFunction', 'QualityOfLife', 'PainScore']
    metric_titles = ['Tumor Size (mm)', 'Lung Function (%)', 'Quality of Life Score', 'Pain Score']
    
    # Create aggregated dataframe based on selected method
    if aggregation_method == "Mean":
        agg_func = 'mean'
    else:
        agg_func = 'median'
    
    # Group by Visit and TreatmentGroup and calculate the aggregation
    agg_df = filtered_df.groupby(['Visit', 'TreatmentGroup'])[line_metrics].agg(agg_func).reset_index()
    
    for i, (metric, title) in enumerate(zip(line_metrics, metric_titles)):
        if i % 2 == 0:  # Start a new row for every 2 charts
            cols = st.columns(2)
        
        with cols[i % 2]:
            line = LinePlot(
                df=agg_df,
                x='Visit',
                y=metric,
                color='TreatmentGroup',
                title=f'{title} Over Time ({aggregation_method})',
                height=400,
                width=600,
                x_title='Visit',
                y_title=title,
                legend_title='Treatment Group',
                color_sequence=['#008080', '#5B9BD5'],  # Teal for Treatment, Light Blue for Placebo
                markers=True
            )
            line.create().display(use_streamlit=True)
    
    # Distribution Analysis
    st.markdown('<div class="section-header">Distribution Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Box plot for tumor size by treatment group
        box = BoxPlot(
            df=filtered_df,
            x='TreatmentGroup',
            y='TumorSize',
            color='TreatmentGroup',
            title='Tumor Size Distribution by Treatment Group',
            height=500,
            width=600,
            x_title='Treatment Group',
            y_title='Tumor Size (mm)',
            legend_title='Treatment Group',
            color_sequence=['#008080', '#5B9BD5'],  # Teal for Treatment, Light Blue for Placebo
        )
        box.create().display(use_streamlit=True)
    
    with col2:
        # Violin plot for lung function by treatment group
        violin = ViolinPlot(
            df=filtered_df,
            x='TreatmentGroup',
            y='LungFunction',
            color='TreatmentGroup',
            title='Lung Function Distribution by Treatment Group',
            height=500,
            width=600,
            x_title='Treatment Group',
            y_title='Lung Function (%)',
            legend_title='Treatment Group',
            color_sequence=['#008080', '#5B9BD5'],  # Teal for Treatment, Light Blue for Placebo
        )
        violin.create().display(use_streamlit=True)
    
    # Individual Patient Trajectories
    st.markdown('<div class="section-header">Individual Patient Trajectories</div>', unsafe_allow_html=True)
    
    # Allow selecting multiple patients
    selected_patients = st.multiselect(
        'Select Patients to View',
        options=filtered_df['PatientID'].unique(),
        default=filtered_df['PatientID'].unique()[:5]  # Default to first 5 patients
    )
    
    if not selected_patients:
        show_message("Please select at least one patient to view trajectories.", "warning")
    else:
        # Filter data for selected patients
        patient_data = filtered_df[filtered_df['PatientID'].isin(selected_patients)]
        
        # Line chart for tumor size trajectory
        line = LinePlot(
            df=patient_data,
            x='Visit',
            y='TumorSize',
            color='PatientID',
            title='Tumor Size Trajectory for Selected Patients',
            height=500,
            width=800,
            x_title='Visit',
            y_title='Tumor Size (mm)',
            legend_title='Patient ID',
            markers=True
        )
        line.create().display(use_streamlit=True)

# Tab 2: Patient Demographics
with tab1:
    st.markdown('<div class="section-header">Patient Demographics</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age distribution
        hist = HistogramPlot(
            df=filtered_df,
            x='Age',
            color='TreatmentGroup',
            title='Age Distribution',
            height=400,
            width=600,
            x_title='Age',
            y_title='Count',
            legend_title='Treatment Group',
            color_sequence=['#008080', '#5B9BD5'],  # Teal for Treatment, Light Blue for Placebo
            nbins=20
        )
        hist.create().display(use_streamlit=True)
    
    with col2:
        # Gender distribution
        gender_df = filtered_df.groupby(['Gender', 'TreatmentGroup']).size().reset_index(name='Count')
        bar = BarChart(
            df=gender_df,
            x='Gender',
            y='Count',
            color='TreatmentGroup',
            title='Gender Distribution',
            height=400,
            width=600,
            x_title='Gender',
            y_title='Count',
            legend_title='Treatment Group',
            color_sequence=['#008080', '#5B9BD5'],  # Teal for Treatment, Light Blue for Placebo
            text='Count',
            text_location='outside',
            text_percentage=False 
        )
        bar.create().display(use_streamlit=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cancer stage distribution
        stage_df = filtered_df.groupby(['CancerStage', 'TreatmentGroup']).size().reset_index(name='Count')
        bar = BarChart(
            df=stage_df,
            x='CancerStage',
            y='Count',
            color='TreatmentGroup',
            title='Cancer Stage Distribution',
            height=400,
            width=600,
            x_title='Cancer Stage',
            y_title='Count',
            legend_title='Treatment Group',
            color_sequence=['#008080', '#5B9BD5'],  # Teal for Treatment, Light Blue for Placebo
            text='Count',
            text_location='outside',
            text_percentage=False 
        )
        bar.create().display(use_streamlit=True)
    
    with col2:
        # Smoking status distribution
        smoking_df = filtered_df.groupby(['SmokingStatus', 'TreatmentGroup']).size().reset_index(name='Count')
        bar = BarChart(
            df=smoking_df,
            x='SmokingStatus',
            y='Count',
            color='TreatmentGroup',
            title='Smoking Status Distribution',
            height=400,
            width=600,
            x_title='Smoking Status',
            y_title='Count',
            legend_title='Treatment Group',
            color_sequence=['#008080', '#5B9BD5'],  # Teal for Treatment, Light Blue for Placebo
            text='Count',
            text_location='outside',
            text_percentage=False 
        )
        bar.create().display(use_streamlit=True)

# Tab 3: Advanced Analysis
with tab3:
    st.markdown('<div class="section-header">Correlation Matrics</div>', unsafe_allow_html=True)
    
    # Correlation heatmap
    numeric_cols = ['Age', 'PackYears', 'ECOGStatus', 'TumorSize', 'LungFunction', 'QualityOfLife', 'PainScore', 'Biomarker']
    corr_df = filtered_df[numeric_cols].corr()
    
    # Create a heatmap using Plotly directly instead of the HeatmapPlot class
    fig = px.imshow(
        corr_df,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        labels=dict(x="Variable", y="Variable", color="Correlation"),
        title="Correlation Matrix"
    )
    
    fig.update_layout(
        height=700,
        width=700,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    
    st.plotly_chart(fig)

# Tab 4: Relationship Analysis
with tab4:
    st.markdown('<div class="section-header">Explore Relationships Between Variables</div>', unsafe_allow_html=True)
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
    
    # Check if the same variable is selected for both axes
    if x_var == y_var:
        show_message(
            "You've selected the same variable for both axes. Please select different variables for a meaningful comparison.", 
            "warning"
        )
    else:
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
            color_sequence=['#008080', '#5B9BD5'],  # Teal for Treatment, Light Blue for Placebo
            trendline='ols'  # Add trend line
        )
        scatter.create().display(use_streamlit=True)
        
        # Add correlation information
        if not filtered_df.empty:
            correlation = filtered_df[[x_var, y_var]].corr().iloc[0, 1]
            
            # Determine correlation strength and message type
            abs_corr = abs(correlation)
            if abs_corr > 0.7:
                strength = "strong"
                msg_type = "success"
            elif abs_corr > 0.3:
                strength = "moderate"
                msg_type = "info"
            else:
                strength = "weak"
                msg_type = "warning"
                
            direction = "positive" if correlation > 0 else "negative"
            
            show_message(
                f"The correlation between {x_var} and {y_var} is {correlation:.2f}, indicating a {strength} {direction} relationship.",
                msg_type
            )

with tab5:

    # Progress semicircle charts
    st.markdown('### Treatment Progress')
    col1, col2, col3 = st.columns(3)

    with col1:
        # Tumor reduction progress
        if selected_visit != 'All' and selected_visit != 'Baseline':
            # Calculate average tumor size reduction percentage
            baseline_data = df[df['Visit'] == 'Baseline']
            current_data = df[df['Visit'] == selected_visit]
            
            # Match patients in both datasets
            common_patients = set(baseline_data['PatientID']).intersection(set(current_data['PatientID']))
            
            if common_patients:
                # Filter to common patients
                baseline_filtered = baseline_data[baseline_data['PatientID'].isin(common_patients)]
                current_filtered = current_data[current_data['PatientID'].isin(common_patients)]
                
                # Calculate average sizes
                avg_baseline_size = baseline_filtered['TumorSize'].mean()
                avg_current_size = current_filtered['TumorSize'].mean()
                
                # Calculate reduction percentage (positive means reduction)
                reduction_pct = max(0, (avg_baseline_size - avg_current_size) / avg_baseline_size * 100)
                
                # Create progress chart
                fig = create_semicircle_progress(
                    value=reduction_pct, 
                    max_value=100, 
                    title="Tumor Reduction", 
                    color="#3F7CAC"  # Updated to match main-color
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                show_message("No matching patient data available for tumor reduction calculation.", "warning")
        else:
            show_message("Select a specific visit (not Baseline) to view tumor reduction progress.", "info")

    with col2:
        # Lung function improvement progress
        if selected_visit != 'All' and selected_visit != 'Baseline':
            # Calculate average lung function improvement
            baseline_data = df[df['Visit'] == 'Baseline']
            current_data = df[df['Visit'] == selected_visit]
            
            # Match patients in both datasets
            common_patients = set(baseline_data['PatientID']).intersection(set(current_data['PatientID']))
            
            if common_patients:
                # Filter to common patients
                baseline_filtered = baseline_data[baseline_data['PatientID'].isin(common_patients)]
                current_filtered = current_data[current_data['PatientID'].isin(common_patients)]
                
                # Calculate average lung function
                avg_baseline_lung = baseline_filtered['LungFunction'].mean()
                avg_current_lung = current_filtered['LungFunction'].mean()
                
                # Calculate improvement percentage (positive means improvement)
                improvement_pct = max(0, (avg_current_lung - avg_baseline_lung) / avg_baseline_lung * 100)
                
                # Create progress chart
                fig = create_semicircle_progress(
                    value=improvement_pct, 
                    max_value=50,  # Lung function typically doesn't improve by more than 50%
                    title="Lung Function Improvement", 
                    color="#5B9BD5"  # Updated to match secondary-color
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                show_message("No matching patient data available for lung function calculation.", "warning")
        else:
            show_message("Select a specific visit (not Baseline) to view lung function improvement.", "info")

    with col3:
        # Quality of life improvement progress
        if selected_visit != 'All' and selected_visit != 'Baseline':
            # Calculate average QoL improvement
            baseline_data = df[df['Visit'] == 'Baseline']
            current_data = df[df['Visit'] == selected_visit]
            
            # Match patients in both datasets
            common_patients = set(baseline_data['PatientID']).intersection(set(current_data['PatientID']))
            
            if common_patients:
                # Filter to common patients
                baseline_filtered = baseline_data[baseline_data['PatientID'].isin(common_patients)]
                current_filtered = current_data[current_data['PatientID'].isin(common_patients)]
                
                # Calculate average QoL
                avg_baseline_qol = baseline_filtered['QualityOfLife'].mean()
                avg_current_qol = current_filtered['QualityOfLife'].mean()
                
                # Calculate improvement percentage (positive means improvement)
                improvement_pct = max(0, (avg_current_qol - avg_baseline_qol) / avg_baseline_qol * 100)
                
                # Create progress chart
                fig = create_semicircle_progress(
                    value=improvement_pct, 
                    max_value=50,  # QoL typically doesn't improve by more than 50%
                    title="Quality of Life Improvement", 
                    color="#81C784"  # Updated to match success-color
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                show_message("No matching patient data available for quality of life calculation.", "warning")
        else:
            show_message("Select a specific visit (not Baseline) to view quality of life improvement.", "info")

# Tab 6: Patient Data
with tab6:
    
    # Individual patient progress charts
    st.markdown('<div class="section-header">Individual Patient Progress</div>', unsafe_allow_html=True)
    patient_id = st.selectbox('Select a Patient ID', filtered_df['PatientID'].unique())
    create_patient_progress_charts(patient_id)

    st.markdown('<div class="section-header">Patient Data</div>', unsafe_allow_html=True)
    
    # Display the filtered data using AgGrid
    try:
        from streamlit_aggrid import AgGrid, GridOptionsBuilder
        from streamlit_aggrid.shared import JsCode
        
        # Configure the grid options
        gb = GridOptionsBuilder.from_dataframe(filtered_df)
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
        gb.configure_selection('multiple', use_checkbox=True)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
        gb.configure_grid_options(enablePagination=True, sideBar=True)
        
        # Center-align all columns
        for col in filtered_df.columns:
            gb.configure_column(col, cellStyle={'textAlign': 'center'})
        
        grid_options = gb.build()
        
        # Display the grid
        grid_response = AgGrid(
            filtered_df,
            gridOptions=grid_options,
            data_return_mode='AS_INPUT', 
            update_mode='MODEL_CHANGED', 
            fit_columns_on_grid_load=False,
            theme='ag-theme-balham',
            enable_enterprise_modules=True,
            allow_unsafe_jscode=True,
            custom_css={
                ".ag-header-cell-label": {
                    "justify-content": "center"
                }
            }
        )
    except ImportError:
        st.warning("The streamlit-aggrid package is not installed. Installing it now...")
        # Attempt to install the package
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit-aggrid"])
            st.success("Installation successful! Please refresh the page.")
        except subprocess.CalledProcessError:
            st.error("Failed to install streamlit-aggrid. Please install it manually using 'pip install streamlit-aggrid'.")
            
        # Display a regular table as fallback
        st.dataframe(filtered_df)
        
# Footer
st.markdown("""
<div style="text-align: center; margin-top: 40px; padding: 20px; color: gray; font-size: 0.8em;">
    Lung Cancer Clinical Trial Dashboard | Created with Streamlit and Plotly | Data is synthetic for demonstration purposes
</div>
""", unsafe_allow_html=True)
