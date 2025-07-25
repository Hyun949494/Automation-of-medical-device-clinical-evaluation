# analysis.py - MEDDEV 분석 프롬프트 모음 (엑셀 지원)

def get_meddev_table_analysis_prompt(processed_text):
    """MEDDEV 2.7/1 Rev. 4 완전한 표 형식 분석 프롬프트 (엑셀용)"""
    return f"""
Please analyze the following paper according to MEDDEV 2.7/1 Rev. 4 criteria and provide a complete structured analysis that will be converted to Excel format.

IMPORTANT: Please provide your response in the exact format shown below, with clear sections and structured data.

═══════════════════════════════════════════════════════════════════
## STEP 1: Paper Summary and Device Information
═══════════════════════════════════════════════════════════════════

### Paper Information
Title: [Extract exact paper title]
Authors: [First author, corresponding author]
Journal: [Journal name and impact factor if available]
Publication Year: [Year]
Study Type: [RCT/Observational/Systematic review/Meta-analysis/Case series]

### Device Information
Company: [Manufacturer name]
Device Name: [Medical device name]
Design: [Size, materials, key features]
Principle of Operation: [How it works, mechanism]

═══════════════════════════════════════════════════════════════════
## STEP 2: Methodological Appraisal
═══════════════════════════════════════════════════════════════════

METHODOLOGICAL_TABLE_START
Aspects covered|Weight|Score|Remarks
Information on elementary aspects|Adequate (2) / Non adequate (1) / Poor (0)|[SCORE]|[Evidence from paper about study design]
Patients number|High (2) / Medium (1) / Poor (0)|[SCORE]|[Exact patient number and adequacy assessment]
Statistical methods|Adequate (2) / Non adequate (1)|[SCORE]|[Statistical methods used]
Adequate controls|Adequate (2) / Non adequate (1)|[SCORE]|[Control group description]
Collection of mortality and SAE data|Adequate (2) / Non adequate (1)|[SCORE]|[Safety data collection methods]
Interpretation of authors|Good (1) / Misinterpretation (0)|[SCORE]|[Authors' interpretation assessment]
Study legality|Legal (1) / Illegal (0)|[SCORE]|[Ethics approval, consent, compliance]
TOTAL METHODOLOGICAL SCORE|[SUM]/12|[TOTAL]|[Overall assessment]
METHODOLOGICAL_TABLE_END

Methodological Grade: [Excellent/Very Good/Good/Poor based on score]

═══════════════════════════════════════════════════════════════════
## STEP 3: Relevance Appraisal
═══════════════════════════════════════════════════════════════════

RELEVANCE_TABLE_START
Description|Weight|Score|Remarks
Appropriate Device|2 = Actual device / 1 = Comparable device|[SCORE]|[Device assessment]
Appropriate device application|3 = Same use / 2 = Minor deviation / 1 = Major deviation|[SCORE]|[Application assessment]
Appropriate patient group|3 = Applicable / 2 = Limited / 1 = Different population|[SCORE]|[Patient group assessment]
Acceptable report/data collation|3 = High quality / 2 = Minor deficiencies / 1 = Insufficient|[SCORE]|[Report quality assessment]
TOTAL RELEVANCE SCORE|[SUM]/11|[TOTAL]|[Overall relevance assessment]
RELEVANCE_TABLE_END

Relevance Grade: [Excellent/Very Good/Good/Poor based on score]

═══════════════════════════════════════════════════════════════════
## STEP 4: Contribution Appraisal
═══════════════════════════════════════════════════════════════════

CONTRIBUTION_TABLE_START
Contribution Criteria|Weight|Score|Remarks
Data source type|2 = Yes / 1 = No|[SCORE]|[Study design appropriateness]
Outcome measures|2 = Yes / 1 = No|[SCORE]|[Endpoints relevance]
Follow up|2 = Yes / 1 = No|[SCORE]|[Follow-up duration adequacy]
Statistical significance|2 = Yes / 1 = No|[SCORE]|[Statistical analysis quality]
Clinical significance|2 = Yes / 1 = No|[SCORE]|[Clinical importance assessment]
TOTAL CONTRIBUTION SCORE|[SUM]/10|[TOTAL]|[Overall contribution assessment]
CONTRIBUTION_TABLE_END

Contribution Grade: [Excellent/Very Good/Good/Poor based on score]

═══════════════════════════════════════════════════════════════════
## STEP 5: Overall Assessment
═══════════════════════════════════════════════════════════════════

OVERALL_TABLE_START
Assessment Category|Score|Maximum|Percentage
Methodological Appraisal|[SCORE]|12|[PERCENTAGE]%
Relevance Appraisal|[SCORE]|11|[PERCENTAGE]%
Contribution Appraisal|[SCORE]|10|[PERCENTAGE]%
TOTAL SCORE|[TOTAL]/33|33|[TOTAL_PERCENTAGE]%
OVERALL_TABLE_END

Overall Grade: [Excellent/Very Good/Good/Poor based on total score]

═══════════════════════════════════════════════════════════════════
## STEP 6: Final Assessment Summary
═══════════════════════════════════════════════════════════════════

### Scores Summary
- Methodological Appraisal: [Score]/12 - [Grade]
- Relevance Appraisal: [Score]/11 - [Grade]
- Contribution Appraisal: [Score]/10 - [Grade]
- TOTAL SCORE: [Total]/33 - [FINAL GRADE]

### Key Findings

**Strengths:**
- [Methodological strength 1]
- [Methodological strength 2]
- [Relevance strength 1]
- [Contribution strength 1]

**Limitations:**
- [Methodological limitation 1]
- [Methodological limitation 2]
- [Relevance limitation 1]
- [Contribution limitation 1]

### MEDDEV Regulatory Recommendations
**Study Acceptability:** [Acceptable/Conditional/Not Acceptable]
**Evidence Level:** [High/Medium/Low]
**Additional Studies Needed:** [Yes/No with rationale]

═══════════════════════════════════════════════════════════════════

**Analyzed Paper:**
{processed_text}

**CRITICAL INSTRUCTIONS:**
1. **REPLACE ALL [PLACEHOLDERS]** with actual data from the paper
2. **PROVIDE EXACT NUMERICAL SCORES** for each criterion (0, 1, 2, or 3)
3. **CALCULATE ACCURATE TOTALS** and percentages
4. **USE EVIDENCE FROM PAPER ONLY** - no external knowledge
5. **MAINTAIN EXACT FORMAT** for proper Excel conversion
6. **FILL ALL TABLE SECTIONS** completely
7. **PROVIDE SPECIFIC JUSTIFICATION** for each score
8. **ALL RESPONSES IN ENGLISH**
9. **FOLLOW MEDDEV STANDARDS** precisely

The format above is designed for automatic Excel conversion - DO NOT change the table markers (TABLE_START/TABLE_END) or structure.
"""

def get_literature_analysis_prompt(processed_text):
    """기존 일반 문헌 분석 프롬프트"""
    return f"""
Please analyze the following medical paper systematically and create a comprehensive literature analysis report in English.

═══════════════════════════════════════════════════════════════════
## 1. Basic Paper Information
═══════════════════════════════════════════════════════════════════

### Paper Overview
- **Title:** [Paper title]
- **Authors:** [First author, corresponding author]
- **Journal:** [Journal name, Impact Factor]
- **Publication Year:** [Publication year]
- **DOI:** [DOI number if available]

### Study Design
- **Study Type:** [RCT/Observational study/Meta-analysis/Systematic review/Others]
- **Study Period:** [Study duration]
- **Study Population:** [Target population description]
- **Sample Size:** [Number of participants]
- **Setting:** [Study location/setting]

═══════════════════════════════════════════════════════════════════
## 2. Methodology Analysis
═══════════════════════════════════════════════════════════════════

### Study Design Details
- **Study Design:** [Detailed study design description]
- **Inclusion Criteria:** [Subject inclusion criteria]
- **Exclusion Criteria:** [Subject exclusion criteria]
- **Sample Size Calculation:** [Power analysis and rationale]
- **Randomization:** [Randomization method if applicable]
- **Blinding:** [Blinding procedures if applicable]

### Intervention Details
- **Primary Intervention:** [Detailed intervention description]
- **Control/Comparison:** [Control group description]
- **Duration:** [Treatment/follow-up duration]
- **Compliance:** [Adherence measurement]

### Outcome Measures
- **Primary Endpoint:** [Main outcome measure]
- **Secondary Endpoints:** [Additional outcome measures]
- **Safety Measures:** [Safety assessments]
- **Assessment Methods:** [How outcomes were measured]

### Statistical Analysis
- **Primary Statistical Methods:** [Statistical techniques used]
- **Significance Level:** [p-value criteria]
- **Effect Size:** [Effect size measurement]
- **Confidence Interval:** [CI settings]
- **Missing Data:** [How missing data was handled]

═══════════════════════════════════════════════════════════════════
## 3. Results Analysis
═══════════════════════════════════════════════════════════════════

### Demographics
- **Total Participants:** [Number enrolled/analyzed]
- **Age:** [Mean age ± SD or median (range)]
- **Gender:** [Male/female distribution]
- **Baseline Characteristics:** [Key baseline data]

### Primary Results
- **Primary Outcome Results:** [Main findings with statistics]
- **Statistical Significance:** [p-values and CI]
- **Effect Size:** [Clinical significance assessment]

### Secondary Results
- **Secondary Outcome Results:** [Additional findings]
- **Subgroup Analysis:** [If performed]
- **Safety Results:** [Adverse events, complications]

### Study Quality Assessment
- **Risk of Bias:** [Assessment of study limitations]
- **Confounding Factors:** [Potential confounders]
- **Generalizability:** [External validity assessment]

═══════════════════════════════════════════════════════════════════
## 4. Clinical Significance
═══════════════════════════════════════════════════════════════════

### Clinical Relevance
- **Clinical Impact:** [Real-world clinical significance]
- **Practice Implications:** [How results apply to practice]
- **Patient Benefits:** [Direct patient benefits]
- **Cost-Effectiveness:** [Economic considerations if mentioned]

### Comparison with Literature
- **Consistency:** [How results compare with existing evidence]
- **Novel Findings:** [New insights from this study]
- **Contradictions:** [Any conflicting results]

═══════════════════════════════════════════════════════════════════
## 5. Study Limitations and Strengths
═══════════════════════════════════════════════════════════════════

### Strengths
- [Study strength 1]
- [Study strength 2]
- [Study strength 3]

### Limitations
- [Study limitation 1]
- [Study limitation 2]
- [Study limitation 3]

### Authors' Conclusions
- **Main Conclusions:** [Authors' primary conclusions]
- **Clinical Recommendations:** [Authors' recommendations]
- **Future Research:** [Authors' suggestions for future studies]

═══════════════════════════════════════════════════════════════════
## 6. Overall Assessment
═══════════════════════════════════════════════════════════════════

### Evidence Quality
- **Study Quality:** [High/Medium/Low with justification]
- **Evidence Level:** [Level I-IV based on study design]
- **Recommendation Grade:** [Based on evidence quality]

### Clinical Application
- **Applicability:** [How applicable to clinical practice]
- **Implementation:** [Barriers or facilitators to implementation]
- **Regulatory Considerations:** [If relevant to regulatory approval]

### Future Directions
- **Research Gaps:** [Identified knowledge gaps]
- **Recommended Studies:** [Suggestions for future research]
- **Clinical Trial Needs:** [If additional trials needed]

═══════════════════════════════════════════════════════════════════

**Analyzed Paper:**
{processed_text}

**Analysis Guidelines:**
1. Extract specific data from the paper only
2. Provide detailed, evidence-based analysis
3. Include exact statistics when available
4. Assess clinical significance objectively
5. Identify study limitations honestly
6. Base all evaluations on paper content
7. Use professional medical language
8. **ALL RESPONSES MUST BE IN ENGLISH**
"""

def get_quick_analysis_prompt(processed_text):
    """빠른 논문 분석 프롬프트"""
    return f"""
Please provide a quick but comprehensive analysis of this medical paper in English.

**Paper to analyze:**
{processed_text}

**Please provide:**

## Quick Summary
- **Study Type:** [RCT/Observational/Review/etc.]
- **Sample Size:** [Number of participants]
- **Main Intervention:** [What was tested]
- **Primary Outcome:** [Main result measured]
- **Key Finding:** [Main result in 1-2 sentences]

## Clinical Significance
- **Clinical Impact:** [How important is this finding]
- **Practice Change:** [Should practice change based on this]
- **Patient Benefit:** [Direct benefit to patients]

## Study Quality
- **Strengths:** [2-3 key strengths]
- **Limitations:** [2-3 key limitations]
- **Reliability:** [High/Medium/Low and why]

## Bottom Line
[One paragraph summary of whether this study is clinically meaningful and reliable]

**Guidelines:**
- Extract from paper content only
- Be concise but thorough
- Focus on clinical relevance
- **ALL RESPONSES IN ENGLISH**
"""

def get_regulatory_analysis_prompt(processed_text):
    """규제 제출용 분석 프롬프트"""
    return f"""
Please analyze this paper for regulatory submission purposes according to international medical device standards.

**Paper for regulatory analysis:**
{processed_text}

**Regulatory Assessment:**

## Study Classification
- **Study Design:** [Detailed classification]
- **Evidence Level:** [Level I-IV with justification]
- **Regulatory Category:** [Pre-market/Post-market/Surveillance]

## Quality Assessment
- **GCP Compliance:** [Good Clinical Practice adherence]
- **Statistical Validity:** [Statistical methods appropriateness]
- **Data Integrity:** [Data quality assessment]
- **Bias Risk:** [Risk of bias evaluation]

## Regulatory Relevance
- **Device Classification:** [Class I/II/III relevance]
- **Safety Evidence:** [Safety data quality and completeness]
- **Efficacy Evidence:** [Efficacy data strength]
- **Predicate Comparison:** [Comparison with existing devices]

## Regulatory Recommendation
- **Acceptability:** [Acceptable/Conditional/Not Acceptable]
- **Evidence Gap:** [What additional evidence is needed]
- **Study Role:** [How this fits in regulatory dossier]

## Risk-Benefit Assessment
- **Benefits:** [Documented clinical benefits]
- **Risks:** [Identified risks and safety concerns]
- **Risk Mitigation:** [Risk management considerations]

**Guidelines:**
- Focus on regulatory requirements
- Assess according to FDA/CE/PMDA standards
- Emphasize safety and efficacy evidence
- **ALL RESPONSES IN ENGLISH**

**Analyzed Paper:**
{processed_text}
"""

def get_systematic_review_prompt(processed_text):
    """체계적 문헌고찰용 분석 프롬프트"""
    return f"""
Please analyze this paper for inclusion in a systematic review, following PRISMA guidelines.

**Paper for systematic review:**
{processed_text}

**Systematic Review Analysis:**

## Eligibility Assessment
- **Population:** [Study population description and relevance]
- **Intervention:** [Intervention details and appropriateness]
- **Comparator:** [Control/comparison group adequacy]
- **Outcomes:** [Outcome measures and relevance]
- **Study Design:** [Design appropriateness for review question]

## Quality Assessment (Risk of Bias)
- **Selection Bias:** [Random sequence generation, allocation concealment]
- **Performance Bias:** [Blinding of participants and personnel]
- **Detection Bias:** [Blinding of outcome assessment]
- **Attrition Bias:** [Incomplete outcome data]
- **Reporting Bias:** [Selective reporting assessment]
- **Other Bias:** [Any other sources of bias]

## Data Extraction
- **Study Characteristics:** [Key study features for review]
- **Participant Characteristics:** [Demographics and baseline data]
- **Intervention Details:** [Detailed intervention description]
- **Outcome Data:** [Extractable outcome data]
- **Statistical Data:** [Means, SDs, effect sizes, CIs]

## Meta-Analysis Suitability
- **Data Availability:** [Sufficient data for meta-analysis]
- **Outcome Compatibility:** [Outcomes suitable for pooling]
- **Statistical Heterogeneity:** [Potential for heterogeneity]
- **Clinical Homogeneity:** [Clinical similarity for pooling]

## GRADE Assessment
- **Study Design:** [Initial quality level]
- **Risk of Bias:** [Quality decrease factors]
- **Inconsistency:** [Between-study consistency]
- **Indirectness:** [Directness of evidence]
- **Imprecision:** [Precision of estimates]
- **Publication Bias:** [Likelihood of publication bias]

## Recommendation
- **Include/Exclude:** [Final recommendation with rationale]
- **Evidence Contribution:** [How this study contributes to review]
- **Quality Rating:** [Overall quality for systematic review]

**Guidelines:**
- Follow PRISMA and Cochrane standards
- Assess methodological quality rigorously
- Extract all relevant data systematically
- **ALL RESPONSES IN ENGLISH**

**Analyzed Paper:**
{processed_text}
"""
