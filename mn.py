import sys
from flask import Flask
from celery import Celery
import socket, select, queue
import sqlite3
from streaming import packets
import time
# sys.path.insert(0, '/streaming')
from streaming.frame_data import UsefulData
from streaming.packets import PacketID, unpack_udp_packet
import threading
from _thread import *
# import frame_data
# import packets
# from frame_data import UseData
# from packets import PacketID, unpack_udp_packet

print_lock = threading.Lock()

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        # abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

                # return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)
socket_queue = queue.Queue()


@celery.task()
def listen_to_udp():

    SERVER = socket.gethostbyname(socket.gethostname())
    PORT = 20777

    PACKET_SIZE = 2048

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((SERVER, PORT))

    current_frame = None
    current_frame_data = {}

    use_data = UsefulData()

    time_from_last_print = time.time()

    # conn = sqlite3.connect('./flask_db.db')
    # cur = conn.cursor()

    while True:
            print('waba')

        # should_run = cur.execute(
        #     f'SELECT should_run FROM streaming WHERE should_run = 1').fetchone()
        # if should_run is not None:

            data, addr = sock.recvfrom(PACKET_SIZE)
            packet = unpack_udp_packet(data)

            current_frame_data[PacketID(packet.header.packetId)] = packet

            any_packet = next(iter(current_frame_data.values()))
            player_car = any_packet.header.playerCarIndex

            current_frame = packet.header.frameIdentifier
            # if time_from_last_print + 0.1 < time.time()

            print(any_packet)

            # if packet.header.packetId == 1:
            #     use_data.sessionTable(current_frame_data, player_car, packet)
            # elif packet.header.packetId == 4:
            #     use_data.updateSessionTable(packet)
            #     use_data.playerTable(packet)

            # elif packet.header.packetId == 2:
            #     use_data.updatePlayerTable(packet)
            #     use_data.lapDataTable(packet)

            # elif packet.header.packetId == 6:
            #     use_data.telemetryTable(packet)

@app.route('/')
def index():
    print('ran', socket_queue.get())
    listen_to_udp.delay()
    return "oof"

# @app.route('/pyfile')
# def handle_udp():
#     print('ran', socket_queue.get())
#     listen_to_udp.delay()
    

if __name__ == '__main__':
    print('running server')
    app.run(port=5000, debug=True)
