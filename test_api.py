import requests as r
import unittest
import time


from requests import session
# Test API endpoint

#SWAGGER dos: https://todo.pixegami.io/docs

ENDPOINT_1 = 'https://todo.pixegami.io'


def test_api_get_1():
    start_time = time.time()  # Start timing
    resp = r.get(ENDPOINT_1)
    acceptable_time_seconds = 3  # Define the acceptable time in seconds
    end_time = time.time()  # End timing

    execution_time = end_time - start_time
    assert execution_time <= acceptable_time_seconds, (
        f"API call took {execution_time:.4f} seconds, which exceeds the limit of {acceptable_time_seconds} seconds"
    )

    print(f"API call completed in {execution_time:.4f} seconds")
    assert resp.json() == {'message': 'Hello World from Todo API'}
    assert resp.headers['Content-Type'] == 'application/json'
    assert resp.status_code == 200

    # second way to assert by using unittest
    unittest.TestCase().assertEqual(resp.status_code, 200)
    unittest.TestCase().assertEqual(resp.json(), {'message': 'Hello World from Todo API'})

def test_can_create_task_2():
    payload = {"content": "blabla",
               "user_id": "dummy",
               "task_id": "1234567",
               "is_done": False}
    create_task = r.put(f'{ENDPOINT_1}/create-task', json=payload)
    global task_id
    task_id = create_task.json()['task']['task_id']
    print(task_id)
    print(create_task.json())
    assert create_task.status_code == 200
    assert create_task.json()['task']['content'] == payload['content']
    assert create_task.json()['task']['user_id'] == payload['user_id']
def test_can_get_task_3():
    print('Test3')
    resp = r.get(ENDPOINT_1 + f'/get-task/{task_id}')
    print(resp.json())
    assert resp.status_code == 200

