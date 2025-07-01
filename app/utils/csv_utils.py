import io
import csv
from app import db
from app.models.timetable import Timetable
from datetime import datetime

# Route name mapping from Japanese to romanized
ROUTE_NAME_MAPPING = {
    "八王子みなみ野駅": "minamino",
    "八王子駅南口": "hachioji", 
    "学生会館": "dormitory"
}

def convert_route_name(japanese_name):
    """Convert Japanese route name to romanized version"""
    return ROUTE_NAME_MAPPING.get(japanese_name, japanese_name)

def import_timetable_csv(file) -> None:
    stream = io.StringIO(file.stream.read().decode('utf-8'))
    reader = csv.DictReader(stream)
    for row in reader:
        # ガード節で空欄対応
        departure_time = (
            datetime.strptime(row['departure_time'].strip(), '%H:%M:%S').time()
            if row['departure_time'] and row['departure_time'].strip() else None
        )
        arrival_time = (
            datetime.strptime(row['arrival_time'].strip(), '%H:%M:%S').time()
            if row.get('arrival_time') and row['arrival_time'].strip() else None
        )
        valid_from = (
            datetime.strptime(row['valid_from'].strip(), '%Y-%m-%d').date()
            if row['valid_from'] and row['valid_from'].strip() else None
        )
        valid_to = (
            datetime.strptime(row['valid_to'].strip(), '%Y-%m-%d').date()
            if row.get('valid_to') and row['valid_to'].strip() else None
        )
        timetable = Timetable(
            route=convert_route_name(row['route']),
            direction=int(row['direction']),
            departure_time=departure_time,
            arrival_time=arrival_time,
            valid_from=valid_from,
            valid_to=valid_to
        )
        db.session.add(timetable)
    db.session.commit()

def export_timetable_csv() -> io.BytesIO:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['id', 'route', 'direction', 'departure_time', 'arrival_time', 'valid_from', 'valid_to'])
    for t in Timetable.query.all():
        writer.writerow([
            t.id, t.route, t.direction, t.departure_time, t.arrival_time, t.valid_from, t.valid_to
        ])
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    return mem

def get_csv_template() -> io.BytesIO:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['route', 'direction', 'departure_time', 'arrival_time', 'valid_from', 'valid_to'])
    writer.writerow(['A', 1, '08:00:00', '08:30:00', '2024-04-01', '2024-09-30'])
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    return mem 