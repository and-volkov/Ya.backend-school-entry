# Ya.backend-school-entry

##  Test task for Yandex Backend School

[Task](task/Task.md)

[Api ROOT](https://likewise-1825.usr.yandex-academy.ru)

[Api Docs (Redoc)](https://likewise-1825.usr.yandex-academy.ru/redoc)

## Tech Stack
- Python 3.10
- Fastapi 0.82.0
- SQLAlchemy 1.4.41
- Pydantic 1.10.2
- Alembic 1.8.1
- Uvicorn 0.17.6

## Server
On server used only deploy folder. Application starting with docker-compose file.
From root derectory of ubuntu user run following commands.

```sh
cd diskapp/deploy
sudo docker-compose up -d
```
Run migrations
```sh
sudo docker-compose exec app alembic upgrade head
```
Run tests
```sh
sudo docker-compose exec app pytest -v
```

After server restart containers are starting automatically

## Setup

Clone repo
```sh
git clone git@github.com:and-volkov/Ya.backend-school-entry.git
```
## Start with docker
In deploy folder create .env file. [Example](deploy/example.env)

Or use default settings
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
Change nginx config if needed nginx/default.conf.

Container with application is pulled from docker hub. After creation of .env file, run following commands:
```sh
docker-compose up -d
```
After container starts run migrations.
```sh
docker-compose exec app alembic upgrade head
```
Run tests
```sh
docker-compose exec app pytest -v
```
Server started locally at http://0.0.0.0:80/

[Documentation](http://0.0.0.0:80/redoc)
