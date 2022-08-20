from extensions import db

class Session(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer)
    session_type = db.Column(db.String)
    weather = db.Column(db.String)
    formula_type = db.Column(db.String)
    isOnline = db.Column(db.Boolean)
    team = db.Column(db.String)
    players = db.relationship('Player', backref='session')


class Player(db.Model):  # points to Session
    
    player_id = db.Column(db.Integer, primary_key=True)
    session_uid = db.Column(db.Integer, db.ForeignKey(
        'session.session_id'))
    # laps_data = db.relationship('LapData', backref='player', lazy=True)
    # setups = db.relationship('Setup', backref='player', lazy=True)

class Streaming(db.Model):
    str_id = db.Column(db.Integer, primary_key=True)
    should_run = db.Column(db.Integer, primary_key=True)

# class LapData(db.Model):  # points to Car class
#     player_id = db.Column(db.Integer, db.ForeignKey(
#         'player.player_id'))
#     lap_id = db.Column(db.Integer, primary_key=True)
#     lap_time = db.Column(db.Integer)
#     is_fastest_lap = db.Column(db.Boolean)
#     sector_1_time = db.Column(db.Integer)
#     sector_2_time = db.Column(db.Integer)
#     sector_3_time = db.Column(db.Integer)
#     is_sector_1_best = db.Column(db.Boolean)
#     is_sector_2_best = db.Column(db.Boolean)
#     is_sector_3_best = db.Column(db.Boolean)
#     current_sector = db.Column(db.Integer)
#     invalidated_lap = db.Column(db.Boolean)
#     lap_number = db.Column(db.Integer)
#     pitted_during_lap = db.Column(db.Boolean)
#     grid_position = db.Column(db.Integer)
#     driverStatus = db.Column(db.String)
#     telemetry_data = db.relationship(
#         'Telemetry', backref='lap_data', lazy=True)


# class Setup(db.Model):  # points to Car class
#     player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'))
#     setup_id = db.Column(db.Integer, primary_key=True)
#     front_wing = db.Column(db.Integer)
#     rear_wing = db.Column(db.Integer)
#     on_throttle_diff = db.Column(db.Integer)
#     off_throttle_diff = db.Column(db.Integer)
#     front_camber = db.Column(db.Float)
#     rear_camber = db.Column(db.Float)
#     front_toe = db.Column(db.Float)
#     rear_toe = db.Column(db.Float)
#     front_suspension = db.Column(db.Integer)
#     rear_suspension = db.Column(db.Integer)
#     front_anti_roll = db.Column(db.Integer)
#     rear_anti_roll = db.Column(db.Integer)
#     brake_pressure = db.Column(db.Integer)
#     brake_bias = db.Column(db.Integer)
#     rl_tyre_pressure = db.Column(db.Float)
#     rr_tyre_pressure = db.Column(db.Float)
#     fl_tyre_pressure = db.Column(db.Float)
#     fr_tyre_pressure = db.Column(db.Float)
#     ballast = db.Column(db.Integer)
#     fuel_load = db.Column(db.Float)


# class Telemetry(db.Model):  # points to LapData class
#     lap_id = db.Column(db.Integer, db.ForeignKey('lap_data.lap_id'))
#     timestamp = db.Column(db.DateTime, primary_key=True)
#     speed = db.Column(db.Integer)
#     throttle = db.Column(db.Float)
#     steer = db.Column(db.Float)
#     brake = db.Column(db.Float)
#     clutch = db.Column(db.Float)
#     gear = db.Column(db.Integer)
#     engine_rpm = db.Column(db.Integer)
#     drs = db.Column(db.Boolean)


# class CarDamage(db.Model):
#     car_id = db.Column(db.Integer, db.ForeignKey('lap_data.lap_id'))
#     timestamp = db.Column(db.DateTime, primary_key=True)
#     tyre_wear = db.Column()
#     tyres_damage = db.Column()
#     fl_wing_damage = db.Column()
#     fr_wing_damage = db.Column()
#     rear_wing_damage = db.Column()
#     drs_fault = db.Column()
#     ers_fault = db.Column()
#     battery_ers = db.Column()
#     gearbox_damage = db.Column()
#     engine_damage = db.Column()

