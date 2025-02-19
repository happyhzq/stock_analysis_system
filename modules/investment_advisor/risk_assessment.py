# investment_advisor/risk_assessment.py
import numpy as np
import pandas as pd
from typing import Dict
from data_processor.data_loader import DataLoader

class RiskAnalyzer:
    def __init__(self, lookback_period: int = 252):
        self.loader = DataLoader()
        self.lookback = lookback_period

    def calculate_volatility(self, prices: pd.Series) -> float:
        log_returns = np.log(prices / prices.shift(1))
        return log_returns.std() * np.sqrt(self.lookback)

    def get_risk_assessment(self, symbol: str) -> RiskAssessment:
        with self.loader.Session() as session:
            query = f"SELECT period, close_price FROM stock_prices WHERE symbol='{symbol}'"
            df = pd.read_sql(query, session.connection())
        
        if len(df) < self.lookback:
            raise ValueError("Insufficient historical data")
            
        prices = df.set_index('period')['close_price'].tail(self.lookback)
        
        volatility = self.calculate_volatility(prices)
        cumulative_returns = (prices.iloc[-1] / prices.iloc[0]) - 1
        sharpe = cumulative_returns / volatility if volatility != 0 else 0
        
        max_price = prices.expanding().max()
        drawdown = (prices - max_price) / max_price
        max_dd = drawdown.min()
        
        return RiskAssessment(
            symbol=symbol,
            volatility=volatility,
            sharpe_ratio=sharpe,
            max_drawdown=max_dd,
            beta=self.calculate_beta(prices),
            risk_category=self.classify_risk(volatility, max_dd)
        )