from fastapi import APIRouter, HTTPException, Depends
from .schemas import UserBase, UserCreate
from sqlalchemy.orm import Session
from .db import SessionLocal
from . import models

router = APIRouter(prefix="/uapi", tags=["UAPI"]) 
def getDB():
    db = SessionLocal()
    try:
        yield db    
    finally:
        db.close()

@router.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(getDB)):
    try:
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        new_user = models.User(email=user.email, username=user.username, full_name=user.full_name, password_hash=user.password)#hash pending
        db.add(new_user)   
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/users/{user_id}", response_model=UserBase)
async def read_user(user_id: int, db: Session = Depends(getDB)):

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

    
@router.get("/users/", response_model=list[UserBase])
async def read_users( db: Session = Depends(getDB)):
    try:
        users = db.query(models.User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(getDB)):
    try:
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(db_user)
        db.commit()
        return {"detail": "User deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
