from app import db
from datetime import date, time

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(32), nullable=False)
    direction = db.Column(db.Integer, nullable=False)
    departure_time = db.Column(db.Time, nullable=False)
    arrival_time = db.Column(db.Time)
    is_shuttle = db.Column(db.Boolean, default=False)
    shuttle_start = db.Column(db.Time)
    shuttle_end = db.Column(db.Time)
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

class ExtraTimetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timetable_id = db.Column(db.Integer, db.ForeignKey('timetable.id'), nullable=False)
    special_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(128))
    timetable = db.relationship('Timetable', backref='extra_dates') 