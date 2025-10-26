import streamlit as st
import os
from src.utils.chatbot import Chatbot

def admin_chatbot_page(data_processor):
    """Admin Chatbot Page"""
    st.markdown("<h1 class='main-header'>Admin Assistant</h1>", unsafe_allow_html=True)
    
    # Check if API key is set
    # api_key = os.getenv("GOOGLE_API_KEY")
    api_key = st.secrets["google"]["GOOGLE_API_KEY"]
    os.environ["GOOGLE_API_KEY"] = api_key
    # api_key = "AIzaSyAUr28Ow-1EC9zPcTqIl3YakXZMSDDwaQE"
    
    if not api_key or api_key == "your-api-key-here":
        st.warning("⚠️ Google API Key not found. Please set your GOOGLE_API_KEY environment variable.")
        
        with st.expander("How to set up your API Key"):
            st.markdown("""
            1. Get a Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
            2. Create a `.env` file in the root directory of this project
            3. Add the following line to the file: `GOOGLE_API_KEY=your_api_key_here`
            4. Restart the application
            """)
        
        # Allow manual entry of API key for testing
        temp_api_key = st.text_input("Enter your Google API Key for this session", type="password")
        if temp_api_key:
            os.environ["GOOGLE_API_KEY"] = temp_api_key
            st.success("API Key set for this session. You can now use the chatbot.")
            st.rerun()
        
        return
    
    # Initialize chatbot
    if 'admin_chatbot' not in st.session_state:
        st.session_state.admin_chatbot = Chatbot(data_processor, user_role="admin")
    
    # Initialize chat history
    if 'admin_chat_history' not in st.session_state:
        st.session_state.admin_chat_history = []
    
    # Display chat history
    for message in st.session_state.admin_chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat interface
    st.markdown("<div class='subheader'>Ask questions about patient data, metrics, and treatment progress</div>", unsafe_allow_html=True)
    
    # Example questions
    with st.expander("Example questions you can ask"):
        st.markdown("""
        - Which patient has the highest health score?
        - What is the average tumor size reduction across all patients?
        - How many patients are at level 3 or higher?
        - Which treatment type shows the best results?
        - What is the correlation between medication adherence and health score?
        - How is Patient P001 progressing with their treatment?
        - Which patients have missed their medication in the last week?
        - What badges are most commonly earned?
        """)
    
    # User input
    user_question = st.chat_input("Ask a question about the patient data...")
    
    if user_question:
        # Add user message to chat history
        st.session_state.admin_chat_history.append({"role": "user", "content": user_question})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_question)
        
        # Get response from chatbot
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.admin_chatbot.ask(user_question)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.admin_chat_history.append({"role": "assistant", "content": response})
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.admin_chat_history = []
        st.rerun()

