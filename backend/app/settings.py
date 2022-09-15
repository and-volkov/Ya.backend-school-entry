import os

import pydantic
from dotenv import load_dotenv

load_dotenv()


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class ApiSettings(BaseSettings):
    title: str = 'Yandex Backend school september 2022. Entry task'
    description: str = 'Тестовое задание'
    host = '0.0.0.0'
    port = 8000

    class Config:
        env_prefix = 'API_'


class ErrorResponse(pydantic.BaseModel):
    """Models for docs."""

    code: int
    message: str


class ValidationErrorResponse(ErrorResponse):
    code: int = 400
    message: str = 'Validation Failed'


class NotFoundResponse(ErrorResponse):
    code: int = 404
    message: str = 'Item Not Found'


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
            'filename': '/backend/backend/logs/diskapp.log',
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
