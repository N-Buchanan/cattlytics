from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging

logging.basicConfig(filename='cattlytics.log', level=logging.DEBUG,
        format='%(levelname)s:%(asctime)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception
from config import ROLLBAR_API_KEY

@app.before_first_request
def init_rollbar():
    rollbar.init(ROLLBAR_API_KEY, 'cattlytics', 
            root=os.path.dirname(os.path.realpath(__file__)), allow_logging_basic_config=False)
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


from flask import Request
from flask_login import current_user
class CustomRequest(Request):
    @property
    def rollbar_person(self):
        # 'id' is required, 'username' and 'email' are indexed but optional.
        # all values are strings.
        return {'id': str(current_user.id), 'username': current_user.username, 'email': current_user.email}

app.request_class = CustomRequest

from app import views, models
