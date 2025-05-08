from pydantic import BaseModel
from typing import List


class UserBase(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    gender: str
    country: str
    is_active: bool


class UserCreate(UserBase):
    password: str  # 用來創建新用戶時提供密碼

class User(UserBase):
    id: int  # 用來顯示用戶的 id
    class Config:
        orm_mode = True  # 讓 FastAPI 知道這是 ORM 類型，並自動轉換數據
