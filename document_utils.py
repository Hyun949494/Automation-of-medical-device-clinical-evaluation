import pandas as pd
import io
from datetime import datetime

def create_excel_download(df, filename_prefix="results"):
    """DataFrame을 엑셀 파일로 변환하여 다운로드 가능한 형태로 반환"""
    excel_bytes = io.BytesIO()
    df.to_excel(excel_bytes, index=False, engine='openpyxl')
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{filename_prefix}_{timestamp}.xlsx"
    
    return excel_bytes.getvalue(), filename

def create_markdown_download(content, filename_prefix="analysis"):
    """텍스트 내용을 마크다운 파일로 변환하여 다운로드 가능한 형태로 반환"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{filename_prefix}_{timestamp}.md"
    
    return content.encode('utf-8'), filename

def format_search_results(papers_list):
    """검색 결과를 보기 좋은 형태로 포맷팅"""
    formatted_results = []
    
    for i, paper in enumerate(papers_list, 1):
        formatted_paper = f"""
**{i}. {paper.get('Title', 'No Title')}**
- **저자**: {paper.get('Authors', 'No Authors')}
- **저널**: {paper.get('Journal', 'No Journal')} ({paper.get('Year', 'No Year')})
- **PMID**: [{paper.get('PMID', 'No PMID')}]({paper.get('URL', '#')})
- **초록**: {paper.get('Abstract', 'No Abstract')[:200]}...

---
"""
        formatted_results.append(formatted_paper)
    
    return '\n'.join(formatted_results)
