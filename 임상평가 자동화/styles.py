# styles.py
import streamlit as st

def load_css():
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #e3f2fd 0%, #f1f8e9 100%);
        }
        
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 20px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            margin-top: 1rem;
        }
        
        .main-title {
            text-align: center;
            color: #1565c0;
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
        }
        
        .subtitle {
            text-align: center;
            color: #388e3c;
            font-size: 1.2rem;
            margin-bottom: 2rem;
            font-style: italic;
        }
        
        .stButton > button {
            background: linear-gradient(45deg, #42a5f5, #66bb6a);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            background: linear-gradient(45deg, #1e88e5, #4caf50);
        }
        
        .custom-card {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin: 1rem 0;
            border-left: 4px solid #42a5f5;
        }
        
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 10px;
        }
        
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 2px solid #e1f5fe;
            background-color: #fafafa;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #42a5f5;
            box-shadow: 0 0 0 2px rgba(66, 165, 245, 0.1);
            background-color: white;
        }
        
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #42a5f5, #66bb6a);
        }
        
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease-in;
        }
    </style>
    """, unsafe_allow_html=True)