# modules/data_processor/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class FinancialReport(Base):
    """财务报告数据模型"""
    __tablename__ = 'financial_reports'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), index=True, nullable=False)
    report_type = Column(String(10), nullable=False)  # annual/quarterly
    period = Column(DateTime, nullable=False)
    revenue = Column(Float)
    net_income = Column(Float)
    eps = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    
    __table_args__ = (
        {'comment': '存储财务报告数据'}
    )

class StockPrice(Base):
    """股票价格数据模型"""
    __tablename__ = 'stock_prices'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), ForeignKey('financial_reports.symbol'), index=True)
    date = Column(DateTime, nullable=False)
    open_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)
    
    __table_args__ = (
        {'comment': '存储历史股价数据'}
    )

class ValuationResult(Base):
    """估值结果数据模型"""
    __tablename__ = 'valuation_results'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), ForeignKey('financial_reports.symbol'), index=True)
    model_type = Column(String(20), nullable=False)
    value = Column(Float, nullable=False)
    calculated_at = Column(DateTime, default=datetime.now)
    
    __table_args__ = (
        {'comment': '存储估值计算结果'}
    )