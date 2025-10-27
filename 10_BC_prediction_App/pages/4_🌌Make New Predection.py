# #==========================================================================#
# #                          Import Libiraries
# #==========================================================================#
from re import S
import sys

import streamlit as st
import pandas as pd
import os
import pandas as pd 
import numpy as np


from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold

from lightgbm import LGBMClassifier 

import warnings
# Suppress specific FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)




#==========================================================================#
#                          Import Data and functions From main file
#==========================================================================#

sys.path.append(os.path.abspath('../functions.py'))

from functions import final_model, X,full_df, clean_data







#==========================================================================#
#                          Coolect Data Function
#==========================================================================#
#
# @st.cache_data()    
# def ml_model_run(dataf):
            
            
def get_data_from_user(model_select):
    with st.form("user_input_form"):
        # st.markdown("### Enter Patient Data")

            
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<h4 style='color: #008080; text-align:center'>Patient & Tumor Information</h4>", unsafe_allow_html=True)
            age_at_diagnosis = st.number_input("Age", value=30, step=1, format="%d")
            tumor_size_cm = st.number_input("Tumor Size (cm)", value=30.0, step=0.1, format="%.2f")
            tumor_grade = st.selectbox("Tumor Grade", options=full_df.tumor_grade.unique())
            tumor_grade = int(tumor_grade)

            lymphovascular_invasion = st.radio("Lymphovascular Invasion", options=["Yes", "No"]) 
            perineural_invasion = st.radio("Perineural Invasion", options=["Yes", "No"]) 
            metastasis = st.radio("Metastasis", options=["Yes", "No"])  
            recurrence = st.radio("Recurrence", options=["Yes", "No"])  

        with col2:
            st.markdown("<h4 style='color: #008080; text-align:center'>Cancer Markers & Treatment</h4>", unsafe_allow_html=True)
            er_status = st.selectbox("ER Status", options=full_df.er_status.unique()) 
            pr_status = st.selectbox("PR Status", options=full_df.pr_status.unique()) 
            her2_status = st.selectbox("HER2 Status", options=full_df.her2_status.unique()) 
            tumor_type = st.selectbox("Tumor Type", options=full_df.tumor_type.unique()) 

            chemotherapy_type = st.selectbox("Chemotherapy Type", options=full_df.chemotherapy_type.unique())  
            radiotherapy_type = st.selectbox("Radiotherapy Type", options=full_df.radiotherapy_type.unique())  
            chemotherapy = st.radio("Received Chemotherapy?", options=["Yes", "No"]) 

        with col3:
            st.markdown("<h4 style='color: #008080; text-align:center'>Lifestyle & Personal Factors</h4>", unsafe_allow_html=True)
            has_children = st.radio("Has Children?", options=["Yes", "No"]) 
            breastfeeding = st.radio("Breastfeeding History", options=["Yes", "No"])  
            physical_activity = st.radio("Physically Active?", options=["Yes", "No"]) 
            smoking = st.radio("Smoking Habit", options=["Yes", "No"])
            alcohol_consumption = st.radio("Alcohol Consumption", options=["Yes", "No"])


        # ✅ Submit button inside the form
        submitted = st.form_submit_button("Submit")

        # ✅ Ensure the form processes user input
        if submitted:
            if age_at_diagnosis < 17:
                st.error("Age must be 17 or above.")
            elif age_at_diagnosis and tumor_size_cm and tumor_grade and lymphovascular_invasion and perineural_invasion and metastasis and recurrence and er_status and pr_status and her2_status and tumor_type and chemotherapy_type and radiotherapy_type and has_children and chemotherapy and physical_activity and smoking and alcohol_consumption and breastfeeding:
                user_data = pd.DataFrame({
                    "age_at_diagnosis": [age_at_diagnosis], 
                    "tumor_size_cm": [tumor_size_cm],
                    "tumor_grade": [tumor_grade],
                    "lymphovascular_invasion": [lymphovascular_invasion],
                    "perineural_invasion": [perineural_invasion],
                    "metastasis": [metastasis],
                    "recurrence": [recurrence],
                    "er_status": [er_status],
                    "pr_status": [pr_status],
                    "her2_status": [her2_status],
                    "tumor_type": [tumor_type],
                    "chemotherapy_type": [chemotherapy_type],
                    "radiotherapy_type": [radiotherapy_type],
                    "has_children": [has_children],
                    "chemotherapy": [chemotherapy],
                    "physical_activity": [physical_activity],
                    "smoking": [smoking],
                    "alcohol_consumption": [alcohol_consumption],
                    "breastfeeding": [breastfeeding]
                })
                user_data = user_data.replace({"Yes": 1, "No": 0})
                user_data = clean_data(user_data)
                # st.write(user_data)   
                new_pred,pre_propability, execution_time = final_model(model_select, user_data)    
                st.sidebar.success(f"The Model execution time is: {execution_time:.2f} seconds")
                # st.write(new_pred,pre_propability, execution_time)
                pre_propability = pd.DataFrame(pre_propability)
                target_reverse_mapping = {
                    0:'Deceased',
                    1:'Survived'
                }
                # st.write()
                st.markdown(f"<h2 style='color: #008080; text-align:center; border: 2px solid red;border-radius: 30px;'>The predicted Outcome for this patient is: {target_reverse_mapping[new_pred[0]]} </h2>", unsafe_allow_html=True)
                st.markdown(f"<h6 style='color: #008080; text-align:center'></h6>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='color: #008080; text-align:center'>The predicted Outcome Probabilities are:</h3>", unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                with col2:
                    st.markdown(f"<h5 style='color: #008080; text-align:center'> Deceased {round(pre_propability.loc[0,0]*100, 2) }%</h5>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<h5 style='color: #008080; text-align:center'> Survived {round(pre_propability.loc[0,1]*100, 2) }%</h5>", unsafe_allow_html=True)

            else:
                st.error("Please fill all fields.")
            
            # st.success("Form Submitted Successfully!")
            # st.write("### User Input Data")
            # st.json(user_data)  # ✅ Display user input in JSON format


#==========================================================================#
#                          Main App
#==========================================================================#


if __name__ == "__main__":
    logo_path = "./TheLogo2.png"  # Replace with the path to your logo image
    st.sidebar.image(logo_path, use_column_width  =True)
    model_select = st.sidebar.selectbox(" ", ["LightGBM", "XGBoost", "Randomforest", "LogisticRegression"], label_visibility="collapsed") 
    # st.write(X.columns)
    # st.write(X)
    st.markdown("<h1 style='color: #008080; text-align:left'>Enter Patient Data</h1>", unsafe_allow_html=True)
    get_data_from_user(model_select)

   
