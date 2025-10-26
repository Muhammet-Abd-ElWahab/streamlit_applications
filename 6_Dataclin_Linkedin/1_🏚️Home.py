#==========================================================================#
#                          Import Libiraries
#==========================================================================#
import sys
import os
from pathlib import Path
# Caution: path[0] is reserved for script path (or '' in REPL)

import streamlit as st
import pandas as pd
#from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
#from st_aggrid.shared import GridUpdateMode
#from streamlit_extras.dataframe_explorer import dataframe_explorer 





st.set_page_config(page_title="Home Page",
                   page_icon = "⚕:",
                   layout="wide"
                   )





#==========================================================================#
#                         Import functions
#==========================================================================#


sys.path.append(os.path.abspath('./functions.py'))


def make_dcs():
    data = {
        "Column": [
            "male", 
            "age", 
            "education", 
            "currentSmok", 
            "cigsPerDay", 
            "BPMeds", 
            "prevalentStroke", 
            "prevalentHyp", 
            "diabetes", 
            "totChol", 
            "sysBP", 
            "diaBP", 
            "BMI", 
            "heartRate", 
            "glucose", 
            "TenYearCHD"
        ],
        "Description": [
            "Patient Gender Binary (1 = Male, 0 = Female)", 
            "Patient age.", 
            "Patient education level.", 
            "Smoker or not Binary (1 = Yes, 0 = No)", 
            "Number of smoking cigars per day", 
            "Blood Pressure Medications.", 
            "Whether the individual has had a stroke previously Binary (1 = Yes, 0 = No)", 
            "Whether the individual has prevalent hypertension (high blood pressure) Binary (1 = Yes, 0 = No)", 
            "Whether the individual has diabetes. Binary (1 = Yes, 0 = No)", 
            "`Total Cholesterol` The total cholesterol level in the blood", 
            "`Systolic Blood Pressure` The pressure in the arteries when the heart beats", 
            "`Diastolic Blood Pressure` The pressure in the arteries when the heart is at rest between beats.", 
            "`Body Mass Index` A measure of body fat based on height and weight, calculated as weight (kg) / height (m)^2.", 
            "Heartbeats per minute.", 
            "The blood glucose level", 
            "`Ten-Year Coronary Heart Disease Risk` The estimated risk of developing CHD over the next ten years"
        ]
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # colored_header(
    # label="Dataset Description",
    # description="This is a description",
    # color_name="violet-70"
    # )

    st.header('Dataset Description', divider='blue')
    st.markdown("> #### The \"Framingham\" heart disease dataset includes over 4,240 records, 16 columns and 15 attributes. The goal of the dataset is to predict whether the patient has 10-year risk of future (CHD) coronary heart disease:")
    st.subheader('Columns Description', divider='blue')
    # st.write("Notebooks by notebook name:")

    



#==========================================================================#
#                          Pie charts Functions
#==========================================================================#


if __name__ == "__main__":
    
    st.image('./TheLogo2.png', use_column_width=True)        
    st.markdown("<h1 style='color: #008080; text-align:center'>Linkedin Exploratory Data Analysis and Machine learning Project</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #008080; text-align:center'>We have 12 datasets, 4 categories (DataClin, CRO, MA, and SMO), Each category has 3 datasets (Visitors, Followers, Content).</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #008080; text-align:center'>Check Exploratory data analysis from here</h4>", unsafe_allow_html=True)
    # st.markdown("<h3 style='color: #008080; text-align:left'>The dataset for this competition (both train and test) was generated from a deep learning model trained on the Cirrhosis Patient Survival Prediction dataset. Feature distributions are close to, but not exactly the same, as the original. Feel free to use the original dataset as part of this competition, both to explore differences as well as to see whether incorporating the original in training improves model performance.</h3>", unsafe_allow_html=True)
    zip_file = Path("Linkedin.rar")

    # Open the .rar file in binary mode
    with open(zip_file, "rb") as f:
        zip_data = f.read()

    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.download_button(
            label="Download EDA Report as rar File",
            data=zip_data,
            file_name="Linkedin.rar",
            mime="application/x-rar-compressed",  # Correct MIME type for .rar files
            key="krakon"
        )
