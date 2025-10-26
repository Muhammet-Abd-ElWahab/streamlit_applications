#==========================================================================#
#                          Import Libiraries
#==========================================================================#
import sys

import streamlit as st
import os

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from statsmodels.stats.anova import AnovaRM
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import chi2_contingency



st.set_page_config(page_title="Dashboard",
                #    page_icon = "⚕:",
                   layout="wide"
                   )





#==========================================================================#
#                         Import functions
#==========================================================================#


sys.path.append(os.path.abspath('./functions.py'))

from functions import bar_chart,  df





#==========================================================================#
#                          Pie charts Functions
#==========================================================================#

# Convert to list to avoid Streamlit unhashable error
numerical_cols = df.select_dtypes(exclude=['object']).columns.tolist()

@st.cache_data
def plot_feature_distributions(df, _numerical_cols):
    """Plots histogram distributions for numerical columns in a Streamlit app."""
    
    if len(_numerical_cols) == 0:
        st.warning("No numerical columns available for plotting.")
        return
    
    n_cols = 3
    n_rows = (len(_numerical_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    axes = axes.flatten()

    for idx, col in enumerate(_numerical_cols):
        sns.histplot(data=df, x=col, kde=True, ax=axes[idx], color="#2f5586", edgecolor="black")
        axes[idx].set_title(f'Distribution of {col}', fontsize=14)

    # Hide unused subplots if any
    for idx in range(len(_numerical_cols), len(axes)):
        fig.delaxes(axes[idx])

    plt.tight_layout()
    st.pyplot(fig)  # Display in Streamlit

@st.cache_data
def plot_density_plots(df, _numerical_cols):
    """Plots density plots for numerical columns in a Streamlit app."""

    if len(_numerical_cols) == 0:
        st.warning("No numerical columns available for density plots.")
        return
    
    n_cols = 4
    n_rows = (len(_numerical_cols) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(25, 5*n_rows))
    axes = axes.flatten()

    for idx, col in enumerate(_numerical_cols):
        sns.kdeplot(df[col], ax=axes[idx], fill=True, color='#2f5586', edgecolor='black', linewidth=1.5, alpha=0.9)
        axes[idx].set_xlabel(col, fontsize=14)
        axes[idx].set_ylabel("Density", fontsize=14)

    # Hide unused subplots if any
    for idx in range(len(_numerical_cols), len(axes)):
        fig.delaxes(axes[idx])

    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    fig.suptitle('Continuous Variables Density Plot', fontsize=20, color="k")

    st.pyplot(fig)  # Display in Streamlit






if __name__ == "__main__":
    logo_path = "./TheLogo2.png"  # Replace with the path to your logo image
    st.sidebar.image(logo_path, use_column_width =True)
    st.sidebar.markdown("<h2 style='color: #008080; text-align:center'>Select Chart option</h2>", unsafe_allow_html=True)
    chart_type_select = st.sidebar.selectbox(" ", ["Distribution", "Density"], label_visibility="collapsed")
    
    if chart_type_select == "Distribution":
        st.markdown(f"<h1 style='color: #008080; text-align:center'>Continuous Variables Distribution</h1>", unsafe_allow_html=True)
        plot_feature_distributions(df, numerical_cols)
    elif chart_type_select == "Density":
        st.markdown(f"<h1 style='color: #008080; text-align:center'>Continuous Variables Density</h1>", unsafe_allow_html=True)
        plot_density_plots(df, numerical_cols)

        
    
