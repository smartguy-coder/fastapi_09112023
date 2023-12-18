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

