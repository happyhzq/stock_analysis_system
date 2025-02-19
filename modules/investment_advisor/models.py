# investment_advisor/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class InvestmentRecommendation:
    symbol: str
    current_price: float
    fair_value: float
    time_horizon: str  # short/medium/long
    recommendation: str  # STRONG_BUY/BUY/HOLD/SELL/STRONG_SELL
    confidence: float
    risk_level: str
    rationale: str
    timestamp: datetime = datetime.now()

@dataclass
class RiskAssessment:
    symbol: str
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    beta: float
    risk_category: str