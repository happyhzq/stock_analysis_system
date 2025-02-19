# valuation_engine/models/dcf_model.py
from typing import Optional
import pandas as pd
from functools import lru_cache

class DCFModel:
    def __init__(self, risk_free_rate: float = 0.025, perpetuity_growth: float = 0.02):
        self.risk_free_rate = risk_free_rate
        self.perpetuity_growth = perpetuity_growth
    
    @lru_cache(maxsize=100)
    def calculate(self, cash_flows: tuple, terminal_value: float) -> float:
        """计算DCF估值"""
        cf_series = pd.Series(cash_flows)
        discount_factors = [(1 + self.risk_free_rate) ** (i+1) for i in range(len(cf_series))]
        present_values = cf_series / discount_factors
        terminal_pv = terminal_value / (1 + self.risk_free_rate) ** len(cf_series)
        return present_values.sum() + terminal_pv