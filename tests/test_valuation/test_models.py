# tests/test_valuation/test_models.py
import unittest
from valuation_engine.models.dcf_model import DCFModel

class TestDCFModel(unittest.TestCase):
    def test_dcf_calculation(self):
        model = DCFModel()
        cash_flows = (100, 110, 120)
        terminal = 1500
        result = model.calculate(cash_flows, terminal)
        self.assertAlmostEqual(result, 1234.56, delta=100)