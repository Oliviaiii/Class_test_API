from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. 設定資料庫 URL，這裡使用 SQLite 資料庫，資料會儲存在 sql_app.db 檔案中
SQLALCHEMY_DATABASE_URL = "sqlite:///sql_app.db"

# 2. 創建資料庫引擎，並指定參數以支援 SQLite 多線程操作
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. 創建會話控制器，設定 autocommit 和 autoflush 都為 False
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 創建基底，用來定義資料庫模型
Base = declarative_base()
