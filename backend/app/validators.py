from datetime import datetime as dt

from fastapi import Query
from fastapi.exceptions import HTTPException

from backend.app.models import DATE_FORMAT


def validate_date(date: str = Query(...)) -> dt:
    try:
        date = dt.strptime(date, DATE_FORMAT)
    except ValueError:
        raise HTTPException(status_code=400, detail='Wrong date format')
    return date
