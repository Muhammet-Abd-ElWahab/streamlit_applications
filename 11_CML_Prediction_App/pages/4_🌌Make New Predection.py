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
import shap

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold

from lightgbm import LGBMClassifier 

import warnings
# Suppress specific FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)




#==========================================================================#
#                          Import Data and functions From main file
#==========================================================================#

sys.path.append(os.path.abspath('../functions.py'))

from functions import final_model, X, y


#==========================================================================#
#                          Coolect Data Function
#==========================================================================#

            
def get_data_from_user(model_select):
    with st.form("user_input_form"):
        st.markdown("### Enter Patient Data")

        col1, col2, col3 = st.columns(3)

        with col1:
            Age_In_Years = st.number_input("Age", value=30, step=1, format="%d")
            Gender = st.selectbox("Gender", options=["Male", "Female"])  # Replace with X.Gender.unique()
            Sweats = st.radio("Sweats", options=["Yes", "No"])  # Replace with X.Sweats.unique()
            Weakness = st.radio("Weakness", options=["Yes", "No"])  # Replace with X.Weakness.unique()

        with col2:
            Anemia = st.radio("Anemia", options=["Yes", "No"])  # Replace with X.Anemia.unique()
            Decreased_Platelet_Counts = st.radio("Decreased Platelet Counts", options=["Yes", "No"])
            Resistance_TKI = st.radio("Resistance TKI", options=["Yes", "No"])
            Elevated_Blast_Cell_Proportion = st.radio("Elevated Blast Cell Proportion", options=["Yes", "No"])

        with col3:
            Increased_Leucocyte_Count = st.radio("Increased Leucocyte Count", options=["Yes", "No"])
            Unexplained_Hemorrhage = st.radio("Unexplained Hemorrhage", options=["Yes", "No"])
            Spleen_Palpable = st.radio("Spleen Palpable", options=["Yes", "No"])

        # ✅ Submit button inside the form
        submitted = st.form_submit_button("Submit")

        # ✅ Ensure the form processes user input
        if submitted:
            if Age_In_Years < 17:
                st.error("Age must be 17 or above.")
            elif Age_In_Years and Gender and Sweats and Weakness and Anemia and Decreased_Platelet_Counts and Resistance_TKI and Elevated_Blast_Cell_Proportion and Increased_Leucocyte_Count and Unexplained_Hemorrhage and Spleen_Palpable:
                if Gender == "Male":
                    Gender = 1
                else:
                    Gender = 0
                user_data = pd.DataFrame({
                    "Age": [Age_In_Years],
                    "Gender": [Gender],
                    "Sweats": [Sweats],
                    "Weakness": [Weakness],
                    "Anemia": [Anemia],
                    "Decreased_Platelet_Counts": [Decreased_Platelet_Counts],
                    "Resistance_TKI": [Resistance_TKI],
                    "Elevated_Blast_Cell_Proportion": [Elevated_Blast_Cell_Proportion],
                    "Increased_Leucocyte_Count": [Increased_Leucocyte_Count],
                    "Unexplained_Hemorrhage": [Unexplained_Hemorrhage],
                    "Spleen_Palpable": [Spleen_Palpable]
                })
                user_data = user_data.replace({"Yes": 1, "No": 0})
                
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
    st.sidebar.image(logo_path, use_container_width =True)
    model_select = st.sidebar.selectbox(" ", ["LightGBM", "XGBoost", "Randomforest", "LogisticRegression"], label_visibility="collapsed") 
    # st.write(X.columns)
    # st.write(X)
    get_data_from_user(model_select)

   
