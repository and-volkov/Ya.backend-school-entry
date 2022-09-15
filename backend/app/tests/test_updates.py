def updates_response(params, test_app):
    return test_app.get('/updates', params=params)


def test_invalid_date(test_app):
    invalid_date = {'date': '2022-02-01T12:00:00'}
    response = updates_response(invalid_date, test_app)
    assert response.status_code == 400, 'Не верный статус при невалидной дате'
