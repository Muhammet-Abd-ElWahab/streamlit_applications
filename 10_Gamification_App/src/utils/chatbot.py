import os
import pandas as pd
import google.generativeai as genai
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class Chatbot:
    def __init__(self, data_processor, user_role=None, user_id=None):
        self.data_processor = data_processor
        self.user_role = user_role
        self.user_id = user_id
        # self.api_key = os.getenv("GOOGLE_API_KEY", "your-api-key-here")
        self.api_key = "AIzaSyAUr28Ow-1EC9zPcTqIl3YakXZMSDDwaQE"
        
        # Initialize Gemini
        genai.configure(api_key=self.api_key)
        
        # Create vector database from patient data
        self.setup_vector_db()
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create the chatbot chain
        self.setup_chat_chain()
    
    def setup_vector_db(self):
        """Create vector database from patient data"""
        # Convert dataframe to text documents
        df = self.data_processor.df
        
        # If user is a patient, filter data to only include their information
        if self.user_role == "patient" and self.user_id:
            df = df[df['patient_id'] == self.user_id]
        
        # Create text documents from dataframe
        documents = []
        for _, row in df.iterrows():
            doc_text = f"Patient ID: {row['patient_id']}\n"
            doc_text += f"Name: {row['name']}\n"
            doc_text += f"Age: {row['age']}\n"
            doc_text += f"Treatment Type: {row['treatment_type']}\n"
            doc_text += f"Initial Diagnosis Date: {row['initial_diagnosis_date']}\n"
            doc_text += f"Visit Number: {row['visit_number']}\n"
            doc_text += f"Visit Date: {row['visit_date']}\n"
            doc_text += f"Next Appointment: {row['next_appointment']}\n"
            doc_text += f"Medical Metrics: Systolic BP {row['systolic_bp']}, Diastolic BP {row['diastolic_bp']}, "
            doc_text += f"Heart Rate {row['heart_rate']}, Temperature {row['temperature']}, "
            doc_text += f"Tumor Size {row['tumor_size_cm']} cm, Side Effect Severity {row['side_effect_severity']}, "
            doc_text += f"Quality of Life {row['quality_of_life']}, Treatment Adherence {row['treatment_adherence']}%, "
            doc_text += f"WBC Count {row['wbc_count']}, Hemoglobin {row['hemoglobin']}, Platelets {row['platelets']}\n"
            doc_text += f"Notes: {row['notes']}\n"
            doc_text += f"Gamification Elements: Medication Streak {row['medication_streak']}, Max Streak {row['max_streak']}, "
            doc_text += f"Attendance Rate {row['attendance_rate']}%, Health Score {row['health_score']}, "
            doc_text += f"Badges: {row['badges']}, Ranking Percentile {row['ranking_percentile']}, "
            doc_text += f"Commitment Score {row['commitment_score']}, Med Tracking 7 Days {row['med_tracking_7days']}, "
            doc_text += f"Points Earned {row['points_earned']}, Total Points {row['total_points']}, Level {row['level']}\n"
            
            documents.append(doc_text)
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        chunks = text_splitter.create_documents(["\n\n".join(documents)])
        
        # Create embeddings and vector store
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vector_store = FAISS.from_documents(chunks, embeddings)
        self.retriever = self.vector_store.as_retriever()
    
    def setup_chat_chain(self):
        """Set up the conversational chain with Gemini"""
        # Create system prompt based on user role
        if self.user_role == "admin":
            system_template = """
            You are a medical assistant AI for healthcare administrators. 
            You have access to patient data including medical metrics and gamification elements.
            Answer questions about patient metrics, leaderboard standings, statistical comparisons, and treatment progress.
            Be professional and provide data-driven insights to help administrators make informed decisions.
            
            Use the following pieces of context to answer the question at the end.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            
            {context}
            
            Question: {question}
            """
        else:  # patient role
            system_template = """
            You are a friendly medical assistant AI for patients. 
            You have access to the patient's medical data including metrics and gamification elements.
            Answer questions about the patient's own metrics, how to improve rankings, treatment progress, and upcoming appointments.
            Be encouraging and supportive while providing accurate information to help the patient stay engaged with their treatment.
            
            Use the following pieces of context to answer the question at the end.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            
            {context}
            
            Question: {question}
            """
        
        # Create prompt from template
        PROMPT = PromptTemplate(
            template=system_template, 
            input_variables=["context", "question"]
        )
        
        # Create LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=self.api_key
        )
        
        # Create chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=self.retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": PROMPT}
        )
    
    def ask(self, question):
        """Ask a question to the chatbot"""
        try:
            response = self.chain.invoke({"question": question})
            return response["answer"]
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}. Please try again or check your API key configuration."
