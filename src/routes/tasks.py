from typing import List

from flask import current_app as app, request
from flask_restx import Resource, fields
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from models.tasks import Task, db
from .conf import tasks_api as api, HEADERS


@api.route('/tasks')
class Tasks(Resource):
    def get(self):
        tasks: List[Task] = db.session.query(Task).all()
        return {'result': [t.to_dict() for t in tasks]}, 200, HEADERS

    @api.expect(api.model('put_a_task', {
        'name': fields.String,
    }, strict=True))
    def post(self):
        try:
            task: Task = Task(
                name=request.json['name'],
                status=False
            )
            db.session.add(task)
            db.session.commit()
            return {'result': task.to_dict()}, 201, HEADERS
        except Exception:
            app.logger.exception(msg := f'Error on tasks with name: {request.json["name"]}')
            return {'message': msg}, 500, HEADERS


@api.route('/tasks/<int:id>')
class ATask(Resource):
    def get(self, id):
        try:
            task: Task = db.session.query(Task).filter_by(id=id).one()
            return {'result': task.to_dict()}, 200, HEADERS
        except NoResultFound:
            app.logger.exception(msg := f'No task with {id=}')
            return {'message': msg}, 404, HEADERS
        except MultipleResultsFound:
            app.logger.exception(msg := f'Multiple tasks with {id=}')
            return {'message': msg}, 500, HEADERS
        except Exception:
            app.logger.exception(msg := f'Error on tasks with {id=}')
            return {'message': msg}, 500, HEADERS

    @api.expect(api.model('put_a_task', {
        'name': fields.String,
        'status': fields.Integer,
    }, strict=True))
    def put(self, id):
        try:
            task: Task = db.session.query(Task).filter_by(id=id).one()
            task.name = request.json['name']
            task.status = bool(request.json['status'])
            db.session.commit()
            return {'result': task.to_dict()}, 200, HEADERS
        except NoResultFound:
            app.logger.exception(msg := f'No task with {id=}')
            return {'message': msg}, 404, HEADERS
        except MultipleResultsFound:
            app.logger.exception(msg := f'Multiple tasks with {id=}')
            return {'message': msg}, 500, HEADERS
        except Exception:
            app.logger.exception(msg := f'Error on tasks with {id=}')
            return {'message': msg}, 500, HEADERS

    def delete(self, id):
        try:
            task: Task = db.session.query(Task).filter_by(id=id).one()
            db.session.delete(task)
            db.session.commit()
            return {'result': True}, 200, HEADERS
        except NoResultFound:
            app.logger.exception(msg := f'No task with {id=}')
            return {'message': msg}, 404, HEADERS
        except MultipleResultsFound:
            app.logger.exception(msg := f'Multiple tasks with {id=}')
            return {'message': msg}, 500, HEADERS
        except Exception:
            app.logger.exception(msg := f'Error on tasks with {id=}')
            return {'message': msg}, 500, HEADERS
