import socket
# from packets import PacketID, unpack_udp_packet
from streaming.packets import PacketID, unpack_udp_packet

import math
import time
import datetime
import json
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import sys
import os

# from dattypes import *
from streaming.dattypes import *
# from models import Session, Player, Streaming

# sessions = db.session.query.order_by(UserSession.session_uid)

class UsefulData():

    
    def __init__(self, cur=None, conn=None):
        
        self.list_data = {
            # loop through every frame? add frame as key?
            'speed': None,
            'throttle': None,
            'brake': None,
            'gear': None,
            'engineRPM': None,
            'drs': None,
            # 'tyreWear': None,
            # 'carPosition': None,
            # 'lastLapTime': None,
            # 'bestLapTime': None,
            # 'sector1Time': None,
            # 'sector2Time': None,
            # 'ersActivated': None,
            # 'tyreSurfaceTemps': None,
        }


        self.conn = conn
        self.cur = cur
    
    def print_object(self):
        # print(self.x)
        # print(UsefulData.list_data)
        return self.list_data

    def sessionTable(self, current_frame_data, player_car, packet):

        val = self.cur.execute(
            f'SELECT session_id FROM session WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchone()
        if val is None:
            self.cur.execute(
                f'''
                INSERT INTO session
                (session_id, track_id, session_type,
                 weather, formula_type, is_online, many_cars)
                VALUES
                (
                    "{int(str(packet.header.sessionUID)[:10])}",
                    "{(TRACK_IDS[packet.trackId])}",
                    "{SESSION_TYPES[packet.sessionType]}",
                    "{WEATHER_TYPES[packet.weather]}",
                    "{FORMULA_TYPES[packet.formula]}",
                    "{packet.networkGame}",
                    "{0 if (SESSION_TYPES[packet.sessionType] in ['Time Trial', 'unknown']) else 1}"
                    )''')
            self.conn.commit()

    def updateSessionTable(self, packet):
        active_cars_val = self.cur.execute(
            f'SELECT active_cars FROM session WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchone()
        if active_cars_val != '':
            self.cur.execute(
                f'UPDATE session SET active_cars={packet.numActiveCars} WHERE session_id={int(str(packet.header.sessionUID)[:10])}')
            self.conn.commit()

    def playerTable(self, packet):

        val = self.cur.execute(
            f'SELECT player_id FROM player WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchall()

        for i in range(packet.numActiveCars):

            if len(val) == 0:

                driver_name = 'User' if packet.participants[
                    i].driverId == 255 else DRIVER_IDS[packet.participants[i].driverId]

                self.cur.execute(
                    f'''INSERT INTO player
                        (session_id, driver, player_index, team)
                        VALUES (
                            "{int(str(packet.header.sessionUID)[:10])}",
                            "{driver_name}",
                            "{i}",
                            "{TEAM_IDS[packet.participants[i].teamId]}")
                            ''')
                self.conn.commit()

    def updatePlayerTable(self, packet):
        player_ids = self.cur.execute(
            f'SELECT player_id FROM player WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchall()
        session_type = self.cur.execute(
            f'SELECT session_type FROM session WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchone()[0] if self.cur.execute(
            f'SELECT session_type FROM session WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchone() is not None else None
        grid_pos_val = self.cur.execute(
            f'SELECT grid_position FROM player WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchone()
        for i in range(len(player_ids)):
            if session_type == 'Race' and grid_pos_val is None:
                self.cur.execute(
                    f'UPDATE player SET grid_position={packet.lapData[i].gridPosition} WHERE player_id={player_ids[i][0]}')
                self.conn.commit()

    def lapDataTable(self, packet):

        player_ids = self.cur.execute(
            f'SELECT player_id FROM player WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchall()

        for i in range(len(player_ids)):
            # lap_number = self.cur.execute(f'SELECT lap_number FROM lap_data WHERE lap_id=(SELECT max(lap_id) FROM lap_data WHERE player_id = {player_ids[i]})').fetchone()
            lap_number = self.cur.execute(
                f'SELECT lap_number FROM lap_data WHERE player_id={player_ids[i][0]} ORDER BY lap_number DESC LIMIT 1').fetchone()
            lap_number = lap_number[0] if lap_number is not None else None
            if lap_number == packet.lapData[i].currentLapNum:
                self.cur.execute(
                    f'''UPDATE lap_data SET sector_1_time = {packet.lapData[i].sector1TimeInMS}, sector_2_time = {packet.lapData[i].sector2TimeInMS}
                     WHERE player_id = {player_ids[i][0]} AND lap_number={lap_number}''')
            elif packet.lapData[i].currentLapNum != lap_number:
                sector1_time = self.cur.execute(
                    f'SELECT sector_1_time FROM lap_data WHERE player_id={player_ids[i][0]} ORDER BY lap_number DESC LIMIT 1').fetchone()
                sector2_time = self.cur.execute(
                    f'SELECT sector_1_time FROM lap_data WHERE player_id={player_ids[i][0]} ORDER BY lap_number DESC LIMIT 1').fetchone()
                if None not in [packet.lapData[i].lastLapTimeInMS, sector1_time, sector2_time]:
                    sector3_time = packet.lapData[i].lastLapTimeInMS - \
                        sector1_time[0] - sector2_time[0]
                    self.cur.execute(
                        f'UPDATE lap_data SET lap_time = {packet.lapData[i].lastLapTimeInMS}, sector_3_time={sector3_time} WHERE player_id = {player_ids[i][0]} AND lap_number={lap_number}')
                else:
                    sector3_time = None
                self.cur.execute(
                    f'''INSERT INTO lap_data
                            (player_id, lap_number, car_position)
                            VALUES (
                                "{player_ids[i][0]}",
                                "{packet.lapData[i].currentLapNum}",
                                "{packet.lapData[i].carPosition}"
                                )''')
            self.conn.commit()

    def setupTable():
        pass

    def telemetryTable(self, packet):
        ct = datetime.datetime.now()
        player_ids = self.cur.execute(
            f'SELECT player_id FROM player WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchall()
        # loop through them then:
        for i in range(len(player_ids)):
            # using player id get last lap_id
            lap_id = self.cur.execute(
                f'SELECT lap_id FROM lap_data WHERE player_id={player_ids[i][0]} ORDER BY lap_id DESC LIMIT 1').fetchone()
            # insert into telem
            if lap_id is not None:
                self.cur.execute(
                    f'''INSERT INTO telemetry
                                (lap_id, timestamp, speed, throttle, steer,
                                brake, clutch, gear, engine_rpm, drs)
                                VALUES (
                                    "{lap_id[0]}",
                                    "{ct}",
                                    "{packet.carTelemetryData[i].speed}",
                                    "{packet.carTelemetryData[i].throttle}",
                                    "{packet.carTelemetryData[i].steer}",
                                    "{packet.carTelemetryData[i].brake}",
                                    "{packet.carTelemetryData[i].clutch}",
                                    "{packet.carTelemetryData[i].gear}",
                                    "{packet.carTelemetryData[i].engineRPM}",
                                    "{packet.carTelemetryData[i].drs}"
                                )''')
        self.conn.commit()
        self.list_data = {
            'speed': packet.carTelemetryData[i].speed,
            'throttle': packet.carTelemetryData[i].throttle,
            'brake': packet.carTelemetryData[i].brake,
            'gear': packet.carTelemetryData[i].gear,
            'engineRPM': packet.carTelemetryData[i].engineRPM,
            'drs': packet.carTelemetryData[i].drs,
        }
        # return self.list_data



# try:

#     SERVER = socket.gethostbyname(socket.gethostname())
#     PORT = 20777

#     PACKET_SIZE = 2048

#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     sock.bind((SERVER, PORT))

#     current_frame = None
#     current_frame_data = {}

#     use_data = UsefulData()

#     time_from_last_print = time.time()

#     conn = sqlite3.connect('./flask_db.db')
#     cur = conn.cursor()

    
#     while True:
        
#         should_run = self.cur.execute(
#             f'SELECT should_run FROM streaming WHERE should_run = 1').fetchone()
#         if should_run is not None:
#             data, addr = sock.recvfrom(PACKET_SIZE)
#             packet = unpack_udp_packet(data)

#             current_frame_data[PacketID(packet.header.packetId)] = packet

#             any_packet = next(iter(current_frame_data.values()))
#             player_car = any_packet.header.playerCarIndex

#             current_frame = packet.header.frameIdentifier
#             # if time_from_last_print + 0.1 < time.time()

#             if packet.header.packetId == 1:
#                 use_data.sessionTable(current_frame_data, player_car, packet)
#             elif packet.header.packetId == 4:
#                 use_data.updateSessionTable(packet)
#                 use_data.playerTable(packet)

#             elif packet.header.packetId == 2:
#                 use_data.updatePlayerTable(packet)
#                 use_data.lapDataTable(packet)

#             elif packet.header.packetId == 6:
#                 use_data.telemetryTable(packet)

#                 # if packet.header.packetId == 1:
#                 #     print(packet.header.sessionUID)
#                 #  use_data.handle_lap_data()

#                 # time_from_last_print = time.time()
# except KeyboardInterrupt:
#     conn.close()
#     print('ended')