# tests/test_investment_advisor/test_advisor.py
import unittest
from investment_advisor.advisor import InvestmentAdvisor

class TestInvestmentAdvisor(unittest.TestCase):
    def test_recommendation_generation(self):
        advisor = InvestmentAdvisor()
        recs = advisor.generate_recommendations('AAPL', 150, 160)
        self.assertEqual(len(recs), 3)
        self.assertIn('short', [r.time_horizon for r in recs])