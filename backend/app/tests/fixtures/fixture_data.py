import pytest


@pytest.fixture(scope='module')
def root():
    root = {
        "items": [
            {
                "type": "FOLDER",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None,
            }
        ],
        "updateDate": "2022-02-01T12:00:00Z",
    }
    return root


@pytest.fixture(scope='module')
def correct_import():
    import_data = {
        "items": [
            {
                "type": "FOLDER",
                "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            },
            {
                "type": "FILE",
                "url": "/file/url1",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "size": 128,
            },
            {
                "type": "FILE",
                "url": "/file/url2",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "size": 256,
            },
        ],
        "updateDate": "2022-02-02T12:00:00Z",
    }
    return import_data


FILE_ITEM = {
    "type": "FILE",
    "url": "/file/url2",
    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
    "size": 256,
}

FOLDER_ITEM = {
    "type": "FOLDER",
    "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
    "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
}


@pytest.fixture(scope='function')
def incorrect_import_type():
    test_item = FILE_ITEM.copy()
    test_item['type'] = 'NOT_FILE'
    return {"items": [test_item]}


@pytest.fixture(scope='function')
def incorrect_import_file_url_len():
    test_item = FILE_ITEM.copy()
    test_item['url'] = "1" * 256
    data = {
        "items": [test_item],
        "updateDate": "2022-02-01T12:00:00Z",
    }
    return data


@pytest.fixture(scope='function')
def incorrect_id_none():
    test_item = FILE_ITEM.copy()
    test_item['id'] = None
    data = {
        "items": [test_item],
        "updateDate": "2022-02-01T12:00:00Z",
    }
    return data


@pytest.fixture(scope='function')
def id_equal_parent_id():
    test_item = FILE_ITEM.copy()
    test_item['parentId'] = 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4"'
    data = {
        "items": [test_item],
        "updateDate": "2022-02-01T12:00:00Z",
    }
    return data


@pytest.fixture(scope='function')
def incorrect_file_size():
    test_item = FILE_ITEM.copy()
    test_item['size'] = 0
    data = {
        "items": [test_item],
        "updateDate": "2022-02-01T12:00:00Z",
    }
    return data


@pytest.fixture(scope='function')
def extra_field_children():
    test_item = FILE_ITEM.copy()
    test_item['children'] = 123
    data = {
        "items": [test_item],
        "updateDate": "2022-02-01T12:00:00Z",
    }
    return data


@pytest.fixture(scope='function')
def parent_not_folder():
    test_item = FILE_ITEM.copy()
    test_item['parentId'] = '863e1a7a-1304-42ae-943b-179184c077e3'
    data = {
        "items": [test_item],
        "updateDate": "2022-02-01T12:00:00Z",
    }
    return data


@pytest.fixture(scope='function')
def change_item_type():
    test_item = FILE_ITEM.copy()
    test_item['type'] = 'FOLDER'
    initial_data = {
        "items": [FILE_ITEM],
        "updateDate": "2022-02-01T12:00:00Z",
    }
    type_changing_data = {
        "items": [test_item],
        "updateDate": "2022-02-01T12:00:00Z",
    }
    return initial_data, type_changing_data


@pytest.fixture(scope='function')
def incorrect_date_format():
    data = {
        "items": [FILE_ITEM],
        "updateDate": "2022-02-01T12:00:00",
    }
    return data


@pytest.fixture(scope='function')
def folder_has_size():
    test_item = FOLDER_ITEM.copy()
    test_item['size'] = 256
    data = {
        "items": [test_item],
        "updateDate": "2022-02-01T12:00:00Z",
    }
    return data


@pytest.fixture(scope='function')
def folder_has_url():
    test_item = FOLDER_ITEM.copy()
    test_item['url'] = '/file/url2'
    data = {
        "items": [test_item],
        "updateDate": "2022-02-01T12:00:00Z",
    }
    return data


@pytest.fixture(scope='function')
def items_with_same_id():
    data = {
        "items": [FILE_ITEM, FILE_ITEM],
        "updateDate": "2022-02-01T12:00:00Z",
    }
    return data
