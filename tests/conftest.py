# tests/conftest.py 新增测试配置
import pytest
from modules.data_processor.data_loader import DataLoader
from modules.data_processor.models import Base

@pytest.fixture(scope="module")
def test_db():
    loader = DataLoader()
    # 创建测试表
    Base.metadata.create_all(loader.engine)
    yield
    # 清理测试表
    Base.metadata.drop_all(loader.engine)
'''
# requirements.txt 完整依赖
flask==3.0.2
flask-socketio==5.3.6
sqlalchemy==2.0.28
pandas==2.1.4
openpyxl==3.1.2
tenacity==8.2.3
pymysql==1.1.0
python-dotenv==1.0.0
pytest==8.0.0
pytest-cov==4.1.0
'''