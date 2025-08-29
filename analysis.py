import streamlit as st
import pandas as pd
import time
import io
import google.generativeai as genai

def analyze_with_gemini(df, gemini_api_key, product_name, user_prompt):
    """Gemini AI를 사용한 논문 분석"""
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    df_copy = df.copy()

    progress_bar = st.progress(0)
    status_text = st.empty()

    with st.spinner("🤖 AI 분석 중..."):
        for idx, row in df_copy.iterrows():
            progress = (idx + 1) / len(df_copy)
            progress_bar.progress(progress)
            status_text.text(f"처리 중... {idx + 1}/{len(df_copy)}")

            # 제품명이 제목이나 초록에 포함되는지 확인
            if (product_name.lower() in str(row['Title']).lower() or 
                product_name.lower() in str(row['Abstract']).lower()):
                df_copy.at[idx, 'Select'] = 'Y'

                # Gemini로 이유 생성
                prompt = user_prompt.format(
                    title=str(row['Title'])[:300],
                    abstract=str(row['Abstract'])[:1000],
                    product=product_name
                )
                try:
                    response = model.generate_content(prompt)
                    if response and response.text:
                        df_copy.at[idx, 'Reason'] = response.text.strip()
                    else:
                        df_copy.at[idx, 'Reason'] = "응답 없음"
                except Exception as e:
                    df_copy.at[idx, 'Reason'] = f"Gemini 오류: {e}"
            else: 
                df_copy.at[idx, 'Select'] = ''
                df_copy.at[idx, 'Reason'] = ''

            # API 요청 제한
            time.sleep(0.5)

    progress_bar.empty()
    status_text.empty()

    # 결과 저장 및 표시
    st.session_state.df = df_copy
    st.success("✅ AI 분석 완료!")

    selected_count = len(df_copy[df_copy['Select'] == 'Y'])
    st.info(f"📊 전체 {len(df_copy)}개 중 {selected_count}개가 관련 있음으로 분석")

    st.dataframe(df_copy, use_container_width=True)

    # 결과 다운로드
    excel_bytes = io.BytesIO()
    df_copy.to_excel(excel_bytes, index=False, engine='openpyxl')
    st.download_button(
        label="📥 분석 결과 다운로드",
        data=excel_bytes.getvalue(),
        file_name=f"gemini_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

def get_meddev_analysis_prompt(text, product_name):
    """MEDDEV 2.7/1 Rev. 4 분석 프롬프트"""
    return f"""
아래는 의료기기 임상 논문의 본문입니다.

분석 대상 기기명: {product_name}

1. 논문 전체에 대한 평가(방법론, 일반적 관련성, 기여도, 종합평가)는 논문 자체 기준으로 MEDDEV 2.7/1 Rev.4에 따라 분석하세요.
2. 단, 'STEP 3: Relevance Suitability' 표만 '{product_name}'(우리 기기)와의 적합성/관련성 기준으로 분석하세요.
**All Remarks, Comments, and explanations in the tables must be written in English.**

논문 내용:
{text[:10000]}

다음 형식으로 분석해주세요:

## 논문 정보
Title: [논문 제목]
Authors: [저자]
Journal: [저널명]
Publication Year: [발행년도]
Study Type: [연구 유형]

## 기기 정보  
Device Name: [의료기기명]
Company: [제조회사]

## STEP 2: Methodological Appraisal
METHODOLOGICAL_TABLE_START
| Aspects covered | Weight | Remarks |
|-----------------|--------|---------|
| Information on elementary aspects | Adequate (2) / Non adequate (1) | [평가 내용] |
| Patients number | High (2) / Medium (1) / Poor (0) | [평가 내용] |
| Statistical method(s) | Adequate (2) / Non adequate (1) | [평가 내용] |
| Adequate controls | Adequate (2) / Non adequate (1) | [평가 내용] |
| Collection of mortality and serious adverse events data | Adequate (2) / Non adequate (1) | [평가 내용] |
| Interpretation of the authors | Good (1) / Misinterpretation (0) | [평가 내용] |
| Study legality | Legal (1) / Illegal (0) | [평가 내용] |
| Total | [총점] (10-12: Excellent, 8-9: Very Good, 6-7: Good, 0-5: Poor) | [종합 평가] |
METHODOLOGICAL_TABLE_END

# ...existing code...

## STEP 3: Relevance Appraisal  
RELEVANCE_TABLE_START
| Description | Examples | V | Comment |
|-------------|----------|---|---------|
# ...existing code...

| To what extent are the data generated from the device under evaluation representative of the device under evaluation? | Device under evaluation | [ ] | |
| | Equivalent device | [ ] | |
| | Benchmark device | [ ] | |
| | Other devices and medical alternatives | [ ] | |
| | Data concerning the medical conditions that are managed with the device | [ ] | |
| What aspects are covered? | Pivotal performance data | [ ] | |
| | Pivotal safety data | [ ] | |
| | Claims | [ ] | |
| | Identification of hazards | [ ] | |
| | Estimation and management of risks | [ ] | |
| | Enhancement of current knowledge / the state of the art | [ ] | |
| | Determination and justification of criteria for the evaluation of the risk/benefit relationship | [ ] | |
| | Determination and justification of criteria for the evaluation of acceptability of undesirable side-effects | [ ] | |
| | Determination of equivalence | [ ] | |
| | Justification of the validity of surrogate endpoints | [ ] | |
| Are the data relevant to the intended purpose of the device or to claims about the device? | Representative of the entire intended purpose for all patient populations and all claims foreseen for the device under evaluation | [ ] | |
| | Concerns specific models/sizes/settings, or concerns specific aspects of the intended purpose or of claims | [ ] | |
| | Does not concern the intended purpose or claims | [ ] | |
| - Model, size, or settings of the device | Smallest / intermediate / largest size | [ ] | |
| | Lowest / intermediate / highest dose | [ ] | |
| | Etc. | [ ] | |
| - User group | Specialists | [ ] | |
| | General practitioners | [ ] | |
| | Nurses | [ ] | |
| | Adult healthy lay persons | [ ] | |
| | Disabled persons | [ ] | |
| | Children | [ ] | |
| | Etc. | [ ] | |
| - Medical indication (if applicable) | Migraine prophylaxis | [ ] | |
| | Treatment of acute migraine | [ ] | |
| | Rehabilitation after stroke | [ ] | |
| | Etc. | [ ] | |
| - Age group | pre-term infants / neonates / children / adolescents / adults / old age | [ ] | |
| - Gender | Female / male | [ ] | |
| - Type and severity of the medical condition | Early / late stage | [ ] | |
| | Mild / intermediate / serious form | [ ] | |
| | Acute / chronic phase | [ ] | |
| | Etc. | [ ] | |
| - Range of time | Duration of application or use | [ ] | |
| | Number of repeat exposures | [ ] | |
| | Duration of follow-up | [ ] | |
RELEVANCE_TABLE_END

## STEP 3: Relevance Appraisal (Suitability)
RELEVANCE_SUITABILITY_TABLE_START
| Suitability Criteria: Description | Weight | Description |
|-----------------------------------|--------|-------------|
| Appropriate Device: Were the data generated from the device in question? | 2 / 1 | Actual device / Comparable device |
| Appropriate device application: Was the device used for the same intended use (e.g., methods of deployment, application, etc.)? | 3 / 2 / 1 | Same use / Minor deviation / Major deviation |
| Appropriate patient group: Was the data generated from a patient group that is representative of the intended treatment population (e.g., age, sex, etc.) and clinical condition (i.e., disease, including state and severity)? | 3 / 2 / 1 | Applicable / Limited / Different population |
| Acceptable report/data collation: Do the reports or collations of data contain sufficient information to be able to undertake a rational and objective assessment? | 3 / 2 / 1 | High quality / Minor deficiencies / Insufficient information |
| Total | 10 to 11 | Excellent |
| | 8 to 9 | Very Good |
| | 6 to 7 | Good |
| | 0 to 5 | Poor |
RELEVANCE_SUITABILITY_TABLE_END


## Acceptance criteria: 
The total Methodological result should be Very Good or Excellent.

## STEP 4: Contribution Appraisal
CONTRIBUTION_TABLE_START
| Contribution Criteria: Description | Weight | Remarks |
|------------------------------------|--------|---------|
| Data source type / Was the design of the study appropriate? | Yes (2) / No (1) | [평가 내용] |
| Outcome measures: Does the outcome measures reported reflect the intended performance of the device? | Yes (2) / No (1) | [평가 내용] |
| Follow up: Long enough to assess whether duration of treatment effects and identify complications? | Yes (2) / No (1) | [평가 내용] |
| Statistical significance: Has a statistical analysis of the data been provided and is it appropriate? | Yes (2) / No (1) | [평가 내용] |
| Clinical significance: Was the magnitude of the treatment effect observed clinically significant? | Yes (2) / No (1) | [평가 내용] |
| Total | | 9 to 10: Excellent / 7 to 8: Very Good / 5 to 6: Good / 0 to 4: Poor |
CONTRIBUTION_TABLE_END


# ...existing code...

## STEP 5: Overall Assessment
OVERALL_TABLE_START
| Appraisal Summary | Weight | Results | Overall appraisal |
|-------------------|--------|---------|------------------|
| Methodological | [점수] / 12 | [평가등급] | |
| Relevance | [점수] / 11 | [평가등급] | [총점] / 33 |
| Contribution | [점수] / 10 | [평가등급] | |
OVERALL_TABLE_END

## Acceptance Criteria
The overall result should be Very Good or Excellent.

## 결론
[종합 평가 및 권장사항]

위 형식을 정확히 따라 분석해주세요. 표 구분자(TABLE_START/TABLE_END)를 반드시 포함해주세요.
"""
