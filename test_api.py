import requests as r
import unittest

from requests import session

# Test API endpoint

#SWAGGER dos: https://todo.pixegami.io/docs

ENDPOINT_1 = 'https://todo.pixegami.io'
ENDPOINT_2 = 'https://codeforces.com/api/get'

def test_api_get_1():
    resp = r.get(ENDPOINT_1)
    assert resp.status_code == 200
    assert resp.json() == {'message': 'Hello World from Todo API'}
    assert resp.headers['Content-Type'] == 'application/json'

    # second way to assert by using unittest
    unittest.TestCase().assertEqual(resp.status_code, 200)
    unittest.TestCase().assertEqual(resp.json(), {'message': 'Hello World from Todo API'})

def test_can_create_task_2():
    payload = {"content": "blabla",
               "user_id": "dummy",
               "task_id": "1234567",
               "is_done": False}
    resp = r.put(f'{ENDPOINT_1}/create-task', json=payload)
    print(resp.json())
    global task_id
    task_id = resp.json()['task']['task_id']
    print(task_id)
    assert resp.status_code == 200

def test_can_get_task_3():
    resp = r.get(ENDPOINT_1 + f'get-task/{task_id}')
    print(resp.json())
    assert resp.status_code == 200

# def test_can_get_task_4():
#     resp = r.get(f'{ENDPOINT_1} + 'get-'get/task_7e086eaf6d7a49b5b0e545517ffc72a8')
#     print(resp.json())
#     assert resp.status_code == 200
