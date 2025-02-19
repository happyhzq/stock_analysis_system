# data_processor/api_clients/yahoo_finance.py
import requests
from tenacity import retry, stop_after_attempt, wait_exponential


class YahooFinanceClient:
    BASE_URL = "https://yfapi.net/v6/finance/quote"
    
    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.session.headers.update({"X-API-KEY": api_key})

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
    def get_quote(self, symbol: str) -> dict:
        params = {"symbols": symbol}
        response = self.session.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    