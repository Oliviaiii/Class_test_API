from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import models
import schemas
from database import SessionLocal

app = FastAPI()

@app.get("/")
async def docs_redirect():
    response = RedirectResponse(url='/docs')
    return response

# 定義 get_db 函數，使用 yield 來返回資料庫會話
def get_db():
    db = SessionLocal()  # 獲取資料庫會話
    try:
        yield db  # 返回會話，FastAPI 會自動處理這個會話的生命周期
    finally:
        db.close()  # 確保在請求結束時關閉會話


# 定義 GET 請求端點，用來獲取所有用戶
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # 呼叫 crud 中的 get_users 函數
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# 定義 GET 請求端點，用來根據用戶 ID 獲取單個用戶
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    # 呼叫 crud 中的 get_user 函數
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        # 如果找不到該用戶，返回 404 錯誤
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 定義 GET 請求端點，用來根據 email 獲取單個用戶
@app.get("/users/email/{user_email}", response_model=schemas.User)
def read_user_by_email(user_email: str, db: Session = Depends(get_db)):
    # 呼叫 crud 中的 get_user_by_email 函數
    db_user = crud.get_user_by_email(db, email=user_email)
    if db_user is None:
        # 如果找不到該用戶，返回 404 錯誤
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 定義 POST 請求端點來新增用戶
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 檢查該 email 是否已經註冊過
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")  # 如果已存在則返回錯誤
    # 呼叫 crud 中的 create_user 函數新增用戶
    return crud.create_user(db=db, user=user)

# 定義 PUT 請求端點來更新用戶
@app.put("/users/", response_model=schemas.User)
def update_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 根據 email 查找用戶
    db_user = crud.get_user_by_email(db, email=user.email)
    
    if db_user:  # 如果用戶存在，則更新資料
        return crud.update_user(db=db, user=user)
    
    # 如果用戶不存在，返回 400 錯誤
    raise HTTPException(status_code=400, detail="User not Found")

# 在 /usercode/Application/main.py 中
@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # 調用 delete_user 函數刪除用戶
    db_user = crud.delete_user(db, user_id=user_id)
    
    # 如果沒有找到用戶，返回 404 錯誤
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 返回刪除的用戶資料
    return db_user

