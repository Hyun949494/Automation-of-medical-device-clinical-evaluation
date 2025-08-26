import streamlit as st
from config import TEAM_CONFIGS
from ui import render_header, render_team_selector, render_footer
from components import render_pubmed_tab, render_ai_tab, render_meddev_tab

# 🎯 Streamlit 앱 시작
st.set_page_config(
    page_title="🏥 임상평가 자동화",
    page_icon="🏥",
    layout="wide"
)

# 🔧 세션 상태 초기화
if 'selected_team' not in st.session_state:
    st.session_state.selected_team = "RND4"
if 'df' not in st.session_state:
    st.session_state.df = None

# CSS 스타일 적용
from styles import apply_styles
apply_styles()

# 헤더 렌더링
render_header()

# 팀 선택 버튼들
render_team_selector(TEAM_CONFIGS)

st.divider()

# 📱 메인 제목
st.markdown('<h1 class="main-header">🏥 임상평가 자동화 도구</h1>', unsafe_allow_html=True)

# 📋 메인 탭 구성
tab1, tab2, tab3 = st.tabs(["🔍 PubMed 검색", "🤖 AI 분석", "📊 MEDDEV 분석"])

# 각 탭 렌더링
with tab1:
    render_pubmed_tab()

with tab2:
    render_ai_tab()

with tab3:
    render_meddev_tab()

# 푸터
render_footer()
