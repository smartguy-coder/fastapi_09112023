poetry config --local virtualenvs.in-project true
touch README.md
poetry init -n
poetry install

 poetry add sqlalchemy
 poetry add alembic 
