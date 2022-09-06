import socket
from packets import PacketID, unpack_udp_packet
import math
import time
import datetime
import json
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import sys
import os
from dattypes import *
sys.path.append('./')
# from models import Session, Player, Streaming
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

        val = cur.execute(
            f'SELECT session_id FROM session WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchone()
        if val is None:
            cur.execute(
                f'''
                INSERT INTO session 
                (session_id, track_id, session_type, weather, formula_type, is_online, many_cars) 
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
            conn.commit()
    
    def updateSessionTable(self, packet):
        active_cars_val = cur.execute(
            f'SELECT active_cars FROM session WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchone()
        if active_cars_val != '':
            cur.execute(
                f'UPDATE session SET active_cars={packet.numActiveCars} WHERE session_id={int(str(packet.header.sessionUID)[:10])}')
            conn.commit()


    
    def playerTable(self, packet):
        
            # val = cur.execute(
            #     f'SELECT player_id FROM player WHERE player_id = {int(str(packet.playerId) + str(packet.header.sessionUID)[:7])}').fetchone()
            val = cur.execute(
                f'SELECT player_id FROM player WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchall()

            for i in range(packet.numActiveCars):
                
                if len(val) == 0:

                    driver_name = 'User' if packet.participants[
                        i].driverId == 255 else DRIVER_IDS[packet.participants[i].driverId]
                    
                    cur.execute(
                        f'''INSERT INTO player 
                        (session_id, driver, player_index, team)
                        VALUES (
                            "{int(str(packet.header.sessionUID)[:10])}",
                            "{driver_name}",
                            "{i}", 
                            "{TEAM_IDS[packet.participants[i].teamId]}")
                            ''')
                    conn.commit()

    def updatePlayerTable(self, packet):
        player_ids = cur.execute(
            f'SELECT player_id FROM player WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchall()
        session_type = cur.execute(
            f'SELECT session_type FROM session WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchone()[0]
        grid_pos_val = cur.execute(
            f'SELECT grid_position FROM player WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchone()[0]
        for i in range(len(player_ids)):
            if session_type == 'Race' and grid_pos_val is None:
                cur.execute(
                    f'UPDATE player SET grid_position={packet.lapData[i].gridPosition} WHERE player_id={player_ids[i][0]}')
                conn.commit()



    def lapDataTable(self, packet):

        player_ids = cur.execute(
            f'SELECT player_id FROM player WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchall()

        for i in range(len(player_ids)):
            # lap_number = cur.execute(f'SELECT lap_number FROM lap_data WHERE lap_id=(SELECT max(lap_id) FROM lap_data WHERE player_id = {player_ids[i]})').fetchone()
            lap_number = cur.execute(
                f'SELECT lap_number FROM lap_data WHERE player_id={player_ids[i][0]} ORDER BY lap_number DESC LIMIT 1').fetchone()
            lap_number = lap_number[0] if lap_number is not None else None
# {player_ids[i]}
            if lap_number == packet.lapData[i].currentLapNum:
                #  = cur.execute(
                #     f'SELECT grid_position FROM player WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchone()[0]
                cur.execute(
                    f'UPDATE lap_data SET sector_1_time = {packet.lapData[i].sector1TimeInMS}, sector_2_time = {packet.lapData[i].sector2TimeInMS} WHERE player_id = {player_ids[i][0]} AND lap_number={lap_number}')

            elif packet.lapData[i].currentLapNum != lap_number:
                sector1_time = cur.execute(
                    f'SELECT sector_1_time FROM lap_data WHERE player_id={player_ids[i][0]} ORDER BY lap_number DESC LIMIT 1').fetchone()[0]
                sector2_time = cur.execute(
                    f'SELECT sector_1_time FROM lap_data WHERE player_id={player_ids[i][0]} ORDER BY lap_number DESC LIMIT 1').fetchone()[0]
                
                if None not in [packet.lapData[i].lastLapTimeInMS, sector1_time, sector2_time]:
                    sector3_time = packet.lapData[i].lastLapTimeInMS - sector1_time - sector2_time
                    cur.execute(
                        f'UPDATE lap_data SET lap_time = {packet.lapData[i].lastLapTimeInMS}, sector_3_time={sector3_time} WHERE player_id = {player_ids[i][0]} AND lap_number={lap_number}')

                else:
                    sector3_time = None

                cur.execute(
                    f'''INSERT INTO lap_data 
                            (player_id, lap_number, car_position)
                            VALUES (
                                "{player_ids[i][0]}",
                                "{packet.lapData[i].currentLapNum}",
                                "{packet.lapData[i].carPosition}"
                                )''')
                
                
            conn.commit()


    def setupTable():
        pass
    
    def telemetryTable():
        ct = datetime.datetime.now()
        player_ids = cur.execute(
            f'SELECT player_id FROM player WHERE session_id = {int(str(packet.header.sessionUID)[:10])}').fetchall()
        #loop through them then:
        for i in range(len(player_ids)):

            pass
            #using player id get last lap_id
            lap_id = cur.execute(
                f'SELECT lap_id FROM lap_data WHERE player_id={player_ids[i][0]} ORDER BY lap_id DESC LIMIT 1').fetchone()[0]
            # lap_id = lap_number[0] if lap_number is not None else None

            #insert into telem
        pass



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

conn = sqlite3.connect('./flask_db.db')
cur = conn.cursor()




while True:

    #query the data, if the shouldrun is true, then run, if not break out of loop

    # if Streaming.query.filter_by(should_run=1).first() is None:
    #     break
    # else:
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
            use_data.updateSessionTable(packet)
            use_data.playerTable(packet)

        elif packet.header.packetId == 2:
            use_data.updatePlayerTable(packet)
            use_data.lapDataTable(packet)

        elif packet.header.packetId == 6:
            pass

        # if packet.header.packetId == 1:
        #     print(packet.header.sessionUID)
        #  use_data.handle_lap_data()

        # time_from_last_print = time.time()
