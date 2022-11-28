import sys
from flask import Flask, render_template
import socket
import select
import queue
import sqlite3
from streaming import packets
import time
from streaming.frame_data import UsefulData
from streaming.packets import PacketID, unpack_udp_packet
import multiprocessing
from multiprocessing import Manager
from multiprocessing.managers import BaseManager
from contextlib import closing
import asyncio
from flask_sqlalchemy import SQLAlchemy
from streaming.listen_to_udp import listen_to_udp


#setting up flask program
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_db.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# db = SQLAlchemy()
# db.init_app(app)


#main page
@app.route('/')
def index():
    return render_template('index.html')


# data request from front-end
# @app.route('/getjson', methods=['GET', 'POST'])
# def get_json():
#     print(f'list data: {telem_obj}')
#     return telem_obj


#telemetry page
@app.route('/telem')
def telemetry():
    return render_template('telem.html')



if __name__ == '__main__':
    # starting a secondary daemon process and running flask app
    p2 = multiprocessing.Process(target=listen_to_udp)
    p2.daemon = True
    p2.start()
    app.run(port=5000)






