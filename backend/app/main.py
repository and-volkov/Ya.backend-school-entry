import uvicorn
from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.exceptions import ValidationError, RequestValidationError
from sqlalchemy.orm import Session

import models
from database import SessionLocal
from settings import api_settings
from exceptions import validation_error_handler

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
    return items


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=api_settings.host,
        port=api_settings.port,
        log_level=api_settings.log_level.lower(),
        reload=True,
    )
