# #==========================================================================#
# #                          Import Libiraries
# #==========================================================================#
import sys
import streamlit as st
import pandas as pd
import os
import time

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from st_aggrid.shared import GridUpdateMode


import shap

import warnings
# Suppress specific FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)



#==========================================================================#
#                          Import Data and functions From main file
#==========================================================================#

sys.path.append(os.path.abspath('../functions.py'))

from functions import test_X, ml_model, train_X, X, shap_description


@st.experimental_fragment()
def disply_shap_values(table, key):
    gd = GridOptionsBuilder.from_dataframe(table)
    gd.configure_column("ID", header_name="ID",minWidth=20,groupable=False,filter=True,autoSize=True,
                    resizable=True,
                    # headerStyle={'textAlign': 'center', 'fontSize': '50px', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f0f0f0', 'color': '#008080'},  # Styling for header
                    cellStyle={'textAlign': 'left', 'fontSize': '16px', 'fontFamily': 'Arial, sans-serif','color': '#008080'},
                    headerClass="left-header"
                    
                        )
    gd.configure_column("Feature", header_name="Feature",minWidth=500,groupable=False,filter=True,autoSize=True,
                    resizable=True,
                    # headerStyle={'textAlign': 'center', 'fontSize': '50px', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f0f0f0', 'color': '#008080'},  # Styling for header
                    cellStyle={'textAlign': 'left', 'fontSize': '16px', 'fontFamily': 'Arial, sans-serif','color': '#008080'},
                    headerClass="left-header"
                    
                        )
    gd.configure_column("Mean(|SHAP VALUES|)", header_name="Mean(|SHAP VALUES|)",minWidth=350,groupable=True,filter=True,autoSize=False,
                    resizable=True,
                    # headerStyle={'textAlign': 'center', 'fontSize': '50px', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f0f0f0', 'color': '#008080'},  # Styling for header
                    cellStyle={'textAlign': 'left', 'fontSize': '16px', 'fontFamily': 'Arial, sans-serif','color': '#008080'},
                    headerClass="left-header"
                    
                        )
    gd.configure_default_column(
                    filter=True,autoSize=False,
                    resizable=True,
                    # headerStyle={'textAlign': 'center', 'fontSize': '50px', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f0f0f0', 'color': '#008080'},  # Styling for header
                    cellStyle={'textAlign': 'left', 'fontSize': '16px', 'fontFamily': 'Arial, sans-serif','color': '#008080'},
                    headerClass="left-header"
                    )

    gridoptions = gd.build()
    gridoptions['domLayout'] = 'normal'
    
    # Configure grid to fill width
    gridoptions['defaultColDef'] = {
        'flex': 1,
        'minWidth': 100,
        'resizable': True,
        'filter': True,
        'sortable': True,
        'headerClass': 'left-header'
    }
    
    # Add custom CSS for left-aligned headers
    st.markdown("""
    <style>
    .left-header .ag-header-cell-label {
        justify-content: left !important;
    }
    </style>
    """, unsafe_allow_html=True)
    # Display the custom CSS
    
    grid_table = AgGrid(table.reset_index(),gridOptions=gridoptions,
                update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
                height = 490,
                allow_unsafe_jscode=True,
                enable_enterprise_modules = True,
                theme = 'alpine',columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, key=key)


#==========================================================================#
#                          Shap Values
#==========================================================================#
@st.experimental_fragment()
@st.cache_data()
def shap_explainer_chart(_selected_model, chart_type, number):

    start_time = time.time()
    # st.write(_selected_model)
    explainer = shap.TreeExplainer(selected_model)

    # calculate shap values. This is what we will plot.
    # Calculate shap_values for all of val_X rather than a single row, to have more data for plot.
    shap_values = explainer.shap_values(test_X)
    mean_abs_shap = np.mean(np.abs(shap_values), axis=1)
    mean_abs_shap_df = pd.DataFrame(mean_abs_shap, columns=test_X.columns)


    mean_abs_shap_df = pd.DataFrame(mean_abs_shap, columns=test_X.columns)

    # Compute mean absolute SHAP values for feature importance
    feature_importance = mean_abs_shap_df.mean().sort_values(ascending=False)
    feature_importance = pd.DataFrame(feature_importance).reset_index()
    feature_importance.reset_index(inplace=True)
    feature_importance.columns = ["ID", "Feature", "Mean(|SHAP VALUES|)"]
    plt.figure(figsize=(1, 1))
    if chart_type =="Bar":
        shap.summary_plot(shap_values, test_X, show=False, class_names=["Deceased","Survived"])
        plt.title('SHAP Bar Plot', fontsize=20, pad=40, color='#008080')
        plt.tight_layout()
        st.pyplot(plt.gcf())
        
        # TODO_ it's completed, but we will hide it untile study the interpretation of this plot
    # elif chart_type == "force":
    #     # feature = st.selectbox('Select feature for dependence plot:', X.columns)
    #     fig, ax = plt.subplots()
    #     shap.initjs()
    #     force_plot = shap.force_plot(explainer.expected_value[1], shap_values[1], test_X)
    #     shap_html = f"<head>{shap.getjs()}</head><body>{force_plot.html()}</body>"
    #     st.components.v1.html(shap_html, height=300)
    elif chart_type =="Summary":
        
        shap.summary_plot(shap_values[1], test_X, show=True, class_names=["Deceased","Survived"])
        plt.title('SHAP Summary Plot', fontsize=20, pad=40, color='#008080')
        import matplotlib.patches as mpatches
        red_patch = mpatches.Patch(color='red', label='Survived')
        blue_patch = mpatches.Patch(color='blue', label='Deceased')

        plt.legend(handles=[blue_patch, red_patch], loc='lower right')
        plt.tight_layout()
        st.pyplot(plt.gcf())
    elif chart_type == "Decision":
        # st.markdown("<h5 style='color: #008080; text-align:center'>SHAP Decision Plot</h5>", unsafe_allow_html=True)
        
        # Compute SHAP values
        shap_values = explainer.shap_values(test_X)

        # Select SHAP values for "Survived" class (class index 1)
        shap_values_class_1 = shap_values[1]

        # Create decision plot
        fig, ax = plt.subplots(figsize=(10, 6))
        shap.decision_plot(
            explainer.expected_value[1],  # Expected value for class 1
            shap_values_class_1, 
            feature_names=list(test_X.columns)
        )

        # Display in Streamlit
        # st.pyplot(fig)
        plt.title('SHAP Decision Plot', fontsize=20, pad=40, color='#008080')
        plt.tight_layout()
        st.pyplot(plt.gcf())
    
    end_time = time.time()

    # Calculate the execution time
    execution_time = end_time - start_time

    return execution_time, feature_importance.iloc[:10]
    










# Example usage:
# st.markdown(shap_description("SHAP Bar Plot", is_medical=True), unsafe_allow_html=True)







import streamlit as st

# def shap_description(chart_type):
#     descriptions = {
#         "SHAP Bar Plot": """
#     <div style="border: 2px solid #13B3E7; border-radius:10px; padding: 15px; font-family: 'Arial', sans-serif; font-size: 14px; background: #F9FAFB;">
#     <h2 style="color: #13B3E7; text-align: center;">SHAP Bar Plot Interpretation</h2>

#     ---

#     ### 1. **Feature Importance Ranking**
#     - Displays **average absolute SHAP values**.
#     - Higher bars indicate **more important features**.
#     - Helps identify **key drivers** of predictions.

#     ---

#     ### 2. **Insights**
#     - **Feature order**: Sorted by importance.
#     - **Magnitude**: Larger bars mean stronger influence.
#     - Useful for **feature selection** in modeling.

#     ---

#     <h3 style="color: #13B3E7;">Practical Applications</h3>
#     - Identify **critical features** affecting predictions.
#     - Guide **feature engineering** efforts.
#     - Compare models based on feature importance.
#     </div>
#     """,

#         "SHAP Summary Plot": """
#     <div style="border: 2px solid #13B3E7; border-radius:10px; padding: 15px; font-family: 'Arial', sans-serif; font-size: 14px; background: #F9FAFB;">
#     <h2 style="color: #13B3E7; text-align: center;">SHAP Summary Plot Interpretation</h2>

#     ---

#     ### 1. **Feature Influence & Distribution**
#     - Each dot represents a **data instance**.
#     - X-axis: **SHAP value (impact on model output)**.
#     - Y-axis: **Feature name** (sorted by importance).

#     ---

#     ### 2. **Color & Spread Meaning**
#     - **Color**: Represents feature values (blue = low, red = high).
#     - **Spread**: Shows how **variable** the impact of each feature is.
#     - **Densely packed points** mean **consistent influence**.

#     ---

#     <h3 style="color: #13B3E7;">Practical Applications</h3>
#     - Understand **how features influence predictions**.
#     - Spot **non-linear effects** by checking spread.
#     - Compare feature importance across multiple cases.
#     </div>
#     """,

#         "SHAP Decision Plot": """
#     <div style="border: 2px solid #13B3E7; border-radius:10px; padding: 15px; font-family: 'Arial', sans-serif; font-size: 14px; background: #F9FAFB;">
#     <h2 style="color: #13B3E7; text-align: center;">SHAP Decision Plot Interpretation</h2>

#     ---

#     ### 1. **Path Analysis**
#     - **Shows prediction path** for each instance.
#     - Reveals **feature contribution sequence**.
#     - Demonstrates **cumulative effects** as features are added.

#     ---

#     ### 2. **Feature Impacts**
#     - **Line slopes**: Indicate the **magnitude** of each feature’s impact.
#     - **Color**: Represents the identity of the feature.
#     - **Crossing lines**: Show how **feature importance** changes over the course of the prediction.

#     ---

#     ### 3. **Model Behavior**
#     - Highlights **overall prediction patterns**.
#     - Identifies **key decision points** where the model’s outcome changes.
#     - Marks **feature value thresholds** that influence predictions.

#     ---

#     <h3 style="color: #13B3E7;">Practical Applications</h3>
#     - **Analyze decision paths** to understand how the model reaches its conclusions.
#     - **Compare similar instances** to identify patterns.
#     - **Identify critical features** that influence predictions.
#     - **Validate model logic** by examining how feature contributions evolve.
#     </div>
#     """,

#         "SHAP Waterfall Plot": """
#     <div style="border: 2px solid #13B3E7; border-radius:10px; padding: 15px; font-family: 'Arial', sans-serif; font-size: 14px; background: #F9FAFB;">
#     <h2 style="color: #13B3E7; text-align: center;">SHAP Waterfall Plot Interpretation</h2>

#     ---

#     ### 1. **Explaining a Single Prediction**
#     - Visualizes how a **single instance** was predicted.
#     - Starts from the **baseline prediction**.
#     - Shows **how each feature pushes the prediction up or down**.

#     ---

#     ### 2. **Feature Contributions**
#     - **Red bars**: Increase the prediction.
#     - **Blue bars**: Decrease the prediction.
#     - The final prediction is reached **step by step**.

#     ---

#     <h3 style="color: #13B3E7;">Practical Applications</h3>
#     - **Understand individual predictions** in detail.
#     - **Debug model behavior** for specific cases.
#     - **Explain decisions** to stakeholders in an interpretable way.
#     </div>
#     """
#     }

#     # Display the selected description
#     st.markdown(descriptions.get(chart_type, "Invalid selection"), unsafe_allow_html=True)


#==========================================================================#
#                          Main Application
#==========================================================================#


if __name__ == "__main__":
    logo_path = "./TheLogo2.png"  # Replace with the path to your logo image
    st.sidebar.image(logo_path, use_column_width =True)
    # st.sidebar.markdown("<h2 style='color: #008080; text-align:center'>Select a Model</h2>", unsafe_allow_html=True)

    # model_select2 = st.sidebar.selectbox(" ", ["LightGBM", "XGBoost"], label_visibility="collapsed", key="second_select") 
    tabs = st.tabs(["Top 10 Features", "Bar Plot", "Summary Plot", "Decision Plot"]) #
    with tabs[0]:
        all_scores_df2, train_test_scores_df2, selected_model, ex_time = ml_model("LighGBM")
        exe_time, fi  = shap_explainer_chart(selected_model, "Barr", 5)
        st.markdown(f"<h2 style='color: #008080; text-align:center'>The Top 10 Features that Influenced the Model.</h2>", unsafe_allow_html=True)

        disply_shap_values(fi, "three")
    with tabs[1]:
        # if model_select2 == "XGBoost":
        #     # all_scores_df2, train_test_scores_df2, selected_model, ex_time = ml_model("xgb")
        #     # exe_time, fi = shap_explainer_chart(selected_model, "Bar", 4)

        #     # st.markdown(f"<h2 style='color: #008080; text-align:center'>The Top 5 Features that Influenced the {model_select2} Model.</h2>", unsafe_allow_html=True)
        #     # disply_shap_values(fi, "three")
            
        #     all_scores_df2, train_test_scores_df2, selected_model, ex_time = ml_model("LighGBM")
        #     exe_time, fi  = shap_explainer_chart(selected_model, "Bar", 4)
            
        #     st.markdown(f"<h2 style='color: #008080; text-align:center'>The Top 5 Features that Influenced the {model_select2} Model.</h2>", unsafe_allow_html=True)
        #     disply_shap_values(fi, "four")

        # elif model_select2 == "LightGBM":
        #     all_scores_df2, train_test_scores_df2, selected_model, ex_time = ml_model("xgb")
        #     exe_time, fi  = shap_explainer_chart(selected_model, "Bar", 5)
            
        #     st.markdown(f"<h2 style='color: #008080; text-align:center'>The Top 5 Features that Influenced the {model_select2} Model.</h2>", unsafe_allow_html=True)
        #     disply_shap_values(fi, "four")
        all_scores_df2, train_test_scores_df2, selected_model, ex_time = ml_model("LighGBM")
        exe_time, fi  = shap_explainer_chart(selected_model, "Bar", 5)
                
        # st.markdown(f"<h2 style='color: #008080; text-align:center'>The Top 5 Features that Influenced the Model.</h2>", unsafe_allow_html=True)
        # disply_shap_values(fi, "four")
        st.markdown(shap_description("SHAP Bar Plot", is_medical=True), unsafe_allow_html=True)

    with tabs[2]:
        # if model_select2 == "XGBoost":
        #     # all_scores_df2, train_test_scores_df2, selected_model, ex_time = ml_model("xgb")
        #     # exe_time, fi = shap_explainer_chart(selected_model, "Summary", 1)
        #     # st.sidebar.success(f"SHAP execution time is: {exe_time:.2f} seconds")
        #     # st.markdown(f"<h2 style='color: #008080; text-align:center'>The Top 5 Features that Influenced the {model_select2} Model.</h2>", unsafe_allow_html=True)

        #     all_scores_df2, train_test_scores_df2, selected_model, ex_time = ml_model("xgb")
        #     exe_time, fi = shap_explainer_chart(selected_model, "Summary", 1)
        #     st.sidebar.success(f"SHAP execution time is: {exe_time:.2f} seconds")
        #     st.markdown(f"<h2 style='color: #008080; text-align:center'>The Top 5 Features that Influenced the {model_select2} Model.</h2>", unsafe_allow_html=True)

        #     disply_shap_values(fi, "onee")

        # elif model_select2 == "LightGBM":
        #     all_scores_df2, train_test_scores_df2, selected_model, ex_time = ml_model("LighGBM")
        #     exe_time, fi = shap_explainer_chart(selected_model, "Summary", 2)
        #     st.sidebar.success(f"SHAP execution time is: {exe_time:.2f} seconds")
        #     st.markdown(f"<h2 style='color: #008080; text-align:center'>The Top 5 Features that Influenced the {model_select2} Model.</h2>", unsafe_allow_html=True)

        #     disply_shap_values(fi, "two")
        # elif model_select2 == "Randomforest":
        #     all_scores_df2, train_test_scores_df2, selected_model, ex_time = ml_model("rf")
        #     exe_time = shap_explainer_chart(selected_model, "Summary", 3)
        #     st.sidebar.success(f"SHAP execution time is: {exe_time:.2f} seconds")
        all_scores_df2, train_test_scores_df2, selected_model, ex_time = ml_model("LighGBM")
        exe_time, fi = shap_explainer_chart(selected_model, "Summary", 2)
        st.sidebar.success(f"SHAP execution time is: {exe_time:.2f} seconds")
        
        # st.markdown(f"<h2 style='color: #008080; text-align:center'>The Top 5 Features that Influenced the Model.</h2>", unsafe_allow_html=True)
        # disply_shap_values(fi, "two")
        
        # For a technical audience who wants the original explanation
        st.markdown(shap_description("SHAP Summary Plot", is_medical=True), unsafe_allow_html=True)

    # TODO_ Hide untill finish interpreting of plot
    with tabs[3]:
        all_scores_df2, train_test_scores_df2, selected_model, ex_time = ml_model("LighGBM")
        exe_time, fi  = shap_explainer_chart(selected_model, "Decision", 7)
        
        # st.markdown(f"<h2 style='color: #008080; text-align:center'>The Top 5 Features that Influenced the Model.</h2>", unsafe_allow_html=True)
        # disply_shap_values(fi, "three")
        # shap_description("SHAP Decision Plot")
        # For a non-technical audience looking at your SHAP Bar Plot
        st.markdown(shap_description("SHAP Decision Plot", is_medical=True), unsafe_allow_html=True)



