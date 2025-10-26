# #==========================================================================#
# #                          Import Libiraries
# #==========================================================================#
import streamlit as st
import sys
import os
import pandas as pd
import numpy as np

import re
import shap
import matplotlib.pyplot as plt
#from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold

#from lightgbm import LGBMClassifier 

import warnings
# Suppress specific FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)




#==========================================================================#
#                          Import Data and functions From main file
#==========================================================================#

sys.path.append(os.path.abspath('../functions.py'))

from functions import ml_model, ml_model_predict, X






Posted_by_dict2 = {
    "Eman Hamdy Enab": 1,
    "Mina Adly":2,
    "Mohamad Taha" : 3,
    "Ahmed Kamel AbdelRazek" :4
}
Page_dict2 = {
     "Dataclin_Group":1, 
     "DataClin_CRO":2, 
     "DataClin_MA":3, 
     "DataClin_SMO":4
 }
 
@st.fragment()
def get_data_from_user2(model):
    model = model
    if 'post' not in st.session_state:
        st.session_state.post = ''
    col1, col2, col3 = st.columns([1,0.5,1])
    with col1:
        Posted_by = st.selectbox("Select oprion", ["Eman Hamdy Enab", "Mina Adly","Mohamad Taha", "Ahmed Kamel AbdelRazek" ])
        eng_rate_yesterday = st.number_input("Engagment Yesterday", value=float(50.0), step=1.0, format="%.2f", placeholder="eng yest",)
    with col3:
        page_name = st.selectbox("Select oprion", ["Dataclin_Group", "DataClin_CRO","DataClin_MA", "DataClin_SMO" ])
        eng_rate_pre_week = st.number_input("Engagment Previous Week", value=float(50.0), step=1.0, format="%.2f", placeholder="eng pre week",)
        
    
    
    post = st.text_input("Enter the post", value=st.session_state.post)
    st.session_state.post = post

        





    
    to_predict = pd.DataFrame(
        {   "Post_title":[""],
            "Posted_by":[0],
            "Page":[0],
            "length":[0],
            "hashtag_count":[0],
            "#ClinicalResearch":[0],
            "#ClinicalTrials":[0],
            "#hiring":[0],
            "#Role_and_respon":[0],
            "#MedicalResearch":[0],
            "#MedicalAdvancem":[0],
            "#Innovation":[0],
            "#Junior_General_":[0],
            "#MedicalWriting":[0],
            "lag_1":[0],
            "lag_7":[0],
            }
        )

    calualte = st.button("Predict Patient Outcome")
    if calualte:
        if (Posted_by and 
            page_name and
            eng_rate_yesterday and
            eng_rate_pre_week and
            post
                  ):
            
            to_predict["Post_title"] = post
            to_predict["Posted_by"] = Posted_by_dict2[Posted_by]
            to_predict["Page"] = Page_dict2[page_name]
            to_predict["length"] = len(page_name)

                        # Function to extract all hashtags using the regex
            def extract_hashtags(text):
                return re.findall(r'#\w+', text)

            hastags = to_predict["Post_title"].apply(extract_hashtags)
            to_predict["hashtag_count"] =  hastags.apply(lambda x : len(x))

            
            to_predict["#ClinicalResearch"] = to_predict["Post_title"].apply(lambda x: 1 if "#ClinicalResearch" in x else 0)
            to_predict["#ClinicalTrials"] = to_predict["Post_title"].apply(lambda x: 1 if "#ClinicalTrials" in x else 0)
            to_predict["#hiring"] = to_predict["Post_title"].apply(lambda x: 1 if "#hiring" in x else 0)
            to_predict["#Role_and_respon"] = to_predict["Post_title"].apply(lambda x: 1 if "#Role_and_respon" in x else 0)
            to_predict["#MedicalResearch"] = to_predict["Post_title"].apply(lambda x: 1 if "#MedicalResearch" in x else 0)
            to_predict["#MedicalAdvancem"] = to_predict["Post_title"].apply(lambda x: 1 if "#MedicalAdvancem" in x else 0)
            to_predict["#Innovation"] = to_predict["Post_title"].apply(lambda x: 1 if "#Innovation" in x else 0)
            to_predict["#Junior_General_"] = to_predict["Post_title"].apply(lambda x: 1 if "#Junior_General_" in x else 0)
            to_predict["#MedicalWriting"] = to_predict["Post_title"].apply(lambda x: 1 if "#MedicalWriting" in x else 0)
            to_predict["lag_1"] = eng_rate_yesterday
            to_predict["lag_7"] = eng_rate_pre_week



            to_predict = to_predict.drop('Post_title', axis=1)
            #st.write(to_predict)
            preds, execution_time = ml_model_predict(model, to_predict)
            st.markdown(f"<h1 style='color: #008080; text-align:center'>The predicted Engagment rate is {np.round(preds[0]*100, 2)} %</h1>", unsafe_allow_html=True)
            st.success(f"The Predection time is: {execution_time:.2f} seconds")
            new_X = pd.concat([X, to_predict],axis=0)
            shap.initjs()
            
           
            st.markdown(f"<h2 style='color: #008080; text-align:center'>SHAP Waterfall Plot for the new prediction</h2>", unsafe_allow_html=True)
            explainer = shap.Explainer(selected_model, new_X)

            # Compute SHAP values (this will return an Explanation object)
            shap_values = explainer(new_X)

            # Select the SHAP values for the last instance (which is an Explanation object)
            instance_shap_values = shap_values[-1]

            # Ensure that we are passing the correct object to the waterfall plot
            if isinstance(instance_shap_values, shap.Explanation):
                plt.figure(figsize=(3, 1))
                shap.plots.waterfall(instance_shap_values)
                
                # Show the plot in Streamlit
                st.pyplot(plt.gcf())
        else:
            st.error("Please fill all fields.")
   

#==========================================================================#
#                          Main App
#==========================================================================#


if __name__ == "__main__":
    logo_path = "./TheLogo2.png"  # Replace with the path to your logo image
    st.sidebar.image(logo_path, use_column_width=True)
    st.sidebar.markdown("<h2 style='color: #008080; text-align:center'>Select a Model</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        model_select = st.sidebar.selectbox(" ", ["LightGBM", "XGBoost"], label_visibility="collapsed")    
    if model_select == "XGBoost":
        train_test_scores_df2, selected_model, ex_time = ml_model("xgb")
    elif model_select == "LightGBM":
        train_test_scores_df2, selected_model, ex_time = ml_model("LighGBM")
   
    st.sidebar.success(f"The Model execution time is: {ex_time:.2f} seconds")

    get_data_from_user2(selected_model)
    # get_data_from_user()

   