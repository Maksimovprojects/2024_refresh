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
    payload = new_task_payload()
    create_task = r.put(f'{ENDPOINT_1}/create-task', json=payload)
    global task_id
    task_id = create_task.json()['task']['task_id']
    print(task_id)
    print(create_task.json())
    assert create_task.status_code == 200
    assert create_task.json()['task']['content'] == payload['content']
    assert create_task.json()['task']['user_id'] == payload['user_id']


def test_can_get_task_3():
    resp = r.get(ENDPOINT_1 + f'/get-task/{task_id}')
    assert resp.status_code == 200
    assert resp.json()['task_id'] == task_id


def test_can_update_task_4():
    # create task
    # update task
    # get task and validate changes
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']
    new_payload = {"content": "my_updated_content",
                   "user_id": payload['user_id'],
                   'task_id': task_id,
                   "is_done": True}
    update_task_response  = update_task(new_payload)
    assert update_task_response.status_code == 200

    # get task and validate changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data['content'] == new_payload['content']
    assert get_task_data['is_done'] == new_payload['is_done']

def test_can_delete_task_5():
    pass


# HELPER FUNCTIONS

# in case of POM pattern we can create a class and put this function in it, and keep in separate module
def create_task(payload):
    # helper function
    return r.put(f'{ENDPOINT_1}/create-task', json=payload)

def update_task(payload):
    # helper function
    return r.put(ENDPOINT_1 +"/update-task", json=payload)

# in case of POM pattern we can create a class and put this function in it, and keep in separate module
def get_task(task_id):
    # helper function
    return r.get(ENDPOINT_1 + f'/get-task/{task_id}')

def new_task_payload():
    # helper function
    payload = {"content": "test_content",
            "user_id": "test_user",
            "task_id": "1234567",
            "is_done": False}
    return payload
