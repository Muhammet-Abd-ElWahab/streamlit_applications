"""
Data Cleaning and Exploration Application
A comprehensive Streamlit app for data upload, cleaning, and exploration
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime
import openpyxl
import pyreadstat
import plotly.express as px
import plotly.graph_objects as go
from utalities import view_dataframe


# ==================== Configuration ====================
st.set_page_config(
    page_title="Data Cleaning & Exploration Tool",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== Custom Functions ====================
def get_color_palette(palette_name, n_colors=10):
    """
    Get color palette based on name
    
    Parameters:
    -----------
    palette_name : str
        Name of the palette (Teal, Blues, Grays, etc.)
    n_colors : int
        Number of colors needed
        
    Returns:
    --------
    list : List of color hex codes
    """
    palettes = {
        'Teal': ['#008080', '#2F4F4F', '#696969', '#A9A9A9', '#20B2AA', 
                 '#5F9EA0', '#48D1CC', '#00CED1', '#40E0D0', '#AFEEEE'],
        'Blues': ['#000080', '#00008B', '#0000CD', '#0000FF', '#1E90FF',
                  '#4169E1', '#6495ED', '#87CEEB', '#87CEFA', '#B0E0E6'],
        'Grays': ['#2F4F4F', '#696969', '#778899', '#808080', '#A9A9A9',
                  '#C0C0C0', '#D3D3D3', '#DCDCDC', '#E8E8E8', '#F5F5F5'],
        'Greens': ['#006400', '#228B22', '#32CD32', '#3CB371', '#90EE90',
                   '#98FB98', '#8FBC8F', '#9ACD32', '#ADFF2F', '#7FFF00'],
        'Purples': ['#4B0082', '#483D8B', '#6A5ACD', '#7B68EE', '#9370DB',
                    '#8B008B', '#9932CC', '#BA55D3', '#DA70D6', '#DDA0DD'],
        'Reds': ['#8B0000', '#B22222', '#DC143C', '#FF0000', '#FF6347',
                 '#FF7F50', '#CD5C5C', '#F08080', '#FA8072', '#FFA07A'],
        'Oranges': ['#FF8C00', '#FFA500', '#FFB347', '#FFCC99', '#FFD700',
                    '#FFDAB9', '#FFE4B5', '#FFEFD5', '#FFF8DC', '#FFFACD']
    }
    
    if palette_name in palettes:
        colors = palettes[palette_name]
        # Repeat colors if needed
        if n_colors > len(colors):
            colors = colors * (n_colors // len(colors) + 1)
        return colors[:n_colors]
    else:
        return px.colors.qualitative.Plotly[:n_colors]


def show_df_info(df, title="DataFrame"):
    """
    Display DataFrame metrics and information
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to display
    title : str
        Title for the DataFrame display
    """
    if df is None or df.empty:
        st.warning("⚠️ No data to display")
        return
    
    st.subheader(f"📊 {title}")
    
    # Display shape
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", f"{df.shape[0]:,}")
    with col2:
        st.metric("Total Columns", f"{df.shape[1]:,}")
    with col3:
        st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Display column data types
    with st.expander("📋 Column Data Types", expanded=False):
        dtype_df = pd.DataFrame({
            'Column': df.columns,
            'Data Type': df.dtypes.values,
            'Non-Null Count': df.count().values,
            'Null Count': df.isnull().sum().values
        })
        st.dataframe(dtype_df, use_container_width=True)


def detect_delimiter_and_encoding(file_content, filename):
    """
    Auto-detect delimiter and encoding for CSV/TSV files
    
    Parameters:
    -----------
    file_content : bytes
        File content
    filename : str
        Name of the file
        
    Returns:
    --------
    tuple : (delimiter, encoding)
    """
    # Try different encodings
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252', 'iso-8859-1']
    detected_encoding = 'utf-8'
    
    for encoding in encodings:
        try:
            file_content.decode(encoding)
            detected_encoding = encoding
            break
        except:
            continue
    
    # Detect delimiter
    if filename.lower().endswith('.tsv'):
        return '\t', detected_encoding
    
    # Try to detect delimiter from first line
    try:
        first_line = file_content.decode(detected_encoding, errors='ignore').split('\n')[0]
        delimiters = [',', ';', '\t', '|']
        delimiter_counts = {d: first_line.count(d) for d in delimiters}
        detected_delimiter = max(delimiter_counts, key=delimiter_counts.get)
        return detected_delimiter, detected_encoding
    except:
        return ',', detected_encoding


def load_file(uploaded_file, delimiter=',', encoding='utf-8', sheet_name=0):
    """
    Load file into pandas DataFrame with auto-detection
    
    Parameters:
    -----------
    uploaded_file : UploadedFile
        Streamlit uploaded file object
    delimiter : str
        Delimiter for CSV/TSV files
    encoding : str
        Encoding for CSV/TSV files
    sheet_name : str or int
        Sheet name or index for Excel files
        
    Returns:
    --------
    pd.DataFrame : Loaded DataFrame
    """
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension in ['csv', 'tsv', 'txt']:
            # Try with detected encoding first, then fallback
            try:
                df = pd.read_csv(uploaded_file, delimiter=delimiter, encoding=encoding)
            except:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, delimiter=delimiter, encoding='latin1')
        
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name, engine='openpyxl')
        
        elif file_extension == 'sas7bdat':
            # Save uploaded file temporarily
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.sas7bdat') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            df, meta = pyreadstat.read_sas7bdat(tmp_path)
            
            # Clean up temp file
            import os
            os.unlink(tmp_path)
        
        else:
            st.error(f"❌ Unsupported file format: .{file_extension}")
            return None
        
        return df
    
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        return None


def get_excel_sheet_names(uploaded_file):
    """
    Get all sheet names from an Excel file
    
    Parameters:
    -----------
    uploaded_file : UploadedFile
        Streamlit uploaded file object
        
    Returns:
    --------
    list : List of sheet names
    """
    try:
        excel_file = pd.ExcelFile(uploaded_file, engine='openpyxl')
        return excel_file.sheet_names
    except Exception as e:
        st.error(f"❌ Error reading Excel file: {str(e)}")
        return []


# ==================== File Upload Section ====================
def file_upload_section():
    """Handle file uploads with automatic loading"""
    st.header("📁 File Upload")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'tsv', 'txt', 'xlsx', 'xls', 'sas7bdat'],
        help="Supported formats: CSV, TSV, Excel, SAS"
    )
    
    if uploaded_file is not None:
        # Check if this is a new file
        if 'last_uploaded_file' not in st.session_state or st.session_state['last_uploaded_file'] != uploaded_file.name:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            # Handle CSV/TSV files - Auto load
            if file_extension in ['csv', 'tsv', 'txt']:
                with st.spinner(f"Loading {uploaded_file.name}..."):
                    # Auto-detect delimiter and encoding
                    file_content = uploaded_file.getvalue()
                    delimiter, encoding = detect_delimiter_and_encoding(file_content, uploaded_file.name)
                    
                    # Reset file pointer and load
                    uploaded_file.seek(0)
                    df = load_file(uploaded_file, delimiter=delimiter, encoding=encoding)
                    
                    if df is not None:
                        st.session_state['df'] = df
                        st.session_state['original_df'] = df.copy()
                        st.session_state['file_name'] = uploaded_file.name
                        st.session_state['last_uploaded_file'] = uploaded_file.name
                        st.success(f"✅ Successfully loaded {uploaded_file.name} (Delimiter: {repr(delimiter)}, Encoding: {encoding})")
                        st.rerun()
            
            # Handle Excel files - Auto load first sheet
            elif file_extension in ['xlsx', 'xls']:
                with st.spinner(f"Loading {uploaded_file.name}..."):
                    sheet_names = get_excel_sheet_names(uploaded_file)
                    
                    if sheet_names:
                        # Auto-load first sheet
                        uploaded_file.seek(0)
                        df = load_file(uploaded_file, sheet_name=sheet_names[0])
                        
                        if df is not None:
                            st.session_state['df'] = df
                            st.session_state['original_df'] = df.copy()
                            st.session_state['file_name'] = f"{uploaded_file.name} - {sheet_names[0]}"
                            st.session_state['last_uploaded_file'] = uploaded_file.name
                            st.session_state['excel_sheets'] = sheet_names
                            st.success(f"✅ Successfully loaded sheet '{sheet_names[0]}' from {uploaded_file.name}")
                            
                            # Show sheet selector if multiple sheets
                            if len(sheet_names) > 1:
                                st.info(f"📋 This file has {len(sheet_names)} sheets. First sheet loaded automatically.")
                            st.rerun()
            
            # Handle SAS files - Auto load
            elif file_extension == 'sas7bdat':
                with st.spinner(f"Loading {uploaded_file.name}..."):
                    uploaded_file.seek(0)
                    df = load_file(uploaded_file)
                    
                    if df is not None:
                        st.session_state['df'] = df
                        st.session_state['original_df'] = df.copy()
                        st.session_state['file_name'] = uploaded_file.name
                        st.session_state['last_uploaded_file'] = uploaded_file.name
                        st.success(f"✅ Successfully loaded {uploaded_file.name}")
                        st.rerun()
        
        # Show sheet selector for Excel files if multiple sheets exist
        if 'excel_sheets' in st.session_state and len(st.session_state['excel_sheets']) > 1:
            st.subheader("📊 Excel Sheet Selector")
            current_sheet = st.session_state['file_name'].split(' - ')[-1] if ' - ' in st.session_state['file_name'] else st.session_state['excel_sheets'][0]
            
            selected_sheet = st.selectbox(
                "Switch to different sheet:",
                options=st.session_state['excel_sheets'],
                index=st.session_state['excel_sheets'].index(current_sheet) if current_sheet in st.session_state['excel_sheets'] else 0,
                key="sheet_selector"
            )
            
            if selected_sheet != current_sheet:
                if st.button("🔄 Load Selected Sheet", key="switch_sheet"):
                    uploaded_file.seek(0)
                    with st.spinner(f"Loading sheet '{selected_sheet}'..."):
                        df = load_file(uploaded_file, sheet_name=selected_sheet)
                        if df is not None:
                            st.session_state['df'] = df
                            st.session_state['original_df'] = df.copy()
                            st.session_state['file_name'] = f"{uploaded_file.name} - {selected_sheet}"
                            st.success(f"✅ Switched to sheet '{selected_sheet}'")
                            st.rerun()


# ==================== View Data Tab ====================
def view_data_tab():
    """Display uploaded data"""
    if 'df' not in st.session_state or st.session_state['df'] is None:
        st.info("👆 Please upload a file to get started")
        return
    
    df = st.session_state['df']
    
    st.header("📊 Data Overview")
    
    # Display DataFrame info
    show_df_info(df, title=f"Current Dataset: {st.session_state.get('file_name', 'Unknown')}")
    
    # Display DataFrame using view_dataframe
    st.subheader("📋 Data Table")
    view_dataframe(df, height=500, page_size=20, key_suffix="view_data")


# ==================== Basic Statistics Tab ====================
def basic_statistics_tab():
    """Display basic statistics for the dataset"""
    if 'df' not in st.session_state or st.session_state['df'] is None:
        st.info("👆 Please upload a file to get started")
        return
    
    df = st.session_state['df']
    
    st.header("📈 Basic Statistics")
    
    tab1, tab2, tab3 = st.tabs(["Numerical Statistics", "Categorical Statistics", "DataFrame Info"])
    
    with tab1:
        # Numerical columns statistics
        numeric_cols = df.select_dtypes(include=['number'])
        if numeric_cols.shape[1] > 0:
            st.write("**Descriptive Statistics for Numerical Columns:**")
            numeric_stats = df.describe().T
            numeric_stats = numeric_stats.reset_index()
            numeric_stats.columns = ['Column'] + list(numeric_stats.columns[1:])
            view_dataframe(numeric_stats, height=400, page_size=20, key_suffix="numeric_stats")
        else:
            st.info("No numerical columns found in the dataset")
    
    with tab2:
        # Categorical columns statistics
        categorical_cols = df.select_dtypes(include=['object', 'category'])
        if categorical_cols.shape[1] > 0:
            st.write("**Descriptive Statistics for Categorical Columns:**")
            cat_stats = df.describe(include=['object', 'category']).T
            cat_stats = cat_stats.reset_index()
            cat_stats.columns = ['Column'] + list(cat_stats.columns[1:])
            view_dataframe(cat_stats, height=400, page_size=20, key_suffix="cat_stats")
        else:
            st.info("No categorical columns found in the dataset")
    
    with tab3:
        # DataFrame info as table
        st.write("**DataFrame Information:**")
        
        # Create info DataFrame
        info_data = {
            'Column': df.columns,
            'Non-Null Count': df.count().values,
            'Null Count': df.isnull().sum().values,
            'Dtype': df.dtypes.values.astype(str),
            'Unique Values': [df[col].nunique() for col in df.columns],
            'Memory Usage (bytes)': [df[col].memory_usage(deep=True) for col in df.columns]
        }
        info_df = pd.DataFrame(info_data)
        
        # Add summary row
        st.write(f"**Total Entries:** {len(df):,}")
        st.write(f"**Total Columns:** {len(df.columns):,}")
        st.write(f"**Total Memory Usage:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        view_dataframe(info_df, height=400, page_size=20, key_suffix="df_info")


# ==================== Value Counts and Visualizations Tab ====================
def value_counts_visualizations_tab():
    """Display value counts and groupby analysis with plotly charts"""
    if 'df' not in st.session_state or st.session_state['df'] is None:
        st.info("👆 Please upload a file to get started")
        return
    
    df = st.session_state['df']
    
    st.header("🔢 Value Counts & GroupBy with Visualizations")
    
    # Analysis type selection
    analysis_type = st.radio(
        "Select Analysis Type:",
        options=["Value Counts", "GroupBy Aggregation"],
        horizontal=True
    )
    
    if analysis_type == "Value Counts":
        st.subheader("📊 Value Counts Analysis")
        
        # Column selection
        selected_column = st.selectbox(
            "Select a column to analyze",
            options=df.columns.tolist(),
            help="Choose a column to see the distribution of values",
            key="vc_column"
        )
        
        if selected_column:
            # Calculate value counts
            value_counts = df[selected_column].value_counts()
            total_count = len(df)
            
            # Create DataFrame with counts and percentages
            value_counts_df = pd.DataFrame({
                'Value': value_counts.index.astype(str),
                'Count': value_counts.values,
                'Percentage': (value_counts.values / total_count * 100).round(2)
            })
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Unique Values", len(value_counts))
            with col2:
                st.metric("Most Common Value", str(value_counts.index[0]))
            with col3:
                st.metric("Most Common Count", f"{value_counts.values[0]:,}")
            
            # Display value counts table
            st.write("**Value Distribution:**")
            view_dataframe(value_counts_df, height=400, page_size=20, key_suffix="value_counts")
            
            # Chart options
            st.subheader("📈 Visualization Options")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                chart_type = st.selectbox("Chart Type", ["Bar", "Pie"], key="vc_chart_type")
            with col2:
                color_palette = st.selectbox(
                    "Color Palette",
                    ["Teal", "Blues", "Grays", "Greens", "Purples", "Reds", "Oranges"],
                    key="vc_color_palette"
                )
            with col3:
                if chart_type == "Bar":
                    bar_mode = st.selectbox(
                        "Bar Mode",
                        ["group", "stack", "relative", "overlay"],
                        key="vc_bar_mode",
                        help="How to display bars when color is selected"
                    )
            
            # Chart configuration
            col1, col2, col3 = st.columns(3)
            with col1:
                x_col = st.selectbox("X Axis", value_counts_df.columns.tolist(), index=0, key="vc_x")
            with col2:
                y_col = st.selectbox("Y Axis", value_counts_df.columns.tolist(), index=1, key="vc_y")
            with col3:
                text_col = st.selectbox("Text", ["None"] + value_counts_df.columns.tolist(), key="vc_text")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                color_col = st.selectbox("Color", ["None"] + value_counts_df.columns.tolist(), key="vc_color_col")
            with col2:
                facet_col = st.selectbox("Facet Column", ["None"] + value_counts_df.columns.tolist(), key="vc_facet_col")
            with col3:
                facet_row = st.selectbox("Facet Row", ["None"] + value_counts_df.columns.tolist(), key="vc_facet_row")
            
            # Facet wrapping
            if facet_col != "None" or facet_row != "None":
                facet_wrap = st.slider("Facet Wrap", min_value=2, max_value=10, value=3, key="vc_facet_wrap")
            else:
                facet_wrap = None
            
            # Get color palette
            n_colors = len(value_counts_df) if color_col == "None" else value_counts_df[color_col].nunique()
            colors = get_color_palette(color_palette, n_colors)
            
            # Create chart
            if chart_type == "Bar":
                fig = px.bar(
                    value_counts_df,
                    x=x_col,
                    y=y_col,
                    text=text_col if text_col != "None" else None,
                    color=color_col if color_col != "None" else None,
                    facet_col=facet_col if facet_col != "None" else None,
                    facet_row=facet_row if facet_row != "None" else None,
                    facet_col_wrap=facet_wrap if facet_wrap else None,
                    color_discrete_sequence=colors,
                    hover_data={'Percentage': ':.2f'},
                    barmode=bar_mode if color_col != "None" else None
                )
            else:  # Pie chart
                fig = px.pie(
                    value_counts_df,
                    names=x_col,
                    values=y_col,
                    color_discrete_sequence=colors
                )
            
            fig.update_layout(
                height=600,
                template="plotly_white",
                font=dict(size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    else:  # GroupBy Aggregation
        st.subheader("🔄 GroupBy Aggregation")
        
        # GroupBy columns
        groupby_cols = st.multiselect(
            "Select column(s) to group by",
            options=df.columns.tolist(),
            help="Choose one or more columns to group by",
            key="gb_cols"
        )
        
        if groupby_cols:
            # Aggregation column
            agg_col = st.selectbox(
                "Select column to aggregate",
                options=df.select_dtypes(include=['number']).columns.tolist(),
                help="Choose a numerical column to aggregate",
                key="gb_agg_col"
            )
            
            # Aggregation type
            agg_type = st.selectbox(
                "Select aggregation type",
                options=["sum", "mean", "median", "count", "min", "max", "std"],
                key="gb_agg_type"
            )
            
            if agg_col:
                # Perform groupby
                grouped_df = df.groupby(groupby_cols)[agg_col].agg(agg_type).reset_index()
                grouped_df.columns = list(groupby_cols) + [f"{agg_type}_{agg_col}"]
                
                # Display grouped data
                st.write(f"**Grouped Data ({agg_type} of {agg_col}):**")
                view_dataframe(grouped_df, height=400, page_size=20, key_suffix="groupby")
                
                # Chart options
                st.subheader("📈 Visualization Options")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    chart_type = st.selectbox("Chart Type", ["Bar", "Pie"], key="gb_chart_type")
                with col2:
                    color_palette = st.selectbox(
                        "Color Palette",
                        ["Teal", "Blues", "Grays", "Greens", "Purples", "Reds", "Oranges"],
                        key="gb_color_palette"
                    )
                with col3:
                    if chart_type == "Bar":
                        bar_mode = st.selectbox(
                            "Bar Mode",
                            ["group", "stack", "relative", "overlay"],
                            key="gb_bar_mode",
                            help="How to display bars when color is selected"
                        )
                
                # Chart configuration
                col1, col2, col3 = st.columns(3)
                with col1:
                    x_col = st.selectbox("X Axis", grouped_df.columns.tolist(), index=0, key="gb_x")
                with col2:
                    y_col = st.selectbox("Y Axis", grouped_df.columns.tolist(), index=len(grouped_df.columns)-1, key="gb_y")
                with col3:
                    text_col = st.selectbox("Text", ["None"] + grouped_df.columns.tolist(), key="gb_text")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    color_col = st.selectbox("Color", ["None"] + grouped_df.columns.tolist(), key="gb_color_col")
                with col2:
                    facet_col = st.selectbox("Facet Column", ["None"] + grouped_df.columns.tolist(), key="gb_facet_col")
                with col3:
                    facet_row = st.selectbox("Facet Row", ["None"] + grouped_df.columns.tolist(), key="gb_facet_row")
                
                # Facet wrapping
                if facet_col != "None" or facet_row != "None":
                    facet_wrap = st.slider("Facet Wrap", min_value=2, max_value=10, value=3, key="gb_facet_wrap")
                else:
                    facet_wrap = None
                
                # Get color palette
                n_colors = len(grouped_df) if color_col == "None" else grouped_df[color_col].nunique()
                colors = get_color_palette(color_palette, n_colors)
                
                # Create chart
                if chart_type == "Bar":
                    fig = px.bar(
                        grouped_df,
                        x=x_col,
                        y=y_col,
                        text=text_col if text_col != "None" else None,
                        color=color_col if color_col != "None" else None,
                        facet_col=facet_col if facet_col != "None" else None,
                        facet_row=facet_row if facet_row != "None" else None,
                        facet_col_wrap=facet_wrap if facet_wrap else None,
                        color_discrete_sequence=colors,
                        barmode=bar_mode if color_col != "None" else None
                    )
                else:  # Pie chart
                    fig = px.pie(
                        grouped_df,
                        names=x_col,
                        values=y_col,
                        color_discrete_sequence=colors
                    )
                
                fig.update_layout(
                    height=600,
                    template="plotly_white",
                    font=dict(size=12)
                )
                
                st.plotly_chart(fig, use_container_width=True)


# ==================== Check Duplicates Tab ====================
def check_duplicates_tab():
    """Check and remove duplicate rows"""
    if 'df' not in st.session_state or st.session_state['df'] is None:
        st.info("👆 Please upload a file to get started")
        return
    
    df = st.session_state['df']
    
    st.header("🔍 Duplicate Detection")
    
    # Column selection for duplicate checking
    st.subheader("Select Columns for Duplicate Check")
    selected_columns = st.multiselect(
        "Choose columns (leave empty to check all columns)",
        options=df.columns.tolist(),
        help="Select specific columns to check for duplicates, or leave empty to check entire rows"
    )
    
    # Determine subset for duplicate checking
    subset = selected_columns if selected_columns else None
    
    # Find duplicates
    if subset:
        duplicates = df[df.duplicated(subset=subset, keep=False)]
        duplicate_count = df.duplicated(subset=subset).sum()
    else:
        duplicates = df[df.duplicated(keep=False)]
        duplicate_count = df.duplicated().sum()
    
    # Display metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Duplicate Rows",
            f"{duplicate_count:,}",
            delta=f"{(duplicate_count / len(df) * 100):.2f}%",
            delta_color="inverse"
        )
    with col2:
        st.metric(
            "Unique Rows",
            f"{len(df) - duplicate_count:,}",
            delta=f"{((len(df) - duplicate_count) / len(df) * 100):.2f}%"
        )
    
    # Display duplicate rows
    if duplicate_count > 0:
        st.subheader("🔎 Duplicate Rows Found")
        view_dataframe(duplicates, height=400, page_size=20, key_suffix="duplicates")
        
        # Remove duplicates button
        st.subheader("🗑️ Remove Duplicates")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🗑️ Remove Duplicates", type="primary"):
                if subset:
                    st.session_state['df'] = df.drop_duplicates(subset=subset)
                else:
                    st.session_state['df'] = df.drop_duplicates()
                
                st.success(f"✅ Removed {duplicate_count:,} duplicate rows!")
                st.rerun()
        
        with col2:
            st.info(f"This will remove {duplicate_count:,} duplicate rows from the dataset")
    else:
        st.success("✅ No duplicate rows found in the dataset!")


# ==================== Check Null Values Tab ====================
def check_null_values_tab():
    """Check and handle null values"""
    if 'df' not in st.session_state or st.session_state['df'] is None:
        st.info("👆 Please upload a file to get started")
        return
    
    df = st.session_state['df']
    
    st.header("🔍 Null Values Analysis")
    
    # Overall null statistics
    st.subheader("📊 Overall Null Statistics")
    
    total_nulls = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Null Values", f"{total_nulls:,}")
    with col2:
        st.metric("Percentage of Nulls", f"{(total_nulls / total_cells * 100):.2f}%")
    with col3:
        st.metric("Columns with Nulls", df.isnull().any().sum())
    
    # Null values by column
    null_df = pd.DataFrame({
        'Column': df.columns,
        'Null Count': df.isnull().sum().values,
        'Null Percentage (%)': (df.isnull().sum().values / len(df) * 100).round(2)
    })
    null_df = null_df[null_df['Null Count'] > 0].sort_values('Null Count', ascending=False)
    
    if len(null_df) > 0:
        st.subheader("📋 Null Values by Column")
        st.dataframe(null_df, use_container_width=True)
    
    # Column-specific null handling
    st.subheader("🛠️ Handle Null Values")
    
    selected_column = st.selectbox(
        "Select a column to handle nulls",
        options=df.columns.tolist(),
        help="Choose a column to view and handle null values"
    )
    
    if selected_column:
        null_count = df[selected_column].isnull().sum()
        null_percentage = (null_count / len(df) * 100)
        
        # Display metrics for selected column
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                f"Null Values in '{selected_column}'",
                f"{null_count:,}",
                delta=f"{null_percentage:.2f}%",
                delta_color="inverse"
            )
        with col2:
            st.metric(
                f"Non-Null Values",
                f"{len(df) - null_count:,}",
                delta=f"{((len(df) - null_count) / len(df) * 100):.2f}%"
            )
        
        # Progress bar for null percentage
        st.progress(null_percentage / 100, text=f"Null Percentage: {null_percentage:.2f}%")
        
        if null_count > 0:
            # Display rows with null values
            with st.expander("👁️ View Rows with Null Values", expanded=False):
                null_rows = df[df[selected_column].isnull()]
                view_dataframe(null_rows, height=400, page_size=20, key_suffix="null_rows")
            
            # Action options
            st.subheader("⚙️ Actions")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Option 1: Remove Rows**")
                if st.button("🗑️ Remove Rows with Null", key="remove_nulls"):
                    original_shape = df.shape
                    st.session_state['df'] = df.dropna(subset=[selected_column])
                    new_shape = st.session_state['df'].shape
                    st.success(f"✅ Removed {original_shape[0] - new_shape[0]:,} rows!")
                    st.rerun()
            
            with col2:
                st.write("**Option 2: Replace Nulls**")
                replacement_value = st.text_input(
                    "Replacement value",
                    help="Enter the value to replace nulls with"
                )
                
                if st.button("🔄 Replace Nulls", key="replace_nulls"):
                    if replacement_value:
                        # Convert replacement value to appropriate type
                        try:
                            if df[selected_column].dtype in ['int64', 'float64']:
                                replacement_value = float(replacement_value)
                        except:
                            pass
                        
                        st.session_state['df'][selected_column] = df[selected_column].fillna(replacement_value)
                        st.success(f"✅ Replaced {null_count:,} null values with '{replacement_value}'!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Please enter a replacement value")
        else:
            st.success(f"✅ No null values found in column '{selected_column}'")


# ==================== Edit Data Tab ====================
def edit_data_tab():
    """Edit and replace values in the dataset"""
    if 'df' not in st.session_state or st.session_state['df'] is None:
        st.info("👆 Please upload a file to get started")
        return
    
    df = st.session_state['df']
    
    st.header("✏️ Edit Data")
    
    st.info("💡 Select a column, choose values to replace, and specify the new value")
    
    # Step 1: Select column
    st.subheader("Step 1: Select Column")
    selected_column = st.selectbox(
        "Choose a column to edit",
        options=df.columns.tolist(),
        help="Select the column containing values you want to replace"
    )
    
    if selected_column:
        # Step 2: Show unique values and allow selection
        st.subheader("Step 2: Select Values to Replace")
        
        unique_values = df[selected_column].dropna().unique()
        
        # Display value counts for context
        with st.expander("📊 View Value Distribution", expanded=False):
            value_counts = df[selected_column].value_counts()
            st.dataframe(
                pd.DataFrame({
                    'Value': value_counts.index,
                    'Count': value_counts.values
                }),
                use_container_width=True
            )
        
        # Multi-select for values to replace
        values_to_replace = st.multiselect(
            "Select values to replace",
            options=unique_values.tolist(),
            help="Choose one or more values that you want to replace"
        )
        
        if values_to_replace:
            # Step 3: Enter replacement value
            st.subheader("Step 3: Enter Replacement Value")
            
            replacement_value = st.text_input(
                "New value",
                help="Enter the value that will replace the selected values"
            )
            
            # Preview affected rows
            if replacement_value:
                affected_rows = df[df[selected_column].isin(values_to_replace)]
                affected_count = len(affected_rows)
                
                st.write(f"**Preview: {affected_count:,} rows will be affected**")
                
                with st.expander("👁️ View Affected Rows (Before)", expanded=False):
                    view_dataframe(affected_rows, height=400, page_size=20, key_suffix="affected_rows")
                
                # Step 4: Execute replacement
                st.subheader("Step 4: Execute Replacement")
                
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    if st.button("🔄 Replace Values", type="primary"):
                        # Convert replacement value to appropriate type
                        try:
                            if df[selected_column].dtype in ['int64', 'float64']:
                                replacement_value = float(replacement_value)
                        except:
                            pass
                        
                        # Perform replacement
                        st.session_state['df'][selected_column] = df[selected_column].replace(
                            values_to_replace,
                            replacement_value
                        )
                        
                        st.success(f"✅ Successfully replaced {affected_count:,} values!")
                        st.rerun()
                
                with col2:
                    st.info(f"Will replace {len(values_to_replace)} unique value(s) in {affected_count:,} rows")


# ==================== Download Section ====================
def download_section():
    """Provide download options for the cleaned dataset"""
    if 'df' not in st.session_state or st.session_state['df'] is None:
        return
    
    df = st.session_state['df']
    
    st.sidebar.header("💾 Download Data")
    
    # Display current dataset info
    st.sidebar.write(f"**Current Dataset:**")
    st.sidebar.write(f"- Rows: {df.shape[0]:,}")
    st.sidebar.write(f"- Columns: {df.shape[1]:,}")
    
    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = st.session_state.get('file_name', 'cleaned_data').split('.')[0]
    
    # CSV Download
    st.sidebar.subheader("📄 CSV Format")
    encoding = st.sidebar.selectbox(
        "Select encoding",
        options=['utf-8', 'utf-8-sig', 'latin1', 'cp1252'],
        index=0
    )
    
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding=encoding)
    csv_data = csv_buffer.getvalue().encode(encoding)
    
    st.sidebar.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name=f"{base_filename}_cleaned_{timestamp}.csv",
        mime="text/csv"
    )
    
    # Excel Download
    st.sidebar.subheader("📊 Excel Format")
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Cleaned Data')
    excel_data = excel_buffer.getvalue()
    
    st.sidebar.download_button(
        label="📥 Download Excel",
        data=excel_data,
        file_name=f"{base_filename}_cleaned_{timestamp}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    


# ==================== Main Application ====================
def main():
    """Main application function"""
    
    # Title and description
    st.title("🧹 Data Cleaning & Exploration Tool")
    st.markdown("""
    A comprehensive tool for uploading, cleaning, and exploring your datasets.
    Upload your data, perform cleaning operations, and download the results.
    """)
    
    # Initialize session state
    if 'df' not in st.session_state:
        st.session_state['df'] = None
    if 'original_df' not in st.session_state:
        st.session_state['original_df'] = None
    
    # File upload section in main area
    file_upload_section()
    
    # Sidebar for download
    download_section()
    
    st.divider()
    
    # Main content area
    if st.session_state['df'] is not None:
        # Tabs for all operations
        tabs = st.tabs([
            "📊 View Data",
            "📈 Basic Statistics",
            "🔢 Value Counts & Visualizations",
            "🔍 Check Duplicates",
            "🔍 Check Nulls",
            "✏️ Edit Data"
        ])
        
        with tabs[0]:
            view_data_tab()
        
        with tabs[1]:
            basic_statistics_tab()
        
        with tabs[2]:
            value_counts_visualizations_tab()
        
        with tabs[3]:
            check_duplicates_tab()
        
        with tabs[4]:
            check_null_values_tab()
        
        with tabs[5]:
            edit_data_tab()
    else:
        # Error message when no file selected
        st.error("⚠️ No file selected! Please upload a file to get started.")
        
        st.subheader("✨ Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📁 File Support:**
            - CSV and TSV files
            - Excel files (.xlsx, .xls)
            - SAS files (.sas7bdat)
            - Multiple sheet support for Excel
            
            **🔍 Data Exploration:**
            - View data with customizable display
            - Value counts and distributions
            - Basic statistics
            """)
        
        with col2:
            st.markdown("""
            **🧹 Data Cleaning:**
            - Duplicate detection and removal
            - Null value handling
            - Value replacement and editing
            - Column-specific operations
            
            **💾 Export Options:**
            - CSV with encoding selection
            - Excel format
            - SAS format
            """)


if __name__ == "__main__":
    main()
