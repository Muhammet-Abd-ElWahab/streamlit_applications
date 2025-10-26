
import streamlit as st
from pathlib import Path

# Load the HTML file
def load_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()





if __name__ == "__main__":

    logo_path = "./TheLogo2.png"  # Replace with the path to your logo image
    st.sidebar.image(logo_path, use_column_width=True)
    # Path to your HTML file
    html_file = Path("2_Linkedin_Analysis.html")

    # Load the HTML content
    html_content = load_html(html_file)

    # Display the HTML content in the Streamlit app


    st.markdown("<h2 style='color: #008080; text-align:left'>Krakon Exploratory Data Analysis Report</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #008080; margin-top: 5px; margin-bottom: 5px;'>", unsafe_allow_html=True)

    st.sidebar.markdown("<h2 style='color: #008080; text-align:center'>Krakon Report</h2>", unsafe_allow_html=True)
    st.sidebar.download_button(
        label="Click to Download Report as HTML",
        data=html_content,
        file_name="2_Linkedin_Analysis.html",
        mime="application/html",
        key="krakon"
    )
    st.components.v1.html(html_content, height=800, scrolling=True)