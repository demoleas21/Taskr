from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)

from src.users.views import users_blueprint
from src.tasks.views import tasks_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)
