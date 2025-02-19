# 在Python交互环境中执行
import os
from pathlib import Path

# 验证关键路径存在
required_paths = [
    Path("/Users/LG/tutorial/stock/stock_analysis_system/app_config/__init__.py"),
    Path("/Users/LG/tutorial/stock/stock_analysis_system/modules/data_processor/data_loader.py")
]

for path in required_paths:
    print(f"{path.exists()}: {path}")

# 临时测试脚本 test_import.py
import sys
print(sys.path)
try:
    from app_config.config import Config
    print("✅ 导入成功")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
