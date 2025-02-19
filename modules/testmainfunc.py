# 系统健康检查脚本
from data_processor.data_loader import DataLoader
from valuation_engine.core import ValuationEngine
from investment_advisor.advisor import InvestmentAdvisor

def system_check():
    # 数据库检查
    loader = DataLoader()
    
    # 估值检查
    valuation = ValuationEngine().run_valuation('AAPL', 'dcf')
    
    # 决策检查
    #advice = InvestmentAdvisor().generate_recommendation(145, 150)
    
    return {
        'database': loader.engine.pool.status(),
        'valuation': valuation,
        #'advice': advice
    }

print(system_check())