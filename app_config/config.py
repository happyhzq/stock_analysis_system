# app_config/config.py 最终版
from pathlib import Path
import yaml


class Config:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent  # 向上两级到项目根目录
        self._verify_structure()
        self._load_config()

    def _verify_structure(self):
        """验证必要目录结构"""
        required = [
            self.base_dir / 'logs',
            self.base_dir / 'data',
            self.base_dir / 'app_config'
        ]
        for path in required:
            if not path.exists():
                raise RuntimeError(f"缺失关键目录: {path}")
 
    @property
    def log_path(self):
        return self.base_dir / 'logs' / 'msscore.log'   
    def _load_config(self):
        config_path = self.base_dir / 'app_config' / 'config.yaml'
        with open(config_path) as f:
            self.settings = yaml.safe_load(f)

        # MySQL配置
        db_config = self.settings['mysql']
        self.DB_URI = (
            f"mysql+pymysql://{db_config['user']}:{db_config['password']}"
            f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
            f"?charset=utf8mb4&autocommit=false"
        )

        # 其他配置
        self.API_CONFIG = self.settings.get('api', {})


config = Config()


# 测试MySQL连接的代码
from sqlalchemy import create_engine
config = Config()
engine = create_engine(config.DB_URI)
try:
    with engine.connect() as conn:
        print("✅ MySQL连接成功！")
        print(f"服务器版本: {conn.scalar('showtables')}")
except Exception as e:
    print(f"❌ 连接失败: {str(e)}")
    print("请检查：\n1. MySQL服务状态\n2. 防火墙设置\n3. 用户权限\n4. 环境变量配置")
    