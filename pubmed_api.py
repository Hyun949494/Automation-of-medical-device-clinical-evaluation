import requests
import xml.etree.ElementTree as ET
import streamlit as st
import time
import pandas as pd
from config import SEARCH_SETTINGS

def pubmed_search_all(query, email, retmax_per_call=100, api_key=None, mindate=None, maxdate=None):
    """PubMed에서 모든 논문 ID 수집"""
    base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'xml',
        'retmax': retmax_per_call,
        'email': email
    }
    if api_key:
        params['api_key'] = api_key
    
    # 날짜 필터를 쿼리에 직접 포함
    if mindate and maxdate:
        date_filter = f"{mindate}:{maxdate}[pdat]"
        params['term'] = f"{query} AND {date_filter}"

    all_ids = []
    retstart = 0
    total = None
    
    while True:
        params['retstart'] = retstart
        try:
            r = requests.get(base, params=params, timeout=30)
            
            if r.status_code != 200:
                st.error(f"❌ HTTP 오류: {r.status_code}")
                break
            
            # XML 파싱
            try:
                root = ET.fromstring(r.text)
            except ET.ParseError as e:
                st.error(f"❌ XML 파싱 실패: {e}")
                break
            
            # 총 결과 수 확인
            if total is None:
                total = int(root.findtext('.//Count', '0'))
                st.success(f"📊 **PubMed 총 결과**: {total}개")
                
                if total == 0:
                    st.warning("⚠️ 검색 결과가 0개입니다")
                    break
                
            # PMID 추출
            batch = [e.text for e in root.findall('.//Id')]
            
            if not batch:
                break
                
            all_ids.extend(batch)
            retstart += len(batch)
            
            # 완료 조건 체크
            if retstart >= total or len(all_ids) >= retmax_per_call:
                break
                
        except requests.exceptions.RequestException as e:
            st.error(f"❌ 네트워크 오류: {e}")
            break
        except Exception as e:
            st.error(f"❌ 예상치 못한 오류: {type(e).__name__}: {e}")
            break
            
    final_count = len(all_ids)
    st.success(f"🎯 **수집된 논문**: {final_count}개")
    
    return all_ids[:retmax_per_call]

def pubmed_details(id_list, email, api_key=None):
    """PMID 리스트로부터 논문 상세 정보 수집"""
    if not id_list:
        return []
        
    base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    results = []
    chunk = SEARCH_SETTINGS["chunk_size"]
    
    for i in range(0, len(id_list), chunk):
        group = id_list[i:i+chunk]
        params = {
            'db': 'pubmed',
            'id': ','.join(group),
            'retmode': 'xml',
            'email': email
        }
        if api_key:
            params['api_key'] = api_key
            
        try:
            r = requests.get(base, params=params, timeout=60)
            r.raise_for_status()
            root = ET.fromstring(r.text)
            
            for article in root.findall('.//PubmedArticle'):
                pmid = article.findtext('.//PMID', default='')
                
                # 제목 추출
                title = article.findtext('.//ArticleTitle', default='')
                if not title:
                    title = f"제목 없음 (PMID: {pmid})"
                
                # Abstract 추출
                abstract_parts = []
                for abst in article.findall('.//AbstractText'):
                    if abst.text:
                        label = abst.get('Label', '')
                        text = abst.text
                        if label:
                            abstract_parts.append(f"{label}: {text}")
                        else:
                            abstract_parts.append(text)
                
                abstract = ' '.join(abstract_parts) if abstract_parts else '초록 없음'
                
                # 저널명 추출
                journal = article.findtext('.//Journal/Title', default='')
                if not journal:
                    journal = article.findtext('.//MedlineTA', default='저널 없음')
                
                # 발행년도 추출
                year = article.findtext('.//PubDate/Year', default='')
                if not year:
                    year = article.findtext('.//DateCompleted/Year', default='')
                if not year:
                    year = '년도 없음'
                
                # DOI 추출
                doi = ''
                for id_elem in article.findall('.//ArticleId'):
                    if id_elem.attrib.get('IdType') == 'doi':
                        doi = id_elem.text
                        break
                
                # 저자 정보 추출
                authors = []
                for author in article.findall('.//Author')[:5]:
                    lastname = author.findtext('.//LastName', '')
                    forename = author.findtext('.//ForeName', '')
                    if lastname:
                        authors.append(f"{lastname} {forename}".strip())
                
                authors_str = ', '.join(authors) if authors else '저자 없음'
                if len(article.findall('.//Author')) > 5:
                    authors_str += ' et al.'
                
                results.append({
                    'PMID': pmid,
                    'Title': title[:500] + '...' if len(title) > 500 else title,
                    'Abstract': abstract[:2000] + '...' if len(abstract) > 2000 else abstract,
                    'Authors': authors_str,
                    'Journal': journal,
                    'Year': year,
                    'DOI': doi,
                    'URL': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    'Select': '',
                    'Reason': ''
                })
                
        except Exception as e:
            st.error(f"상세 정보 수집 오류: {e}")
            continue
            
        # API 요청 제한 고려
        time.sleep(SEARCH_SETTINGS["api_delay"])
    
    return results

def build_query(components):
    """PICO 구성요소들을 AND로 연결하여 쿼리 생성"""
    parts = [f"({comp})" for comp in components if comp.strip()]
    return " AND ".join(parts)

def build_filters(filter_options):
    """필터 옵션들을 PubMed 쿼리 형식으로 변환 (PubMed 웹과 최대한 유사하게)"""
    filters = []

    # Text Availability 필터
    if filter_options.get('text_filters', {}).get('abstract'):
        filters.append('hasabstract[Filter]')
    if filter_options.get('text_filters', {}).get('free_full_text'):
        filters.append('fft[Filter]')
    if filter_options.get('text_filters', {}).get('full_text'):
        filters.append('full text[Filter]')

    # Article Type 필터
    article_type_filters = []
    if filter_options.get('article_type_filters', {}).get('books_docs'):
        article_type_filters.append('booksdocs[Filter]')
    if filter_options.get('article_type_filters', {}).get('clinical_trial'):
        article_type_filters.append('clinicaltrial[Filter]')
    if filter_options.get('article_type_filters', {}).get('meta_analysis'):
        article_type_filters.append('meta-analysis[Filter]')
    if filter_options.get('article_type_filters', {}).get('rct'):
        article_type_filters.append('randomizedcontrolledtrial[Filter]')
    if filter_options.get('article_type_filters', {}).get('review'):
        article_type_filters.append('review[Filter]')
    if filter_options.get('article_type_filters', {}).get('systematic_review'):
        article_type_filters.append('systematicreview[Filter]')

    if article_type_filters:
        filters.append(f"({' OR '.join(article_type_filters)})")

    # Article Attribute 필터
    if filter_options.get('associated_data'):
        filters.append('data[Filter]')

    # Additional 필터
    if filter_options.get('additional_filters', {}).get('human'):
        filters.append('humans[Filter]')
    if filter_options.get('additional_filters', {}).get('english'):
        filters.append('english[Filter]')

    # Species
    if filter_options.get('species', {}).get('humans'):
        filters.append('humans[Filter]')
    if filter_options.get('species', {}).get('other_animals'):
        filters.append('animals[Filter]')

    # Sex
    if filter_options.get('sex', {}).get('female'):
        filters.append('female[Filter]')
    if filter_options.get('sex', {}).get('male'):
        filters.append('male[Filter]')

    # Age
    if filter_options.get('age', {}).get('child'):
        filters.append('child[Filter]')
    if filter_options.get('age', {}).get('adult'):
        filters.append('adult[Filter]')
    if filter_options.get('age', {}).get('aged'):
        filters.append('aged[Filter]')

    # Other
    if filter_options.get('other', {}).get('exclude_preprints'):
        filters.append('NOT preprints[Filter]')
    if filter_options.get('other', {}).get('medline'):
        filters.append('medline[Filter]')        

    return filters
