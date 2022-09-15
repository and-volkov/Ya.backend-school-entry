def delete_response(id, params, test_app):
    return test_app.delete(f'/delete/{id}', params=params)


def test_not_existing_id(test_app):
    not_existing_id = 'a1b2c3d4'
    params = {'date': '2022-02-01T12:00:00Z'}
    expected_json = {"code": 404, "message": "Item Not Found"}
    response = delete_response(not_existing_id, params, test_app)
    assert (
        response.status_code == 404
    ), 'Не верный статус при отсутствии удаляемого элемента'
    assert response.json() == expected_json, 'Не верное тело ответа'


def test_incorrect_date(test_app):
    existing_id = '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'
    invalid_date = {'date': '2022-02-01T12:00:00'}
    response = delete_response(existing_id, invalid_date, test_app)
    assert response.status_code == 400, 'Не верный статус при невалидной дате'
