from fastapi import APIRouter, status, Depends, HTTPException
from api.schemas_user import RegisterUserRequest, BaseFields
from database import get_async_session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import dao
from library.security_lib import PasswordEncrypt


router = APIRouter(
    prefix='/api/user',
    tags=['Users', 'API']
)


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user_account(
        new_user: RegisterUserRequest,
        session: AsyncSession = Depends(get_async_session),
) -> RegisterUserRequest:

    maybe_user = await dao.get_user_by_email(new_user.email, session)
    if maybe_user:
        raise HTTPException(detail=f'User {maybe_user.name} with email {maybe_user.email} already exists',
                            status_code=status.HTTP_403_FORBIDDEN)

    hashed_password = await PasswordEncrypt.get_password_hash(new_user.password)

    saved_user = await dao.create_user(
        name=new_user.name,
        email=new_user.email,
        hashed_password=hashed_password,
        session=session,
    )
    return new_user
