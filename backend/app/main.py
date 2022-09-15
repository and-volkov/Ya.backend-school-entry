import os
import logging
from logging.config import dictConfig

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Path, status
from fastapi.exceptions import ValidationError, RequestValidationError
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.app import models
from backend.app import settings
from backend.app.database import SessionLocal
from backend.app.exceptions import not_found, validation_error_handler
from backend.app.handlers.base import NodeHandler
from backend.app.handlers.events import update_size_and_date
from backend.app.validators import validate_date

if not os.path.exists('/backend/backend/logs'):
    os.mknod('/backend/backend/logs')
    open('/backend/backend/logs/diskapp.log', 'w').close()

dictConfig(settings.LogConfig().dict())
logger = logging.getLogger('diskapp')

app = FastAPI(
    title=settings.api_settings.title,
    description=settings.api_settings.description,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'model': settings.ValidationErrorResponse
        },
    },
)

app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(IntegrityError, validation_error_handler)
app.add_exception_handler(ValidationError, validation_error_handler)


def get_db():
    db = SessionLocal()
    try:
        event.listen(db, 'before_commit', update_size_and_date)
        yield db
    finally:
        db.close()


@app.on_event('startup')
async def startup_event():
    logger.info('App started')
    try:
        db = SessionLocal()
        db.execute('SELECT 1')
        logger.info('Successfully connected to database')
    except Exception as e:
        logger.error('Could not connect to database', exc_info=e)


@app.on_event('shutdown')
async def shutdown_event():
    logger.info('Shutdown app')


@app.post('/imports')
async def import_node(items: models.ImportNode, db: Session = Depends(get_db)):
    try:
        NodeHandler(db).insert_or_update_nodes(items)
    except Exception as e:
        logger.error(e)
        raise RequestValidationError(e)
    return status.HTTP_200_OK


@app.get(
    '/nodes/{id}',
    response_model=models.ResponseNode,
    responses={
        status.HTTP_404_NOT_FOUND: {'model': settings.NotFoundResponse}
    },
)
async def get_node(
    id: str = Path(regex='^[a-zA-Z0-9-_]*$', min_length=1),
    db: Session = Depends(get_db),
):
    logger.info(id)
    try:
        node = NodeHandler(db).get_node(id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=503)
    if not node:
        return not_found()
    return node


@app.delete(
    '/delete/{id}',
    responses={
        status.HTTP_404_NOT_FOUND: {'model': settings.NotFoundResponse}
    },
)
async def delete_node(
    id: str = Path(regex='^[a-zA-Z0-9-_]*$', min_length=1),
    date: str = Depends(validate_date),
    db: Session = Depends(get_db),
):
    node = NodeHandler(db).get_node(id)
    if not node:
        return not_found()
    try:
        NodeHandler(db).delete_node(id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=503)


@app.get('/updates', response_model=models.ResponseUpdates)
async def get_updates(
    date: str = Depends(validate_date), db: Session = Depends(get_db)
):
    try:
        updates = NodeHandler(db).get_node_updates(date)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=503)
    return models.ResponseUpdates(items=updates)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.api_settings.host,
        port=settings.api_settings.port,
        reload=True,
    )
