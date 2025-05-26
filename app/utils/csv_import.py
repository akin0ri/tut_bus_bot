import csv
from app import db
from app.models.timetable import Timetable
from datetime import datetime

def import_timetable_csv(file_path: str) -> dict:
    results = {"success": 0, "failed": 0}
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                timetable = Timetable(
                    route=row['route'],
                    direction=int(row['direction']),
                    departure_time=datetime.strptime(row['departure_time'], '%H:%M').time(),
                    arrival_time=datetime.strptime(row['arrival_time'], '%H:%M').time() if row.get('arrival_time') else None,
                    is_shuttle=str(row.get('is_shuttle', '0')).strip() == '1',
                    shuttle_start=datetime.strptime(row['shuttle_start'], '%H:%M').time() if row.get('shuttle_start') else None,
                    shuttle_end=datetime.strptime(row['shuttle_end'], '%H:%M').time() if row.get('shuttle_end') else None,
                    valid_from=datetime.strptime(row['valid_from'], '%Y-%m-%d').date(),
                    valid_to=datetime.strptime(row['valid_to'], '%Y-%m-%d').date() if row.get('valid_to') else None
                )
                db.session.add(timetable)
                results["success"] += 1
            except Exception as e:
                results["failed"] += 1
                continue
        db.session.commit()
    return results 