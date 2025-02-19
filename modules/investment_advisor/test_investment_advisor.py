## modules/investment_advisor/test_investment_advisor.py
import unittest
from investment_advisor import InvestmentAdvisor, RiskAnalyzer
from unittest.mock import Mock

class TestInvestmentAdvisor(unittest.TestCase):
    def setUp(self):
        self.advisor = InvestmentAdvisor()
        self.mock_loader = Mock()
        
    def test_risk_assessment(self):
        analyzer = RiskAnalyzer()
        # 添加模拟数据测试
        
    def test_recommendation_logic(self):
        recommendations = self.advisor.generate_recommendations('AAPL', 150, 160)
        self.assertEqual(len(recommendations), 3)
        
    def test_compliance_checks(self):
        checker = ComplianceChecker(['RESTRICTED'])
        rec = InvestmentRecommendation(...)
        result = checker.check_compliance(rec)
        self.assertIn('is_compliant', result)