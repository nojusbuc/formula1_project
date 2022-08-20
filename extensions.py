from flask_sqlalchemy import SQLAlchemy
from flask import Flask
db = SQLAlchemy()


# def create_app():
#     app = Flask(__name__)
#     db.init_app(app)
#     app.app_context().push()
#     return app


app = Flask(__name__)
app.config['SECRET KEY'] = 'abd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config.update(CELERY_CONFIG={
#     'broker_url': 'redis://localhost:6379',
#     'result_backend': 'redis://localhost:6379',
# })
db.init_app(app)
app.app_context().push()




