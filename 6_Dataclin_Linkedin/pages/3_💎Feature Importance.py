# #==========================================================================#
# #                          Import Libiraries
# #==========================================================================#
import streamlit as st
import sys
import os
import time

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

import shap
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


#from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
#from st_aggrid.shared import GridUpdateMode



# Suppress specific FutureWarnings



#==========================================================================#
#                          Import Data and functions From main file
#==========================================================================#

sys.path.append(os.path.abspath('../functions.py'))

from functions import test_X, ml_model





#==========================================================================#
#                          Shap Values
#==========================================================================#
@st.fragment()
def shap_explainer_chart(_selected_model, chart_type):
    
    start_time = time.time()
    explainer = shap.TreeExplainer(selected_model)
    shap_values = explainer.shap_values(test_X)
    plt.figure(figsize=(3, 1))
    if chart_type =="Bar":
        
        #shap.summary_plot(shap_values, test_X, max_display=20)
        shap.summary_plot(shap_values, test_X, plot_type="bar")
        st.pyplot(plt.gcf())
        
       
    elif chart_type =="Summary":
        shap.summary_plot(shap_values, test_X)
        st.pyplot(plt.gcf())
    else:
       
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            feature = st.selectbox("Select Feature",["Posted_by", "Page", "length", "hashtag_count"], key="depend")
        shap.dependence_plot(str(feature), shap_values, test_X)
        st.pyplot(plt.gcf())
    end_time = time.time()

    # Calculate the execution time
    execution_time = end_time - start_time

    return execution_time
    
#==========================================================================#
#                          Main Application
#==========================================================================#


if __name__ == "__main__":
    logo_path = "./TheLogo2.png"  # Replace with the path to your logo image
    st.sidebar.image(logo_path, use_column_width=True)
    st.sidebar.markdown("<h2 style='color: #008080; text-align:center'>Select a Model</h2>", unsafe_allow_html=True)

    model_select2 = st.sidebar.selectbox(" ", ["LightGBM", "XGBoost"], label_visibility="collapsed", key="second_select") 
    tabs = st.tabs([ "Bar Plot", "Summary Plot", "Dependence Plot"]) #, "Force Plot"
    with tabs[0]:
        if model_select2 == "XGBoost":
            train_test_scores_df2, selected_model, ex_time = ml_model("xgb")
            st.markdown(f"<h2 style='color: #008080; text-align:center'>Features importance using {model_select2} Model.</h2>", unsafe_allow_html=True)
            exe_time = shap_explainer_chart(selected_model, "Bar")
            
            #disply_shap_values(fi, "three")

        elif model_select2 == "LightGBM":
            train_test_scores_df2, selected_model, ex_time = ml_model("LighGBM")
            st.markdown(f"<h2 style='color: #008080; text-align:center'>Features importance using {model_select2} Model.</h2>", unsafe_allow_html=True)
            exe_time  = shap_explainer_chart(selected_model, "Bar")
            
            #disply_shap_values(fi, "four")
    
    with tabs[1]:
        if model_select2 == "XGBoost":
            train_test_scores_df2, selected_model, ex_time = ml_model("xgb")
            st.markdown(f"<h2 style='color: #008080; text-align:center'>Features importance using {model_select2} Model.</h2>", unsafe_allow_html=True)
            exe_time = shap_explainer_chart(selected_model, "Summary")
            st.sidebar.success(f"SHAP execution time is: {exe_time:.2f} seconds")

            #disply_shap_values(fi, "one")
        elif model_select2 == "LightGBM":
            train_test_scores_df2, selected_model, ex_time = ml_model("LighGBM")
            st.markdown(f"<h2 style='color: #008080; text-align:center'>Features importance using {model_select2} Model.</h2>", unsafe_allow_html=True)
            exe_time = shap_explainer_chart(selected_model, "Summary")
            st.sidebar.success(f"SHAP execution time is: {exe_time:.2f} seconds")

    with tabs[2]:
        if model_select2 == "XGBoost":
            train_test_scores_df2, selected_model, ex_time = ml_model("xgb")
            st.markdown(f"<h2 style='color: #008080; text-align:center'>Features importance using {model_select2} Model.</h2>", unsafe_allow_html=True)
            exe_time = shap_explainer_chart(selected_model, "Dependence")
            #st.sidebar.success(f"SHAP execution time is: {exe_time:.2f} seconds")

            #disply_shap_values(fi, "one")
        elif model_select2 == "LightGBM":
            train_test_scores_df2, selected_model, ex_time = ml_model("LighGBM")
            st.markdown(f"<h2 style='color: #008080; text-align:center'>Features importance using {model_select2} Model.</h2>", unsafe_allow_html=True)
            exe_time = shap_explainer_chart(selected_model, "Dependence")
           