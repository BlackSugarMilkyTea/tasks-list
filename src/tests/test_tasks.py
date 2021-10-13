import pytest
from app import app
from models.tasks import db, Task
from unittest.mock import MagicMock, patch
from setup import app  # read and setup configurations of the server and import flask app instance


class TestTasks:
    @pytest.fixture(autouse=True, scope='function')
    def client(self):
        with (
            app.test_client() as client,
            app.app_context()
        ):
            yield client

    @pytest.fixture(autouse=True, scope='function')
    def mock_session(self):
        db.drop_all()
        db.create_all()
        task_1 = Task(
            name='pre-task-1'
        )
        task_2 = Task(
            name='pre-task-2'
        )
        db.session.add_all([task_1, task_2])
        db.session.commit()
        return db.session

    def test_get_tasks(self, client, mock_session):
        with patch('routes.tasks.db', MagicMock(session=mock_session)):
            resp = client.get('/tasks')
            assert resp.status_code == 200
            assert resp.headers['Content-Type'] == 'application/json'
            assert resp.json == {
                'result': [
                    {
                        'id': 1,
                        'name': 'pre-task-1',
                        'status': 0,
                    },
                    {
                        'id': 2,
                        'name': 'pre-task-2',
                        'status': 0,
                    }
                ]
            }

    def test_post_tasks(self, client, mock_session):
        with patch('routes.tasks.db', MagicMock(session=mock_session)):
            resp = client.post('/tasks', json={'name': 'post-task-3'})
            assert resp.status_code == 201
            assert resp.headers['Content-Type'] == 'application/json'
            task: Task = mock_session.query(Task).filter_by(name='post-task-3').one()
            assert task.to_dict() == {
                'id': 3,
                'name': 'post-task-3',
                'status': 0,
            }

    def test_get_a_task(self, client, mock_session):
        with patch('routes.tasks.db', MagicMock(session=mock_session)):
            resp = client.get('/tasks/2')
            assert resp.status_code == 200
            assert resp.headers['Content-Type'] == 'application/json'
            assert resp.json == {
                'result':
                    {
                        'id': 2,
                        'name': 'pre-task-2',
                        'status': 0,
                    }
            }
            resp = client.get('/tasks/3')
            assert resp.status_code == 404
            assert resp.headers['Content-Type'] == 'application/json'
            assert resp.json == {
                'message': 'No task with id=3'
            }

    def test_put_a_task(self, client, mock_session):
        with patch('routes.tasks.db', MagicMock(session=mock_session)):
            resp = client.put('/tasks/1', json={
                'name': 'pre-task-1-ex',
                'status': 1,
            })
            assert resp.status_code == 200
            assert resp.headers['Content-Type'] == 'application/json'
            task: Task = mock_session.query(Task).filter_by(id=1).one()
            assert task.to_dict() == {
                'id': 1,
                'name': 'pre-task-1-ex',
                'status': 1,
            }
            resp = client.put('/tasks/3', json={
                'name': 'pre-task-3-ex',
                'status': 1,
            })
            assert resp.status_code == 404
            assert resp.headers['Content-Type'] == 'application/json'
            assert resp.json == {
                'message': 'No task with id=3'
            }

    def test_delete_a_task(self, client, mock_session):
        with patch('routes.tasks.db', MagicMock(session=mock_session)):

            task: Task = mock_session.query(Task).filter_by(id=1).one()
            assert task is not None

            resp = client.delete('/tasks/1', json={
                'id': 1,
                'name': 'pre-task-1-ex',
                'status': 1,
            })
            assert resp.status_code == 200
            assert resp.headers['Content-Type'] == 'application/json'
            assert resp.json == {'result': True}
            task: Task = mock_session.query(Task).filter_by(id=1).scalar()
            assert task is None

            resp = client.delete('/tasks/1')
            assert resp.status_code == 404
            assert resp.headers['Content-Type'] == 'application/json'
            assert resp.json == {
                'message': 'No task with id=1'
            }
