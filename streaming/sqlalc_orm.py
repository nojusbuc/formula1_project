from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship

Model = declarative_base()

engine = create_engine('sqlite:///flask_db.db')

class SessionsTable(Model):
    __tablename__ = 'session'
    session_id = Column('session_id', Integer, primary_key=True)
    track_id = Column(Integer)
    session_type = Column(String)
    weather = Column(String)
    formula_type = Column(String)
    is_online = Column(Boolean)
    many_cars = Column(Boolean)
    active_cars = Column(Integer)
    players = relationship('Player', backref='session')

    players = relationship(
        "PlayersTable", backref="session")


class PlayersTable(Model):  # points to Session


    __tablename__ = 'player'
    player_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey(
        'session.session_id'))
    team = Column(String)
    driver = Column(String)
    player_index = Column(Integer)
    grid_position = Column(Integer)
    laps = relationship('LapsTable', backref='player')
    setups = relationship('SetupsTable', backref='setup')


class LapsTable(Model):  # points to Car class
    __tablename__ = 'lap_data'
    player_id = Column(Integer, ForeignKey(
        'player.player_id'))
    lap_id = Column(Integer, primary_key=True)
    lap_time = Column(Integer)
    is_fastest_lap = Column(Boolean)
    sector_1_time = Column(Integer)
    sector_2_time = Column(Integer)
    sector_3_time = Column(Integer)
    is_sector_1_best = Column(Boolean)
    is_sector_2_best = Column(Boolean)
    is_sector_3_best = Column(Boolean)
    current_sector = Column(Integer)
    invalidated_lap = Column(Boolean)
    lap_number = Column(Integer)
    pitted_during_lap = Column(Boolean)
    car_position = Column(Integer)
    driverStatus = Column(String)

    telemetry_data = relationship(
        'TelemetryTable', backref='lap_data')


class SetupsTable(Model):  # points to Car class
    __tablename__ = 'setup'
    player_id = Column(Integer, ForeignKey('player.player_id'))
    setup_id = Column(Integer, primary_key=True)
    front_wing = Column(Integer)
    rear_wing = Column(Integer)
    on_throttle_diff = Column(Integer)
    off_throttle_diff = Column(Integer)
    front_camber = Column(Float)
    rear_camber = Column(Float)
    front_toe = Column(Float)
    rear_toe = Column(Float)
    front_suspension = Column(Integer)
    rear_suspension = Column(Integer)
    front_anti_roll = Column(Integer)
    rear_anti_roll = Column(Integer)
    brake_pressure = Column(Integer)
    brake_bias = Column(Integer)
    rl_tyre_pressure = Column(Float)
    rr_tyre_pressure = Column(Float)
    fl_tyre_pressure = Column(Float)
    fr_tyre_pressure = Column(Float)
    ballast = Column(Integer)
    fuel_load = Column(Float)


class TelemetryTable(Model):  # points to LapData class
    __tablename__ = 'telemetry'
    lap_id = Column(Integer, ForeignKey('lap_data.lap_id'))
    player_id = Column
    timestamp = Column(DateTime, primary_key=True)
    speed = Column(Integer)
    throttle = Column(Float)
    steer = Column(Float)
    brake = Column(Float)
    clutch = Column(Float)
    gear = Column(Integer)
    engine_rpm = Column(Integer)
    drs = Column(Boolean)


# class CarDamage(Model):
#     car_id = Column(Integer, ForeignKey('lap_data.lap_id'))
#     timestamp = Column(DateTime, primary_key=True)
#     tyre_wear = Column()
#     tyres_damage = Column()
#     fl_wing_damage = Column()
#     fr_wing_damage = Column()
#     rear_wing_damage = Column()
#     drs_fault = Column()
#     ers_fault = Column()
#     battery_ers = Column()
#     gearbox_damage = Column()
#     engine_damage = Column()

class Streaming(Model):
    __tablename__ = 'streaming'
    str_id = Column(Integer, primary_key=True)
    should_run = Column(Integer)


Model.metadata.create_all(engine)
