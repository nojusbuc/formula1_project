import socket
from packets import PacketID, unpack_udp_packet
import math
import time
import json
import sqlite3


class UsefulData():

    def __init__(self):
        self.list_data = {
            # loop through every frame? add frame as key?
            'speed': None,
            'throttle': None,
            'brake': None,
            'gear': None,
            'engineRPM': None,
            'drs': None,
            'tyreWear': None,
            'carPosition': None,
            'lastLapTime': None,
            'bestLapTime': None,
            'sector1Time': None,
            'sector2Time': None,
            'ersActivated': None,
            'tyreSurfaceTemps': None,

        }

    def fill_in_data(self, current_frame, current_frame_data, player_car):
        self.list_data['speed'] = current_frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].speed
        self.list_data['throttle'] = current_frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].throttle
        self.list_data['brake'] = current_frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].brake
        self.list_data['gear'] = current_frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].gear
        self.list_data['engineRPM'] = current_frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].engineRPM
        self.list_data['drs'] = current_frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].drs
        self.list_data['ersActivated'] = True if current_frame_data[PacketID.CAR_STATUS].carStatusData[player_car].ersDeployMode != 0 else False
        self.list_data['tyreWear'] = current_frame_data[PacketID.CAR_DAMAGE].carDamageData[player_car].tyresWear[:]
        self.list_data['tyreSurfaceTemps'] = current_frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].tyresSurfaceTemperature[:]

        # print(self.list_data['speed'])

    def write_to_json(self):
        json_string = json.dumps(self.list_data)
        with open('./f1_telem/interface/live_telemetry/telem-data.json', 'w') as f:
            # with open('f1_telem/interface/live_telemetry/telem-data.json', 'w') as f:

            json.dump(json_string, f)

    def handle_lap_data(self):

        # print('db function')

        sector = current_frame_data[PacketID.LAP_DATA].lapData[player_car].sector + 1

        test_cur.execute(
            'SELECT current_sector FROM lap_data ORDER BY id DESC LIMIT 1')  # select last
        sector_db = test_cur.fetchone()
        sector_db = 0 if sector_db is None else sector_db[0]
        # sector_db = sector_db[0]

        test_cur.execute('SELECT * FROM lap_data')

        lap_id = len(test_cur.fetchall()) + 1

        if sector != sector_db:
            print(f'sector from udp: {sector}')
            print(f'sector from db: {sector_db}')
            print(f'lap id: {lap_id}')

            sector1_time = current_frame_data[PacketID.LAP_DATA].lapData[player_car].sector1TimeInMS / 1000
            sector2_time = current_frame_data[PacketID.LAP_DATA].lapData[player_car].sector2TimeInMS / 1000

            # test_cur.execute(f'UPDATE lap_data SET current_sector = {sector}')
            if sector == 1:
                # update sector three time and decide whether prev lap was fastest
                sector3_time = current_frame_data[PacketID.LAP_DATA].lapData[
                    player_car].lastLapTimeInMS / 1000 - sector1_time - sector2_time

                test_cur.execute(
                    f'UPDATE lap_data SET sector3_time = {sector3_time}, current_sector = {sector} WHERE id = {lap_id - 1}')

            if sector == 2:
                sector1_time = current_frame_data[PacketID.LAP_DATA].lapData[player_car].sector1TimeInMS / 1000
                test_cur.execute(
                    f'INSERT INTO lap_data (id, sector1_time, current_sector) VALUES ({lap_id}, {sector1_time}, {sector})')
                # create new row and add sector 1 to it

            if sector == 3:

                test_cur.execute(
                    f'UPDATE lap_data SET sector2_time = {sector2_time}, current_sector = {sector} WHERE id = {lap_id - 1}')
                # update row to add second sector
            test_conn.commit()
            self.print_db()

    def print_db(self):

        # print('print_db function')
        test_cur.execute('SELECT * FROM lap_data')
        print(test_cur.fetchall())


SERVER = socket.gethostbyname(socket.gethostname())
PORT = 20777

PACKET_SIZE = 2048

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((SERVER, PORT))

shouldRun = False

current_frame = None
current_frame_data = {}

use_data = UsefulData()

test_conn = sqlite3.connect('./f1_telem/local_database/test_db.db')
test_cur = test_conn.cursor()

test_cur.execute('DELETE FROM lap_data')
test_conn.commit()

l = []
# functionality

time_from_last_print = time.time()

conn = sqlite3.connect('./f1_telem/local_database/pydatabase.db')
c = conn.cursor()


while True:

    current_val = (
        c.execute('SELECT * FROM runningProgram WHERE id = 0')).fetchone()

    if current_val[1] == 'True':

        data, addr = sock.recvfrom(PACKET_SIZE)
        packet = unpack_udp_packet(data)

        current_frame_data[PacketID(packet.header.packetId)] = packet

        any_packet = next(iter(current_frame_data.values()))
        player_car = any_packet.header.playerCarIndex

        if time_from_last_print + 0.1 < time.time():
            try:
                use_data.fill_in_data(
                    current_frame, current_frame_data, player_car)
            except:
                current_frame = packet.header.frameIdentifier

            use_data.write_to_json()

            if packet.header.packetId == 2:
                use_data.handle_lap_data()

            time_from_last_print = time.time()

        # try:

        #     if time_from_last_print + 0.1 < time.time():
        #         use_data.fill_in_data(
        #             current_frame, current_frame_data, player_car)
        #         use_data.write_to_json()

        #         if packet.header.packetId == 2:
        #             use_data.handle_lap_data()

        #         time_from_last_print = time.time()
        # except:
        #     current_frame = packet.header.frameIdentifier
