# from extensions import db
from celery import Celery
from threading import Thread
from flask import Flask
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import sys
# from multiprocessing import Process, Value
sys.path.insert(0, 'streaming')
from models import *
from extensions import db, app


# def make_celery(app):
#     celery = Celery(app.import_name)
#     celery.conf.update(app.config["CELERY_CONFIG"])

#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery


# @app.route('/')
# def home():
#     Streaming.query.filter_by(str_id=0).update({'should_run': 0})
#     db.session.commit()

#     return render_template('index.html')


# @app.route('/telemetry')
# def telemetry(): 
#     Streaming.query.filter_by(str_id=0).update({'should_run': 1})
#     db.session.commit()

#     Thread(target=thread2).start
#     return render_template('telemetry/time_trial_telem/telem.html')

# def thread1():
#     app.run()

# def thread2():
#     code = compile(d.read(
#         ), 'C:/Users/noahm/Desktop/Projects/f1_telem/streaming/frame_data.py', "exec")
#     exec(code, {})
#     print('executed')


db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()


# celery = make_celery(app)


# @celery.task()
# def read_packets():
#     with open('C:/Users/noahm/Desktop/Projects/f1_telem/streaming/frame_data.py', "rb") as source_file:
#         code = compile(source_file.read(
#         ), 'C:/Users/noahm/Desktop/Projects/f1_telem/streaming/frame_data.py', "exec")
#         exec(code, {})
    # try:
    #     exec(open('C:/Users/noahm/Desktop/Projects/f1_telem/streaming/frame_data.py').read())
    # except SystemExit:
    #     print('sys exit on executing ')



# if __name__ == '__main__':
#     try:
#         d = open('C:/Users/noahm/Desktop/Projects/f1_telem/streaming/frame_data.py', "rb")
#         Thread(target=thread1).start()
#         # app.run()
    
#     except KeyboardInterrupt:
#         d.close()
#         sys.exit('keyboard inter')
        



