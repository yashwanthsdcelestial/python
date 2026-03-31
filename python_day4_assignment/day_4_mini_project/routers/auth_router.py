from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.schemas import UserCreate, UserResponse, UserLogin, LoginResponse
from services.user_service import UserService
from utils.session_store import create_session

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    return UserService(db).register(data)


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    result = UserService(db).login(data.username, data.password)
    token = create_session(result.user_id, result.username, result.role)
    return {
        "message": result.message,
        "user_id": result.user_id,
        "username": result.username,
        "role": result.role,
        "token": token,
    }