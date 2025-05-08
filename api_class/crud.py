from sqlalchemy.orm import Session
from sqlalchemy import update
import models, schemas
import hashlib

def get_users(db: Session, skip: int = 0, limit: int = 100):
    # 查詢用戶並返回，使用 offset 和 limit 來控制查詢範圍
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    # 根據用戶 ID 查詢單個用戶，並返回第一個匹配的結果
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    # 根據 email 查詢單個用戶，並返回第一個匹配的結果
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # 假設Hashing passwords的方式（實際專案中應該使用更安全的方式，比如 bcrypt 或 passlib）
    fake_hashed_password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()  # 哈希處理
    db_user = models.User(
        email=user.email,
        hashed_password=fake_hashed_password,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender,
        country=user.country,
        isActive=user.isActive
    )
    db.add(db_user)  # 將用戶資料加入到資料庫
    db.commit()  # 提交到資料庫
    db.refresh(db_user)  # 刷新用戶資料
    return db_user  # 返回創建的用戶資料

def update_user(db: Session, user: schemas.UserCreate):
    # 根據 email 查找用戶
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    # 如果找到用戶，則更新其資料
    if db_user:
        for field in user.__dict__:  # 遍歷用戶資料，更新用戶對應的字段
            setattr(db_user, field, getattr(user, field))
        
        db.commit()  # 提交更新
        db.refresh(db_user)  # 刷新用戶資料
        return db_user  # 返回更新後的用戶資料
    return None  # 如果用戶不存在，返回 None


def delete_user(db: Session, user_id: int):
    # 查找用戶
    record_obj = db.query(models.User).filter(models.User.id == user_id).first()
    
    # 如果找到了該用戶，刪除並提交
    if record_obj:
        db.delete(record_obj)
        db.commit()
        return record_obj
    return None  # 如果沒有找到用戶，返回 None
