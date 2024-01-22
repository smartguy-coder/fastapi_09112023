from typing import Optional

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates

from pathlib import Path


web_router = APIRouter(
    prefix='',
    tags=['WEB'],
    include_in_schema=False,
)

templates = Jinja2Templates(directory=Path(__file__).parent.parent / 'templates')


@web_router.get('/')
async def index(request: Request):
    context = {
        'request': request,
        'my_list': [89898988, 889999, 5656, 565],
        # 'user': {'name': 'Ivan', 'age': 45}
    }

    return templates.TemplateResponse('index.html', context=context)


async def get_form_data(request: Request):
    form = await request.form()


    return form


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

    async def is_valid(self):
        if not self.email or '@' not in self.email:
            self.errors.append('Please? enter valid email')
        if not self.name or len(str(self.name)) < 3:
            self.errors.append('Please? enter valid name')
        if not self.password or len(str(self.password)) < 8:
            self.errors.append('Please? enter passworl at least 8 symbols')
        if self.password != self.password_confirm:
            self.errors.append('Confirm password did not match!')
        if not self.errors:
            return True
        return False


@web_router.get('/signup', description='get form for registration')
@web_router.post('/signup', description='fill out the registration form')
async def web_register(request: Request):
    if request.method == 'GET':
        return templates.TemplateResponse('registration.html', context={'request': request})

    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        # create user
        pass
    else:
        return templates.TemplateResponse('registration.html', context=form.__dict__)
