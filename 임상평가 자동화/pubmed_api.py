# pubmed_api.py
import requests
import xml.etree.ElementTree as ET

def pubmed_details(id_list, email, api_key=None):
    """PubMed 상세 정보 가져오기"""
    base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    results = []
    chunk = 100
    
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
            
        r = requests.get(base, params=params)
        r.raise_for_status()
        root = ET.fromstring(r.text)
        
        for article in root.findall('.//PubmedArticle'):
            pmid = article.findtext('.//PMID', default='')
            title = article.findtext('.//ArticleTitle', default='')
            abstract = ' '.join([abst.text or '' for abst in article.findall('.//AbstractText')])
            journal = article.findtext('.//Journal/Title', default='')
            doi = ''
            for id_elem in article.findall('.//ArticleId'):
                if id_elem.attrib.get('IdType') == 'doi':
                    doi = id_elem.text
                    
            results.append({
                'PMID': pmid,
                'Title': title,
                'Abstract': abstract,
                'Journal': journal,
                'DOI': doi,
                'Select': '',
                'Reason': ''
            })
    return results

def build_query(components):
    """쿼리 생성"""
    parts = [f"({comp})" for comp in components if comp]
    return " AND ".join(parts)

def pubmed_search_all(query, email, retmax_per_call=100, api_key=None, mindate=None, maxdate=None):
    """PubMed 전체 검색"""
    base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'xml',
        'retmax': retmax_per_call,
        'email': email,
        'datetype': 'pdat'
    }
    if api_key:
        params['api_key'] = api_key
    if mindate and maxdate:
        params['mindate'], params['maxdate'] = mindate, maxdate

    all_ids = []
    retstart = 0
    total = None
    
    while True:
        params['retstart'] = retstart
        r = requests.get(base, params=params)
        r.raise_for_status()
        root = ET.fromstring(r.text)
        
        if total is None:
            total = int(root.findtext('.//Count', '0'))
            
        batch = [e.text for e in root.findall('.//Id')]
        if not batch:
            break
            
        all_ids.extend(batch)
        retstart += len(batch)
        
        if retstart >= total:
            break
            
    return all_ids