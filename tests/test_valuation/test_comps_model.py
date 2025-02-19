# tests/test_valuation/test_comps_model.py
import unittest
from valuation_engine.models.comps_model import ComparablesModel

class TestComparablesModel(unittest.TestCase):
    def setUp(self):
        self.model = ComparablesModel()
        
    def test_valuation_calculation(self):
        # 需配合模拟数据
        valuation = self.model.calculate('AAPL')
        self.assertGreater(valuation, 0)