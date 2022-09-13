import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.exceptions import ValidationError, RequestValidationError
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.app import models
from backend.app import settings
from backend.app.database import SessionLocal
from backend.app.exceptions import validation_error_handler
from backend.app.handlers.base import NodeHandler
from backend.app.handlers.events import update_size_and_date
from backend.app.validators import validate_date


app = FastAPI(
    title=settings.api_settings.title,
    description=settings.api_settings.description,
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': settings.ErrorResponse},
    }
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


@app.post('/imports')
async def import_node(items: models.ImportNode, db: Session = Depends(get_db)):
    NodeHandler(db).insert_or_update_nodes(items)
    return status.HTTP_200_OK


@app.get('/nodes/{id}', response_model=models.ResponseNode,
         responses={
             status.HTTP_404_NOT_FOUND: {'model': settings.ErrorResponse}
         })
async def get_node(id: str, db: Session = Depends(get_db)):
    node = NodeHandler(db).get_node(id)
    if not node:
        raise HTTPException(status_code=404)
    return node


@app.delete('/delete/{id}')
async def delete_node(
    id: str, date: str = Depends(validate_date), db: Session = Depends(get_db)
):
    return NodeHandler(db).delete_node(id)


@app.get('/updates', response_model=models.ResponseUpdates)
async def get_updates(
    date: str = Depends(validate_date), db: Session = Depends(get_db)
):
    updates = NodeHandler(db).get_node_updates(date)
    return models.ResponseUpdates(items=updates)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.api_settings.host,
        port=settings.api_settings.port,
        log_level=settings.api_settings.log_level.lower(),
        reload=True,
    )
