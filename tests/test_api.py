import datetime

import pytest
from fastapi.testclient import TestClient

from tasks import models
from database import get_db
from main import app
from tests.config import get_test_db, engine_test

BASE_URL = 'http://localhost:8000/api/v1.0/'

client = TestClient(app)


@pytest.fixture(autouse=True)
def prepare_database():
    models.Base.metadata.create_all(bind=engine_test)
    yield
    models.Base.metadata.drop_all(bind=engine_test)


app.dependency_overrides[get_db] = get_test_db


def create_task(tittle, text="", deadline=None):
    return client.post(BASE_URL + 'tasks/', json={'title': tittle, 'text': text, 'deadline': deadline})


def get_task_by_id(task_id):
    return client.get(BASE_URL + 'tasks/%d' % task_id)


def test_task_creation():
    response = create_task("New task", "")
    assert response.status_code == 201
    check = get_task_by_id(response.json()['id']).json()
    assert check['title'] == 'New task'
    assert check['text'] == ''
    assert check['completed'] is False
    assert check['deadline'] is None


def test_get_tasks_list():
    create_task("New task")
    response = client.get(BASE_URL + 'tasks')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['title'] == 'New task'


def test_get_tasks_limit_offset():
    task_tittles = ["task%d" % number for number in range(20)]
    for tittle in task_tittles:
        create_task(tittle)
    first_five = client.get(BASE_URL + 'tasks', params={'limit': 5}).json()
    assert len(first_five) == 5
    assert first_five[0]['title'] == 'task0'
    assert first_five[-1]['title'] == 'task4'
    seven_from_five = client.get(BASE_URL + 'tasks', params={'limit': 7, 'offset': 5}).json()
    assert len(seven_from_five) == 7
    assert seven_from_five[0]['title'] == 'task5'
    assert seven_from_five[-1]['title'] == 'task11'


def test_get_task_by_id():
    new_task = create_task("Task", "Text").json()
    check_task = get_task_by_id(new_task['id']).json()
    assert new_task == check_task


def test_get_task_by_not_existing_id():
    check_task = get_task_by_id(1000)
    assert check_task.status_code == 404


def test_task_completion():
    task = create_task("Task").json()
    assert task['completed'] is False
    client.patch(BASE_URL + 'tasks/%d/complete' % task['id'])
    task = get_task_by_id(task['id']).json()
    assert task['completed'] is True


def test_task_deleting():
    task = create_task("Task").json()
    assert get_task_by_id(task['id']).status_code == 200
    client.delete(BASE_URL + "tasks/%d" % task['id'])
    assert get_task_by_id(task['id']).status_code == 404
