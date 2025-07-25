# config.py 페이지설정
import streamlit as st

def load_team_config(team_name):
    """팀 설정 로드"""
    try:
        if team_name == "RND4":
            import rnd4
            return rnd4.TEAM_CONFIG
        elif team_name == "RND35":
            import rnd35
            return rnd35.TEAM_CONFIG
        else:
            return None
    except ImportError:
        st.error(f"{team_name} 설정 파일을 찾을 수 없습니다.")
        return None

def setup_page():
    """페이지 기본 설정"""
    st.set_page_config(
        page_title="🔬 임상 문헌 분석 도구",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )