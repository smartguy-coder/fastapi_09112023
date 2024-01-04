from fastapi import APIRouter, status

router = APIRouter(
    prefix='/api/user',
    tags=['Users', 'API']
)


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user_account():
    pass
