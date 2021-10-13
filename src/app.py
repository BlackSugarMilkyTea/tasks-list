from flask import Flask

app = Flask(__name__)
app.config['RESTX_VALIDATE'] = True
