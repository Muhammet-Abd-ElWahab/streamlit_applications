#==========================================================================#
#                          Import Libiraries
#==========================================================================#
import sys
# Caution: path[0] is reserved for script path (or '' in REPL)
from streamlit_extras.colored_header import colored_header 
from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.shared import GridUpdateMode
from streamlit_extras.dataframe_explorer import dataframe_explorer 
import os
import yaml
import time

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import plotly.express as px
import plotly.express as px
import plotly.graph_objects as go
import datetime




# import machine learning libiraries
from sklearn.metrics import make_scorer, confusion_matrix, precision_score, recall_score, accuracy_score, classification_report, f1_score,roc_auc_score, roc_curve, auc, log_loss
from sklearn.linear_model import LogisticRegression

from sklearn.preprocessing import StandardScaler, MinMaxScaler, label_binarize, OrdinalEncoder, OneHotEncoder
from sklearn.feature_selection import mutual_info_classif

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold

import xgboost as xgb
from lightgbm import LGBMClassifier 
from sklearn.ensemble import RandomForestClassifier


import re
import shap
import optuna

import warnings
# Suppress specific FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)




#==========================================================================#
#                          Charts Functions
#==========================================================================#



def bar_chart(df, xx, yy,  txt="", labls={},hover={}, colors=[], hight=600, wdth=900, ttle="ttle",xtitle="xtitle" , ytitle="ytitle" ,colour=None, bg=0.6, bgg=0.1, leg=None, box=False,yscale=False,yscale_percentage=False, start=-1, end=1):
    if box:
        fig = px.box(df,  x=xx, y=yy, color=colour,
            color_discrete_sequence=colors,height=hight, width=wdth
            )
    elif colour ==None:
        fig = px.bar(df, x=xx, y=yy, barmode='group',text=txt,
             labels=labls,
             hover_data=hover,
             title=ttle,
            color_discrete_sequence=colors,
                     height=hight, width=wdth)
    else:
        fig = px.bar(df, x=xx, y=yy, color=colour, barmode='group',text=txt,
                     labels=labls,
                     hover_data=hover,
                     title=ttle,
                     color_discrete_sequence=colors,height=hight, width=wdth)


    if box == False:
        fig.update_traces(textfont_size=15, textposition='inside')
    
    fig.update_layout(
        legend_title_text=leg,
        #background 
        # plot_bgcolor="white",  #background color
        bargap=bg,  # Gap between bars
        bargroupgap=bgg, 
    
        # Title
         title={'text': ttle, 'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}, #title center and size
         title_font_size=22,  # Title font size
    
        # Xaxis
        xaxis=dict(
            title=xtitle,  # Example X axis title
            titlefont_size=18,  # Size of the X axis title font
            tickfont_size=12,   # Size of the X axis tick labels font
            showline=True,  # Show x-axis line
            showgrid=False, # showgrid
            gridcolor="lightgray", #grid color
            
        ),
        yaxis=dict(
            title=ytitle,  # Example Y axis title
            titlefont_size=18,  # Size of the Y axis title font
            tickfont_size=12,   # Size of the Y axis tick labels font
         
            showgrid=True, # showgrid
            
        ),

    legend=dict(
                font_size=14,  # Size of the legend font
                
            ),
        # font
        font=dict(
            family='Arial', size=14  # Overall font size
        )
    )
    if yscale_percentage and yscale:
        fig.update_xaxes(title_text=xtitle, # Y axisTitle
                         zeroline=True,
                         showline=True,  # Show y-axis line
                        linecolor='gray',
                        titlefont_size=18,  # Set the title font size (optional)
                        titlefont_color="#008080",  # Set the title font color (optional)
                         )
        fig.update_yaxes(title_text=ytitle, # Y axisTitle
                         range=[start, end],
                         tickformat='.0%',
                         zeroline=True,
                         showline=True,  # Show y-axis line
                         linecolor='gray',  # Color of the y-axis line
                         titlefont_size=18,  # Set the title font size (optional)
                        titlefont_color="#008080",  # Set the title font color (optional)         )
                        )
    elif yscale_percentage:
        fig.update_xaxes(title_text=xtitle, # Y axisTitle
                         zeroline=True,
                         showline=True,  # Show y-axis line
                        linecolor='gray',
                        titlefont_size=18,  # Set the title font size (optional)
                        titlefont_color="#008080",  # Set the title font color (optional)
                         )
        fig.update_yaxes(title_text=ytitle, # Y axisTitle
                         zeroline=True,
                         tickformat='.0%',
                         showline=True,  # Show y-axis line
                         linecolor='gray',  # Color of the y-axis line
                         titlefont_size=16,  # Set the title font size (optional)
                        titlefont_color="#008080",  # Set the title font color (optional)         )
                        )
    elif yscale:
        fig.update_xaxes(title_text=xtitle, # Y axisTitle
                         zeroline=True,
                         showline=True,  # Show y-axis line
                        linecolor='gray',
                        titlefont_size=18,  # Set the title font size (optional)
                        titlefont_color="#008080",  # Set the title font color (optional)
                         )
        fig.update_yaxes(title_text=ytitle, # Y axisTitle
                         range=[start, end],
                         zeroline=True,
                         showline=True,  # Show y-axis line
                         linecolor='gray',  # Color of the y-axis line
                         titlefont_size=18,  # Set the title font size (optional)
                        titlefont_color="#008080",  # Set the title font color (optional)         )
                        )
    else:
        fig.update_xaxes(title_text=xtitle, # Y axisTitle
                         showline=True,  # Show y-axis line
                        linecolor='gray',
                        titlefont_size=18,  # Set the title font size (optional)
                        titlefont_color="#008080",  # Set the title font color (optional)
                         )
        
        fig.update_yaxes(title_text=ytitle, # Y axisTitle
                         showline=True,  # Show y-axis line
                         linecolor='gray',  # Color of the y-axis line
                         titlefont_size=18,  # Set the title font size (optional)
                        titlefont_color="#008080",  # Set the title font color (optional)         )
        )
        #  Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)


#==========================================================================#
#                          Data Cleaning 1 Function
#==========================================================================#
# function to clean data 

target_mapping = {
    'C':0,
    'CL':1,
    'D':2
}

target_reverse_mapping = {
    0:'C',
    1:'CL',
    2:'D'
}


@st.cache_data()
def wrangle(dfff):
    df = dfff.copy()
    # Add new Age column in years
    df["Age_In_Years"] = df['Age'] / 365.25
    
    # Change data types to boolean for better ML handling
    df["Ascites"] = df["Ascites"].apply(lambda x: 0 if x == "N" else 1).astype("int")
    df["Hepatomegaly"] = df["Hepatomegaly"].apply(lambda x: 0 if x == "N" else 1).astype("int")
    df["Spiders"] = df["Spiders"].apply(lambda x: 0 if x == "N" else 1).astype("int")
    df["Edema"] = df["Edema"].apply(lambda x: 0 if x == "N" else 1).astype("int")
    df["Drug"] = df["Drug"].apply(lambda x: 0 if x == "Placebo" else 1).astype("int")
    df["Sex"] = df["Sex"].apply(lambda x: 0 if x == "F" else 1).astype("int")
    
    
    # Drop N_Days to avoid Data leakage
    if 'N_Days' in df.columns:
        df.drop(['N_Days'],axis=1,inplace=True)
    if 'Status' in df.columns:
        df.Status = df.Status.map(target_mapping)
        df.Status = df.Status.astype(int)
    return df.copy()


#==========================================================================#
#                          Read Data
#==========================================================================#


df = pd.read_csv('./Data/modeling.csv')
# df_test = pd.read_csv('test.csv')

# df_clean = wrangle(df)
# df_test_clean = wrangle(df_test)








#==========================================================================#
#                          ML Wrangle Function
#==========================================================================#


# def ml_wrangle(dff):
#     df = dff.copy()
#     # 4.1.1 Flag for normal Bilirubin levels Bilirubin_Normal column
#     df["Bilirubin_Normal"] = df["Bilirubin"].apply(lambda x: 0 if x < 0.1 or x > 1.2 else 1).astype("int")

#     #4.1.2 Flag for normal Cholesterol levels Cholesterol_Normal column¶
#     df["Cholesterol_Normal"] = df["Cholesterol"].apply(lambda x: 0 if x > 200 else 1).astype("int")
    
#     #4.1.3 Flag for normal Albumin levels Albumin_Normal column¶
#     df["Albumin_Normal"] = df["Albumin"].apply(lambda x: 0 if x < 3.5 or x > 5 else 1).astype("int")

#     #4.1.4 Flag for normal Copper levels Copper_Normal column
#     df["Copper_Normal"] = df["Copper"].apply(lambda x: 0 if x < 70 or x > 150 else 1).astype("int")

#     #4.1.5 Flag for normal Alk_Phos levels Alk_Phos_Normal column
#     df["Alk_Phos_Normal"] = df["Alk_Phos"].apply(lambda x: 0 if x < 40 or x > 150 else 1).astype("int")

#     #4.1.6 Flag for normal SGOT levels SGOT_Normal column¶
#     df["SGOT_Normal"] = df["SGOT"].apply(lambda x: 0 if x < 8 or x > 40 else True).astype("int")

#     #4.1.7 Flag for normal Tryglicerides levels Tryglicerides_Normal column¶
#     df["Tryglicerides_Normal"] = df["Tryglicerides"].apply(lambda x: 0 if  x > 150 else 1).astype("int")

#     #4.1.8 Flag for normal Platelets levels Platelets_Normal column
#     df["Platelets_Normal"] = df["Platelets"].apply(lambda x: 0 if x < 150 or x > 450 else 1).astype("int")

#     #4.1.9 Flag for normal Prothrombin levels Prothrombin_Normal column¶
#     df["Prothrombin_Normal"] = df["Prothrombin"].apply(lambda x: 0 if x < 9.5 or x > 13.5 else 1).astype("int")

#     # Mean for metrics
#     df["Mean_Metrics"] = df[["Ascites", "Hepatomegaly", "Spiders", "Edema"]].mean(axis=1)

#     #AST_ALT_Ratio
    
#     df['AST_ALT_Ratio'] = df['SGOT'] / df['Alk_Phos']

#     # Albumin to Bilirubin Ratio
#     df['Albumin_Bilirubin_Ratio'] = df['Albumin'] / df['Bilirubin']
#     # Interaction Terms
#     df['Age_Bilirubin'] = df['Age_In_Years'] * df['Bilirubin']
#     df['Albumin_Platelets'] = df['Albumin'] * df['Platelets']

#     # pugh score 
#     df['Child_Pugh_Proxy'] = (df['Bilirubin'] > 2).astype(int) + (df['Albumin'] < 2.8).astype(int) + df['Ascites'] + df['Hepatomegaly']


    

#     for col in ['Bilirubin', 'Cholesterol', 'SGOT', 'Tryglicerides']:
#         df[col] = np.log1p(df[col])
#         df.rename(columns={col: col+"_log"}, inplace=True)
        
#     return df.copy()




# df_ml = ml_wrangle(df_clean)
# df_test_ml = ml_wrangle(df_test_clean)




#==========================================================================#
#                          ML Models
#==========================================================================#




# columns = ["Drug","Age_In_Years","Sex","Ascites","Hepatomegaly","Spiders","Edema","Bilirubin_log","Cholesterol_log","Albumin","Copper","Alk_Phos","SGOT_log","Tryglicerides_log","Platelets","Prothrombin","Stage","Mean_Metrics","AST_ALT_Ratio","Albumin_Bilirubin_Ratio","Age_Bilirubin","Albumin_Platelets","Child_Pugh_Proxy"]


#==========================================================================#
#                          ML Models
#==========================================================================#

target = 'Survival_Status'
X = df.drop(target, axis=1)
y = df[target]

# X = df_ml[columns].copy()
# y = df_ml.Status.copy()
# test = df_test_ml[columns].copy()

# Split data 
random_state = 42
train_X, test_X, train_y, test_y = train_test_split(X, y, random_state=random_state)

# Proportions of all classes
# class_proportions = {0: 0.628083, 2: 0.337128, 1: 0.034788}

# Calculate class weights as inverse of proportions
# class_weights = {cls: 1.0 / proportion for cls, proportion in class_proportions.items()}



#==========================================================================#
#                         Model Training
#==========================================================================#
@st.experimental_fragment()
@st.cache_data()
def ml_model(model_name):
    if model_name == "LighGBM":
        start_time = time.time()
        best_params = {'num_leaves': 168,
                        'learning_rate': 0.06544266928947275,
                        'feature_fraction': 0.5922361978092556,
                        'bagging_fraction': 0.6302302918919024,
                        'bagging_freq': 2,
                        'min_child_samples': 60
 }
        model = LGBMClassifier(**best_params, random_state=random_state)
        

    elif model_name == "xgb":
        start_time = time.time()
        best_params = {'max_depth': 2,
                        'learning_rate': 0.4087005515394254,
                        'n_estimators': 780,
                        'min_child_weight': 6,
                        'subsample': 0.728008352354839,
                        'colsample_bytree': 0.8036052871375078,
                        'gamma': 2.196665592338322e-07
        }

        model = xgb.XGBClassifier(**best_params, random_state=random_state)

    elif model_name == "rf":
        start_time = time.time()
        best_params = {'n_estimators': 745,
                        'max_depth': 14,
                        'min_samples_split': 3,
                        'min_samples_leaf': 2,
                        'max_features': 0.4379232747784616
        }
        model = RandomForestClassifier(**best_params, random_state=random_state)

    elif model_name == "lr":
        start_time = time.time()
        best_params = {'C': 0.3422978316089267}
        model = LogisticRegression(**best_params, random_state=random_state)
        


    model.fit(train_X, train_y)
    preds = model.predict(test_X)
    # Predict on train and test sets
    train_preds_proba = model.predict_proba(train_X)
    test_preds_proba = model.predict_proba(test_X)

    # Calculate log loss on train and test sets
    train_log_loss = log_loss(train_y, train_preds_proba)
    test_log_loss = log_loss(test_y, test_preds_proba)


    # Evaluate model
    train_acc = model.score(train_X, train_y)
    test_acc = model.score(test_X, test_y)

    precision = precision_score(test_y, preds, average='weighted')
    recall = recall_score(test_y, preds, average='weighted')
    f1 = f1_score(test_y, preds, average='weighted')

    train_test_scores = {
    "Metric": [
        "LogLoss", 
        "Accuracy", 
    ],
    "Train_Score": [
        train_log_loss, 
        train_acc,
    ]
    ,
    "Test_Score": [
        test_log_loss,
        test_acc
    ]
}
    train_test_scores_df = pd.DataFrame(train_test_scores)

    all_scores = {
        "Metric": [
            "LogLoss", 
            "Accuracy", 
            "Precision", 
            "Recall", 
            " F1", 
        ],
        "Score": [
            round(train_log_loss,4), 
            round(train_acc,4), 
            round(precision,4), 
            round(recall,4), 
            round(f1,4)
        ],
        "Interpretation":[
            "This measures how well the model's predicted probabilities match the actual outcomes. A lower value indicates better performance." ,

            f"Accuracy: This tells us that the model correctly predicted the outcome about {round(train_acc, 2)*100}% of the time.",

            f"Precision: This indicates that when the model predicted a certain class, it was correct about {round(precision, 2)*100}% of the time.",

            f"""Recall: This measures the model's ability to correctly identify all the relevant instances. The model successfully identified about {round(recall, 2)*100}% of the actual instances of a class.""",

            f"F1 Score: This is a balance between precision and recall."]
    }
    all_scores_df = pd.DataFrame(all_scores)

    # Record the end time
    end_time = time.time()

    # Calculate the execution time
    execution_time = end_time - start_time
    

    return all_scores_df, train_test_scores_df, model, execution_time
    

#==========================================================================#
#                         Final Model
#==========================================================================#
@st.experimental_fragment()
@st.cache_data()
def final_model(model_name, to_predict, full_X= X, full_y= y):
    if model_name == "LightGBM":
        start_time = time.time()
        best_params = {'num_leaves': 168,
                        'learning_rate': 0.06544266928947275,
                        'feature_fraction': 0.5922361978092556,
                        'bagging_fraction': 0.6302302918919024,
                        'bagging_freq': 2,
                        'min_child_samples': 60
 }
        model = LGBMClassifier(**best_params, random_state=random_state)
        

    elif model_name == "XGBoost":
        start_time = time.time()
        best_params = {'max_depth': 2,
                        'learning_rate': 0.4087005515394254,
                        'n_estimators': 780,
                        'min_child_weight': 6,
                        'subsample': 0.728008352354839,
                        'colsample_bytree': 0.8036052871375078,
                        'gamma': 2.196665592338322e-07
        }

        model = xgb.XGBClassifier(**best_params, random_state=random_state)

    elif model_name == "Randomforest":
        start_time = time.time()
        best_params = {'n_estimators': 745,
                        'max_depth': 14,
                        'min_samples_split': 3,
                        'min_samples_leaf': 2,
                        'max_features': 0.4379232747784616
        }
        model = RandomForestClassifier(**best_params, random_state=random_state)

    elif model_name == "LogisticRegression":
        start_time = time.time()
        best_params = {'C': 0.3422978316089267}
        model = LogisticRegression(**best_params, random_state=random_state)
        


    model.fit(full_X, full_y)
    new_pred = model.predict(to_predict)
    pre_propability = model.predict_proba(to_predict)
    
    # Record the end time
    end_time = time.time()

    # Calculate the execution time
    execution_time = end_time - start_time
    

    return new_pred,pre_propability, execution_time
    


#-------------------------------------------------------
# Shap Interpretation Function
#-------------------------------------------------------

def shap_description(chart_type, is_medical=True):
    """
    Provides interpretations for SHAP charts in plain language.
    
    Parameters:
    -----------
    chart_type : str
        The type of SHAP chart to explain
    is_medical : bool, default=True
        Whether to use medical-specific explanations
    
    Returns:
    --------
    str
        HTML-formatted explanation
    """
    
    # Base descriptions (technical)
    base_descriptions = {
        "SHAP Bar Plot": """
    <div style="border: 2px solid #13B3E7; border-radius:10px; padding: 15px; font-family: 'Arial', sans-serif; font-size: 14px; >
    <h2 style="color: red; text-align: center;">SHAP Bar Plot Interpretation</h2>

    ---

    ### 1. **Feature Importance Ranking**
    - Displays **average absolute SHAP values**.
    - Higher bars indicate **more important features**.
    - Helps identify **key drivers** of predictions.

    ---

    ### 2. **Insights**
    - **Feature order**: Sorted by importance.
    - **Magnitude**: Larger bars mean stronger influence.
    - Useful for **feature selection** in modeling.

    ---

    <h3 style="color: #13B3E7;">Practical Applications</h3>
    - Identify **critical features** affecting predictions.
    - Guide **feature engineering** efforts.
    - Compare models based on feature importance.
    </div>
    """,

        "SHAP Summary Plot": """
    <div style="border: 2px solid #13B3E7; border-radius:10px; padding: 15px; font-family: 'Arial', sans-serif; font-size: 14px;">
    <h2 style="color: #13B3E7; text-align: center;">SHAP Summary Plot Interpretation</h2>

    ---

    ### 1. **Feature Influence & Distribution**
    - Each dot represents a **data instance**.
    - X-axis: **SHAP value (impact on model output)**.
    - Y-axis: **Feature name** (sorted by importance).

    ---

    ### 2. **Color & Spread Meaning**
    - **Color**: Represents feature values (blue = low, red = high).
    - **Spread**: Shows how **variable** the impact of each feature is.
    - **Densely packed points** mean **consistent influence**.

    ---

    <h3 style="color: #13B3E7;">Practical Applications</h3>
    - Understand **how features influence predictions**.
    - Spot **non-linear effects** by checking spread.
    - Compare feature importance across multiple cases.
    </div>
    """,

        "SHAP Decision Plot": """
    <div style="border: 2px solid #13B3E7; border-radius:10px; padding: 15px; font-family: 'Arial', sans-serif; font-size: 14px; ">
    <h2 style="color: #13B3E7; text-align: center;">SHAP Decision Plot Interpretation</h2>

    ---

    ### 1. **Path Analysis**
    - **Shows prediction path** for each instance.
    - Reveals **feature contribution sequence**.
    - Demonstrates **cumulative effects** as features are added.

    ---

    ### 2. **Feature Impacts**
    - **Line slopes**: Indicate the **magnitude** of each feature's impact.
    - **Color**: Represents the identity of the feature.
    - **Crossing lines**: Show how **feature importance** changes over the course of the prediction.

    ---

    ### 3. **Model Behavior**
    - Highlights **overall prediction patterns**.
    - Identifies **key decision points** where the model's outcome changes.
    - Marks **feature value thresholds** that influence predictions.

    ---

    <h3 style="color: #13B3E7;">Practical Applications</h3>
    - **Analyze decision paths** to understand how the model reaches its conclusions.
    - **Compare similar instances** to identify patterns.
    - **Identify critical features** that influence predictions.
    - **Validate model logic** by examining how feature contributions evolve.
    </div>
    """,

        "SHAP Waterfall Plot": """
    <div style="border: 2px solid #13B3E7; border-radius:10px; padding: 15px; font-family: 'Arial', sans-serif; font-size: 14px;">
    <h2 style="color: #13B3E7; text-align: center;">SHAP Waterfall Plot Interpretation</h2>

    ---

    ### 1. **Explaining a Single Prediction**
    - Visualizes how a **single instance** was predicted.
    - Starts from the **baseline prediction**.
    - Shows **how each feature pushes the prediction up or down**.

    ---

    ### 2. **Feature Contributions**
    - **Red bars**: Increase the prediction.
    - **Blue bars**: Decrease the prediction.
    - The final prediction is reached **step by step**.

    ---

    <h3 style="color: #13B3E7;">Practical Applications</h3>
    - **Understand individual predictions** in detail.
    - **Debug model behavior** for specific cases.
    - **Explain decisions** to stakeholders in an interpretable way.
    </div>
    """
    }
    
    # Medical-specific plain language descriptions
    medical_descriptions = {
        "SHAP Bar Plot": """
    <div style="border: 2px solid #13B3E7; border-radius:10px; padding: 15px; font-family: 'Arial', sans-serif; font-size: 14px;">
    <h2 style="color: #13B3E7; text-align: center;">SHAP Bar Plot Interpretation</h2>

    ---

    ### The Big Picture
    This chart shows **which medical factors are most important** in predicting patient outcomes. 
    
    - Increased white blood cell count (Increased Leucocyte Count) is clearly the most influential factor
    - Elevated blast cells and unexplained bleeding are also major indicators
    - Gender appears to have minimal impact on prediction

    ---

    ### What The Colors Mean
    - **Blue sections**: Impact for patients who didn't survive
    - **Red sections**: Impact for patients who survived
    - **Longer bars**: Factors that strongly influence the prediction
    
    ---

    ### What This Means For Doctors
    By focusing on the top factors like white blood cell counts, blast cell proportion, and bleeding tendencies, doctors can prioritize which symptoms to monitor closely for early intervention.
    </div>
    """,

        "SHAP Summary Plot": """
    <div style="border: 2px solid #13B3E7; border-radius:10px; padding: 15px; font-family: 'Arial', sans-serif; font-size: 14px; ">
    <h2 style="color: #13B3E7; text-align: center;">SHAP Summary Plot Interpretation</h2>

    ---

    ### The Big Picture
    This chart shows **how each medical factor influences patient survival** and how this relationship changes based on the value of each factor.
    
    - Each dot represents a different patient
    - Red dots indicate high values for that factor, blue dots indicate low values
    - Dots to the right of center (positive SHAP values) increase likelihood of survival
    - Dots to the left of center (negative SHAP values) decrease likelihood of survival

    ---

    ### Key Insights
    - **High white blood cell counts** (red dots) strongly push predictions toward survival
    - **Elevated blast cell proportion** shows a similar pattern
    - **Unexplained hemorrhage** when present (red) strongly indicates survival
    - **Age** shows a mixed effect - both young and old patients have dots on both sides of center
    
    ---

    ### What This Means For Doctors
    This chart helps visualize which symptom patterns are most associated with different outcomes. For example, patients with high white blood cell counts tend to have better survival chances according to this model.
    </div>
    """,

    #     "SHAP Decision Plot": """
    # <div style="border: 2px solid #13B3E7; border-radius:10px; padding: 15px; font-family: 'Arial', sans-serif; font-size: 14px; ">
    # <h2 style="color: #13B3E7; text-align: center;">SHAP Decision Plot Interpretation</h2>

    "SHAP Decision Plot": """
    <div style="border: 2px solid #13B3E7; border-radius:10px; padding: 15px; font-family: 'Arial', sans-serif; font-size: 14px; ">
    <h2 style="color: #13B3E7; text-align: center;">SHAP Decision Plot Interpretation</h2>

    ### The Big Picture
    This chart shows **how each patient's risk is calculated** by the model, step-by-step as each factor is considered.
    
    - Each colored line represents a different patient
    - The horizontal axis shows the prediction value (more negative = higher risk)
    - Lines moving from top to bottom show how the prediction changes as each factor is added

    ---

    ### Key Insights
    - **Most patients start with similar risk** (lines clustered at the top)
    - **Increased white blood cell count** creates the most dramatic shifts in prediction
    - **The top 5 factors** (white blood cells, blast cells, bleeding, anemia, and platelets) create the most significant changes in prediction
    - **Later factors** like age and gender have minimal impact on most patients
    
    ---

    ### What This Means For Doctors
    This chart helps visualize the "decision path" for each patient. Some patients may start at moderate risk but have their risk assessment significantly changed by just one or two key factors.
    </div>
    """
    }
    
    # Choose the appropriate description based on the chart type and audience
    if is_medical and chart_type in medical_descriptions:
        return medical_descriptions.get(chart_type)
    else:
        return base_descriptions.get(chart_type, "Invalid selection")
