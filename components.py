import streamlit as st
import pandas as pd
import io
import time
import google.generativeai as genai
import re  
from ui import render_pico_inputs, render_search_options
from pubmed_api import pubmed_search_all, pubmed_details, build_query, build_filters
from analysis import analyze_with_gemini, get_meddev_analysis_prompt

def render_pubmed_tab():
    """PubMed 검색 탭 렌더링"""
    # PICO 입력
    P, I, C, O = render_pico_inputs()
    
    # 검색 조합 선택
    st.markdown("### 🎯 검색 조합 선택")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        use_P = st.checkbox("✅ P 포함", value=True)
    with col2:
        use_I = st.checkbox("✅ I 포함", value=True)
    with col3:
        use_C = st.checkbox("✅ C 포함", value=False)
    with col4:
        use_O = st.checkbox("✅ O 포함", value=False)

    # 선택된 조합 표시
    selected_components = []
    if use_P and P: selected_components.append("P")
    if use_I and I: selected_components.append("I") 
    if use_C and C: selected_components.append("C")
    if use_O and O: selected_components.append("O")

    if selected_components:
        combo_display = " + ".join(selected_components)
        st.success(f"🔍 **선택된 조합**: {combo_display}")

    # 검색 옵션 (논문수와 검색기간 제거)
    email, api_key = render_search_options()
    
    # 검색 필터 (검색기간 추가)
    filter_options = render_search_filters()
    
    # 검색 실행
    if st.button("🚀 검색 실행", use_container_width=True):
        execute_pubmed_search(P, I, C, O, use_P, use_I, use_C, use_O, 
                             email, api_key, filter_options)

def render_search_filters():
    """검색 필터 UI 렌더링 - 검색 기간 및 PubMed 주요 필터 추가"""
    st.markdown("### 🔍 검색 필터")
    
    # Publication Date 필터
    st.markdown("#### 📅 Publication Date")
    use_date_filter = st.checkbox("날짜 필터 사용", value=False)
    period = ""
    if use_date_filter:
        period = st.text_input(
            "📅 검색 기간", 
            placeholder="YYYY/MM/DD-YYYY/MM/DD",
            help="예: 2020/01/01-2024/12/31"
        )
    
    # Text Availability 필터
    st.markdown("#### 📄 Text Availability")
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_abstract = st.checkbox("Abstract", value=False)
    with col2:
        filter_free_full_text = st.checkbox("Free full text", value=False)
    with col3:
        filter_full_text = st.checkbox("Full text", value=True)
    
    # Article Attribute 필터
    st.markdown("#### 📊 Article Attribute")
    filter_associated_data = st.checkbox("Associated data", value=False)
    
    # Article Type 필터
    st.markdown("#### 📝 Article Type")
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_books_docs = st.checkbox("Books and Documents", value=False)
        filter_clinical_trial = st.checkbox("Clinical Trial", value=True)
    with col2:
        filter_meta_analysis = st.checkbox("Meta-Analysis", value=True)
        filter_rct = st.checkbox("Randomized Controlled Trial", value=True)
    with col3:
        filter_review = st.checkbox("Review", value=True)
        filter_systematic_review = st.checkbox("Systematic Review", value=True)
    
    # Species 필터
    st.markdown("#### 🧬 Species")
    col1, col2 = st.columns(2)
    with col1:
        species_humans = st.checkbox("Humans", value=True)
    with col2:
        species_other_animals = st.checkbox("Other Animals", value=False)

    # Sex 필터
    st.markdown("#### ⚧️ Sex")
    col1, col2 = st.columns(2)
    with col1:
        sex_female = st.checkbox("Female", value=False)
    with col2:
        sex_male = st.checkbox("Male", value=False)

    # Age 필터
    st.markdown("#### 🎂 Age")
    col1, col2, col3 = st.columns(3)
    with col1:
        age_child = st.checkbox("Child: birth-18 years", value=False)
    with col2:
        age_adult = st.checkbox("Adult: 19+ years", value=False)
    with col3:
        age_aged = st.checkbox("Aged: 65+ years", value=False)

    # Other 필터
    st.markdown("#### 🗂️ Other")
    col1, col2 = st.columns(2)
    with col1:
        other_exclude_preprints = st.checkbox("Exclude preprints", value=False)
    with col2:
        other_medline = st.checkbox("MEDLINE", value=False)


    return {
        'period': period,
        'text_filters': {
            'abstract': filter_abstract,
            'free_full_text': filter_free_full_text,
            'full_text': filter_full_text
        },
        'article_type_filters': {
            'books_docs': filter_books_docs,
            'clinical_trial': filter_clinical_trial,
            'meta_analysis': filter_meta_analysis,
            'rct': filter_rct,
            'review': filter_review,
            'systematic_review': filter_systematic_review
        },
        'associated_data': filter_associated_data,
        'species': {
            'humans': species_humans,
            'other_animals': species_other_animals,
        },
        'sex': {
            'female': sex_female,
            'male': sex_male,
        },
        'age': {
            'child': age_child,
            'adult': age_adult,
            'aged': age_aged,
        },
        'other': {
            'exclude_preprints': other_exclude_preprints,
            'medline': other_medline,
        },

    }

def execute_pubmed_search(P, I, C, O, use_P, use_I, use_C, use_O, 
                         email, api_key, filter_options):
    """PubMed 검색 실행"""
    selected_components = []
    if use_P and P: selected_components.append("P")
    if use_I and I: selected_components.append("I") 
    if use_C and C: selected_components.append("C")
    if use_O and O: selected_components.append("O")
    
    if not selected_components:
        st.error("❌ PICO 요소를 선택하고 입력하세요!")
        return
    elif not email:
        st.error("❌ NCBI 이메일을 입력하세요!")
        return
    
    # 쿼리 생성
    query_components = []
    if use_P and P: query_components.append(P)
    if use_I and I: query_components.append(I)
    if use_C and C: query_components.append(C)
    if use_O and O: query_components.append(O)

    query = build_query(query_components)
    
    # 필터 적용
    filters = build_filters(filter_options)
    
    if filters:
        filter_str = ' AND ' + ' AND '.join(filters)
        final_query = query + filter_str
    else:
        final_query = query

    st.info(f"🔍 **검색 쿼리**: {final_query}")
    
    # 날짜 파싱 (필터 옵션에서 가져오기)
    period = filter_options.get('period', '')
    mindate = maxdate = None
    if period and '-' in period:
        try:
            mindate, maxdate = period.split('-', 1)
            mindate = mindate.strip()
            maxdate = maxdate.strip()
            st.success(f"📅 **날짜 범위**: {mindate} ~ {maxdate}")
        except:
            st.warning("⚠️ 날짜 형식: YYYY/MM/DD-YYYY/MM/DD")

    try:
        # PMID 검색 (논문수 제한 없이 모든 결과)
        with st.spinner("🔍 PubMed에서 논문 검색 중..."):
            pmids = pubmed_search_all(final_query, email, retmax_per_call=10000,  # 큰 수로 설정
                                      api_key=api_key or None, mindate=mindate, maxdate=maxdate)
        
        if pmids:
            st.success(f"✅ {len(pmids)}개의 논문을 찾았습니다!")

            # 상세 정보 수집
            with st.spinner("📄 논문 상세 정보 수집 중..."):
                details = pubmed_details(pmids, email, api_key or None)

            if details:
                # 결과 표시
                df = pd.DataFrame(details)
                st.session_state.df = df
                st.dataframe(df, use_container_width=True)

                # 엑셀 다운로드
                excel_bytes = io.BytesIO()
                df.to_excel(excel_bytes, index=False, engine='openpyxl')
                st.download_button(
                    label="📥 엑셀 다운로드",
                    data=excel_bytes.getvalue(),
                    file_name=f"pubmed_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

    except Exception as e:
        st.error(f"❌ 검색 오류: {e}")

def render_ai_tab():
    """AI 분석 탭 렌더링"""
    st.markdown("### 🤖 Gemini AI 분석")

    # PubMed 검색 결과 확인
    if st.session_state.df is None or st.session_state.df.empty:
        st.warning("⚠️ 먼저 PubMed 검색을 실행하여 논문을 가져와주세요!")
        st.info("👈 **PubMed 검색** 탭에서 검색을 실행한 후 이 탭으로 돌아오세요.")
        return

    # 검색된 논문 개수 표시
    total_papers = len(st.session_state.df)
    st.success(f"✅ 분석 대상: **{total_papers}개 논문**")

    # AI 설정
    col1, col2 = st.columns(2)
    with col1:
        gemini_api_key = st.text_input(
            "🔑 Gemini API 키", 
            value=st.session_state.get('team_gemini_api_key', ''),
            type="password", 
            help="Gemini API 키를 입력하세요"
        )
    with col2:
        product_name = st.text_input(
            "🏷️ 제품/기술명", 
            value=st.session_state.get('team_product', ''),
            help="분석할 제품이나 기술명을 입력하세요"
        )

    # 분석 프롬프트 설정
    st.markdown("### 📝 분석 설정")
    analysis_mode = st.selectbox(
        "분석 모드 선택",
        ["관련성 분석", "안전성 분석", "효과성 분석", "커스텀 분석"],
        help="어떤 관점에서 분석할지 선택하세요"
    )

    if analysis_mode == "관련성 분석":
        user_prompt = f"""논문 제목: {{title}}
초록: {{abstract}}

이 논문이 '{product_name}'와 관련이 있는지 분석하고, 관련 있다면 그 이유를 한국어로 간단히 설명해주세요.
관련 없다면 '관련 없음'이라고 답해주세요."""

    elif analysis_mode == "안전성 분석":
        user_prompt = f"""논문 제목: {{title}}
초록: {{abstract}}

이 논문에서 '{product_name}'의 안전성과 관련된 내용이 있는지 분석하고, 
부작용, 합병증, 안전성 데이터 등이 언급되었다면 핵심 내용을 한국어로 요약해주세요."""

    elif analysis_mode == "효과성 분석":
        user_prompt = f"""논문 제목: {{title}}
초록: {{abstract}}

이 논문에서 '{product_name}'의 효과성과 관련된 내용이 있는지 분석하고,
치료 효과, 성공률, 개선 정도 등이 언급되었다면 핵심 내용을 한국어로 요약해주세요."""

    else:  # 커스텀 분석
        user_prompt = st.text_area(
            "💬 커스텀 프롬프트",
            value=f"논문 제목: {{title}}\n초록: {{abstract}}\n\n이 논문이 '{product_name}'와 관련 있다고 판단한 이유를 한국어로 간단히 설명해주세요.",
            height=100,
            help="분석에 사용할 프롬프트를 직접 작성하세요. {title}, {abstract}를 변수로 사용할 수 있습니다."
        )

    # Gemini 연결 상태 확인
    gemini_status = False
    if gemini_api_key:
        try:
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = model.generate_content("안녕하세요")
            if response and response.text:
                gemini_status = True
                st.success("✅ Gemini API 연결 성공!")
        except Exception as e:
            st.error(f"❌ Gemini API 오류: {e}")

    # 분석 실행 버튼
    col1, col2 = st.columns(2)
    with col1:
        analyze_all = st.button("🚀 전체 논문 분석", use_container_width=True)
    with col2:
        analyze_sample = st.button("🎯 상위 10개 샘플 분석", use_container_width=True)

    # 분석 실행
    if analyze_all or analyze_sample:
        if not gemini_status:
            st.error("❌ Gemini API 키를 확인하세요!")
        elif not product_name:
            st.error("❌ 제품/기술명을 입력하세요!")
        else:
            # 분석할 논문 선택
            df_to_analyze = st.session_state.df.copy()
            if analyze_sample:
                df_to_analyze = df_to_analyze.head(10)
                st.info("🎯 상위 10개 논문을 분석합니다")
            else:
                st.info(f"🚀 전체 {len(df_to_analyze)}개 논문을 분석합니다")

            # analysis.py의 analyze_with_gemini 함수 사용
            analyze_with_gemini(df_to_analyze, gemini_api_key, product_name, user_prompt)



def render_meddev_tab():
    """MEDDEV 분석 탭 렌더링"""
    st.markdown("### 📊 MEDDEV 2.7/1 Rev. 4 분석")

    # PDF 업로드
    uploaded_file = st.file_uploader("📎 PDF 논문 업로드", type="pdf")

    if uploaded_file is not None:
        try:
            import pdfplumber

            # PDF 텍스트 추출
            with pdfplumber.open(uploaded_file) as pdf:
                pdf_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        pdf_text += text + "\n"

            st.success(f"✅ PDF 업로드 성공! ({len(pdf.pages)}페이지)")

            # 텍스트 미리보기
            with st.expander("📖 텍스트 미리보기"):
                st.text_area("PDF 내용 (처음 2000자)", 
                            pdf_text[:2000] + "..." if len(pdf_text) > 2000 else pdf_text, 
                            height=200)

            # Gemini API 키 입력
            gemini_key_for_meddev = st.text_input(
                "🤖 Gemini API 키", 
                value=st.session_state.get('team_gemini_api_key', ''),
                type="password", 
                key="meddev_gemini_key",
                help="MEDDEV 분석에 사용할 Gemini API 키를 입력하세요"
            )
            
            # 분석 실행 버튼
            if st.button("📊 MEDDEV 분석 실행", key="pdf_analysis", use_container_width=True):
                if not gemini_key_for_meddev:
                    st.error("❌ Gemini API 키를 입력하세요!")
                elif not product_name:
                    st.error("❌ 제품/기기명을 입력하세요!")
                else:
                    execute_meddev_analysis(pdf_text, gemini_key_for_meddev)

        except ImportError:
            st.error("❌ pdfplumber가 설치되지 않았습니다.")
            st.code("pip install pdfplumber", language="bash")
            st.info("위 명령어를 터미널에서 실행하여 pdfplumber를 설치해주세요.")
        except Exception as e:
            st.error(f"❌ PDF 처리 오류: {e}")
    else:
        st.info("📄 PDF 파일을 업로드하면 MEDDEV 2.7/1 Rev. 4 분석이 진행됩니다")
        
        # 사용법 안내
        with st.expander("💡 사용법 안내"):
            st.markdown("""
            ### MEDDEV 2.7/1 Rev. 4 분석 사용법
            
            1. **PDF 업로드**: 분석할 의료기기 논문의 PDF 파일을 업로드하세요
            2. **API 키 입력**: Gemini API 키를 입력하세요
            3. **분석 실행**: "MEDDEV 분석 실행" 버튼을 클릭하세요
            
            ### 분석 결과
            - 논문 정보 (제목, 저자, 저널 등)
            - 기기 정보 (기기명, 제조회사)
            - Methodological Appraisal (방법론적 평가)
            - Relevance Appraisal (관련성 평가)
            - Contribution Appraisal (기여도 평가)
            - Overall Assessment (종합 평가)
            
            ### 주의사항
            - PDF는 텍스트 추출이 가능한 형태여야 합니다
            - 분석에 2-3분 정도 소요됩니다
            - 결과는 마크다운 파일로 다운로드 가능합니다
            """)

# ...existing code...

def render_meddev_tab():
    """MEDDEV 분석 탭 렌더링"""
    st.markdown("### 📊 MEDDEV 2.7/1 Rev. 4 분석")

    # 세션 상태 초기화
    if 'meddev_analysis_result' not in st.session_state:
        st.session_state.meddev_analysis_result = None
    if 'meddev_excel_data' not in st.session_state:
        st.session_state.meddev_excel_data = None

    # PDF 업로드
    uploaded_file = st.file_uploader("📎 PDF 논문 업로드", type="pdf")

    if uploaded_file is not None:
        try:
            import pdfplumber

            # PDF 텍스트 추출
            with pdfplumber.open(uploaded_file) as pdf:
                pdf_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        pdf_text += text + "\n"

            st.success(f"✅ PDF 업로드 성공! ({len(pdf.pages)}페이지)")

            # 제품/기기명 입력란 추가
            product_name = st.text_input(
                "🏷️ 제품/기기명",
                value=st.session_state.get('team_product', ''),
                help="분석할 제품이나 기술명을 입력하세요"
            )

            # 텍스트 미리보기
            with st.expander("📖 텍스트 미리보기"):
                st.text_area("PDF 내용 (처음 2000자)", 
                            pdf_text[:2000] + "..." if len(pdf_text) > 2000 else pdf_text, 
                            height=200)

            # Gemini API 키 입력
            gemini_key_for_meddev = st.text_input(
                "🤖 Gemini API 키", 
                value=st.session_state.get('team_gemini_api_key', ''),
                type="password", 
                key="meddev_gemini_key",
                help="MEDDEV 분석에 사용할 Gemini API 키를 입력하세요"
            )
            
            # 분석 실행 버튼과 리셋 버튼
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 MEDDEV 분석 실행", key="pdf_analysis", use_container_width=True):
                    if not gemini_key_for_meddev:
                        st.error("❌ Gemini API 키를 입력하세요!")
                    else:
                        # 분석 실행 및 세션에 저장
                        try:
                            import google.generativeai as genai
                            
                            # Gemini 설정
                            genai.configure(api_key=gemini_key_for_meddev)
                            model = genai.GenerativeModel('gemini-2.0-flash-exp')

                            # 텍스트 길이 제한
                            max_length = 50000
                            processed_text = pdf_text
                            if len(pdf_text) > max_length:
                                processed_text = pdf_text[:max_length] + "\n...(텍스트 길이 제한)"
                                st.warning(f"⚠️ 텍스트가 {max_length}자로 제한되어 분석됩니다")

                            # 분석 실행
                            prompt = get_meddev_analysis_prompt(processed_text, product_name)
                            
                            with st.spinner("📊 MEDDEV 분석 중... (2-3분 소요)"):
                                response = model.generate_content(prompt)

                                if response and response.text:
                                    # 세션에 결과 저장
                                    st.session_state.meddev_analysis_result = response.text
                                    
                                    # 엑셀 데이터 생성 및 저장
                                    excel_data = parse_meddev_to_excel(response.text)
                                    excel_bytes = create_meddev_excel_file(excel_data, pdf_text, processed_text, response.text)
                                    st.session_state.meddev_excel_data = excel_bytes.getvalue()
                                    
                                    st.success("✅ 분석 완료!")
                                else:
                                    st.error("❌ Gemini 분석 응답을 받지 못했습니다")
                        except Exception as e:
                            st.error(f"❌ 분석 오류: {e}")
            
            with col2:
                if st.button("🔄 결과 초기화", use_container_width=True):
                    st.session_state.meddev_analysis_result = None
                    st.session_state.meddev_excel_data = None
                    st.success("✅ 결과가 초기화되었습니다!")
                    st.rerun()

        except ImportError:
            st.error("❌ pdfplumber가 설치되지 않았습니다.")
            st.code("pip install pdfplumber", language="bash")
            st.info("위 명령어를 터미널에서 실행하여 pdfplumber를 설치해주세요.")
        except Exception as e:
            st.error(f"❌ PDF 처리 오류: {e}")
    else:
        st.info("📄 PDF 파일을 업로드하면 MEDDEV 2.7/1 Rev. 4 분석이 진행됩니다")
        
        # 사용법 안내
        with st.expander("💡 사용법 안내"):
            st.markdown("""
            ### MEDDEV 2.7/1 Rev. 4 분석 사용법
            
            1. **PDF 업로드**: 분석할 의료기기 논문의 PDF 파일을 업로드하세요
            2. **API 키 입력**: Gemini API 키를 입력하세요
            3. **분석 실행**: "MEDDEV 분석 실행" 버튼을 클릭하세요
            4. **결과 확인**: 분석 완료 후 결과를 확인하고 다운로드하세요
            5. **초기화**: 새로운 분석을 위해 "결과 초기화" 버튼을 사용하세요
            
            ### 분석 결과
            - 논문 정보 (제목, 저자, 저널 등)
            - 기기 정보 (기기명, 제조회사)
            - Methodological Appraisal (방법론적 평가)
            - Relevance Appraisal (관련성 평가)
            - Contribution Appraisal (기여도 평가)
            - Overall Assessment (종합 평가)
            
            ### 주의사항
            - PDF는 텍스트 추출이 가능한 형태여야 합니다
            - 분석에 2-3분 정도 소요됩니다
            - 결과는 엑셀과 마크다운 파일로 다운로드 가능합니다
            - 다운로드 후에도 결과가 유지됩니다
            """)

    # 분석 결과 표시 (다운로드 후에도 유지됨)
    if st.session_state.meddev_analysis_result:
        st.markdown("### 📊 MEDDEV 분석 결과")
        st.markdown(st.session_state.meddev_analysis_result)

        if st.session_state.meddev_excel_data:
            col1, col2 = st.columns(2)
            
            with col1:
                # 엑셀 다운로드
                st.download_button(
                    label="📊 엑셀 다운로드",
                    data=st.session_state.meddev_excel_data,
                    file_name=f"MEDDEV_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col2:
                # 마크다운 다운로드
                markdown_result = f"""# MEDDEV 2.7/1 Rev. 4 분석

분석 날짜: {pd.Timestamp.now().strftime('%Y년 %m월 %d일 %H시 %M분')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{st.session_state.meddev_analysis_result}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

분석 도구: Gemini AI 기반 MEDDEV 분석 시스템
생성 시간: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                st.download_button(
                    label="📝 마크다운 다운로드",
                    data=markdown_result,
                    file_name=f"MEDDEV_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
# ...existing code...

def parse_meddev_to_excel(text):
    """MEDDEV 분석 결과를 엑셀용 데이터로 파싱 - 새로운 표 형식 반영"""
    data = {
        'paper_info': [],
        'device_info': [],
        'methodological': [],
        'relevance': [],
        'relevance_suitability': [],  # 새로 추가
        'contribution': [],
        'overall': []
    }
    
    try:
        # 논문 정보 추출
        paper_patterns = [
            r'Title:\s*(.+)',
            r'Authors:\s*(.+)', 
            r'Journal:\s*(.+)',
            r'Publication Year:\s*(.+)',
            r'Study Type:\s*(.+)'
        ]
        
        for pattern in paper_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                field_name = pattern.split(':')[0].replace('r\'', '').replace('\\s*', '')
                data['paper_info'].append([field_name, match.group(1).strip()])
        
        # 기기 정보 추출
        device_patterns = [
            r'Device Name:\s*(.+)',
            r'Company:\s*(.+)'
        ]
        
        for pattern in device_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                field_name = pattern.split(':')[0].replace('r\'', '').replace('\\s*', '')
                data['device_info'].append([field_name, match.group(1).strip()])
        

        # 표 데이터 추출 함수
        def extract_table_between_markers(start_marker, end_marker):
            pattern = f'{start_marker}(.*?){end_marker}'
            match = re.search(pattern, text, re.DOTALL)
            if match:
                table_content = match.group(1).strip()
                lines = table_content.split('\n')
                
                table_data = []
                for line in lines:
                    line = line.strip()
                    if line and line.startswith('|') and line.endswith('|'):
                        if not ('---' in line or line.count('|') < 3):
                            cells = [cell.strip() for cell in line.split('|')[1:-1]]
                            if len(cells) >= 2:
                                # 컬럼 수를 4개로 통일
                                while len(cells) < 4:
                                    cells.append('')
                                table_data.append(cells[:4])  # 4개만 사용
                
                return table_data
            return []
        
        # 각 표 데이터 추출
        data['methodological'] = extract_table_between_markers('METHODOLOGICAL_TABLE_START', 'METHODOLOGICAL_TABLE_END')
        data['relevance'] = extract_table_between_markers('RELEVANCE_TABLE_START', 'RELEVANCE_TABLE_END')
        data['relevance_suitability'] = extract_table_between_markers('RELEVANCE_SUITABILITY_TABLE_START', 'RELEVANCE_SUITABILITY_TABLE_END')
        data['contribution'] = extract_table_between_markers('CONTRIBUTION_TABLE_START', 'CONTRIBUTION_TABLE_END')
        data['overall'] = extract_table_between_markers('OVERALL_TABLE_START', 'OVERALL_TABLE_END')
        
    except Exception as e:
        st.warning(f"파싱 중 오류: {e}")
        data['raw_text'] = text
    
    return data

def create_meddev_excel_file(data, pdf_text, processed_text, analysis_text):
    """엑셀 파일 생성 - 새로운 표 형식 반영"""
    excel_bytes = io.BytesIO()
    
    with pd.ExcelWriter(excel_bytes, engine='openpyxl') as writer:
        # # 1. 요약 시트
        # summary_data = {
        #     '항목': ['분석 날짜', '원본 텍스트 길이', '처리된 텍스트 길이', '분석 결과 길이'],
        #     '내용': [
        #         pd.Timestamp.now().strftime('%Y년 %m월 %d일 %H시 %M분'),
        #         f"{len(pdf_text):,} 글자",
        #         f"{len(processed_text):,} 글자",
        #         f"{len(analysis_text):,} 글자"
        #     ]
        # }
        # summary_df = pd.DataFrame(summary_data)
        # summary_df.to_excel(writer, sheet_name='요약', index=False)
        
        # 2-3. 논문/기기 정보 시트
        if data['paper_info']:
            paper_df = pd.DataFrame(data['paper_info'], columns=['항목', '내용'])
            paper_df.to_excel(writer, sheet_name='논문정보', index=False)
        
        if data['device_info']:
            device_df = pd.DataFrame(data['device_info'], columns=['항목', '내용'])
            device_df.to_excel(writer, sheet_name='기기정보', index=False)
        
        # 4. STEP 2: Methodological Appraisal
        if data['methodological']:
            # 처음 3개 컬럼만 사용
            method_data = [row[:3] for row in data['methodological']]
            method_df = pd.DataFrame(method_data, columns=['Aspects covered', 'Weight', 'Remarks'])
            method_df.to_excel(writer, sheet_name='STEP2_Methodological', index=False)
        
        # 5. STEP 3: Relevance Appraisal
        if data['relevance']:
            # 4개 컬럼 모두 사용
            relevance_df = pd.DataFrame(data['relevance'], columns=['Description', 'Examples', 'V', 'Comment'])
            relevance_df.to_excel(writer, sheet_name='STEP3_Relevance', index=False)
        
        # 6. STEP 3: Relevance Suitability (새로 추가)
        if data['relevance_suitability']:
            # 처음 3개 컬럼만 사용
            suitability_data = [row[:3] for row in data['relevance_suitability']]
            rel_suit_df = pd.DataFrame(suitability_data, columns=['Suitability Criteria', 'Weight', 'Description'])
            rel_suit_df.to_excel(writer, sheet_name='STEP3_Relevance_Suitability', index=False)
        
        # 7. STEP 4: Contribution Appraisal  
        if data['contribution']:
            # 처음 3개 컬럼만 사용
            contribution_data = [row[:3] for row in data['contribution']]
            contribution_df = pd.DataFrame(contribution_data, columns=['Contribution Criteria', 'Weight', 'Remarks'])
            contribution_df.to_excel(writer, sheet_name='STEP4_Contribution', index=False)
        
        # 8. STEP 5: Overall Assessment
        if data['overall']:
            # 4개 컬럼 모두 사용
            overall_df = pd.DataFrame(data['overall'], columns=['Appraisal Summary', 'Weight', 'Results', 'Overall appraisal'])
            overall_df.to_excel(writer, sheet_name='STEP5_Overall', index=False)

        
        # # 9. 전체 분석 결과
        # full_result_df = pd.DataFrame({'전체 분석 결과': [analysis_text]})
        # full_result_df.to_excel(writer, sheet_name='전체결과', index=False)
        
        # 10. 파싱 실패시 원본 저장
        if 'raw_text' in data:
            raw_df = pd.DataFrame({'원본 분석 결과': [data['raw_text']]})
            raw_df.to_excel(writer, sheet_name='원본데이터', index=False)
    
    return excel_bytes
