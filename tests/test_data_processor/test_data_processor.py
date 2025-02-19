# tests/test_data_processor.py (单元测试示例)
import unittest
from modules.data_processor.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader()
        
    def test_api_loading(self):
        df = self.loader.load_from_api('AAPL', 'quarterly')
        self.assertGreater(len(df), 0)