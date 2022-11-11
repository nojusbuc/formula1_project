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
from variab import use_data


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_db.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)


def listen_to_udp():

    with closing(sqlite3.connect("./flask_db.db")) as conn:
        with closing(conn.cursor()) as cur:

            print('udp')
            SERVER = socket.gethostbyname(socket.gethostname())
            PORT = 20777

            PACKET_SIZE = 2048

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((SERVER, PORT))

            current_frame_data = {}

            use_data.conn = conn
            use_data.cur = cur



            while True:

                # should_run = cur.execute(
                #     f'SELECT should_run FROM streaming WHERE should_run = 1').fetchone()
                # if should_run is not None:

                data, addr = sock.recvfrom(PACKET_SIZE)
                packet = unpack_udp_packet(data)

                current_frame_data[PacketID(packet.header.packetId)] = packet

                any_packet = next(iter(current_frame_data.values()))
                player_car = any_packet.header.playerCarIndex


                if packet.header.packetId == 1:
                    use_data.sessionTable(current_frame_data, player_car, packet)
                elif packet.header.packetId == 4:
                    use_data.updateSessionTable(packet)
                    use_data.playerTable(packet)

                elif packet.header.packetId == 2:
                    use_data.updatePlayerTable(packet)
                    use_data.lapDataTable(packet)

                elif packet.header.packetId == 6:
                    # use_data.telemetryTable()
                    global telem_obj
                    telem_obj = use_data.telemetryTable(packet)
                    print(telem_obj)
                    # print(use_data.list_data, 'PROC.PY when packet is telemetry')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getjson', methods=['GET', 'POST'])
def get_json():
    return telem_obj

@app.route('/telem')
def telemetry():
    return render_template('telem.html')


if __name__ == '__main__':
    
    p2 = multiprocessing.Process(target=listen_to_udp)
    p2.daemon = True
    p2.start()
    app.run(port=5000)
