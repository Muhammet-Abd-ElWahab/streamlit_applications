import streamlit as st
import pandas as pd
import sweetviz as sv
import os
import tempfile
import warnings
from io import BytesIO

# Suppress warnings
warnings.filterwarnings('ignore')
import numpy as np
if not hasattr(np, 'VisibleDeprecationWarning'):
    np.VisibleDeprecationWarning = DeprecationWarning

# Page configuration
st.set_page_config(
    page_title="DataClin Data Profiler",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS
st.markdown("""
<style>
    .main {
        background-color: #F5F5F5;
    }
    
    .main-header {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.8rem 2rem;
        border-radius: 10px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
    }
    
    .stDownloadButton > button {
        background-color: #1976D2;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.7rem 1.5rem;
    }
    
    .stDownloadButton > button:hover {
        background-color: #1565C0;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #1976D2;
        font-weight: 700;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #424242;
        font-weight: 600;
    }
    
    .footer-text {
        text-align: center;
        padding: 1.5rem;
        color: #00897B;
        margin-top: 2rem;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def detect_file_type(filename):
    """Auto-detect file type from filename"""
    ext = filename.lower().split('.')[-1]
    if ext == 'csv':
        return "CSV"
    elif ext in ['xlsx', 'xls']:
        return "Excel"
    elif ext == 'sas7bdat':
        return "SAS"
    return None

def load_excel_sheets(uploaded_file):
    """Load sheet names from Excel file"""
    try:
        bytes_data = BytesIO(uploaded_file.getvalue())
        file_ext = uploaded_file.name.lower().split('.')[-1]
        
        if file_ext == 'xls':
            xl_file = pd.ExcelFile(bytes_data, engine='xlrd')
        else:
            xl_file = pd.ExcelFile(bytes_data, engine='openpyxl')
        
        sheet_names = xl_file.sheet_names
        xl_file.close()
        return sheet_names
    except Exception as e:
        st.error(f"❌ Error reading Excel file: {str(e)}")
        return []

def load_data(uploaded_file, file_type, sheet_name=None):
    """Load data from uploaded file"""
    try:
        if file_type == "CSV":
            df = pd.read_csv(uploaded_file, encoding='utf-8', encoding_errors='ignore')
        elif file_type == "Excel":
            file_ext = uploaded_file.name.lower().split('.')[-1]
            
            if file_ext == 'xls':
                if sheet_name:
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name, engine='xlrd')
                else:
                    df = pd.read_excel(uploaded_file, engine='xlrd')
            else:
                if sheet_name:
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name, engine='openpyxl')
                else:
                    df = pd.read_excel(uploaded_file, engine='openpyxl')
        elif file_type == "SAS":
            with tempfile.NamedTemporaryFile(delete=False, suffix='.sas7bdat') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            df = pd.read_sas(tmp_path, encoding='utf-8')
            os.unlink(tmp_path)
        else:
            raise ValueError("Unsupported file format")
        
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

def generate_report(df):
    """Generate data profile report"""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            report = sv.analyze(df)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            report.show_html(filepath=tmp_path, open_browser=False, layout='widescreen')
        except (TypeError, AttributeError):
            try:
                report.show_html(tmp_path, open_browser=False)
            except AttributeError:
                with open(tmp_path, 'w', encoding='utf-8') as f:
                    f.write(str(report))
        
        with open(tmp_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        os.unlink(tmp_path)
        return html_content
    except Exception as e:
        st.error(f"❌ Error generating report: {str(e)}")
        return None

def main():
    # Logo in sidebar
    with st.sidebar:
        logo_path = os.path.join(os.path.dirname(__file__), "Logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, use_column_width=True)
        st.markdown("---")
        st.markdown("### About")
        st.markdown("Professional data profiling and analysis tool")
        st.markdown("---")
        st.markdown("### Supported Formats")
        st.markdown("- CSV (.csv)")
        st.markdown("- Excel (.xlsx, .xls)")
        st.markdown("- SAS (.sas7bdat)")
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>Dataset Profile Report</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader (auto-detect type) - NO EMPTY CONTAINERS
    uploaded_file = st.file_uploader(
        "📤 Upload Your Data File (CSV, Excel, or SAS)",
        type=["csv", "xlsx", "xls", "sas7bdat"],
        help="Upload your data file for analysis"
    )
    
    if uploaded_file is not None:
        # Auto-detect file type
        file_type = detect_file_type(uploaded_file.name)
        
        if file_type:
            st.success(f"✅ File uploaded: **{uploaded_file.name}** (Type: {file_type})")
            
            # Excel sheet selection - NO EMPTY CONTAINER
            selected_sheet = None
            if file_type == "Excel":
                st.markdown("#### 📑 Excel Sheet Selection")
                sheets = load_excel_sheets(uploaded_file)
                if sheets:
                    selected_sheet = st.selectbox(
                        "Select the sheet to analyze:",
                        sheets,
                        help="Choose which sheet to analyze"
                    )
            
            # Load data
            with st.spinner("📥 Loading data..."):
                df = load_data(uploaded_file, file_type, selected_sheet)
            
            if df is not None:
                # Convert dtypes to string to fix Arrow serialization issue
                df_display = df.copy()
                
                # Dataset Overview as Metrics
                st.markdown("---")
                st.markdown("### 📊 Dataset Overview")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Rows", f"{len(df):,}")
                
                with col2:
                    st.metric("Total Columns", f"{len(df.columns):,}")
                
                with col3:
                    memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
                    st.metric("Memory Usage", f"{memory_mb:.2f} MB")
                
                with col4:
                    missing_count = df.isnull().sum().sum()
                    st.metric("Missing Values", f"{missing_count:,}")
                
                # Data preview
                st.markdown("---")
                st.markdown("### 👀 Data Preview")
                st.dataframe(df_display.head(10), use_container_width=True)
                
                # Column information - Fix Arrow serialization
                with st.expander("📋 Column Information"):
                    col_info = pd.DataFrame({
                        'Column': df.columns.astype(str),
                        'Type': df.dtypes.astype(str).values,
                        'Non-Null': df.count().values,
                        'Null': df.isnull().sum().values,
                        'Unique': [df[col].nunique() for col in df.columns]
                    })
                    st.dataframe(col_info, use_container_width=True)
                
                # Generate report button
                st.markdown("---")
                if st.button("🚀 Generate Data Profile Report", use_container_width=True):
                    with st.spinner("⚙️ Generating comprehensive report..."):
                        html_content = generate_report(df)
                    
                    if html_content:
                        st.success("✅ Report Generated Successfully!")
                        
                        # Display report
                        st.markdown("---")
                        st.markdown("### 📊 Interactive Report")
                        st.components.v1.html(html_content, height=800, scrolling=True)
                        
                        # Download button
                        st.markdown("---")
                        st.download_button(
                            label="📥 Download Report",
                            data=html_content,
                            file_name="data_profile_report.html",
                            mime="text/html"
                        )
        else:
            st.error("❌ Unsupported file type")
    
    # Footer - Single line
    st.markdown("---")
    st.markdown("""
    <div class="footer-text">
        🔬 Powered by DataClin | 🚀 Built by Data Science Team
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
