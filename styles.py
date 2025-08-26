import streamlit as st

def render_header():
    """상단 헤더 렌더링"""
    st.markdown("### ⚡ 팀별 설정")

def render_team_selector(team_configs):
    """팀 선택 버튼들 렌더링"""
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        if st.button("📋 RND4", use_container_width=True):
            config = team_configs["RND4"]
            for key, value in config.items():
                st.session_state[f"team_{key}"] = value
            st.session_state.selected_team = "RND4"
            st.rerun()

    with col2:
        if st.button("📋 RND35", use_container_width=True):
            config = team_configs["RND35"]
            for key, value in config.items():
                st.session_state[f"team_{key}"] = value
            st.session_state.selected_team = "RND35"
            st.rerun()

    with col3:
        if st.button("🔄 커스텀", use_container_width=True):
            config = team_configs["커스텀"]
            for key, value in config.items():
                st.session_state[f"team_{key}"] = value
            st.session_state.selected_team = "커스텀"
            st.rerun()

    with col4:
        if st.button("🗑️ 초기화", use_container_width=True):
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith('team_')]
            for key in keys_to_remove:
                del st.session_state[key]
            st.rerun()

def render_footer():
    """푸터 렌더링"""
    st.markdown("---")
    st.markdown("🏥 **임상평가 자동화 도구** | 🤖 Powered by Gemini AI")

def render_pico_inputs():
    """PICO 입력 폼 렌더링"""
    st.markdown("### 📝 PICO 입력")
    
    col1, col2 = st.columns(2)
    with col1:
        P = st.text_input("👥 환자/문제 (Population)", 
                          value=st.session_state.get('team_P', ''),
                          placeholder="예: 수술 후 통증 환자")
        I = st.text_input("💊 중재 (Intervention)", 
                          value=st.session_state.get('team_I', ''),
                          placeholder="예: 경피 신경 자극 치료")

    with col2:
        C = st.text_input("⚖️ 비교 (Comparison)", 
                          value=st.session_state.get('team_C', ''),
                          placeholder="예: 진통제 투여")
        O = st.text_input("🎯 결과 (Outcome)", 
                          value=st.session_state.get('team_O', ''),
                          placeholder="예: 통증 완화 정도")
    
    return P, I, C, O

def render_search_options():
    """검색 옵션 렌더링 - 논문수와 검색기간 제거"""
    st.markdown("### 🔧 검색 옵션")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("📧 NCBI 이메일", value=st.session_state.get('team_email', ''))
    with col2:
        api_key = st.text_input("🔑 NCBI API 키", 
                               value=st.session_state.get('team_api_key', ''),
                               type="password")
    
    return email, api_key
