import streamlit as st

def apply_styles():
    """CSS 스타일 적용"""
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            color: #1f4e79;
            margin-bottom: 2rem;
        }
        .team-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 2rem;
            justify-content: flex-start;
        }
        .filter-section {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .search-result {
            border: 1px solid #e0e0e0;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
