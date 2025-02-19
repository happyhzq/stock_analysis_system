# investment_advisor/compliance_checker.py
from typing import Dict, List

class ComplianceChecker:
    def __init__(self, restricted_symbols: List[str] = None):
        self.restricted = restricted_symbols or []
        
    def check_compliance(self, 
                       recommendation: InvestmentRecommendation) -> Dict:
        """执行合规性检查"""
        checks = {
            'restricted_symbol': recommendation.symbol in self.restricted,
            'risk_level': self._check_risk_level(recommendation.risk_level),
            'position_size': self._check_position_size(recommendation)
        }
        return {
            'is_compliant': not any(checks.values()),
            'violations': [k for k, v in checks.items() if v]
        }
        
    def _check_risk_level(self, risk_level: str) -> bool:
        return risk_level in ['high', 'very_high']
        
    def _check_position_size(self, rec: InvestmentRecommendation) -> bool:
        max_allocation = self.config.get('max_allocation', 0.1)
        return rec.confidence > max_allocation