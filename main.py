# main.py
"""
股票分析系统主入口
Usage:
    python main.py [--port PORT] [--env ENV]
"""

import argparse
from flask import Flask
from modules.web_interface.app import create_app
from modules.data_processor.data_loader import DataLoader
from app_config.config import Config


def initialize_system(env: str = 'production') -> Flask:
    """系统初始化流程"""
    # 加载配置
    config = Config()
    print(f"日志路径验证: {config.log_path.exists()}")

    # 初始化数据库
    try:
        loader = DataLoader()
        print(f"✅ 成功连接 {config.DB_URI} 数据库")
    except Exception as e:
        print(f"❌ 数据库连接失败: {str(e)}")
        raise

    # 创建Flask应用
    app = create_app(env)

    # 开发模式下初始化测试数据
    if env == 'development':
        _seed_test_data(loader)

    return app


def _seed_test_data(loader: DataLoader):
    """注入测试数据（仅开发模式）"""
    from modules.data_processor.models import FinancialReport
    from datetime import datetime

    test_data = [
        FinancialReport(
            symbol='AAPL',
            report_type='quarterly',
            period=datetime(2023, 3, 31),
            revenue=94836e6,
            net_income=2413e6,
            eps=1.52
        )
    ]

    with loader.get_session() as session:
        session.bulk_save_objects(test_data)
        session.commit()
    print("🧪 已注入开发测试数据")
    

def parse_args() -> dict:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='股票分析系统')
    parser.add_argument('--port', type=int, default=5006,\
                       help='服务端口号 (默认: 5006)')
    parser.add_argument('--env', choices=['production', 'development'], \
                       default='development', help='运行环境 (默认: production)')
    return vars(parser.parse_args())

if __name__ == '__main__':
    args = parse_args()

    try:
        app = initialize_system(args['env'])
        app.run(
            host='0.0.0.0',
            port=args['port'],
            debug=(args['env'] == 'development'),
            use_reloader=False
        )
    except Exception as e:
        print(f"⛔ 系统启动失败: {str(e)}")
        exit(1)
        