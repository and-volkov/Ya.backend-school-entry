def nodes_response(id, test_app):
    return test_app.get(f'/nodes/{id}')


def test_not_existing_id(test_app):
    test_id = 'a1b2c3d4'
    expected_json = {"code": 404, "message": "Item Not Found"}
    response = nodes_response(test_id, test_app)
    assert (
        response.status_code == 404
    ), 'Не верный статус при отсутствии искомого элемента'
    assert response.json() == expected_json, 'Не верное тело ответа'


def test_incorrect_request(test_app):
    incorrect_request = ' '
    response = nodes_response(incorrect_request, test_app)
    assert (
        response.status_code == 400
    ), 'Неверный статус при невалидном запросе'
