import socket
from packets import PacketID, unpack_udp_packet
import math
import time
import json
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import sys
import os
from dattypes import SESSION_TYPES, TRACK_IDS, WEATHER_TYPES, FORMULA_TYPES, IS_ONLINE, TEAM_IDS
sys.path.append('./')
from models import Session, Player, Streaming
from extensions import db, app

                # sessions = db.session.query.order_by(UserSession.session_uid)

        # def handle_lap_data(self):

        #     # print('db function')

        #     sector = current_frame_data[PacketID.LAP_DATA].lapData[player_car].sector + 1

        #     test_cur.execute(
        #         'SELECT current_sector FROM lap_data ORDER BY id DESC LIMIT 1')  # select last
        #     sector_db = test_cur.fetchone()
        #     sector_db = 0 if sector_db is None else sector_db[0]
        #     # sector_db = sector_db[0]

        #     test_cur.execute('SELECT * FROM lap_data')

        #     lap_id = len(test_cur.fetchall()) + 1

        #     if sector != sector_db:
        #         print(f'sector from udp: {sector}')
        #         print(f'sector from db: {sector_db}')
        #         print(f'lap id: {lap_id}')

        #         sector1_time = current_frame_data[PacketID.LAP_DATA].lapData[player_car].sector1TimeInMS / 1000
        #         sector2_time = current_frame_data[PacketID.LAP_DATA].lapData[player_car].sector2TimeInMS / 1000

        #         # test_cur.execute(f'UPDATE lap_data SET current_sector = {sector}')
        #         if sector == 1:
        #             # update sector three time and decide whether prev lap was fastest
        #             sector3_time = current_frame_data[PacketID.LAP_DATA].lapData[
        #                 player_car].lastLapTimeInMS / 1000 - sector1_time - sector2_time

        #             test_cur.execute(
        #                 f'UPDATE lap_data SET sector3_time = {sector3_time}, current_sector = {sector} WHERE id = {lap_id - 1}')

        #         if sector == 2:
        #             sector1_time = current_frame_data[PacketID.LAP_DATA].lapData[player_car].sector1TimeInMS / 1000
        #             test_cur.execute(
        #                 f'INSERT INTO lap_data (id, sector1_time, current_sector) VALUES ({lap_id}, {sector1_time}, {sector})')
        #             # create new row and add sector 1 to it

        #         if sector == 3:

        #             test_cur.execute(
        #                 f'UPDATE lap_data SET sector2_time = {sector2_time}, current_sector = {sector} WHERE id = {lap_id - 1}')
        #             # update row to add second sector
        #         test_conn.commit()
        #         self.print_db()

        # def print_db(self):

        #     # print('print_db function')
        #     test_cur.execute('SELECT * FROM lap_data')
        #     print(test_cur.fetchall())

    # def shouldRun():

    # while True:

    #     current_val = (
    #         c.execute('SELECT * FROM runningProgram WHERE id = 0')).fetchone()

    #     if current_val[1] == 'True':

    #         data, addr = sock.recvfrom(PACKET_SIZE)
    #         packet = unpack_udp_packet(data)

    #         current_frame_data[PacketID(packet.header.packetId)] = packet

    #         any_packet = next(iter(current_frame_data.values()))
    #         player_car = any_packet.header.playerCarIndex

    #         if time_from_last_print + 0.1 < time.time():
    #             try:
    #                 use_data.fill_in_data(
    #                     current_frame, current_frame_data, player_car)
    #             except:
    #                 current_frame = packet.header.frameIdentifier

    #             use_data.write_to_json()

    #             # if packet.header.packetId == 2:
    #             #     use_data.handle_lap_data()

    #             time_from_last_print = time.time()

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


# def read_packets(sock, PACKET_SIZE, current_frame_data, use_data):

    # while True:

    #     data, addr = sock.recvfrom(PACKET_SIZE)
    #     packet = unpack_udp_packet(data)

    #     current_frame_data[PacketID(packet.header.packetId)] = packet

    #     any_packet = next(iter(current_frame_data.values()))
    #     player_car = any_packet.header.playerCarIndex

    #         # if time_from_last_print + 0.1 < time.time():
    #     try:
    #         use_data.fill_in_data(
    #                     current_frame, current_frame_data, player_car)
    #     except:
    #         current_frame = packet.header.frameIdentifier

    #                 # use_data.write_to_json()
    #     use_data.sessionTable()

    #     argum = False

    #         # if packet.header.packetId == 1:
    #         #     print(packet.header.sessionUID)
    #             # use_data.handle_lap_data()

    #         # time_from_last_print = time.time()



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
        self.list_data['ersActivated'] = True if current_frame_data[
            PacketID.CAR_STATUS].carStatusData[player_car].ersDeployMode != 0 else False
        self.list_data['tyreWear'] = current_frame_data[PacketID.CAR_DAMAGE].carDamageData[player_car].tyresWear[:]
        self.list_data['tyreSurfaceTemps'] = current_frame_data[
            PacketID.CAR_TELEMETRY].carTelemetryData[player_car].tyresSurfaceTemperature[:]


    def sessionTable(self, current_frame_data, player_car, packet):
        if Session.query.filter_by(session_id=int(str(packet.header.sessionUID)[:10])).first() is None:
            # if db.session.query(Session.session_id).filter_by(session_id=current_frame_data[PacketID.SESSION].header.sessionUID).first() is None:
            session_data = Session(
                session_id=int(str(packet.header.sessionUID)[:10]),
                track_id=TRACK_IDS[packet.trackId],
                session_type=SESSION_TYPES[packet.sessionType],
                weather=WEATHER_TYPES[packet.weather],
                formula_type=FORMULA_TYPES[packet.formula],
                isOnline=IS_ONLINE[packet.networkGame],
                # team=TEAM_IDS[current_frame_data[PacketID.PARTICIPANT].participants[player_car].teamId]
            )

            db.session.add(session_data)
            db.session.commit()
        
    def addTeam(self, packet, player_car):
        Session.query.filter_by(session_id=int(
            str(packet.header.sessionUID)[:10])).update({'team': TEAM_IDS[packet.participants[player_car].teamId]})
        db.session.commit()



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

conn = sqlite3.connect('../flask_db.db')
c = conn.cursor()




while True:

    #query the data, if the shouldrun is true, then run, if not break out of loop

    if Streaming.query.filter_by(should_run=1).first() is None:
        break
    else:
        data, addr = sock.recvfrom(PACKET_SIZE)
        packet = unpack_udp_packet(data)

        current_frame_data[PacketID(packet.header.packetId)] = packet

        any_packet = next(iter(current_frame_data.values()))
        player_car = any_packet.header.playerCarIndex

        # if time_from_last_print + 0.1 < time.time():
        try:
            use_data.fill_in_data(
                    current_frame, current_frame_data, player_car)
        except:
            current_frame = packet.header.frameIdentifier

                # use_data.write_to_json()
        # print(packet.header.sessionUID)

        
        if packet.header.packetId == 1:
            use_data.sessionTable(current_frame_data, player_car, packet)
        elif packet.header.packetId == 4:
            use_data.addTeam(packet, player_car)

    

        # if packet.header.packetId == 1:
        #     print(packet.header.sessionUID)
        #  use_data.handle_lap_data()

        # time_from_last_print = time.time()
