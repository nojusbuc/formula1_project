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
            'frontLeftTireWear': None,
            'frontRightTireWear': None,
            'RearLeftTireWear': None,
            'RearRightTireWear': None,
            'carPosition': None,
            'lastLapTime': None,
            'bestLapTime': None,
            'sector1Time': None,
            'sector2Time': None,
            'ersActivated': None,
        }

    def fill_in_data(self, current_frame, current_frame_data, playerCar):
        self.list_data['speed'] = current_frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].speed
        self.list_data['throttle'] = current_frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].throttle
        self.list_data['brake'] = current_frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].brake
        self.list_data['gear'] = current_frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].gear
        self.list_data['engineRPM'] = current_frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].engineRPM
        self.list_data['drs'] = current_frame_data[PacketID.CAR_TELEMETRY].carTelemetryData[player_car].drs
        self.list_data['ersActivated'] = True if current_frame_data[PacketID.CAR_STATUS].carStatusData[player_car].ersDeployMode != 0 else False

        print(self.list_data['speed'])

    def print_list_data(self):
        for key, value in self.list_data.items():
            print(f'{key}: {value}')
        print('iteration complete')

    def write_to_json(self):
        json_string = json.dumps(self.list_data)
        with open('./interface/live_telemetry/telem-data.json', 'w') as f:
            print('json')
            json.dump(json_string, f)


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

# functionality

time_from_last_print = time.time()
while True:

    conn = sqlite3.connect('./local_database/pydatabase.db')
    c = conn.cursor()
    current_val = (
        c.execute('SELECT * FROM runningProgram WHERE id = 0')).fetchone()

    if current_val[1] == 'True':

        data, addr = sock.recvfrom(PACKET_SIZE)
        packet = unpack_udp_packet(data)

        current_frame_data[PacketID(packet.header.packetId)] = packet

        any_packet = next(iter(current_frame_data.values()))
        player_car = any_packet.header.playerCarIndex

        try:

            if time_from_last_print + 0.1 < time.time():
                use_data.fill_in_data(
                    current_frame, current_frame_data, player_car)
                use_data.print_list_data()
                use_data.write_to_json()
                time_from_last_print = time.time()
        except:
            current_frame = packet.header.frameIdentifier

    # data, addr = sock.recvfrom(PACKET_SIZE)
    # packet = unpack_udp_packet(data)

    # current_frame_data[PacketID(packet.header.packetId)] = packet

    # any_packet = next(iter(current_frame_data.values()))
    # player_car = any_packet.header.playerCarIndex

    # try:

    #     if time_from_last_print + 0.1 < time.time():
    #         use_data.fill_in_data(
    #             current_frame, current_frame_data, player_car)
    #         use_data.print_list_data()
    #         use_data.write_to_json()
    #         time_from_last_print = time.time()
    # except:
    #     current_frame = packet.header.frameIdentifier
