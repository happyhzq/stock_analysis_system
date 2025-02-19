# modules/valuation_engine/models/comps_model.py
from typing import List, Dict
import pandas as pd
from sqlalchemy import text
from data_processor.data_loader import DataLoader
from valuation_engine.core import ValuationModel

class ComparablesModel(ValuationModel):
    """基于可比公司分析的估值模型"""
    
    def __init__(self, multiples: List[str] = ['pe', 'ev_ebitda']):
        self.multiples = multiples
        self.loader = DataLoader()
        
    def calculate(self, symbol: str) -> float:
        """
        计算可比公司估值
        步骤：
        1. 获取目标公司财务数据
        2. 筛选可比公司
        3. 计算估值倍数
        4. 应用倍数计算估值
        """
        target = self._get_company_data(symbol)
        peers = self._get_peer_companies(symbol)
        
        if not peers:
            raise ValueError("未找到可比公司")
            
        multiples = self._calculate_multiples(peers)
        return self._apply_multiples(target, multiples)
        
    def _get_company_data(self, symbol: str) -> Dict:
        """获取目标公司最新财务数据"""
        with self.loader.Session() as session:
            query = text("""
                SELECT revenue, net_income, eps 
                FROM financial_reports
                WHERE symbol = :symbol
                ORDER BY period DESC
                LIMIT 1
            """)
            result = session.execute(query, {'symbol': symbol}).fetchone()
            
        return {
            'revenue': result[0],
            'net_income': result[1],
            'eps': result[2]
        }
        
    def _get_peer_companies(self, symbol: str) -> List[Dict]:
        """获取同行业可比公司（示例实现）"""
        # 实际应连接行业分类数据库
        return [
            {'symbol': 'MSFT', 'pe': 30.5, 'ev_ebitda': 18.2},
            {'symbol': 'ORCL', 'pe': 25.1, 'ev_ebitda': 15.8}
        ]
        
    def _calculate_multiples(self, peers: List[Dict]) -> Dict:
        """计算平均估值倍数"""
        df = pd.DataFrame(peers)
        return {
            'pe': df['pe'].median(),
            'ev_ebitda': df['ev_ebitda'].mean()
        }
        
    def _apply_multiples(self, target: Dict, multiples: Dict) -> float:
        """应用倍数计算估值"""
        valuations = []
        if 'pe' in self.multiples:
            valuations.append(target['net_income'] * multiples['pe'])
        if 'ev_ebitda' in self.multiples:
            valuations.append(target['revenue'] * multiples['ev_ebitda'])
        return sum(valuations) / len(valuations) if valuations else 0.0