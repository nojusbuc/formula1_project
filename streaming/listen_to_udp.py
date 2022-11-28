from streaming.frame_data import UsefulData
from contextlib import closing
import sqlite3
import socket
from streaming.packets import PacketID, unpack_udp_packet
import json

def listen_to_udp(telem_obj):

    use_data = UsefulData()
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

                # adding session data to database
                if packet.header.packetId == 1:
                    use_data.sessionTable(
                        current_frame_data, player_car, packet)

                # updating session data in the database
                elif packet.header.packetId == 4:
                    use_data.updateSessionTable(packet)
                    use_data.playerTable(packet)

                # adding lap data to the database and upating player data
                elif packet.header.packetId == 2:
                    use_data.updatePlayerTable(packet)
                    use_data.lapDataTable(packet)

                # adding telemetry data to the database
                elif packet.header.packetId == 6:
                    use_data.telemetryTable(packet)
                    # telem_obj['speed'] = packet.carTelemetryData[0].speed
                    # telem_obj = {
                    #     'speed': packet.carTelemetryData[0].speed,
                    #     'throttle': packet.carTelemetryData[0].throttle,
                    #     'brake': packet.carTelemetryData[0].brake,
                    #     'gear': packet.carTelemetryData[0].gear,
                    #     'engineRPM': packet.carTelemetryData[0].engineRPM,
                    #     'drs': packet.carTelemetryData[0].drs,
                    # }
                    
                    #     return list_data
