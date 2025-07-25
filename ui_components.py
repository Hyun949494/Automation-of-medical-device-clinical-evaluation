# ui_components.py
import streamlit as st
from config import load_team_config

def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.markdown("### 🎛️ 제어판")
        st.markdown("---")
        
        # 팀 설정
        st.markdown("#### ⚡ 팀 설정")
        team_col1, team_col2 = st.columns(2)
        
        with team_col1:
            if st.button("🔵 개발4팀", key="btn_rnd4"):
                config = load_team_config("RND4")
                if config:
                    for key, value in config.items():
                        st.session_state[f"team_{key}"] = value
                    st.rerun()
        
        with team_col2:
            if st.button("🟢 개발3,5팀", key="btn_rnd35"):
                config = load_team_config("RND35")
                if config:
                    for key, value in config.items():
                        st.session_state[f"team_{key}"] = value
                    st.rerun()
        
        if st.button("🔄 초기화", key="btn_reset"):
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('team_')]
            for key in keys_to_remove:
                del st.session_state[key]
            st.rerun()

def render_header():
    """헤더 렌더링"""
    st.markdown('<h1 class="main-title">🔬 임상 문헌 분석 도구</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">PICO PubMed 검색 + Gemini AI 분석 + 문헌 분석</p>', unsafe_allow_html=True)

def render_footer():
    """푸터 렌더링"""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #42a5f5; padding: 20px; background: rgba(227, 242, 253, 0.3); border-radius: 10px;'>
            <p>🔬 임상 문헌 분석 도구 | Gemini AI 기반</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
