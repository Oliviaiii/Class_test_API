from sqlalchemy import Boolean, Column, Integer, String
from database import Base, engine


class User(Base):
    __tablename__ = "users"
    
    # 定義欄位
    id = Column(Integer, primary_key=True, index=True)  # 主鍵欄位
    email = Column(String(255), unique=True)  # 唯一的電子郵件欄位，限制長度為255
    username = Column(String(50), unique=True)  # 唯一的使用者名稱欄位
    first_name = Column(String)  # 名字欄位
    last_name = Column(String)  # 姓氏欄位
    gender = Column(String)  # 性別欄位
    country = Column(String)  # 國家欄位
    is_active = Column(Boolean)  # 是否啟用的欄位
    hashed_password = Column(String)  # 存儲密碼的欄位

# 創建資料表
Base.metadata.create_all(bind=engine)
