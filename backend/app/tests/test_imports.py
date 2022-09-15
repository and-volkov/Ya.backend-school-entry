import json


def import_response(data, test_app):
    return test_app.post('/imports', data=json.dumps(data))


def test_correct_data_import(root, correct_import, test_app):

    root_response = import_response(root, test_app)
    child_response = import_response(correct_import, test_app)

    assert root_response.status_code == 200
    assert child_response.status_code == 200


def test_file_url_len(incorrect_import_file_url_len, test_app):
    response = import_response(incorrect_import_file_url_len, test_app)
    assert response.status_code == 400, 'Не верный статус при длине url > 255'


def test_item_type(incorrect_import_type, test_app):
    response = import_response(incorrect_import_type, test_app)
    assert (
        response.status_code == 400
    ), 'Не верный статус при не правильном типе'


def test_item_id(incorrect_id_none, test_app):
    response = import_response(incorrect_id_none, test_app)
    assert response.status_code == 400, 'Не верный статус при id = None'


def test_item_id_not_equal_parent_id(id_equal_parent_id, test_app):
    response = import_response(id_equal_parent_id, test_app)
    assert response.status_code == 400, 'Не верный статус при id == parentId'


def test_file_size(incorrect_file_size, test_app):
    response = import_response(incorrect_file_size, test_app)
    assert response.status_code == 400, 'Не верный статус при size = 0'


def test_extra_field(extra_field_children, test_app):
    response = import_response(extra_field_children, test_app)
    assert response.status_code == 400, 'Не верный статус при лишнем поле'


def test_parent_not_folder(parent_not_folder, test_app):
    response = import_response(parent_not_folder, test_app)
    assert (
        response.status_code == 400
    ), 'Не верный статус при parent type = File'


def test_type_change(change_item_type, test_app):
    initial_data, type_changing_data = change_item_type
    initial_response = import_response(initial_data, test_app)
    type_change_response = import_response(type_changing_data, test_app)

    assert initial_response.status_code == 200
    assert (
        type_change_response.status_code == 400
    ), 'Неверный статус при изменении типа'


def test_incorrect_date_format(incorrect_date_format, test_app):
    response = import_response(incorrect_date_format, test_app)
    assert (
        response.status_code == 400
    ), 'Не верный статус при не правильном формате даты и времени'


def test_folder_item_has_size(folder_has_size, test_app):
    response = import_response(folder_has_size, test_app)
    assert (
        response.status_code == 400
    ), 'Не верный статус при наличии поля size у папки'


def test_folder_item_has_url(folder_has_url, test_app):
    response = import_response(folder_has_url, test_app)
    assert (
        response.status_code == 400
    ), 'Не верный статус при наличии поля url у папки'


def test_items_have_save_ids(items_with_same_id, test_app):
    response = import_response(items_with_same_id, test_app)
    assert (
        response.status_code == 400
    ), 'Не верный статус при импорте двух элементов с одинаковым id'
