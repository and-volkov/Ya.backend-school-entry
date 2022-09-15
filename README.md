# Ya.backend-school-entry

##  Tестовоe заданиe в Школу Бэкенд Разработки Яндекс

[Задание](task/Task.md)

[Api ROOT](https://likewise-1825.usr.yandex-academy.ru)

[Api Docs (Redoc)](https://likewise-1825.usr.yandex-academy.ru/redoc)

## Технологии
- Python 3.10
- Fastapi 0.82.0
- SQLAlchemy 1.4.41
- Pydantic 1.10.2
- Alembic 1.8.1
- Uvicorn 0.17.6


## Установка

Клонируйте репозиторий.
```sh
git clone git@github.com:and-volkov/Ya.backend-school-entry.git
```
## Запуск производится с помощью Docker
В папке деплой необходимо создать файл .env. [Образец](deploy/example.env)

Или воспользуйтесь дефолтными значениями.
```sh
cd Ya.backend-school-entry/deploy
touch .env
echo POSTGRES_VERSION=13.3-alpine >> .env
echo POSTGRES_VOLUME="/home/ubuntu/diskapp/data" >> .env
echo POSTGRES_USER="root" >> .env
echo POSTGRES_PASSWORD="example" >> .env
echo POSTGRES_DB="disk" >> .env
echo APP_LOG="/home/ubuntu/diskapp/logs" >> .env
```
Контейнер с приложением загружается из DockerHub. После создания .env файла необходимо выполнить команду (Используйте sudo при необходимости):
```sh
docker-compose up -d
```
После запуска контейнера выполните миграции.
```sh
docker-compose exec app alembic upgrade head
```
Проверить, что все работает верно, можно выполнив тесты.
```sh
docker-compose exec app pytest -v
```
Сервер будет доступен по адресу http://0.0.0.0:80/

[Документация](http://0.0.0.0:80/redoc)
