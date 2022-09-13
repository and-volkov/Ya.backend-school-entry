import pydantic


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class ApiSettings(BaseSettings):
    title: str = 'Yandex Backend school september 2022. Entry task'
    description: str = 'Тестовое задание'
    host = 'HOST'
    port = 8000

    class Config:
        env_prefix = 'API_'


class DBSettings(BaseSettings):
    uri = 'URI'

    class Config:
        env_prefix = 'DB_'


class ErrorResponse(pydantic.BaseModel):
    code: int
    message: str


class LogConfig(pydantic.BaseModel):
    LOGGER_NAME: str = 'diskapp'
    LOG_FORMAT: str = '%(levelprefix)s | %(asctime)s | %(message)s'
    LOG_LEVEL: str = 'INFO'

    version = 1
    disable_existing_loggers = False
    formatters = {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'fileFormatter': {
            'format': '%(asctime)s - %(levelname)s -  %(name)s - %(module)s '
                      '- %(funcName)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'class': 'logging.Formatter',
        },
    }
    handlers = {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'fileHandler': {
            'level': 'ERROR',
            'formatter': 'fileFormatter',
            'filename': 'logs/diskapp.log',
            'class': 'logging.FileHandler',
            'mode': 'a',
        },
    }
    loggers = {
        LOGGER_NAME: {
            'handlers': ['default', 'fileHandler'],
            'level': LOG_LEVEL,
        },
    }


api_settings = ApiSettings()
db_settings = DBSettings()
