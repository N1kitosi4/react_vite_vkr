import uuid
import shutil
import jwt
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.config import settings
from app.core.security import (verify_password, get_password_hash,
                               create_access_token, decode_access_token)
from app.core.email_utils import send_registration_email
from app.schemas.user import UserCreate, UserResponse, Token
from app.models.user import User
from app.db.database import get_db
from datetime import timedelta

router = APIRouter()

UPLOAD_DIR = Path("app/uploads/avatars")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# @router.post("/register", status_code=status.HTTP_201_CREATED,
#              response_model=UserResponse, tags=["Registration"])
# def register_user(user: UserCreate, db: Session = Depends(get_db)):
#     existing_user_email = db.query(User).filter(User.email == user.email).first()
#     if existing_user_email:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail="Email already registered")
#
#     existing_user = db.query(User).filter(User.username == user.username).first()
#     if existing_user:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail="Username already registered")
#
#     hashed_password = get_password_hash(user.password)
#
#     new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
#
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#
#     return new_user


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse, tags=["Registration"])
async def register_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    existing_user_email = db.query(User).filter(User.email == user.email).first()
    if existing_user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Данная почта уже зарегистрирована")

    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь с таким именем уже зарегистрирован")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password, is_verified=False)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 🔹 Отправляем письмо в фоновом режиме
    background_tasks.add_task(send_registration_email, new_user.email, new_user.username, new_user.id)

    return new_user


@router.get("/verify-email", tags=["Registration"])
def verify_email(token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Невалидный или истекший токен")

    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    if user.is_verified:
        return {"message": "Email уже подтвержден"}

    user.is_verified = True
    db.commit()

    return RedirectResponse(url="http://localhost:85/login?message=email_verified")


@router.post("/login", tags=["Authentication"], response_model=Token)
def login_user(user_info: OAuth2PasswordRequestForm = Depends(),
               db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_info.username).first()
    if not user or not verify_password(user_info.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Почта не подтверждена. Проверьте входящие и спам.")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username},
                                       expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse, tags=["Users"])
def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/me/avatar", tags=["Users"])
def update_user_avatar(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = UPLOAD_DIR / file_name

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if current_user.avatar:
        old_avatar_path = Path(current_user.avatar.replace("/static/", "app/static/"))
        if old_avatar_path.exists():
            old_avatar_path.unlink()

    current_user.avatar = f"/static/avatars/{file_name}"
    db.commit()
    db.refresh(current_user)

    return {"avatar_url": current_user.avatar}


@router.post("/logout", tags=["Authentication"])
def logout_user():
    return {"message": "Успешный выход из аккаунта"}
