import json

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.models import DATE_FORMAT
from backend.app.handlers.base import NodeHandler
from backend.db.schema import Node

client = TestClient(app)


def import_response(data):
    return client.post('/imports', data=json.dumps(data))


def test_correct_data_import(root, correct_import):

    root_response = import_response(root)
    child_response = import_response(correct_import)

    assert root_response.status_code == 200
    assert child_response.status_code == 200


def test_file_url_len(incorrect_import_file_url_len):
    response = import_response(incorrect_import_file_url_len)
    assert response.status_code == 400, 'Не верный статус при длине url > 255'


def test_item_type(incorrect_import_type):
    response = import_response(incorrect_import_type)
    assert (
        response.status_code == 400
    ), 'Не верный статус при не правильном типе'


def test_item_id(incorrect_id_none):
    response = import_response(incorrect_id_none)
    assert response.status_code == 400, 'Не верный статус при id = None'


def test_item_id_not_equal_parent_id(id_equal_parent_id):
    response = import_response(id_equal_parent_id)
    assert response.status_code == 400, 'Не верный статус при id == parentId'


def test_file_size(incorrect_file_size):
    response = import_response(incorrect_file_size)
    assert response.status_code == 400, 'Не верный статус при size = 0'


def test_extra_field(extra_field_children):
    response = import_response(extra_field_children)
    assert response.status_code == 400, 'Не верный статус при лишнем поле'


def test_parent_not_folder(parent_not_folder):
    response = import_response(parent_not_folder)
    assert (
        response.status_code == 400
    ), 'Не верный статус при parent type = File'


def test_type_change(change_item_type):
    initial_data, type_changing_data = change_item_type
    initial_response = import_response(initial_data)
    type_change_response = import_response(type_changing_data)

    assert initial_response.status_code == 200
    assert (
        type_change_response.status_code == 400
    ), 'Неверный статус при изменении типа'


def test_incorrect_date_format(incorrect_date_format):
    response = import_response(incorrect_date_format)
    assert (
        response.status_code == 400
    ), 'Не верный статус при не правильном формате даты и времени'
