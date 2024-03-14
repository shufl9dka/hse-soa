import datetime
import string

import jwt

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from typing import Optional
from pydantic import BaseModel
from passlib.context import CryptContext

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import UserData
from utils.config import AppConfig
from utils.depends import on_db_session, on_current_user

router = APIRouter(prefix="/user")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthUserModel(BaseModel):
    username: str
    password: str


class UpdateUserModel(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[datetime.datetime] = None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now() + datetime.timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, AppConfig.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


@router.post("/register")
async def post_register(
    data: AuthUserModel,
    db_session: AsyncSession = Depends(on_db_session),
):
    valid_chars = set(string.ascii_letters + string.digits + "_-.@$")
    if any(s not in valid_chars for s in data.username) or len(data.username) < 3 or len(data.password) < 3:
        return JSONResponse({
            "status": "error",
            "message": "Invalid data given",
        }, status_code=400)

    password_hash = get_password_hash(data.password)

    async with db_session.begin():
        db_session.add(UserData(
            username=data.username,
            password_hash=password_hash
        ))
        await db_session.commit()

    return JSONResponse({
        "status": "ok",
        "message": "User registered successfully",
    }, status_code=201)


@router.post("/auth")
async def post_auth(
    data: AuthUserModel,
    db_session: AsyncSession = Depends(on_db_session),
):
    async with db_session.begin():
        user = await db_session.execute(
            select(UserData).where(UserData.username == data.username)
        )
        user = user.scalar_one_or_none()
        if user is None:
            return JSONResponse({
                "status": "error",
                "message": "Invalid credentials",
            }, status_code=401)

    if not verify_password(data.password, user.password_hash):
        return JSONResponse({
            "status": "error",
            "message": "Invalid credentials",
        }, status_code=401)

    jwt_token = create_access_token(data={"sub": user.id})
    return JSONResponse({
        "status": "ok",
        "message": "Successful auth",
        "token": jwt_token,
    }, status_code=201)


@router.post("/update")
async def post_auth(
    data: UpdateUserModel,
    db_session: AsyncSession = Depends(on_db_session),
    user_id: int = Depends(on_current_user),
):
    async with db_session.begin():
        user = await db_session.execute(
            select(UserData).where(UserData.id == user_id)
        )
        user = user.scalar_one_or_none()
        if user is None:
            return JSONResponse({
                "status": "error",
                "message": "Invalid user",
            }, status_code=403)

    if data.first_name:
        user.first_name = data.first_name
    if data.last_name:
        user.last_name = data.last_name
    if data.email:
        user.email = data.email
    if data.phone:
        user.phone = data.phone
    if data.birthdate:
        user.birthdate = data.birthdate
    return JSONResponse({
        "status": "ok",
        "message": "Data updated successfully",
    }, status_code=200)
