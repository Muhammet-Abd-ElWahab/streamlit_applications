#==========================================================================#
#                          Import Libiraries
#==========================================================================#
import streamlit as st
import sys
import os
# Caution: path[0] is reserved for script path (or '' in REPL)
#from streamlit_extras.colored_header import colored_header 
#from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
#from datetime import datetime
#from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
#from st_aggrid.shared import GridUpdateMode
#from streamlit_extras.dataframe_explorer import dataframe_explorer 
import yaml
import time

import matplotlib.pyplot as plt
import seaborn as sns
#from scipy import stats
import plotly.express as px

from collections import Counter



# import machine learning libiraries
from sklearn.metrics import make_scorer, confusion_matrix, precision_score, recall_score, accuracy_score, classification_report, f1_score,roc_auc_score, roc_curve, auc, log_loss

from sklearn.preprocessing import StandardScaler, MinMaxScaler, label_binarize, OrdinalEncoder, OneHotEncoder
from sklearn.feature_selection import mutual_info_classif

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, KFold

import xgboost as xgb
import lightgbm as lgb
#from lightgbm import LGBMClassifier 
#from sklearn.ensemble import RandomForestClassifier



import re
#import shap
#import optuna

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

Posted_by_dict = {
    "Mina Adly": 1,
    "Eman Hamdy Enab, ongoing SHRM-SCP":2,
    "Mohamad Taha, MD, MSc.," : 3,
    "Ahmed Kamel AbdelRazek" :4
}
Page_dict = {
     "Dataclin_Group":1, 
     "DataClin_CRO":2, 
     "DataClin_MA":3, 
     "DataClin_SMO":4
 }



@st.cache_data()
def wrangle(dfff):
    posts = dfff.copy()

    posts["Created_date"] = pd.to_datetime(posts["Created_date"])

    posts["length"] = posts["Post_title"].apply(lambda x:len(x))

    def extract_hashtags(text):
        return re.findall(r'#\w+', text)

    posts['hashtags'] = posts['Post_title'].apply(extract_hashtags)
    posts['hashtag_count']  = posts['hashtags'].apply(lambda x : len(x))

    all_hashtags = [hashtag for hashtags_list in posts['hashtags'] for hashtag in hashtags_list]
    hashtag_count = Counter(all_hashtags)
    hashtag_dict = dict(hashtag_count)
    hashtag_df = pd.Series(hashtag_dict).sort_values(ascending=False).to_frame()
    hashtag_df = hashtag_df.reset_index()
    hashtag_df.columns = ["Tag", "Count"]
    final_df = hashtag_df[(hashtag_df.Count >=6) & (~hashtag_df['Tag'].isin(["#DataClinGroup", "#CRO"]))]
    tags = [final_df.Tag]
    posts["Post_title"] = posts["Post_title"].fillna("")
    posts["#ClinicalResearch"] = posts["Post_title"].apply(lambda x: 1 if "#ClinicalResearch" in x else 0)
    posts["#ClinicalTrials"] = posts["Post_title"].apply(lambda x: 1 if "#ClinicalTrials" in x else 0)
    posts["#hiring"] = posts["Post_title"].apply(lambda x: 1 if "#hiring" in x else 0)
    posts["#Role_and_respon"] = posts["Post_title"].apply(lambda x: 1 if "#Role_and_respon" in x else 0)
    posts["#MedicalResearch"] = posts["Post_title"].apply(lambda x: 1 if "#MedicalResearch" in x else 0)
    posts["#MedicalAdvancem"] = posts["Post_title"].apply(lambda x: 1 if "#MedicalAdvancem" in x else 0)
    posts["#Innovation"] = posts["Post_title"].apply(lambda x: 1 if "#Innovation" in x else 0)
    posts["#Junior_General_"] = posts["Post_title"].apply(lambda x: 1 if "#Junior_General_" in x else 0)
    posts["#MedicalWriting"] = posts["Post_title"].apply(lambda x: 1 if "#MedicalWriting" in x else 0)
    posts = posts.sort_values(by="Created_date")
    posts.set_index('Created_date', inplace=True)

    # Create lag features
    for i in [1, 7]:  # Creating 3 lag features
        posts[f'lag_{i}'] = posts["Engagement_rate"].shift(i)
    posts.dropna(subset=["lag_1", "lag_7"], inplace=True)
    posts.Posted_by = posts.Posted_by.map(Posted_by_dict)
    posts.Page = posts.Page.map(Page_dict)
    return posts.copy()


#==========================================================================#
#                          Read Data
#==========================================================================#


df = pd.read_csv("all_posts.csv")
df_clean = wrangle(df)








#==========================================================================#
#                          ML Wrangle Function
#==========================================================================#








#==========================================================================#
#                          ML Models
#==========================================================================#
columns = [
    "Posted_by",
    "Page",
    "length",
    "hashtag_count",
    "#ClinicalResearch"	,
    "#ClinicalTrials",
    "#hiring",
    "#Role_and_respon",
    "#MedicalResearch",
    "#MedicalAdvancem",
    "#Innovation",
    "#Junior_General_",
    "#MedicalWriting",
    "lag_1",
    "lag_7",
]

X = df_clean[columns].copy()
y = df_clean.Engagement_rate.copy()


# Set Random_state to 1
random_state=1
# Split data into train and test datasets
train_X, test_X, train_y, test_y = train_test_split(X, y, random_state = random_state, test_size=0.25)

#==========================================================================#
#                         Light GBM
#==========================================================================#
@st.fragment()
@st.cache_data()
def ml_model(model_name):
    if model_name == "LighGBM":
        start_time = time.time()
        model = lgb.LGBMRegressor()
        
    elif model_name == "xgb":
        start_time = time.time()
        model = xgb.XGBRegressor()
        


    model.fit(train_X, train_y)
    preds = model.predict(test_X)
    # Predict on train and test sets
    kf = KFold(n_splits=5, shuffle=True, random_state=random_state)
    cv_trian_scores = - cross_val_score(model, train_X, train_y,  cv=kf, scoring="neg_mean_squared_error")
    cv_test_scores = - cross_val_score(model, test_X, test_y,  cv=kf, scoring="neg_mean_squared_error")

    train_test_scores = {
    "Metric": [
        "Mean Square Error"
    ],
    "Train_Score": [
        np.round(cv_trian_scores, 2),
    ]
    ,
    "Test_Score": [
        np.round(cv_test_scores,2),    ]
}
    train_test_scores_df = pd.DataFrame(train_test_scores)


    # Record the end time
    end_time = time.time()

    # Calculate the execution time
    execution_time = end_time - start_time
    

    return train_test_scores_df, model, execution_time
    



def ml_model_predict(model, data):
    start_time = time.time()
    model.fit(X, y)
    preds = model.predict(data)
    
    # Record the end time
    end_time = time.time()

    # Calculate the execution time
    execution_time = end_time - start_time
    

    return preds, execution_time
    


