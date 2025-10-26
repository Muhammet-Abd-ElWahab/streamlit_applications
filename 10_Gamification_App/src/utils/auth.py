import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

class Authentication:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        
        # Initialize session state variables if they don't exist
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
        if 'user_name' not in st.session_state:
            st.session_state.user_name = None
    
    def login_form(self):
        """Display login form and handle authentication"""
        st.title("Patient Gamification Portal")
        
        with st.form("login_form"):
            st.subheader("Login")
            
            # Create two columns for role selection
            col1, col2 = st.columns(2)
            with col1:
                admin_role = st.checkbox("Admin")
            with col2:
                patient_role = st.checkbox("Patient")
            
            # Username/ID field
            user_id = st.text_input("Username/Patient ID")
            
            # Password field (in a real app, you'd use proper password hashing)
            password = st.text_input("Password", type="password")
            
            submitted = st.form_submit_button("Login")
            
            if submitted:
                # Validate role selection (only one should be selected)
                if admin_role and patient_role:
                    st.error("Please select only one role: Admin OR Patient")
                    return
                elif not admin_role and not patient_role:
                    st.error("Please select a role: Admin OR Patient")
                    return
                
                role = "admin" if admin_role else "patient"
                
                # Authenticate based on role
                if role == "admin":
                    # In a real app, you'd check against a secure admin database
                    # For demo purposes, we'll use a simple check
                    if user_id == "admin" and password == "admin123":
                        self._set_logged_in(role, "admin", "Administrator")
                        st.success("Admin login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid admin credentials")
                else:  # Patient role
                    # Check if patient ID exists in our data
                    patients = self.data_processor.get_all_patients()
                    patient_exists = patients['patient_id'].str.lower() == user_id.lower()
                    
                    if patient_exists.any():
                        # In a real app, you'd verify the password securely
                        # For demo purposes, we'll use a simple check (patient ID as password)
                        if password == user_id or password == "patient123":
                            patient_data = patients[patient_exists].iloc[0]
                            self._set_logged_in(role, patient_data['patient_id'], patient_data['name'])
                            st.success(f"Welcome, {patient_data['name']}!")
                            st.rerun()
                        else:
                            st.error("Invalid password")
                    else:
                        st.error("Patient ID not found")
    
    def logout(self):
        """Log out the current user"""
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.rerun()
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return st.session_state.logged_in
    
    def get_user_role(self):
        """Get the role of the logged-in user"""
        return st.session_state.user_role
    
    def get_user_id(self):
        """Get the ID of the logged-in user"""
        return st.session_state.user_id
    
    def get_user_name(self):
        """Get the name of the logged-in user"""
        return st.session_state.user_name
    
    def _set_logged_in(self, role, user_id, user_name):
        """Set session state for logged-in user"""
        st.session_state.logged_in = True
        st.session_state.user_role = role
        st.session_state.user_id = user_id
        st.session_state.user_name = user_name
