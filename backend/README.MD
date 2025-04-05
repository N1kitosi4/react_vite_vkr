#### Создание миграции для основной базы данных:

alembic -c alembic.ini revision --autogenerate -m "Create main_db tables"


#### Применение миграции для основной базы данных:

alembic -c alembic.ini upgrade head


#### Создание миграции для тестовой базы данных:

alembic -c test_alembic.ini revision --autogenerate -m "Create test_db tables"


#### Применение миграции для тестовой базы данных:

alembic -c test_alembic.ini upgrade head

#### Запуск контейнера Docker для FastAPI

docker run -d --name vkr_books_cont -p 8000:8000 vkr_books

#### Запуск контейнера

docker-compose up --build -d
docker-compose up -d

docker-compose down -v

StairwayToHeaven123


psql -U ${DATABASE_USERNAME} -d ${TEST_DATABASE_NAME}