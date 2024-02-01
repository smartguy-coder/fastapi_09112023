from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import sentry_sdk

from api import api_router_user, general_routers, api_router_auth
from web import web_router

sentry_sdk.init(
    dsn="https://a7c00c533ae3a9a03f18d40bb8edec40@o4505229726318592.ingest.sentry.io/4506655477465088",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/static/product_images', StaticFiles(directory='static/product_images'), name='product_images')

app.include_router(api_router_user.router)
app.include_router(general_routers.router_public)
app.include_router(general_routers.router_private)
app.include_router(api_router_auth.public_router)

app.include_router(web_router.web_router)



# @app.get('/')
# def index() -> HTMLResponse:
#     return HTMLResponse('<h1>Hello</h1>')

# @app.get('/')
# async def index() -> dict:
#     return {'message': 'Hello'}
#
#
# my_list = [1, 2, 3, 4, 5]
#
#
# class BaseInfo(BaseModel):
#     message: str = Field(default='api', min_length=5)
#     user: int
#     my_list: list[int] = Field(examples=[[36, 89, 15]])
#     password: str
#
#
# class MoreInfo(BaseInfo):
#     age: int = Field(default=55)
#
#
# @app.get('/api/{user_id}')
# async def api_route(user_id: int,
#                     limit: int = Query(gt=0, default=2),
#                     password: str = Query(min_length=10),
#                     ) -> MoreInfo:
#     return {"message": "api6666666666", 'user': user_id, 'my_list': my_list[:limit],
#             'password': password, 'dum': 99999}
#
#     # return MoreInfo(message='mnjgfjhd'[:2], user=user_id, my_list=my_list[:limit], password=password)
#
#
# @app.post('/api')
# async def get_info(
#         info: BaseInfo,
#         limit: int = Query(gt=0, default=2),
#         password: str = Query(min_length=10),
# ) -> BaseInfo:
#     print(type(info))
#     print(info.model_dump())
#     return info






if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True, host='0.0.0.0', port=8000)
