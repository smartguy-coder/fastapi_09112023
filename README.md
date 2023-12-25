poetry config --local virtualenvs.in-project true
touch README.md
poetry init -n
poetry install

 poetry add sqlalchemy
 poetry add alembic 
poetry add asyncpg
poetry add psycopg2
poetry add psycopg2-binary
poetry add "fastapi[all]"  
 alembic init migrations
alembic revision --autogenerate -m 'initial'
alembic upgrade head 
alembic upgrade 2d8bb3d81f97 
 alembic downgrade -1



uvicorn main:app  --port 5678 --reload
