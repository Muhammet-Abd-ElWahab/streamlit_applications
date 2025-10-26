
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode
import uuid
import time

# def apply_button_styling():
#     """Apply consistent button styling: light blue for pre-submit, green for post-submit, default for delete"""
#     st.markdown("""
#     <style>
#     /* Light blue buttons for pre-submit actions */
#     .stButton > button {
#         background: linear-gradient(135deg, #87CEEB, #4682B4);
#         color: white;
#         border: none;
#         border-radius: 15px;
#         padding: 0.6rem 1.2rem;
#         font-size: 16px;
#         font-weight: 600;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 8px rgba(70, 130, 180, 0.3);
#         text-transform: uppercase;
#         letter-spacing: 0.5px;
#     }
#     .stButton > button:hover {
#         background: linear-gradient(135deg, #4682B4, #1E90FF);
#         transform: translateY(-3px);
#         box-shadow: 0 6px 12px rgba(70, 130, 180, 0.4);
#     }
#     .stButton > button:active {
#         transform: translateY(-1px);
#         box-shadow: 0 4px 8px rgba(70, 130, 180, 0.3);
#     }
#     .stButton > button:disabled {
#         background: #B0C4DE;
#         cursor: not-allowed;
#         transform: none;
#         box-shadow: 0 2px 4px rgba(176, 196, 222, 0.2);
#     }
    
#     /* Green buttons for post-submit/success actions */
#     .stButton > button[kind="secondary"] {
#         background: linear-gradient(135deg, #90EE90, #32CD32);
#         color: white;
#         border: none;
#         border-radius: 15px;
#         padding: 0.6rem 1.2rem;
#         font-size: 16px;
#         font-weight: 600;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 8px rgba(50, 205, 50, 0.3);
#         text-transform: uppercase;
#         letter-spacing: 0.5px;
#     }
#     .stButton > button[kind="secondary"]:hover {
#         background: linear-gradient(135deg, #32CD32, #228B22);
#         transform: translateY(-3px);
#         box-shadow: 0 6px 12px rgba(50, 205, 50, 0.4);
#     }
#     .stButton > button[kind="secondary"]:active {
#         transform: translateY(-1px);
#         box-shadow: 0 4px 8px rgba(50, 205, 50, 0.3);
#     }
    
#     /* Custom pagination styling */
#     .ag-paging-panel {
#         background: #f8f9fa;
#         border-top: 1px solid #dee2e6;
#         padding: 10px;
#     }
    
#     .ag-paging-page-size {
#         margin-left: 20px;
#     }
    
#     .ag-paging-page-size select {
#         background: #87CEEB;
#         color: white;
#         border: 1px solid #4682B4;
#         border-radius: 5px;
#         padding: 5px;
#         font-weight: 600;
#     }
#     </style>
#     """, unsafe_allow_html=True)





#------------------------------------------------------------------------------------#
# View Dataframe Widget
#------------------------------------------------------------------------------------#

@st.fragment
def view_dataframe(df, height=450, theme='alpine', page_size=20, 
                  font_size='16px', font_family='Arial, sans-serif', cell_color='#008080',
                  header_color='#333333', header_font_size='14px', header_font_family='Arial, sans-serif',
                  header_font_weight='600', header_background='#f0f0f0',
                  min_col_width=280, key_suffix="", row_height=50):
    """Display a read-only AG-Grid table with styling options and pagination controls"""
    if df.empty:
        st.info("No data available")
        return
    
    # Page size will be controlled within the grid pagination
    
    # Use simple header class for styling (like working disply_shap_values function)
    header_class = "custom-header"
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_side_bar(filters_panel=True, columns_panel=True)
    
    # Configure each column individually
    for col in df.columns:
        # Calculate minimum width based on header text length
        header_width = len(str(col)) * 12
        col_min_width = max(min_col_width, header_width)
        
        gb.configure_column(
            col,
            editable=False,
            filter=True,
            sortable=True,
            autoSize=False,
            resizable=True,
            headerClass=header_class,
            minWidth=col_min_width,
            width=col_min_width,
            maxWidth=400,
            autoHeight=True,
            wrapText=True,
            cellStyle={
                'textAlign': 'left',
                'fontSize': font_size,
                'fontFamily': font_family,
                'color': cell_color,
                'white-space': 'normal',
                'line-height': '20px',
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'flex-start'
            }
        )
    

    gb.configure_default_column(
        flex=1,
        minWidth=min_col_width,
        filter=True,
        autoSize=False,
        resizable=True,
        sortable=True,
        headerClass=header_class,
        cellStyle={
            'textAlign': 'left',
            'fontSize': font_size,
            'fontFamily': font_family,
            'color': cell_color
        }
    )
    
    # Configure grid options using your preferred method
    gb.configure_grid_options(
        domLayout='normal',
        pagination=True,
        paginationPageSize=page_size,
        paginationPageSizeSelector=[10, 20, 50, 100],
        enableCellTextSelection=True,
        ensureDomOrder=True,
        suppressColumnVirtualisation=False,
        suppressRowVirtualisation=False,
        columnSize="autoSize",
        sizeColumnsToFit=False,
        skipHeaderOnAutoSize=False,
        enableColResize=True
    )
    
    grid_options = gb.build()
    
    # Configure sidebar
    grid_options["sideBar"] = {
        "toolPanels": [
            {
                "id": "columns",
                "labelDefault": "Columns",
                "labelKey": "columns",
                "iconKey": "columns",
                "toolPanel": "agColumnsToolPanel"
            },
            {
                "id": "filters",
                "labelDefault": "Filters",
                "labelKey": "filters",
                "iconKey": "filter",
                "toolPanel": "agFiltersToolPanel"
            }
        ]
    }
    
    # Simple CSS for header styling (working approach like disply_shap_values)
    st.markdown(f"""
    <style>
    .{header_class} {{
        background-color: {header_background} !important;
    }}
    
    .{header_class} .ag-header-cell-label {{
        justify-content: center !important;
        color: {header_color} !important;
        font-size: {header_font_size} !important;
        font-family: {header_font_family} !important;
        font-weight: {header_font_weight} !important;
    }}
    
    /* Checkbox positioning */
    .ag-selection-checkbox {{
        margin-right: 8px !important;
    }}
    
    .ag-cell {{
        display: flex !important;
        align-items: center !important;
        padding: 8px 12px !important;
    }}
    
    /* Row styling */
    .ag-row {{
        border-bottom: 1px solid #e0e0e0 !important;
    }}
    
    .ag-row:hover {{
        background-color: #f5f5f5 !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    AgGrid(
        df.reset_index(drop=True),
        gridOptions=grid_options,
        data_return_mode=DataReturnMode.AS_INPUT,
        update_mode=GridUpdateMode.NO_UPDATE,
        fit_columns_on_grid_load=True,
        key=f"view_grid_{key_suffix}",
        height=height,
        theme=theme,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
    )





#------------------------------------------------------------------------------------#
# Edit Dataframe Widget
#------------------------------------------------------------------------------------#

# @st.fragment
# def edit_dataframe(df, height=450, theme='alpine', page_size=20,
#                   font_size='16px', font_family='Arial, sans-serif', cell_color='#008080',
#                   header_color='#333333', header_font_size='14px', header_font_family='Arial, sans-serif',
#                   header_font_weight='600', header_background='#f0f0f0',
#                   min_col_width=280, columns_not_editable=None, key_suffix="", row_height=50,
#                   edit_page_size=10, edit_font_size='14px', edit_font_family='Arial, sans-serif', edit_cell_color='green',
#                   edit_header_color='#333333', edit_header_font_size='14px', 
#                   edit_header_font_family='Arial, sans-serif', edit_header_font_weight='bold',
#                   edit_header_background='#e0e0e0'):
#     """Edit selected rows with pagination controls and return the edited data"""
#     if df.empty:
#         st.info("No data available to edit")
#         return None
    
#     # Page size will be controlled within the grid pagination
    
#     # Initialize session state for reset functionality
#     reset_key = f'reset_{key_suffix}'
#     if reset_key not in st.session_state:
#         st.session_state[reset_key] = False
    
#     # Use simple header class for original table
#     header_class = "custom-header"
    
#     # Selection mode - Original table styling
#     gb = GridOptionsBuilder.from_dataframe(df)
#     gb.configure_selection('multiple', use_checkbox=True)
#     gb.configure_side_bar(filters_panel=True, columns_panel=True)
    
#     # Configure columns with original styling
#     columns_not_editable = set(columns_not_editable or [])
#     for col in df.columns:
#         # Calculate minimum width based on header text length
#         header_width = len(str(col)) * 12
#         col_min_width = max(min_col_width, header_width)
        
#         gb.configure_column(
#             col,
#             editable=False,
#             filter=True,
#             sortable=True,
#             autoSize=False,
#             resizable=True,
#             headerClass=header_class,
#             minWidth=col_min_width,
#             width=col_min_width,
#             maxWidth=400,
#             autoHeight=True,
#             wrapText=True,
#             cellStyle={
#                 'textAlign': 'left',
#                 'fontSize': font_size,
#                 'fontFamily': font_family,
#                 'color': cell_color,
#                 'white-space': 'normal',
#                 'line-height': '20px',
#                 'display': 'flex',
#                 'align-items': 'center',
#                 'justify-content': 'flex-start'
#             }
#         )
    
#     # Configure default column for original table
#     gb.configure_default_column(
#         flex=1,
#         minWidth=min_col_width,
#         filter=True,
#         autoSize=False,
#         resizable=True,
#         sortable=True,
#         headerClass=header_class,
#         cellStyle={
#             'textAlign': 'left',
#             'fontSize': font_size,
#             'fontFamily': font_family,
#             'color': cell_color
#         }
#     )
    
#     # Configure grid options using your preferred method
#     gb.configure_grid_options(
#         domLayout='normal',
#         pagination=True,
#         paginationPageSize=page_size,
#         paginationPageSizeSelector=[10, 20, 50, 100],
#         enableCellTextSelection=True,
#         ensureDomOrder=True,
#         suppressColumnVirtualisation=False,
#         suppressRowVirtualisation=False,
#         columnSize="autoSize",
#         sizeColumnsToFit=False,
#         skipHeaderOnAutoSize=False,
#         enableColResize=True
#     )
    
#     grid_options = gb.build()
    
#     # Configure sidebar
#     grid_options["sideBar"] = {
#         "toolPanels": [
#             {
#                 "id": "columns",
#                 "labelDefault": "Columns",
#                 "labelKey": "columns",
#                 "iconKey": "columns",
#                 "toolPanel": "agColumnsToolPanel"
#             },
#             {
#                 "id": "filters",
#                 "labelDefault": "Filters",
#                 "labelKey": "filters",
#                 "iconKey": "filter",
#                 "toolPanel": "agFiltersToolPanel"
#             }
#         ]
#     }
    
#     # Get theme class for proper CSS targeting
#     theme_class = {
#         'alpine': 'ag-theme-alpine',
#         'alpine-dark': 'ag-theme-alpine-dark',
#         'balham': 'ag-theme-balham',
#         'balham-dark': 'ag-theme-balham-dark',
#         'material': 'ag-theme-material',
#         'streamlit': 'ag-theme-streamlit'
#     }.get(theme, 'ag-theme-alpine')
    
#     # Add enhanced CSS for proper styling
#     st.markdown(f"""
#     <style>
#     /* Header styling */
#     .{theme_class} .ag-header-cell.{header_class} {{
#         background-color: {header_background} !important;
#     }}
    
#     .{theme_class} .ag-header-cell.{header_class} .ag-header-cell-label {{
#         justify-content: center !important;
#         display: flex !important;
#         align-items: center !important;
#         color: {header_color} !important;
#         font-size: {header_font_size} !important;
#         font-family: {header_font_family} !important;
#         font-weight: {header_font_weight} !important;
#         text-align: center !important;
#     }}
    
#     /* Checkbox positioning */
#     .{theme_class} .ag-selection-checkbox {{
#         margin-right: 8px !important;
#     }}
    
#     .{theme_class} .ag-cell {{
#         display: flex !important;
#         align-items: center !important;
#         padding: 8px 12px !important;
#     }}
    
#     /* Row styling */
#     .{theme_class} .ag-row {{
#         border-bottom: 1px solid #e0e0e0 !important;
#     }}
    
#     .{theme_class} .ag-row:hover {{
#         background-color: #f5f5f5 !important;
#     }}
#     </style>
#     """, unsafe_allow_html=True)
    
#     # Reset selected rows if needed
#     if st.session_state[reset_key]:
#         st.session_state[reset_key] = False
#         st.rerun()
    
#     st.markdown("**Select rows to edit:**")
#     grid_response = AgGrid(
#         df.reset_index(drop=True),
#         gridOptions=grid_options,
#         data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
#         update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
#         fit_columns_on_grid_load=True,
#         key=f"edit_select_{key_suffix}",
#         height=int(height * 0.6),
#         theme=theme,
#         enable_enterprise_modules=True,
#         allow_unsafe_jscode=True,
#         columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
#     )
    
#     selected_rows = grid_response['selected_rows']
    
#     if selected_rows is not None and len(selected_rows) > 0:
#         st.markdown("**Edit selected rows:**")
        
#         selected_df = pd.DataFrame(selected_rows)
        
#         # Generate unique header class for edit table
#         edit_header_class = f"edit-header-{uuid.uuid4().hex[:8]}"
        
#             # Page size will be controlled within the edit grid pagination
        
#         # Editing mode - Different styling for edit table
#         gb_edit = GridOptionsBuilder.from_dataframe(selected_df)
        
#         # Configure columns for editing - inherit ALL styling from original table
#         for col in selected_df.columns:
#             is_editable = col not in columns_not_editable
#             # Calculate same width as original table
#             header_width = len(str(col)) * 12
#             col_min_width = max(min_col_width, header_width)
            
#             gb_edit.configure_column(
#                 col,
#                 editable=is_editable,
#                 filter=True,
#                 sortable=True,
#                 autoSize=False,
#                 resizable=True,
#                 headerClass=edit_header_class,
#                 minWidth=col_min_width,
#                 width=col_min_width,
#                 maxWidth=400,
#                 autoHeight=True,
#                 wrapText=True,
#                 cellStyle={
#                     'textAlign': 'left',  # Same as original table
#                     'fontSize': edit_font_size,
#                     'fontFamily': edit_font_family,
#                     'color': edit_cell_color,
#                     'white-space': 'normal',
#                     'line-height': '20px',
#                     'display': 'flex',
#                     'align-items': 'center',
#                     'justify-content': 'flex-start',  # Same alignment as original
#                     'height': f'{row_height}px',
#                     'max-height': f'{row_height}px',
#                     'overflow': 'hidden'
#                 }
#             )
        
#         # Configure default column for edit table - inherit original table settings
#         gb_edit.configure_default_column(
#             flex=1,
#             minWidth=min_col_width,
#             filter=True,
#             autoSize=False,
#             resizable=True,
#             sortable=True,
#             headerClass=edit_header_class,
#             cellStyle={
#                 'textAlign': 'left',
#                 'fontSize': edit_font_size,
#                 'fontFamily': edit_font_family,
#                 'color': edit_cell_color,
#                 'height': f'{row_height}px',
#                 'max-height': f'{row_height}px',
#                 'overflow': 'hidden'
#             }
#         )
        
#         # Configure edit grid options using your preferred method
#         gb_edit.configure_grid_options(
#             domLayout='normal',
#             pagination=True,
#             paginationPageSize=edit_page_size,
#             paginationPageSizeSelector=[10, 20, 50, 100],
#             enableCellTextSelection=True,
#             ensureDomOrder=True,
#             suppressColumnVirtualisation=False,
#             suppressRowVirtualisation=False,
#             columnSize="autoSize",
#             sizeColumnsToFit=False,
#             skipHeaderOnAutoSize=False,
#             enableColResize=True,
#             singleClickEdit=True
#         )
        
#         grid_options_edit = gb_edit.build()
        
#         # Configure edit grid to fill width
#         grid_options_edit['defaultColDef'] = {
#             'flex': 1,
#             'minWidth': 100,
#             'resizable': True,
#             'headerClass': edit_header_class
#         }
        
#         # Custom CSS for edit table headers
#         st.markdown(f"""
#         <style>
#         .{edit_header_class} .ag-header-cell-label {{
#             justify-content: center !important;
#             color: {edit_header_color} !important;
#             font-size: {edit_header_font_size} !important;
#             font-family: {edit_header_font_family} !important;
#             font-weight: {edit_header_font_weight} !important;
#         }}
#         .{edit_header_class} {{
#             background-color: {edit_header_background} !important;
#         }}
#         </style>
#         """, unsafe_allow_html=True)
        
#         edit_response = AgGrid(
#             selected_df.reset_index(drop=True),
#             gridOptions=grid_options_edit,
#             data_return_mode=DataReturnMode.AS_INPUT,
#             update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
#             fit_columns_on_grid_load=True,
#             key=f"edit_grid_{key_suffix}",
#             height=int(height * 0.6),
#             theme=theme,
#             enable_enterprise_modules=True,
#             allow_unsafe_jscode=True,
#             columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
#         )
        
#         # Enhanced validation and button styling
#         try:
#             edited_data = pd.DataFrame(edit_response['data'])
#             original_data = pd.DataFrame(selected_rows)
            
#             # Check if any changes were made
#             has_changes = not edited_data.equals(original_data)
            
#             # Validation without custom styling
            
#             # Show submit button with validation - warning if no changes
#             if not has_changes:
#                 st.warning("⚠️ No changes detected. Please modify the data before submitting.")
#                 return None
#             else:
#                 if st.button("Submit Changes", key=f"submit_{key_suffix}"):
#                     st.success(f"✅ Successfully edited {len(edited_data)} rows")
#                     # Reset selection
#                     st.session_state[reset_key] = True
#                     return edited_data
#         except Exception as e:
#             st.error(f"Error comparing data: {str(e)}")
            
#     else:
#         st.warning("Please Select Tasks for Update")
    
#     return None

# @st.fragment
# def edit_dataframe(df, height=450, theme='alpine', page_size=20,
#                   font_size='16px', font_family='Arial, sans-serif', cell_color='#008080',
#                   header_color='#333333', header_font_size='14px', header_font_family='Arial, sans-serif',
#                   header_font_weight='600', header_background='#f0f0f0',
#                   min_col_width=280, columns_not_editable=None, key_suffix="", row_height=50,
#                   edit_page_size=10, edit_font_size='14px', edit_font_family='Arial, sans-serif', edit_cell_color='green',
#                   edit_header_color='#333333', edit_header_font_size='14px', 
#                   edit_header_font_family='Arial, sans-serif', edit_header_font_weight='bold',
#                   edit_header_background='#e0e0e0'):
#     """Edit selected rows with pagination controls and return the edited data"""
#     if df.empty:
#         st.info("No data available to edit")
#         return None
    
#     # Initialize grid refresh counter for cancel functionality
#     grid_refresh_key = f"grid_refresh_edit_{key_suffix}"
#     if grid_refresh_key not in st.session_state:
#         st.session_state[grid_refresh_key] = 0
    
#     # Page size will be controlled within the grid pagination
    
#     # Initialize session state for reset functionality
#     reset_key = f'reset_{key_suffix}'
#     if reset_key not in st.session_state:
#         st.session_state[reset_key] = False
    
#     # Use simple header class for original table
#     header_class = "custom-header"
    
#     # Selection mode - Original table styling
#     gb = GridOptionsBuilder.from_dataframe(df)
#     gb.configure_selection('multiple', use_checkbox=True)
#     gb.configure_side_bar(filters_panel=True, columns_panel=True)
    
#     # Configure columns with original styling
#     columns_not_editable = set(columns_not_editable or [])
#     for col in df.columns:
#         # Calculate minimum width based on header text length
#         header_width = len(str(col)) * 12
#         col_min_width = max(min_col_width, header_width)
        
#         gb.configure_column(
#             col,
#             editable=False,
#             filter=True,
#             sortable=True,
#             autoSize=False,
#             resizable=True,
#             headerClass=header_class,
#             minWidth=col_min_width,
#             width=col_min_width,
#             maxWidth=400,
#             autoHeight=True,
#             wrapText=True,
#             cellStyle={
#                 'textAlign': 'left',
#                 'fontSize': font_size,
#                 'fontFamily': font_family,
#                 'color': cell_color,
#                 'white-space': 'normal',
#                 'line-height': '20px',
#                 'display': 'flex',
#                 'align-items': 'center',
#                 'justify-content': 'flex-start'
#             }
#         )
    
#     # Configure default column for original table
#     gb.configure_default_column(
#         flex=1,
#         minWidth=min_col_width,
#         filter=True,
#         autoSize=False,
#         resizable=True,
#         sortable=True,
#         headerClass=header_class,
#         cellStyle={
#             'textAlign': 'left',
#             'fontSize': font_size,
#             'fontFamily': font_family,
#             'color': cell_color
#         }
#     )
    
#     # Configure grid options using your preferred method
#     gb.configure_grid_options(
#         domLayout='normal',
#         pagination=True,
#         paginationPageSize=page_size,
#         paginationPageSizeSelector=[10, 20, 50, 100],
#         enableCellTextSelection=True,
#         ensureDomOrder=True,
#         suppressColumnVirtualisation=False,
#         suppressRowVirtualisation=False,
#         columnSize="autoSize",
#         sizeColumnsToFit=False,
#         skipHeaderOnAutoSize=False,
#         enableColResize=True
#     )
    
#     grid_options = gb.build()
    
#     # Configure sidebar
#     grid_options["sideBar"] = {
#         "toolPanels": [
#             {
#                 "id": "columns",
#                 "labelDefault": "Columns",
#                 "labelKey": "columns",
#                 "iconKey": "columns",
#                 "toolPanel": "agColumnsToolPanel"
#             },
#             {
#                 "id": "filters",
#                 "labelDefault": "Filters",
#                 "labelKey": "filters",
#                 "iconKey": "filter",
#                 "toolPanel": "agFiltersToolPanel"
#             }
#         ]
#     }
    
#     # Get theme class for proper CSS targeting
#     theme_class = {
#         'alpine': 'ag-theme-alpine',
#         'alpine-dark': 'ag-theme-alpine-dark',
#         'balham': 'ag-theme-balham',
#         'balham-dark': 'ag-theme-balham-dark',
#         'material': 'ag-theme-material',
#         'streamlit': 'ag-theme-streamlit'
#     }.get(theme, 'ag-theme-alpine')
    
#     # Add enhanced CSS for proper styling
#     st.markdown(f"""
#     <style>
#     /* Header styling */
#     .{theme_class} .ag-header-cell.{header_class} {{
#         background-color: {header_background} !important;
#     }}
    
#     .{theme_class} .ag-header-cell.{header_class} .ag-header-cell-label {{
#         justify-content: center !important;
#         display: flex !important;
#         align-items: center !important;
#         color: {header_color} !important;
#         font-size: {header_font_size} !important;
#         font-family: {header_font_family} !important;
#         font-weight: {header_font_weight} !important;
#         text-align: center !important;
#     }}
    
#     /* Checkbox positioning */
#     .{theme_class} .ag-selection-checkbox {{
#         margin-right: 8px !important;
#     }}
    
#     .{theme_class} .ag-cell {{
#         display: flex !important;
#         align-items: center !important;
#         padding: 8px 12px !important;
#     }}
    
#     /* Row styling */
#     .{theme_class} .ag-row {{
#         border-bottom: 1px solid #e0e0e0 !important;
#     }}
    
#     .{theme_class} .ag-row:hover {{
#         background-color: #f5f5f5 !important;
#     }}
#     </style>
#     """, unsafe_allow_html=True)
    
#     # Reset selected rows if needed
#     if st.session_state[reset_key]:
#         st.session_state[reset_key] = False
#         st.rerun()
    
#     st.markdown("**Select rows to edit:**")
    
#     # Create dynamic key using refresh counter
#     current_grid_key = f"edit_select_{key_suffix}_{st.session_state[grid_refresh_key]}"
    
#     grid_response = AgGrid(
#         df.reset_index(drop=True),
#         gridOptions=grid_options,
#         data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
#         update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
#         fit_columns_on_grid_load=True,
#         key=current_grid_key,
#         height=int(height * 0.6),
#         theme=theme,
#         enable_enterprise_modules=True,
#         allow_unsafe_jscode=True,
#         columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
#     )
    
#     selected_rows = grid_response['selected_rows']
    
#     if selected_rows is not None and len(selected_rows) > 0:
#         st.markdown("**Edit selected rows:**")
        
#         selected_df = pd.DataFrame(selected_rows)
        
#         # Generate unique header class for edit table
#         edit_header_class = f"edit-header-{uuid.uuid4().hex[:8]}"
        
#             # Page size will be controlled within the edit grid pagination
        
#         # Editing mode - Different styling for edit table
#         gb_edit = GridOptionsBuilder.from_dataframe(selected_df)
        
#         # Configure columns for editing - inherit ALL styling from original table
#         for col in selected_df.columns:
#             is_editable = col not in columns_not_editable
#             # Calculate same width as original table
#             header_width = len(str(col)) * 12
#             col_min_width = max(min_col_width, header_width)
            
#             gb_edit.configure_column(
#                 col,
#                 editable=is_editable,
#                 filter=True,
#                 sortable=True,
#                 autoSize=False,
#                 resizable=True,
#                 headerClass=edit_header_class,
#                 minWidth=col_min_width,
#                 width=col_min_width,
#                 maxWidth=400,
#                 autoHeight=True,
#                 wrapText=True,
#                 cellStyle={
#                     'textAlign': 'left',  # Same as original table
#                     'fontSize': edit_font_size,
#                     'fontFamily': edit_font_family,
#                     'color': edit_cell_color,
#                     'white-space': 'normal',
#                     'line-height': '20px',
#                     'display': 'flex',
#                     'align-items': 'center',
#                     'justify-content': 'flex-start',  # Same alignment as original
#                     'height': f'{row_height}px',
#                     'max-height': f'{row_height}px',
#                     'overflow': 'hidden'
#                 }
#             )
        
#         # Configure default column for edit table - inherit original table settings
#         gb_edit.configure_default_column(
#             flex=1,
#             minWidth=min_col_width,
#             filter=True,
#             autoSize=False,
#             resizable=True,
#             sortable=True,
#             headerClass=edit_header_class,
#             cellStyle={
#                 'textAlign': 'left',
#                 'fontSize': edit_font_size,
#                 'fontFamily': edit_font_family,
#                 'color': edit_cell_color,
#                 'height': f'{row_height}px',
#                 'max-height': f'{row_height}px',
#                 'overflow': 'hidden'
#             }
#         )
        
#         # Configure edit grid options using your preferred method
#         gb_edit.configure_grid_options(
#             domLayout='normal',
#             pagination=True,
#             paginationPageSize=edit_page_size,
#             paginationPageSizeSelector=[10, 20, 50, 100],
#             enableCellTextSelection=True,
#             ensureDomOrder=True,
#             suppressColumnVirtualisation=False,
#             suppressRowVirtualisation=False,
#             columnSize="autoSize",
#             sizeColumnsToFit=False,
#             skipHeaderOnAutoSize=False,
#             enableColResize=True,
#             singleClickEdit=True
#         )
        
#         grid_options_edit = gb_edit.build()
        
#         # Configure edit grid to fill width
#         grid_options_edit['defaultColDef'] = {
#             'flex': 1,
#             'minWidth': 100,
#             'resizable': True,
#             'headerClass': edit_header_class
#         }
        
#         # Custom CSS for edit table headers
#         st.markdown(f"""
#         <style>
#         .{edit_header_class} .ag-header-cell-label {{
#             justify-content: center !important;
#             color: {edit_header_color} !important;
#             font-size: {edit_header_font_size} !important;
#             font-family: {edit_header_font_family} !important;
#             font-weight: {edit_header_font_weight} !important;
#         }}
#         .{edit_header_class} {{
#             background-color: {edit_header_background} !important;
#         }}
#         </style>
#         """, unsafe_allow_html=True)
        
#         edit_response = AgGrid(
#             selected_df.reset_index(drop=True),
#             gridOptions=grid_options_edit,
#             data_return_mode=DataReturnMode.AS_INPUT,
#             update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
#             fit_columns_on_grid_load=True,
#             key=f"edit_grid_{key_suffix}",
#             height=int(height * 0.6),
#             theme=theme,
#             enable_enterprise_modules=True,
#             allow_unsafe_jscode=True,
#             columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
#         )
        
#         # Enhanced validation and button styling
#         try:
#             edited_data = pd.DataFrame(edit_response['data'])
#             original_data = pd.DataFrame(selected_rows)
            
#             # Check if any changes were made
#             has_changes = not edited_data.equals(original_data)
            
#             # Validation without custom styling
            
#             # Show submit button with validation - warning if no changes
#             if not has_changes:
#                 st.warning("⚠️ No changes detected. Please modify the data before submitting.")
#                 # Add cancel button even when no changes
#                 col1, col2 = st.columns([1, 1])
#                 with col2:
#                     if st.button("Cancel", key=f"cancel_edit_{key_suffix}"):
#                         # Increment the refresh counter to force grid re-render with new key
#                         st.session_state[grid_refresh_key] += 1
#                         st.info("🔵 Selection cleared. No changes made.")
#                         st.rerun()
#                 return None
#             else:
#                 # Add submit and cancel buttons when changes are detected
#                 col1, col2, col3 = st.columns([1, 1,3])
                
#                 with col1:
#                     if st.button("Submit Changes", key=f"submit_{key_suffix}"):
#                         st.success(f"✅ Successfully edited {len(edited_data)} rows")
#                         # Reset selection
#                         st.session_state[reset_key] = True
#                         return edited_data
                
#                 with col2:
#                     if st.button("Cancel", key=f"cancel_edit_changes_{key_suffix}"):
#                         # Increment the refresh counter to force grid re-render with new key
#                         st.session_state[grid_refresh_key] += 1
#                         st.info("🔵 Selection cleared. Changes discarded.")
#                         time.sleep(1)
#                         st.rerun()
                        
#         except Exception as e:
#             st.error(f"Error comparing data: {str(e)}")
            
#     else:
#         st.warning("Please Select Tasks for Update")
    
#     return None

# @st.fragment
# def edit_dataframe(df, height=450, theme='alpine', page_size=20,
#                   font_size='16px', font_family='Arial, sans-serif', cell_color='#008080',
#                   header_color='#333333', header_font_size='14px', header_font_family='Arial, sans-serif',
#                   header_font_weight='600', header_background='#f0f0f0',
#                   min_col_width=280, columns_not_editable=None, key_suffix="", row_height=50,
#                   edit_page_size=10, edit_font_size='14px', edit_font_family='Arial, sans-serif', edit_cell_color='green',
#                   edit_header_color='#333333', edit_header_font_size='14px', 
#                   edit_header_font_family='Arial, sans-serif', edit_header_font_weight='bold',
#                   edit_header_background='#e0e0e0'):
#     """Edit selected rows with pagination controls and return the edited data"""
#     if df.empty:
#         st.info("No data available to edit")
#         return None
    
#     # Initialize grid refresh counter for cancel functionality
#     grid_refresh_key = f"grid_refresh_edit_{key_suffix}"
#     if grid_refresh_key not in st.session_state:
#         st.session_state[grid_refresh_key] = 0
    
#     # Page size will be controlled within the grid pagination
    
#     # Initialize session state for reset functionality
#     reset_key = f'reset_{key_suffix}'
#     if reset_key not in st.session_state:
#         st.session_state[reset_key] = False
    
#     # Use simple header class for original table
#     header_class = "custom-header"
    
#     # Selection mode - Original table styling
#     gb = GridOptionsBuilder.from_dataframe(df)
#     gb.configure_selection('multiple', use_checkbox=True)
#     gb.configure_side_bar(filters_panel=True, columns_panel=True)
    
#     # Configure columns with original styling
#     columns_not_editable = set(columns_not_editable or [])
#     for col in df.columns:
#         # Calculate minimum width based on header text length
#         header_width = len(str(col)) * 12
#         col_min_width = max(min_col_width, header_width)
        
#         gb.configure_column(
#             col,
#             editable=False,
#             filter=True,
#             sortable=True,
#             autoSize=False,
#             resizable=True,
#             headerClass=header_class,
#             minWidth=col_min_width,
#             width=col_min_width,
#             maxWidth=400,
#             autoHeight=True,
#             wrapText=True,
#             cellStyle={
#                 'textAlign': 'left',
#                 'fontSize': font_size,
#                 'fontFamily': font_family,
#                 'color': cell_color,
#                 'white-space': 'normal',
#                 'line-height': '20px',
#                 'display': 'flex',
#                 'align-items': 'center',
#                 'justify-content': 'flex-start'
#             }
#         )
    
#     # Configure default column for original table
#     gb.configure_default_column(
#         flex=1,
#         minWidth=min_col_width,
#         filter=True,
#         autoSize=False,
#         resizable=True,
#         sortable=True,
#         headerClass=header_class,
#         cellStyle={
#             'textAlign': 'left',
#             'fontSize': font_size,
#             'fontFamily': font_family,
#             'color': cell_color
#         }
#     )
    
#     # Configure grid options using your preferred method
#     gb.configure_grid_options(
#         domLayout='normal',
#         pagination=True,
#         paginationPageSize=page_size,
#         paginationPageSizeSelector=[10, 20, 50, 100],
#         enableCellTextSelection=True,
#         ensureDomOrder=True,
#         suppressColumnVirtualisation=False,
#         suppressRowVirtualisation=False,
#         columnSize="autoSize",
#         sizeColumnsToFit=False,
#         skipHeaderOnAutoSize=False,
#         enableColResize=True
#     )
    
#     grid_options = gb.build()
    
#     # Configure sidebar
#     grid_options["sideBar"] = {
#         "toolPanels": [
#             {
#                 "id": "columns",
#                 "labelDefault": "Columns",
#                 "labelKey": "columns",
#                 "iconKey": "columns",
#                 "toolPanel": "agColumnsToolPanel"
#             },
#             {
#                 "id": "filters",
#                 "labelDefault": "Filters",
#                 "labelKey": "filters",
#                 "iconKey": "filter",
#                 "toolPanel": "agFiltersToolPanel"
#             }
#         ]
#     }
    
#     # Get theme class for proper CSS targeting
#     theme_class = {
#         'alpine': 'ag-theme-alpine',
#         'alpine-dark': 'ag-theme-alpine-dark',
#         'balham': 'ag-theme-balham',
#         'balham-dark': 'ag-theme-balham-dark',
#         'material': 'ag-theme-material',
#         'streamlit': 'ag-theme-streamlit'
#     }.get(theme, 'ag-theme-alpine')
    
#     # Add enhanced CSS for proper styling
#     st.markdown(f"""
#     <style>
#     /* Header styling */
#     .{theme_class} .ag-header-cell.{header_class} {{
#         background-color: {header_background} !important;
#     }}
    
#     .{theme_class} .ag-header-cell.{header_class} .ag-header-cell-label {{
#         justify-content: center !important;
#         display: flex !important;
#         align-items: center !important;
#         color: {header_color} !important;
#         font-size: {header_font_size} !important;
#         font-family: {header_font_family} !important;
#         font-weight: {header_font_weight} !important;
#         text-align: center !important;
#     }}
    
#     /* Checkbox positioning */
#     .{theme_class} .ag-selection-checkbox {{
#         margin-right: 8px !important;
#     }}
    
#     .{theme_class} .ag-cell {{
#         display: flex !important;
#         align-items: center !important;
#         padding: 8px 12px !important;
#     }}
    
#     /* Row styling */
#     .{theme_class} .ag-row {{
#         border-bottom: 1px solid #e0e0e0 !important;
#     }}
    
#     .{theme_class} .ag-row:hover {{
#         background-color: #f5f5f5 !important;
#     }}
#     </style>
#     """, unsafe_allow_html=True)
    
#     # Reset selected rows if needed
#     if st.session_state[reset_key]:
#         st.session_state[reset_key] = False
#         st.rerun()
    
#     st.markdown("**Select rows to edit:**")
    
#     # Create dynamic key using refresh counter
#     current_grid_key = f"edit_select_{key_suffix}_{st.session_state[grid_refresh_key]}"
    
#     grid_response = AgGrid(
#         df.reset_index(drop=True),
#         gridOptions=grid_options,
#         data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
#         update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
#         fit_columns_on_grid_load=True,
#         key=current_grid_key,
#         height=int(height * 0.6),
#         theme=theme,
#         enable_enterprise_modules=True,
#         allow_unsafe_jscode=True,
#         columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
#     )
    
#     selected_rows = grid_response['selected_rows']
    
#     if selected_rows is not None and len(selected_rows) > 0:
#         st.markdown("**Edit selected rows:**")
        
#         selected_df = pd.DataFrame(selected_rows)
        
#         # Generate unique header class for edit table
#         edit_header_class = f"edit-header-{uuid.uuid4().hex[:8]}"
        
#             # Page size will be controlled within the edit grid pagination
        
#         # Editing mode - Different styling for edit table
#         gb_edit = GridOptionsBuilder.from_dataframe(selected_df)
        
#         # Configure columns for editing - inherit ALL styling from original table
#         for col in selected_df.columns:
#             is_editable = col not in columns_not_editable
#             # Calculate same width as original table
#             header_width = len(str(col)) * 12
#             col_min_width = max(min_col_width, header_width)
            
#             gb_edit.configure_column(
#                 col,
#                 editable=is_editable,
#                 filter=True,
#                 sortable=True,
#                 autoSize=False,
#                 resizable=True,
#                 headerClass=edit_header_class,
#                 minWidth=col_min_width,
#                 width=col_min_width,
#                 maxWidth=400,
#                 autoHeight=True,
#                 wrapText=True,
#                 cellStyle={
#                     'textAlign': 'left',  # Same as original table
#                     'fontSize': edit_font_size,
#                     'fontFamily': edit_font_family,
#                     'color': edit_cell_color,
#                     'white-space': 'normal',
#                     'line-height': '20px',
#                     'display': 'flex',
#                     'align-items': 'center',
#                     'justify-content': 'flex-start',  # Same alignment as original
#                     'height': f'{row_height}px',
#                     'max-height': f'{row_height}px',
#                     'overflow': 'hidden'
#                 }
#             )
        
#         # Configure default column for edit table - inherit original table settings
#         gb_edit.configure_default_column(
#             flex=1,
#             minWidth=min_col_width,
#             filter=True,
#             autoSize=False,
#             resizable=True,
#             sortable=True,
#             headerClass=edit_header_class,
#             cellStyle={
#                 'textAlign': 'left',
#                 'fontSize': edit_font_size,
#                 'fontFamily': edit_font_family,
#                 'color': edit_cell_color,
#                 'height': f'{row_height}px',
#                 'max-height': f'{row_height}px',
#                 'overflow': 'hidden'
#             }
#         )
        
#         # Configure edit grid options using your preferred method
#         gb_edit.configure_grid_options(
#             domLayout='normal',
#             pagination=True,
#             paginationPageSize=edit_page_size,
#             paginationPageSizeSelector=[10, 20, 50, 100],
#             enableCellTextSelection=True,
#             ensureDomOrder=True,
#             suppressColumnVirtualisation=False,
#             suppressRowVirtualisation=False,
#             columnSize="autoSize",
#             sizeColumnsToFit=False,
#             skipHeaderOnAutoSize=False,
#             enableColResize=True,
#             singleClickEdit=True
#         )
        
#         grid_options_edit = gb_edit.build()
        
#         # Configure edit grid to fill width
#         grid_options_edit['defaultColDef'] = {
#             'flex': 1,
#             'minWidth': 100,
#             'resizable': True,
#             'headerClass': edit_header_class
#         }
        
#         # Custom CSS for edit table headers
#         st.markdown(f"""
#         <style>
#         .{edit_header_class} .ag-header-cell-label {{
#             justify-content: center !important;
#             color: {edit_header_color} !important;
#             font-size: {edit_header_font_size} !important;
#             font-family: {edit_header_font_family} !important;
#             font-weight: {edit_header_font_weight} !important;
#         }}
#         .{edit_header_class} {{
#             background-color: {edit_header_background} !important;
#         }}
#         </style>
#         """, unsafe_allow_html=True)
        
#         edit_response = AgGrid(
#             selected_df.reset_index(drop=True),
#             gridOptions=grid_options_edit,
#             data_return_mode=DataReturnMode.AS_INPUT,
#             update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
#             fit_columns_on_grid_load=True,
#             key=f"edit_grid_{key_suffix}",
#             height=int(height * 0.6),
#             theme=theme,
#             enable_enterprise_modules=True,
#             allow_unsafe_jscode=True,
#             columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
#         )
        
#         # Enhanced validation and button styling
#         try:
#             edited_data = pd.DataFrame(edit_response['data']).reset_index(drop=True)
#             original_data = pd.DataFrame(selected_rows).reset_index(drop=True)
            
#             # Ensure both dataframes have the same columns in the same order
#             if not edited_data.columns.equals(original_data.columns):
#                 # Reorder columns to match
#                 edited_data = edited_data[original_data.columns]
            
#             # Convert all columns to string for comparison to avoid data type issues
#             edited_data_str = edited_data.astype(str)
#             original_data_str = original_data.astype(str)
            
#             # Check if any changes were made by comparing string representations
#             has_changes = not edited_data_str.equals(original_data_str)
            
#             # Alternative comparison method - check row by row
#             if not has_changes:
#                 # Double check with row-by-row comparison
#                 for i in range(len(edited_data)):
#                     for col in edited_data.columns:
#                         if str(edited_data.iloc[i][col]) != str(original_data.iloc[i][col]):
#                             has_changes = True
#                             break
#                     if has_changes:
#                         break
            
#             # Show submit button with validation - warning if no changes
#             if not has_changes:
#                 st.warning("⚠️ No changes detected. Please modify the data before submitting.")
#                 # Add cancel button even when no changes
#                 col1, col2 = st.columns([1, 1])
#                 with col2:
#                     if st.button("Cancel", key=f"cancel_edit_{key_suffix}"):
#                         # Increment the refresh counter to force grid re-render with new key
#                         st.session_state[grid_refresh_key] += 1
#                         st.info("🔵 Selection cleared. No changes made.")
#                         st.rerun()
#                 return None
#             else:
#                 # Add submit and cancel buttons when changes are detected
#                 col1, col2 = st.columns([1, 1])
                
#                 with col1:
#                     if st.button("Submit Changes", key=f"submit_{key_suffix}"):
#                         st.success(f"✅ Successfully edited {len(edited_data)} rows")
#                         # Reset selection
#                         st.session_state[reset_key] = True
#                         # Return only the edited data (selected rows after editing)
#                         return edited_data
                
#                 with col2:
#                     if st.button("Cancel", key=f"cancel_edit_changes_{key_suffix}"):
#                         # Increment the refresh counter to force grid re-render with new key
#                         st.session_state[grid_refresh_key] += 1
#                         st.info("🔵 Selection cleared. Changes discarded.")
#                         st.rerun()
                        
#         except Exception as e:
#             st.error(f"Error comparing data: {str(e)}")
#             st.write("Debug info:")
#             st.write("Edited data shape:", edited_data.shape if 'edited_data' in locals() else "Not defined")
#             st.write("Original data shape:", original_data.shape if 'original_data' in locals() else "Not defined")
            
#     else:
#         st.warning("Please Select Tasks for Update")
    
    
    # return None



@st.fragment
def edit_dataframe(df, table_name_to_show_on_messages, height=450, theme='alpine', page_size=20,
                  font_size='16px', font_family='Arial, sans-serif', cell_color='#008080',
                  header_color='#333333', header_font_size='14px', header_font_family='Arial, sans-serif',
                  header_font_weight='600', header_background='#f0f0f0',
                  min_col_width=280, columns_not_editable=None, key_suffix="", row_height=50,
                  edit_page_size=10, edit_font_size='14px', edit_font_family='Arial, sans-serif', edit_cell_color='green',
                  edit_header_color='#333333', edit_header_font_size='14px', 
                  edit_header_font_family='Arial, sans-serif', edit_header_font_weight='bold',
                  edit_header_background='#e0e0e0'):
    """Edit selected rows with pagination controls and return the edited data"""
    if df.empty:
        st.info("No data available to edit")
        return None
    
    # Initialize grid refresh counter for cancel functionality
    grid_refresh_key = f"grid_refresh_edit_{key_suffix}"
    if grid_refresh_key not in st.session_state:
        st.session_state[grid_refresh_key] = 0
    
    # Page size will be controlled within the grid pagination
    
    # Initialize session state for reset functionality
    reset_key = f'reset_{key_suffix}'
    if reset_key not in st.session_state:
        st.session_state[reset_key] = False
    
    # Use simple header class for original table
    header_class = "custom-header"
    
    # Selection mode - Original table styling
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection('multiple', use_checkbox=True)
    gb.configure_side_bar(filters_panel=True, columns_panel=True)
    
    # Configure columns with original styling
    columns_not_editable = set(columns_not_editable or [])
    for col in df.columns:
        # Calculate minimum width based on header text length
        header_width = len(str(col)) * 12
        col_min_width = max(min_col_width, header_width)
        
        gb.configure_column(
            col,
            editable=False,
            filter=True,
            sortable=True,
            autoSize=False,
            resizable=True,
            headerClass=header_class,
            minWidth=col_min_width,
            width=col_min_width,
            maxWidth=400,
            autoHeight=True,
            wrapText=True,
            cellStyle={
                'textAlign': 'left',
                'fontSize': font_size,
                'fontFamily': font_family,
                'color': cell_color,
                'white-space': 'normal',
                'line-height': '20px',
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'flex-start'
            }
        )
    
    # Configure default column for original table
    gb.configure_default_column(
        flex=1,
        minWidth=min_col_width,
        filter=True,
        autoSize=False,
        resizable=True,
        sortable=True,
        headerClass=header_class,
        cellStyle={
            'textAlign': 'left',
            'fontSize': font_size,
            'fontFamily': font_family,
            'color': cell_color
        }
    )
    
    # Configure grid options using your preferred method
    gb.configure_grid_options(
        domLayout='normal',
        pagination=True,
        paginationPageSize=page_size,
        paginationPageSizeSelector=[10, 20, 50, 100],
        enableCellTextSelection=True,
        ensureDomOrder=True,
        suppressColumnVirtualisation=False,
        suppressRowVirtualisation=False,
        columnSize="autoSize",
        sizeColumnsToFit=False,
        skipHeaderOnAutoSize=False,
        enableColResize=True
    )
    
    grid_options = gb.build()
    
    # Configure sidebar
    grid_options["sideBar"] = {
        "toolPanels": [
            {
                "id": "columns",
                "labelDefault": "Columns",
                "labelKey": "columns",
                "iconKey": "columns",
                "toolPanel": "agColumnsToolPanel"
            },
            {
                "id": "filters",
                "labelDefault": "Filters",
                "labelKey": "filters",
                "iconKey": "filter",
                "toolPanel": "agFiltersToolPanel"
            }
        ]
    }
    
    # Get theme class for proper CSS targeting
    theme_class = {
        'alpine': 'ag-theme-alpine',
        'alpine-dark': 'ag-theme-alpine-dark',
        'balham': 'ag-theme-balham',
        'balham-dark': 'ag-theme-balham-dark',
        'material': 'ag-theme-material',
        'streamlit': 'ag-theme-streamlit'
    }.get(theme, 'ag-theme-alpine')
    
    # Add enhanced CSS for proper styling
    st.markdown(f"""
    <style>
    /* Header styling */
    .{theme_class} .ag-header-cell.{header_class} {{
        background-color: {header_background} !important;
    }}
    
    .{theme_class} .ag-header-cell.{header_class} .ag-header-cell-label {{
        justify-content: center !important;
        display: flex !important;
        align-items: center !important;
        color: {header_color} !important;
        font-size: {header_font_size} !important;
        font-family: {header_font_family} !important;
        font-weight: {header_font_weight} !important;
        text-align: center !important;
    }}
    
    /* Checkbox positioning */
    .{theme_class} .ag-selection-checkbox {{
        margin-right: 8px !important;
    }}
    
    .{theme_class} .ag-cell {{
        display: flex !important;
        align-items: center !important;
        padding: 8px 12px !important;
    }}
    
    /* Row styling */
    .{theme_class} .ag-row {{
        border-bottom: 1px solid #e0e0e0 !important;
    }}
    
    .{theme_class} .ag-row:hover {{
        background-color: #f5f5f5 !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Reset selected rows if needed
    if st.session_state[reset_key]:
        st.session_state[reset_key] = False
        st.rerun()
    
    # st.markdown("**Select rows to edit:**")
    st.markdown(
            "<h5 style='color: #FF8C42;'>Select rows to edit:</h5>",
            unsafe_allow_html=True
        )
    
    # Create dynamic key using refresh counter
    current_grid_key = f"edit_select_{key_suffix}_{st.session_state[grid_refresh_key]}"
    
    grid_response = AgGrid(
        df.reset_index(drop=True),
        gridOptions=grid_options,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
        fit_columns_on_grid_load=True,
        key=current_grid_key,
        height=int(height * 0.6),
        theme=theme,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
    )
    
    selected_rows = grid_response['selected_rows']
    
    if selected_rows is not None and len(selected_rows) > 0:
        st.markdown("**Edit selected rows:**")
        
        selected_df = pd.DataFrame(selected_rows)
        
        # Generate unique header class for edit table
        edit_header_class = f"edit-header-{uuid.uuid4().hex[:8]}"
        
            # Page size will be controlled within the edit grid pagination
        
        # Editing mode - Different styling for edit table
        gb_edit = GridOptionsBuilder.from_dataframe(selected_df)
        
        # Configure columns for editing - inherit ALL styling from original table
        for col in selected_df.columns:
            is_editable = col not in columns_not_editable
            # Calculate same width as original table
            header_width = len(str(col)) * 12
            col_min_width = max(min_col_width, header_width)
            
            gb_edit.configure_column(
                col,
                editable=is_editable,
                filter=True,
                sortable=True,
                autoSize=False,
                resizable=True,
                headerClass=edit_header_class,
                minWidth=col_min_width,
                width=col_min_width,
                maxWidth=400,
                autoHeight=True,
                wrapText=True,
                cellStyle={
                    'textAlign': 'left',  # Same as original table
                    'fontSize': edit_font_size,
                    'fontFamily': edit_font_family,
                    'color': edit_cell_color,
                    'white-space': 'normal',
                    'line-height': '20px',
                    'display': 'flex',
                    'align-items': 'center',
                    'justify-content': 'flex-start',  # Same alignment as original
                    'height': f'{row_height}px',
                    'max-height': f'{row_height}px',
                    'overflow': 'hidden'
                }
            )
        
        # Configure default column for edit table - inherit original table settings
        gb_edit.configure_default_column(
            flex=1,
            minWidth=min_col_width,
            filter=True,
            autoSize=False,
            resizable=True,
            sortable=True,
            headerClass=edit_header_class,
            cellStyle={
                'textAlign': 'left',
                'fontSize': edit_font_size,
                'fontFamily': edit_font_family,
                'color': edit_cell_color,
                'height': f'{row_height}px',
                'max-height': f'{row_height}px',
                'overflow': 'hidden'
            }
        )
        
        # Configure edit grid options using your preferred method
        gb_edit.configure_grid_options(
            domLayout='normal',
            pagination=True,
            paginationPageSize=edit_page_size,
            paginationPageSizeSelector=[10, 20, 50, 100],
            enableCellTextSelection=True,
            ensureDomOrder=True,
            suppressColumnVirtualisation=False,
            suppressRowVirtualisation=False,
            columnSize="autoSize",
            sizeColumnsToFit=False,
            skipHeaderOnAutoSize=False,
            enableColResize=True,
            singleClickEdit=True
        )
        
        grid_options_edit = gb_edit.build()
        
        # Configure edit grid to fill width
        grid_options_edit['defaultColDef'] = {
            'flex': 1,
            'minWidth': 100,
            'resizable': True,
            'headerClass': edit_header_class
        }
        
        # Custom CSS for edit table headers
        st.markdown(f"""
        <style>
        .{edit_header_class} .ag-header-cell-label {{
            justify-content: center !important;
            color: {edit_header_color} !important;
            font-size: {edit_header_font_size} !important;
            font-family: {edit_header_font_family} !important;
            font-weight: {edit_header_font_weight} !important;
        }}
        .{edit_header_class} {{
            background-color: {edit_header_background} !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        edit_response = AgGrid(
            selected_df.reset_index(drop=True),
            gridOptions=grid_options_edit,
            data_return_mode=DataReturnMode.AS_INPUT,
            update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
            fit_columns_on_grid_load=True,
            key=f"edit_grid_{key_suffix}",
            height=int(height * 0.6),
            theme=theme,
            enable_enterprise_modules=True,
            allow_unsafe_jscode=True,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
        )
        
        # Enhanced validation and button styling
        try:
            # edited_data = pd.DataFrame(edit_response['data']).reset_index(drop=True)
            # original_data = pd.DataFrame(selected_rows).reset_index(drop=True)
            
            # # Ensure both dataframes have the same columns in the same order
            # if not edited_data.columns.equals(original_data.columns):
            #     # Reorder columns to match
            #     edited_data = edited_data[original_data.columns]
            
            # # Convert all columns to string for comparison to avoid data type issues
            # edited_data_str = edited_data.astype(str)
            # original_data_str = original_data.astype(str)
            
            # # Check if any changes were made by comparing string representations
            # has_changes = not edited_data_str.equals(original_data_str)
            
            # # Alternative comparison method - check row by row
            # if not has_changes:
            #     # Double check with row-by-row comparison
            #     for i in range(len(edited_data)):
            #         for col in edited_data.columns:
            #             orig_val = str(original_data.iloc[i][col])
            #             edit_val = str(edited_data.iloc[i][col])
            #             if orig_val != edit_val:
            #                 has_changes = True
            #                 break
            #         if has_changes:
            #             break
            # edited_data = pd.DataFrame(edit_response['data']).reset_index(drop=True)
            # original_data = pd.DataFrame(selected_rows).reset_index(drop=True)
            # st.write(edited_data['has_po'])
            # st.write(selected_df)
            # Ensure both dataframes have the same columns in the same order
            # if not edited_data.columns.equals(original_data.columns):
            #     # Reorder columns to match
            #     edited_data = edited_data[original_data.columns]

            # # Check if any changes were made using DataFrame.equals()
            # has_changes = not original_data.equals(edited_data)
            
            # Show submit and cancel buttons
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("Submit Changes", key=f"submit_{key_suffix}"):
                    # if has_changes:
                    # st.success(f"✅ Successfully edited {len(edited_data)} rows")
                    # Reset selection and return data
                    st.session_state[reset_key] = True
                    # Store the result in session state to handle fragment rerun
                    st.session_state[f"edit_result_{key_suffix}"] = edit_response['data'].copy()
                    st.session_state[grid_refresh_key] += 1
                    st.rerun()
                    # else:
                    #     st.warning("⚠️ No changes detected. Please modify the data before submitting.")
            
            with col2:
                if st.button("Cancel", key=f"cancel_edit_changes_{key_suffix}"):
                    # Increment the refresh counter to force grid re-render with new key
                    st.session_state[grid_refresh_key] += 1
                    st.info("🔵 Selection cleared. Changes discarded.")
                    st.rerun()
            
            # Check if there's a result to return from session state
            result_key = f"edit_result_{key_suffix}"
            if result_key in st.session_state:
                result = st.session_state[result_key].copy()
                del st.session_state[result_key]  # Clean up
                return result
                        
        except Exception as e:
            st.error(f"Error in edit comparison: {str(e)}")
            return None
            
    else:
        st.warning(f"Please Select {table_name_to_show_on_messages} for Update")
    
    # Fragment functions should not return values - use session state instead
#------------------------------------------------------------------------------------#
# Delete Dataframe Widget
#------------------------------------------------------------------------------------#

@st.fragment
def delete_dataframe(df, height=450, theme='alpine', page_size=20,
                    font_size='16px', font_family='Arial, sans-serif', cell_color='#008080',
                    header_color='#333333', header_font_size='14px', header_font_family='Arial, sans-serif',
                    header_font_weight='600', header_background='#f0f0f0',
                    min_col_width=280, key_suffix="", row_height=50, table_name_to_show_on_messages=""):
    """Delete selected rows with pagination controls and return the deleted data"""
    if df.empty:
        st.info("No data available to delete")
        return None
    
    # Initialize grid refresh counter for cancel functionality
    grid_refresh_key = f"grid_refresh_{key_suffix}"
    if grid_refresh_key not in st.session_state:
        st.session_state[grid_refresh_key] = 0
    
    # Page size will be controlled within the grid pagination
    
    # Generate unique header class for styling
    header_class = f"header-{uuid.uuid4().hex[:8]}"
    
    # Selection mode
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection('multiple', use_checkbox=True)
    gb.configure_side_bar(filters_panel=True, columns_panel=True)
    
    # Configure columns with styling
    for col in df.columns:
        # Calculate minimum width based on header text length
        header_width = len(str(col)) * 12
        col_min_width = max(min_col_width, header_width)
        
        gb.configure_column(
            col,
            editable=False,
            filter=True,
            sortable=True,
            autoSize=False,
            resizable=True,
            headerClass=header_class,
            minWidth=col_min_width,
            width=col_min_width,
            maxWidth=400,
            autoHeight=True,
            wrapText=True,
            cellStyle={
                'textAlign': 'left',
                'fontSize': font_size,
                'fontFamily': font_family,
                'color': cell_color,
                'white-space': 'normal',
                'line-height': '20px',
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'flex-start'
            }
        )
    
    # Configure default column
    gb.configure_default_column(
        flex=1,
        minWidth=min_col_width,
        filter=True,
        autoSize=False,
        resizable=True,
        sortable=True,
        headerClass=header_class,
        cellStyle={
            'textAlign': 'left',
            'fontSize': font_size,
            'fontFamily': font_family,
            'color': cell_color
        }
    )
    
    # Configure grid options using your preferred method
    gb.configure_grid_options(
        domLayout='normal',
        pagination=True,
        paginationPageSize=page_size,
        paginationPageSizeSelector=[10, 20, 50, 100],
        enableCellTextSelection=True,
        ensureDomOrder=True,
        suppressColumnVirtualisation=False,
        suppressRowVirtualisation=False,
        columnSize="autoSize",
        sizeColumnsToFit=False,
        skipHeaderOnAutoSize=False,
        enableColResize=True
    )
    
    grid_options = gb.build()
    
    # Configure sidebar
    grid_options["sideBar"] = {
        "toolPanels": [
            {
                "id": "columns",
                "labelDefault": "Columns",
                "labelKey": "columns",
                "iconKey": "columns",
                "toolPanel": "agColumnsToolPanel"
            },
            {
                "id": "filters",
                "labelDefault": "Filters",
                "labelKey": "filters",
                "iconKey": "filter",
                "toolPanel": "agFiltersToolPanel"
            }
        ]
    }
    
    # Get theme class for proper CSS targeting
    theme_class = {
        'alpine': 'ag-theme-alpine',
        'alpine-dark': 'ag-theme-alpine-dark',
        'balham': 'ag-theme-balham',
        'balham-dark': 'ag-theme-balham-dark',
        'material': 'ag-theme-material',
        'streamlit': 'ag-theme-streamlit'
    }.get(theme, 'ag-theme-alpine')
    
    # Add enhanced CSS for proper styling
    st.markdown(f"""
    <style>
    /* Header styling */
    .{theme_class} .ag-header-cell.{header_class} {{
        background-color: {header_background} !important;
    }}
    
    .{theme_class} .ag-header-cell.{header_class} .ag-header-cell-label {{
        justify-content: center !important;
        display: flex !important;
        align-items: center !important;
        color: {header_color} !important;
        font-size: {header_font_size} !important;
        font-family: {header_font_family} !important;
        font-weight: {header_font_weight} !important;
        text-align: center !important;
    }}
    
    /* Checkbox positioning */
    .{theme_class} .ag-selection-checkbox {{
        margin-right: 8px !important;
    }}
    
    .{theme_class} .ag-cell {{
        display: flex !important;
        align-items: center !important;
        padding: 8px 12px !important;
    }}
    
    /* Row styling */
    .{theme_class} .ag-row {{
        border-bottom: 1px solid #e0e0e0 !important;
    }}
    
    .{theme_class} .ag-row:hover {{
        background-color: #f5f5f5 !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # st.markdown("**Select rows to delete:**")
    st.markdown(
            "<h5 style='color: #FF8C42;'>Select rows to delete:</h5>",
            unsafe_allow_html=True
        )
    
    
    # Create dynamic key using refresh counter
    current_grid_key = f"delete_select_{key_suffix}_{st.session_state[grid_refresh_key]}"
    
    grid_response = AgGrid(
        df.reset_index(drop=True),
        gridOptions=grid_options,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
        fit_columns_on_grid_load=True,
        key=current_grid_key,
        height=height,
        theme=theme,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
    )
    
    selected_rows = grid_response['selected_rows']
    
    if selected_rows is not None and len(selected_rows) > 0:
        selected_df = pd.DataFrame(selected_rows)
        
        st.markdown(f"**{len(selected_df)} rows selected for deletion**")
        
        # Add delete and cancel buttons
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("Delete Selected Rows", key=f"delete_{key_suffix}"):
                # Store the deleted data and trigger processing
                st.session_state[f"deleted_data_{key_suffix}"] = selected_df
                st.rerun()
            
            # Check if we have deleted data to process
            if f"deleted_data_{key_suffix}" in st.session_state:
                deleted_data_to_process = st.session_state[f"deleted_data_{key_suffix}"]
                del st.session_state[f"deleted_data_{key_suffix}"]  # Clean up
                return deleted_data_to_process
                
        with col2:
            if st.button("Cancel", key=f"cancel_delete_{key_suffix}"):
                # Increment the refresh counter to force grid re-render with new key
                st.session_state[grid_refresh_key] += 1
                st.info("🔵 Selection cleared. No changes made.")
                time.sleep(1)
                st.rerun()
    else:
        st.warning(f"Please Select {table_name_to_show_on_messages} for Delete")
    
    return None