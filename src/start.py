from setup import app  # read and setup configurations of the server and import flask app instance

if __name__ == '__main__':
    app.logger.info(app.url_map)
    app.run(host='0.0.0.0', port=58080, debug=False)
