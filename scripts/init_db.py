# scripts/init_db.py
from data_processor.models import Base
from data_processor.data_loader import DataLoader
from app_config.config import Config
import argparse

def create_tables():
    """创建所有数据库表"""
    loader = DataLoader()
    print(f"正在连接到数据库: {Config().DB_URI}")
    Base.metadata.create_all(loader.engine)
    print("✅ 数据库表创建成功")

def drop_tables():
    """删除所有数据库表（慎用）"""
    loader = DataLoader()
    Base.metadata.drop_all(loader.engine)
    print("⚠️ 数据库表已删除")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='数据库管理工具')
    parser.add_argument('--action', choices=['create', 'drop'], required=True)
    
    args = parser.parse_args()
    
    if args.action == 'create':
        create_tables()
    elif args.action == 'drop':
        confirm = input("确认删除所有表？(y/n): ")
        if confirm.lower() == 'y':
            drop_tables()