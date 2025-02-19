# modules/data_processor/data_sources/api_client.py
import requests
from tenacity import retry, stop_after_attempt, wait_exponential


class StockAPIClient:
    def __init__(self, api_key):
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = api_key

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def get_fundamentals(self, symbol):
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()
    