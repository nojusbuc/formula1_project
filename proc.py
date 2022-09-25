import sys
from flask import Flask
import socket
import select
import queue
import sqlite3
from streaming import packets
import time
from streaming.frame_data import UsefulData
from streaming.packets import PacketID, unpack_udp_packet
import multiprocessing


app = Flask(__name__)

def listen_to_udp():

    SERVER = socket.gethostbyname(socket.gethostname())
    PORT = 20777

    PACKET_SIZE = 2048

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((SERVER, PORT))

    current_frame = None
    current_frame_data = {}

    conn = sqlite3.connect('./flask_db.db')
    cur = conn.cursor()

    use_data = UsefulData(conn=conn, cur=cur)

    time_from_last_print = time.time()

    try:
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

            # print(any_packet)

            if packet.header.packetId == 1:
                use_data.sessionTable(current_frame_data, player_car, packet)
            elif packet.header.packetId == 4:
                use_data.updateSessionTable(packet)
                use_data.playerTable(packet)

            elif packet.header.packetId == 2:
                use_data.updatePlayerTable(packet)
                use_data.lapDataTable(packet)

            elif packet.header.packetId == 6:
                use_data.telemetryTable(packet)

    except KeyboardInterrupt:
        multiprocessing.Process.terminate(self=p1)
        # p1.terminate()


@app.route('/')
def index():
    # listen_to_udp.delay()
    return "oof"


@app.route('/pyfile')
def handle_udp():
    listen_to_udp.delay()


def run_flask():
    print('running server')
    app.run(port=5000, debug=True)


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=run_flask)
    p2 = multiprocessing.Process(target=listen_to_udp)

    p1.start()
    p2.start()

