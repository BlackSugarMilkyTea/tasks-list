from flask_restx import Api

tasks_api = Api()

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json'
}
