from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


public_router = APIRouter(
    prefix='/api/auth',
    tags=['API', 'Auth']
)


@public_router.post('/login')
async def user_login(data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):

    return {}