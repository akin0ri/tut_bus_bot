from app import db
from datetime import date, time

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(32), nullable=False)  # hachioji, minamino, kamata
    direction = db.Column(db.Integer, nullable=False)  # 0: 大学発, 1: 駅発
    timetable_type = db.Column(db.Integer, nullable=False)  # 1: 通常平日, 2: 通常土曜日, 3: 特別日
    departure_time = db.Column(db.Time, nullable=False)
    arrival_time = db.Column(db.Time)
    is_shuttle = db.Column(db.Boolean, default=False)
    shuttle_start = db.Column(db.Time)
    shuttle_end = db.Column(db.Time)
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    @property
    def route_japanese(self):
        """路線名を日本語に変換"""
        route_map = {
            "hachioji": "八王子",
            "minamino": "南野",
            "kamata": "蒲田"
        }
        return route_map.get(self.route, self.route)

    @property
    def timetable_type_name(self):
        """時刻表の種類を日本語で取得"""
        type_map = {
            1: "通常平日",
            2: "通常土曜日",
            3: "特別日"
        }
        return type_map.get(self.timetable_type, "不明")

class ExtraTimetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timetable_id = db.Column(db.Integer, db.ForeignKey('timetable.id'), nullable=False)
    special_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(128))
    timetable = db.relationship('Timetable', backref='extra_dates') 