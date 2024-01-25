from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Request, Depends, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import EmailStr

from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
import dao

from pathlib import Path

from library.email_sender import send_email_verification
from library.security_lib import PasswordEncrypt, AuthHandler, SecurityHandler
from settings import settings

web_router = APIRouter(
    prefix='',
    tags=['WEB'],
    include_in_schema=False,
)

templates = Jinja2Templates(directory=Path(__file__).parent.parent / 'templates')


class UserCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.email: Optional[str] = None
        self.name: Optional[str] = None
        self.password: Optional[str] = None
        self.password_confirm: Optional[str] = None
        self.hashed_password: str = ''

    async def load_data(self):
        form = await self.request.form()
        self.email = form.get('email')
        self.name = form.get('name') or ''
        self.password = form.get('password')
        self.password_confirm = form.get('password_confirm')

    async def is_valid(self, session: AsyncSession):
        if not self.email or '@' not in self.email:
            self.errors.append('Please? enter valid email')

        maybe_user = await dao.get_user_by_email(self.email, session)
        if maybe_user:
            self.errors.append('User with this email  already exists')

        if not self.name or len(str(self.name)) < 3:
            self.errors.append('Please? enter valid name')
        if not self.password or len(str(self.password)) < 8:
            self.errors.append('Please? enter password at least 8 symbols')
        if self.password != self.password_confirm:
            self.errors.append('Confirm password did not match!')
        if not self.errors:
            return True
        return False


@web_router.get('/')
async def index(request: Request, user=Depends(SecurityHandler.get_current_user_web)):
    context = {
        'request': request,
        'user': user,
    }

    response = templates.TemplateResponse('index.html', context=context)
    return await SecurityHandler.set_cookies_web(user, response)


@web_router.get('/signup', description='get form for registration')
@web_router.post('/signup', description='fill out the registration form')
async def web_register(
    request: Request,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
):
    if request.method == 'GET':
        return templates.TemplateResponse('registration.html', context={'request': request})

    new_user_form = UserCreateForm(request)
    await new_user_form.load_data()
    if await new_user_form.is_valid(session):
        hashed_password = await PasswordEncrypt.get_password_hash(new_user_form.password)

        saved_user = await dao.create_user(
            name=new_user_form.name,
            email=new_user_form.email,
            hashed_password=hashed_password,
            session=session,
        )
        background_tasks.add_task(
            send_email_verification,
            user_email=saved_user.email,
            user_uuid=saved_user.user_uuid,
            user_name=saved_user.name,
            host=request.base_url,
        )

        context = {
            'request': request,
            'user': saved_user,
        }
        response = templates.TemplateResponse('index.html', context=context)
        return await SecurityHandler.set_cookies_web(saved_user, response)
    else:
        return templates.TemplateResponse('registration.html', context=new_user_form.__dict__)


@web_router.get('/login', description='get form for login')
@web_router.post('/login', description='fill out the login form')
async def user_login_web(
    request: Request,
    login: EmailStr = Form(None),
    password: str = Form(None),
    session: AsyncSession = Depends(get_async_session),
):
    if request.method == 'GET':
        return templates.TemplateResponse('login.html', context={'request': request})

    user, is_password_correct = await SecurityHandler.authenticate_user_web(login, password or '', session)
    if all([user, is_password_correct]):
        context = {
            'request': request,
            'user': user,
        }
        response = templates.TemplateResponse('index.html', context=context)
        return await SecurityHandler.set_cookies_web(user, response)
    return templates.TemplateResponse('login.html', context={'request': request})


@web_router.get('/logout', description='log out')
async def user_logout_web(request: Request):
    response = templates.TemplateResponse('login.html', context={'request': request})
    response.delete_cookie(key='token')
    return response
