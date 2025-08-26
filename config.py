from rnd4 import TEAM_CONFIG as RND4_CONFIG
from rnd35 import TEAM_CONFIG as RND35_CONFIG

# 🏗️ 전체 팀 설정 데이터
TEAM_CONFIGS = {
    "RND4": {
        "name": "RND4 팀 - Pulmonary Valve",
        **RND4_CONFIG
    },
    "RND35": {
        "name": "RND35 팀 - 사용자 설정",
        **RND35_CONFIG
    },
    "커스텀": {
        "name": "커스텀 설정",
        "P": "",
        "I": "",
        "C": "",
        "O": "",
        "email": "",
        "api_key": "",
        "product": "",
        "gemini_api_key": ""
    }
}

# 검색 설정
SEARCH_SETTINGS = {
    "max_results_per_call": 200,
    "default_results": 50,
    "chunk_size": 50,
    "api_delay": 1.0
}

# 날짜 필터 설정 - 커스텀 방식
DATE_FILTER_OPTIONS = {
    "custom_range_only": True,  # 사용자가 직접 입력하는 방식만 사용
    "format_help": "YYYY/MM/DD-YYYY/MM/DD 형식으로 입력하세요",
    "placeholder": "예: 2020/01/01-2024/12/31"
}
