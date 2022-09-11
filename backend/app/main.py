import uvicorn
from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.exceptions import ValidationError, RequestValidationError
from sqlalchemy.orm import Session

from backend.app import models
from backend.app.database import SessionLocal
from backend.app.settings import api_settings
from backend.app.exceptions import validation_error_handler
from backend.app.handlers.base import NodeHandler

app = FastAPI()
app.add_exception_handler(RequestValidationError, validation_error_handler)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def test():
    return {'text': 'hello'}


@app.post('/imports/')
def import_node(items: models.ImportNode, db: Session = Depends(get_db)):
    NodeHandler(db).insert_or_update_nodes(items)
    return items


@app.get('/nodes/{id}')
def get_node(id: str, db: Session = Depends(get_db)):
    return NodeHandler(db).get_node(id)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=api_settings.host,
        port=api_settings.port,
        log_level=api_settings.log_level.lower(),
        reload=True,
    )
