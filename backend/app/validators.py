from datetime import datetime as dt

from fastapi import Query
from fastapi.exceptions import RequestValidationError

from backend.app.models import DATE_FORMAT


def validate_date(date: str = Query(...)) -> dt:
    try:
        date = dt.strptime(date, DATE_FORMAT)
    except ValueError as e:
        raise RequestValidationError(errors=e.args)
    return date
