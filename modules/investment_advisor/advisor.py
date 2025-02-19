## modules/investment_advisor/advisor.py
from typing import List
from app_config.config import Config
from .models import InvestmentRecommendation, RiskAssessment


class InvestmentAdvisor:
    def __init__(self):
        self.config = Config()
        self.risk_analyzer = RiskAnalyzer()
        
    def generate_recommendations(self, 
                               symbol: str,
                               current_price: float,
                               fair_value: float) -> List[InvestmentRecommendation]:
        """生成多时间维度投资建议"""
        risk_profile = self.risk_analyzer.get_risk_assessment(symbol)
        base_diff = (current_price - fair_value) / fair_value
        
        return [
            self._generate_for_horizon('short', base_diff, risk_profile),
            self._generate_for_horizon('medium', base_diff, risk_profile),
            self._generate_for_horizon('long', base_diff, risk_profile)
        ]
        
    def _generate_for_horizon(self, 
                            horizon: str,
                            price_diff: float,
                            risk: RiskAssessment) -> InvestmentRecommendation:
        thresholds = self.config.get_thresholds()[horizon]
        confidence = self._calculate_confidence(price_diff, risk.volatility)
        
        return InvestmentRecommendation(
            symbol=risk.symbol,
            current_price=current_price,
            fair_value=fair_value,
            time_horizon=horizon,
            recommendation=self._determine_action(price_diff, thresholds),
            confidence=confidence,
            risk_level=risk.risk_category,
            rationale=self._generate_rationale(horizon, price_diff, risk)
        )
    