# data_processor/data_loader.py (核心数据加载)
import pandas as pd
from typing import Union, Dict
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_exponential

from models import FinancialReport, Base
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

import sys
import os
from pathlib import Path
# 动态计算项目根目录
current_dir = Path(__file__).parent.absolute()
root_dir = current_dir.parent.parent  # 根据实际层级调整
from .app_config.config import Config

class DataLoader:
    def __init__(self):
        # 添加连接池和MySQL特定参数
        self.engine = create_engine(
            Config().DB_URI,
            pool_size=5,
            pool_recycle=3600,
            connect_args={
                'connect_timeout': 10,
                'ssl': {'ssl_disabled': True}  # 根据实际需要调整
            }
        )
        self._verify_connection()

        self.session_factory = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False
        )

    def get_session(self):
        """生成新的数据库会话"""
        return self.session_factory()
    
    def __enter__(self):
        self.session = self.session_factory()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def _verify_connection(self):
        """验证数据库连接"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
        except Exception as e:
            raise RuntimeError(f"数据库连接失败: {str(e)}")
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential())

    def _verify_tables_exist(self):
        """启动时验证表是否存在"""
        required_tables = {
            'financial_reports', 
            'stock_prices',
            'valuation_results'
        }
        
        with self.engine.connect() as conn:
            existing = set(inspect(conn).get_table_names())
            missing = required_tables - existing
            
            if missing:
                raise RuntimeError(
                    f"缺失关键数据表: {missing}\n"
                    "请执行: python scripts/init_db.py --action create"
                )

    def load_from_api(self, symbol: str, report_type: str) -> pd.DataFrame:
        """从模拟API加载财务数据"""
        # 实际应替换为真实API调用
        data = {
            'symbol': symbol,
            'reports': [{
                'period': '2023-03-31',
                'revenue': 1.5e9,
                'net_income': 3e8,
                'eps': 2.5
            }]
        }
        return self._process_data(data, report_type)
        
    def load_from_local(self, file_path: Path) -> pd.DataFrame:
        """加载本地CSV/Excel文件"""
        if file_path.suffix == '.csv':
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        return self._validate_data(df)
        
    def _process_data(self, raw_data: Dict, report_type: str) -> pd.DataFrame:
        """统一数据处理管道"""
        df = pd.DataFrame(raw_data['reports'])
        df['symbol'] = raw_data['symbol']
        df['report_type'] = report_type
        df['period'] = pd.to_datetime(df['period'])
        return self._validate_data(df)
        
    def _validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据验证和清洗"""
        # 实现实际验证逻辑
        if df.isnull().sum().sum() > 0:
            df = df.dropna()
        return df
        
    def save_to_db(self, df: pd.DataFrame) -> int:
        """保存清洗后的数据到数据库"""
        records = df.to_dict('records')
        with self.Session() as session:
            for record in records:
                report = FinancialReport(**record)
                session.add(report)
            session.commit()
        return len(records)