import uuid
from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas_user import LoginResponse
import dao
from models import User
from settings import settings


class PasswordEncrypt:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @classmethod
    async def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)


class AuthHandler:
    secret = settings.JWT_SECRET
    algorithm = settings.JWT_ALGORITHM

    @classmethod
    async def get_login_token_pairs(cls, data: OAuth2PasswordRequestForm, session: AsyncSession) -> LoginResponse:
        user = await dao.get_user_by_email(email=data.username, session=session)

        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with this email not found')
        is_valid_password = await PasswordEncrypt.verify_password(data.password, user.hashed_password)
        if not is_valid_password:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Password is incorrect')
        if not user.verified_at:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Your account is not verified')
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are banned. Please contact support')

        token_pairs: LoginResponse = await cls.generate_token_pair(user, session)
        return token_pairs

    @classmethod
    async def generate_token(cls, payload: dict, expiry: timedelta) -> str:
        now = datetime.utcnow()
        time_payload = {'exp': now + expiry, 'iat': now}
        payload.update(time_payload)
        token_ = jwt.encode(payload, cls.secret, cls.algorithm)
        return token_

    @classmethod
    async def generate_token_pair(cls, user: User, session: AsyncSession) -> LoginResponse:
        access_token_payload = {
            'sub': user.id,
            'email': user.email,
        }
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_TIME_MINUTES)
        access_token = await cls.generate_token(access_token_payload, access_token_expires)

        refresh_token_payload = {
            'sub': user.id,
            'email': user.email,
            'db': str(uuid.uuid4()),
        }
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_TIME_MINUTES)
        refresh_token = await cls.generate_token(refresh_token_payload, refresh_token_expires)

