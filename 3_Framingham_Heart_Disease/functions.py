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

@st.cache_data()
def wrangle(df):
    #Fill null values
    df.loc[:, 'education'] = df['education'].fillna(-1)
    df = df.dropna(subset=['cigsPerDay'])
    df.loc[:, 'BPMeds'] = df['BPMeds'].fillna(-1)
    # df["BPMeds"].fillna(-1, inplace=True)
    df = df.dropna(subset=['totChol'])
    df = df.dropna(subset=['heartRate'])
    df = df.dropna(subset=['glucose'])
    df = df.dropna(subset=['BMI'])

    # Fix Datatypes
    df["education"] = df["education"].astype(int)
    df["cigsPerDay"] = df["cigsPerDay"].astype(int)

    # Make age groupos 	
    age_bins = [30, 40, 50, 60, 70, np.inf]
    age_labels = ['Thirties', 'Forties', 'Fifties', 'Sixties', 'Seventies or Older']
    
    # Create a new column for age group with descriptive labels
    df['ageGroup'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False)


    # Make BMI Groups 
    
    bmi_bins = [0, 18.6, 25, 30, np.inf]
    bmi_labels = ['Underweight', 'Normal weight', 'Overweight', 'Obesity']
    
    # Create BMI categories
    df['BMICategory'] = pd.cut(df['BMI'], bins=bmi_bins, labels=bmi_labels, right=False)

    # Add MAP column Mean Arterial Pressure MAP = (SBP + 2 (DBP))/3
    df['MAP'] = (df['sysBP'] + 2 * df['diaBP']) / 3

    return df
    


#==========================================================================#
#                          Read Data
#==========================================================================#

@st.cache_data()
def read_data(name):
    df = pd.read_csv(name)
    return df

df = read_data('framingham.csv')
df_clean = wrangle(df)






#==========================================================================#
#                          Density Data Frame
#==========================================================================#
@st.cache_data()
def new_data():
    box = df_clean.copy()
    box["TenYearCHD"] = box["TenYearCHD"].apply(lambda x : "CHD" if x == 1 else "No CHD")
    box["currentSmoker"] = box["currentSmoker"].apply(lambda x : "Smoker" if x == 1 else "Non-Smoker")
    box["prevalentStroke"] = box["prevalentStroke"].apply(lambda x : "Had Stroke" if x == 1 else "No Stroke")
    box["diabetes"] = box["diabetes"].apply(lambda x : "Has Diabetes" if x == 1 else "No Diabetes")

    return box

df_clean_box = new_data()




#==========================================================================#
#                          Density Function
#==========================================================================#

@st.experimental_fragment()
def density():
    sns.set_style("whitegrid")
    fig,ax = plt.subplots(3,2,figsize=(16,8))

    sns.kdeplot(df_clean_box, x="age", 
                    fill=False,hue="TenYearCHD",
                    linewidth=1.5, alpha=0.8,
                    zorder=3,
                ax=ax[0,0]
                )
    ax[0,0].set_title("Age Distribution", fontsize=14, color="k")
    ax[0,0].set_xlabel("Age", fontsize=12, color="k")
    ax[0,0].set_ylabel("Density", fontsize=12, color="k")


    sns.kdeplot(df_clean_box, x="totChol", 
                    fill=False,hue="TenYearCHD",
                    linewidth=1.5, alpha=0.8,
                    zorder=3,
                ax=ax[0,1]
                )
    ax[0,1].set_title("Cholesterol Level Distribution", fontsize=14, color="k")
    ax[0,1].set_xlabel("Cholesterol Level", fontsize=12, color="k")
    ax[0,1].set_ylabel("Density", fontsize=12, color="k")


    sns.kdeplot(df_clean_box, x="glucose", 
                    fill=False,hue="TenYearCHD",
                    linewidth=1.5, alpha=0.8,
                    zorder=3,
                ax=ax[1,1]
                )
    ax[1,1].set_title("Glucose Level Distribution", fontsize=14, color="k")
    ax[1,1].set_xlabel("Glucose Level", fontsize=12, color="k")
    ax[1,1].set_ylabel("Density", fontsize=12, color="k")


    sns.kdeplot(df_clean_box, x="heartRate", 
                    fill=False,hue="TenYearCHD",
                    linewidth=1.5, alpha=0.8,
                    zorder=3,
                ax=ax[1,0]
                )
    ax[1,0].set_title("Heart Rate Distribution", fontsize=12, color="k")
    ax[1,0].set_xlabel("Heart Rate", fontsize=12, color="k")
    ax[1,0].set_ylabel("Density", fontsize=12, color="k")


    sns.kdeplot(df_clean_box, x="BMI", 
                    fill=False,hue="TenYearCHD",
                    linewidth=1.5, alpha=0.8,
                    zorder=3,
                ax=ax[2,0]
                )
    ax[2,0].set_title("BMI Distribution", fontsize=14, color="k")
    ax[2,0].set_xlabel("BMI", fontsize=12, color="k")
    ax[2,0].set_ylabel("Density", fontsize=12, color="k")




    sns.kdeplot(df_clean_box, x="MAP", 
                    fill=False,hue="TenYearCHD",
                    linewidth=1.5, alpha=0.8,
                    zorder=3,
                ax=ax[2,1]
                )
    ax[2,1].set_title("MAP Distribution", fontsize=14, color="k")
    ax[2,1].set_xlabel("MAP ", fontsize=12, color="k")
    ax[2,1].set_ylabel("Density", fontsize=12, color="k")

    plt.subplots_adjust(hspace = 0.8, wspace=0.2);
    st.pyplot(fig)

