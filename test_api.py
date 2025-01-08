import requests as r
import unittest
import time
import uuid


from requests import session
# Test API endpoint

#SWAGGER dos: https://todo.pixegami.io/docs

ENDPOINT_1 = 'https://todo.pixegami.io'


def test_api_get_1():
    print('Test_1____________:\n')
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
    print(resp.json())

    # second way to assert by using unittest
    unittest.TestCase().assertEqual(resp.status_code, 200)
    unittest.TestCase().assertEqual(resp.json(), {'message': 'Hello World from Todo API'})

def test_can_create_task_2():
    print('Test_2____________:\n')
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
    print('Test_3____________:\n')
    resp = r.get(ENDPOINT_1 + f'/get-task/{task_id}')
    assert resp.status_code == 200
    assert resp.json()['task_id'] == task_id
    print(resp.json())


def test_can_update_task_4():
    # create task
    # update task
    # get task and validate changes
    print('Test_4____________:\n')
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
    print(get_task_response.json())


def test_user_can_list_all_tasks_5():
    #     # create X tasks
    print('Test_5____________:\n')
    x = 3
    payload = new_task_payload()
    for task in range(x):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200
    # list all tasks. and check that there X tasks
    user_id = payload['user_id']
    list_task_response = list_tasks(user_id)
    assert list_task_response.status_code == 200
    data = list_task_response.json()
    assert len(data['tasks']) == x, f"Expected {x} tasks, but got {len(data['tasks'])}"


def test_can_delete_task_6():
    # Create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']

    # Delete the task
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200, f"Failed to delete task {task_id}"

    # Get the task and validate that it does not exist
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404
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

def list_tasks(user_id):
    return r.get(ENDPOINT_1 +f"/list-tasks/{user_id}")

def new_task_payload():
    # helper function
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"

    print(f"Creating task for user {user_id} with content {content}")
    payload = {"content": content,
            "user_id": user_id,
            "is_done": False}
    return payload

def delete_task(task_id):
    return r.delete(ENDPOINT_1 + f"/delete-task/{task_id}")
