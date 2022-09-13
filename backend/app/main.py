import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import event
from fastapi.exceptions import ValidationError, RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.app import models
from backend.app.database import SessionLocal
from backend.app.settings import api_settings
from backend.app.exceptions import validation_error_handler
from backend.app.handlers.base import NodeHandler
from backend.app.handlers.events import update_size

app = FastAPI()
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(IntegrityError, validation_error_handler)
app.add_exception_handler(ValidationError, validation_error_handler)


def get_db():
    db = SessionLocal()
    try:
        event.listen(db, 'before_commit', update_size)
        yield db
    finally:
        db.close()


@app.get('/')
def test():
    return {'text': 'hello'}


@app.post('/imports', status_code=200)
async def import_node(items: models.ImportNode, db: Session = Depends(get_db)):
    NodeHandler(db).insert_or_update_nodes(items)
    return status.HTTP_200_OK


@app.get('/nodes/{id}', response_model=models.ResponseNode)
async def get_node(id: str, db: Session = Depends(get_db)):
    node = NodeHandler(db).get_node(id)
    if not node:
        raise HTTPException(status_code=404)
    return node


@app.delete('/delete/{id}')
async def delete_node(id: str, db: Session = Depends(get_db)):
    req = id.split('?')
    node_id = req[0]
    return NodeHandler(db).delete_node(node_id)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=api_settings.host,
        port=api_settings.port,
        log_level=api_settings.log_level.lower(),
        reload=True,
    )
