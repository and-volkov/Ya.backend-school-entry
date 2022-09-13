import pydantic


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class ApiSettings(BaseSettings):
    title: str = 'Yandex Backend school september 2022. Disk app'
    host = 'HOST'
    port = 8000
    log_level: str = 'INFO'

    class Config:
        env_prefix = 'API_'


class DBSettings(BaseSettings):
    uri = 'URI'

    class Config:
        env_prefix = 'DB_'


api_settings = ApiSettings()
db_settings = DBSettings()
