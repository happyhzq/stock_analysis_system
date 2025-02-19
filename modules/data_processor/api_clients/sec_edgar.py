# data_processor/api_clients/sec_edgar.py
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import Dict, Any


class SECEdgarClient:
    BASE_URL = "https://data.sec.gov/api/xbrl"
    
    def __init__(self, user_agent: str):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
    def get_company_facts(self, cik: str) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/companyfacts/CIK{cik}.json"
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    