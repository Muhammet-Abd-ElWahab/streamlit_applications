import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import utilities
from src.utils.data_processor import DataProcessor
from src.utils.auth import Authentication

# Import pages
from src.pages.admin_dashboard import admin_dashboard_page
from src.pages.admin_patient_info import admin_patient_info_page
from src.pages.admin_leaderboard import admin_leaderboard_page
from src.pages.admin_chatbot import admin_chatbot_page
from src.pages.patient_info import patient_info_page
from src.pages.patient_leaderboard import patient_leaderboard_page
from src.pages.patient_chatbot import patient_chatbot_page

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Patient Gamification Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0077B6;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #0096C7;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: rgba(240, 240, 240, 0.1);
        box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border: 1px solid rgba(0, 119, 182, 0.2);
    }
    .metric-card {
        text-align: center;
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: rgba(144, 224, 239, 0.1);
        margin-bottom: 1rem;
        border: 1px solid rgba(0, 119, 182, 0.2);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #0077B6;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #0096C7;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        background-color: rgba(0, 150, 199, 0.1);
        color: #0077B6;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid rgba(0, 119, 182, 0.2);
    }
    .sidebar .sidebar-content {
        background-color: rgba(144, 224, 239, 0.05);
    }
    .stProgress > div > div > div > div {
        background-color: #0096C7;
    }
    /* Ensure text is readable in both light and dark modes */
    .stApp {
        color: inherit;
    }
    /* Style for info boxes */
    .stAlert {
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize data processor
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'all_patients.csv')
    data_processor = DataProcessor(data_path)
    
    # Initialize authentication
    auth = Authentication(data_processor)
    
    # Check if user is logged in
    if not auth.is_logged_in():
        auth.login_form()
    else:
        # Display sidebar navigation
        with st.sidebar:
            st.image("https://img.icons8.com/color/96/000000/hospital-3.png", width=100)
            st.title(f"Welcome, {auth.get_user_name()}")
            st.caption(f"Role: {auth.get_user_role().capitalize()}")
            st.divider()
            
            # Navigation based on user role
            if auth.get_user_role() == "admin":
                page = st.radio(
                    "Navigation",
                    ["Dashboard", "Patient Information", "Leaderboard", "Chatbot"],
                    index=0
                )
            else:  # patient role
                page = st.radio(
                    "Navigation",
                    ["My Information", "Leaderboard", "Chatbot"],
                    index=0
                )
            
            st.divider()
            if st.button("Logout"):
                auth.logout()
        
        # Display selected page based on user role
        if auth.get_user_role() == "admin":
            if page == "Dashboard":
                admin_dashboard_page(data_processor)
            elif page == "Patient Information":
                admin_patient_info_page(data_processor)
            elif page == "Leaderboard":
                admin_leaderboard_page(data_processor)
            elif page == "Chatbot":
                admin_chatbot_page(data_processor)
        else:  # patient role
            if page == "My Information":
                patient_info_page(data_processor, auth.get_user_id())
            elif page == "Leaderboard":
                patient_leaderboard_page(data_processor, auth.get_user_id())
            elif page == "Chatbot":
                patient_chatbot_page(data_processor, auth.get_user_id())

if __name__ == "__main__":
    main()
