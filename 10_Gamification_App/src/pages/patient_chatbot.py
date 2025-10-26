import streamlit as st
import os
from src.utils.chatbot import Chatbot
def patient_chatbot_page(data_processor, patient_id):
    """Patient Chatbot Page"""
    st.markdown("<h1 class='main-header'>My Health Assistant</h1>", unsafe_allow_html=True)
    
    # Check if API key is set
    # api_key = os.getenv("GOOGLE_API_KEY")
    api_key =  st.secrets["google"]["GOOGLE_API_KEY"]
    os.environ["GOOGLE_API_KEY"] = api_key
    #api_key = "AIzaSyAUr28Ow-1EC9zPcTqIl3YakXZMSDDwaQE"

    if not api_key or api_key == "your-api-key-here":
        st.warning("u26a0ufe0f Google API Key not found. Please set your GOOGLE_API_KEY environment variable.")
        
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
    if 'patient_chatbot' not in st.session_state:
        st.session_state.patient_chatbot = Chatbot(data_processor, user_role="patient", user_id=patient_id)
    
    # Initialize chat history
    if 'patient_chat_history' not in st.session_state:
        st.session_state.patient_chat_history = []
    
    # Display chat history
    for message in st.session_state.patient_chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat interface
    st.markdown("<div class='subheader'>Ask questions about your health, treatment, and progress</div>", unsafe_allow_html=True)
    
    # Example questions
    with st.expander("Example questions you can ask"):
        st.markdown("""
        - When is my next appointment?
        - How has my tumor size changed since my first visit?
        - What can I do to improve my health score?
        - How many points do I need to reach the next level?
        - What badges have I earned?
        - How does my treatment adherence compare to other patients?
        - What side effects should I watch out for?
        - How can I improve my medication streak?
        """)
    
    # User input
    user_question = st.chat_input("Ask a question about your health journey...")
    
    if user_question:
        # Add user message to chat history
        st.session_state.patient_chat_history.append({"role": "user", "content": user_question})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_question)
        
        # Get response from chatbot
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.patient_chatbot.ask(user_question)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.patient_chat_history.append({"role": "assistant", "content": response})
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.patient_chat_history = []
        st.rerun()

