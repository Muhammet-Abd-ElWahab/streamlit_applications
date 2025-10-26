#==========================================================================#
#                          Import Libiraries
#==========================================================================#
import sys
# Caution: path[0] is reserved for script path (or '' in REPL)

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.shared import GridUpdateMode
from streamlit_extras.dataframe_explorer import dataframe_explorer 
import os





st.set_page_config(page_title="Home Page",
                   page_icon = "⚕:",
                   layout="wide"
                   )





#==========================================================================#
#                         Import functions
#==========================================================================#


sys.path.append(os.path.abspath('./functions.py'))


#==========================================================================#
#                          Pie charts Functions
#==========================================================================#


if __name__ == "__main__":

    st.image('./TheLogo2.png', use_container_width =True)        
    st.markdown("<h1 style='color: #008080; text-align:center; font-size:80px'>Breast Cancer Survival Prediction</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #008080; text-align:center'>This project aims to leverage machine learning techniques to predict breast cancer patient survival based on clinical, demographic, and treatment-related data. By analyzing a rich dataset containing key diagnostic factors, tumor characteristics, treatment regimens, and genetic markers, the model seeks to provide valuable insights into survival probabilities. The primary goal is to assist medical professionals in identifying high-risk patients and optimizing treatment strategies by predicting patient outcomes. The dataset includes critical features such as hormone receptor status, tumor stage, genetic mutations, and prior treatments, making it a powerful resource for developing predictive models. Machine learning models trained on this dataset can help enhance early prognosis, improve personalized treatment plans, and contribute to better decision-making in oncology. By integrating predictive analytics into breast cancer management, this project supports advancements in precision medicine, ultimately leading to improved patient survival rates and quality of care.</h3>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #008080; text-align:center'>Dataset Description</h1>", unsafe_allow_html=True)
    # st.markdown("<h3 style='color: #008080; text-align:left'>The dataset for this competition (both train and test) was generated from a deep learning model trained on the Cirrhosis Patient Survival Prediction dataset. Feature distributions are close to, but not exactly the same, as the original. Feel free to use the original dataset as part of this competition, both to explore differences as well as to see whether incorporating the original in training improves model performance.</h3>", unsafe_allow_html=True)

    data = {
    "Column": [
        "Age", "Gender", "Sweats", "Weakness", "Anemia", "Decreased_Platelet_Counts",
        "Resistance_TKI", "Elevated_Blast_Cell_Proportion", "Increased_Leucocyte_Count",
        "Unexplained_Hemorrhage", "Spleen_Palpable", "Radiation_Exposure",
        "Previous_Cancer_Treatment", "Genetic_Disorders", "Family_History_Leukemia",
        "Tobacco_Smoke", "Chemical_Exposures", "Frequent_Severe_Infections",
        "Neutrophil_Proportion_High", "Increased_Basophils", "BCR_ABL_Positive",
        "Survival_Status"
    ],
    "Description": [
        "Patient age.",
        "Patient Gender Binary (1 = Male, 0 = Female).",
        "Presence of night sweats (1 = Yes, 0 = No).",
        "General weakness (1 = Yes, 0 = No).",
        "Presence of anemia (1 = Yes, 0 = No).",
        "Decreased platelet counts (1 = Yes, 0 = No).",
        "Resistance to Tyrosine Kinase Inhibitor (1 = Yes, 0 = No).",
        "Elevated proportion of blast cells in the blood (1 = Yes, 0 = No).",
        "Increased leucocyte (white blood cell) count (1 = Yes, 0 = No).",
        "Unexplained hemorrhage (1 = Yes, 0 = No).",
        "Palpable spleen enlargement (1 = Yes, 0 = No).",
        "History of radiation exposure (1 = Yes, 0 = No).",
        "Previous treatment for cancer (1 = Yes, 0 = No).",
        "Presence of genetic disorders (1 = Yes, 0 = No).",
        "Family history of leukemia (1 = Yes, 0 = No).",
        "Exposure to tobacco smoke (1 = Yes, 0 = No).",
        "Exposure to industrial chemicals or solvents.",
        "Frequent and severe infections (1 = Yes, 0 = No).",
        "High neutrophil proportion (1 = Yes, 0 = No).",
        "Increased basophil levels (1 = Yes, 0 = No).",
        "BCR-ABL gene fusion presence (1 = Yes, 0 = No), a marker for CML.",
        "Survival status (1 = Survived, 0 = Deceased)."
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .custom-table {
        font-family: Arial, sans-serif;
        font-size: 16px;
        text-align: center;
        border-collapse: collapse;
        width: 100%;
    }
    .custom-table th, .custom-table td {
        border: 1px solid #ddd;
        padding: 10px;
        text-align: center;
    }
    .custom-table th {
        font-size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Convert DataFrame to HTML and apply styling
st.markdown(df.to_html(index=False, classes="custom-table"), unsafe_allow_html=True)
