import csv
from datetime import datetime, timedelta, timezone
import logging

logger = logging.getLogger(__name__)

def get_hachioji_bus_times(isWeekdays, now_date, direction, extraordinary=0, is_saturday=False):
    next_bus_times = []
    isShuttle = False
    shuttle_distance = None
    
    if extraordinary == 1:
        weekdays_file = "/workspace/extraordinary_time_table/1/hachioji.csv"
        holiday_file = "/workspace/extraordinary_time_table/1/hachioji.csv"
    elif extraordinary == 2:
        weekdays_file = "/workspace/extraordinary_time_table/2/hachioji.csv"
        holiday_file = "/workspace/extraordinary_time_table/2/hachioji.csv"
    elif extraordinary == 3:
        weekdays_file = "/workspace/extraordinary_time_table/3/hachioji.csv"
        holiday_file = "/workspace/extraordinary_time_table/3/hachioji.csv"
    else:
        if is_saturday:
            weekdays_file = "/workspace/app/latest_time_table/hachioji_saturday.csv"
        else:
            weekdays_file = "/workspace/app/latest_time_table/hachioji_weekdays.csv"
        holiday_file = "/workspace/app/latest_time_table/hachioji_holiday.csv"
    
    print(weekdays_file)

    if isWeekdays or is_saturday:
        with open(weekdays_file, "r") as f:
            reader = csv.reader(f)
            before_row = next(reader)

            for row in reader:
                hour, minute = row[direction].split(":")
                table_time = datetime(now_date.year, now_date.month, now_date.day, int(hour), int(minute), 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))

                if table_time > now_date:
                    # set shuttle flag
                    if before_row[0] == "1":
                        isShuttle = True
                        shuttle_distance = [before_row[1], before_row[3]]
                    
                    if row[0] != "1":
                        next_bus_times.append([row[direction], row[direction+1]])
                    else:
                        isShuttle = True
                        shuttle_distance = [row[1], row[3]]
                    if len(next_bus_times) > 5:
                        break
                else:
                    before_row = row

    else:
        with open(holiday_file, "r") as f:
            reader = csv.reader(f)
            before_row = next(reader)
            
            for row in reader:
                hour, minute = row[direction].split(":")
                table_time = datetime(now_date.year, now_date.month, now_date.day, int(hour), int(minute), 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))

                if table_time > now_date:
                    # set shuttle flag
                    if before_row[0] == "1":
                        isShuttle = True
                        shuttle_distance = [before_row[1], before_row[3]]

                    if row[0] != "1":
                        next_bus_times.append([row[direction], row[direction+1]])
                    else:
                        isShuttle = True
                        shuttle_distance = [row[1], row[3]]
                    if len(next_bus_times) > 5:
                        break
                else:
                    before_row = row

    return isShuttle, next_bus_times, shuttle_distance

def get_minamino_bus_times(isWeekdays, now_date, direction, extraordinary=0, is_saturday=False):
    next_bus_times = []
    isShuttle = False
    shuttle_distance = None
    
    if extraordinary == 1:
        weekdays_file = "/workspace/extraordinary_time_table/1/minamino.csv"
        holiday_file = "/workspace/extraordinary_time_table/1/minamino.csv"
    elif extraordinary == 2:
        weekdays_file = "/workspace/extraordinary_time_table/2/minamino.csv"
        holiday_file = "/workspace/extraordinary_time_table/2/minamino.csv"
    elif extraordinary == 3:
        weekdays_file = "/workspace/extraordinary_time_table/3/minamino.csv"
        holiday_file = "/workspace/extraordinary_time_table/3/minamino.csv"
    else:
        if is_saturday:
            weekdays_file = "/workspace/app/latest_time_table/minamino_saturday.csv"
        else:
            weekdays_file = "/workspace/app/latest_time_table/minamino_weekdays.csv"
        holiday_file = "/workspace/app/latest_time_table/minamino_holiday.csv"

    if isWeekdays or is_saturday:
        with open(weekdays_file, "r") as f:
            reader = csv.reader(f)
            before_row = next(reader)

            for row in reader:
                hour, minute = row[direction].split(":")
                table_time = datetime(now_date.year, now_date.month, now_date.day, int(hour), int(minute), 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))

                if table_time > now_date:
                    # set shuttle flag
                    if before_row[0] == "1":
                        isShuttle = True
                        shuttle_distance = [before_row[1], before_row[3]]
                    
                    if row[0] != "1":
                        next_bus_times.append([row[direction], row[direction+1]])
                    else:
                        isShuttle = True
                        shuttle_distance = [row[1], row[3]]
                    if len(next_bus_times) > 5:
                        break
                else:
                    before_row = row

    else:
        with open(holiday_file, "r") as f:
            reader = csv.reader(f)
            before_row = next(reader)
            
            for row in reader:
                hour, minute = row[direction].split(":")
                table_time = datetime(now_date.year, now_date.month, now_date.day, int(hour), int(minute), 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))

                if table_time > now_date:
                    # set shuttle flag
                    if before_row[0] == "1":
                        isShuttle = True
                        shuttle_distance = [before_row[1], before_row[3]]
                    
                    if row[0] != "1":
                        next_bus_times.append([row[direction], row[direction+1]])
                    else:
                        isShuttle = True
                        shuttle_distance = [row[1], row[3]]
                    if len(next_bus_times) > 5:
                        break
                else:
                    before_row = row

    return isShuttle, next_bus_times, shuttle_distance

def get_dormitory_bus_times(isWeekdays, now_date, direction, extraordinary=0, is_saturday=False):
    next_bus_times = []
    isShuttle = False
    shuttle_distance = None
    
    if extraordinary == 1:
        weekdays_file = "/workspace/extraordinary_time_table/1/dormitory.csv"
    elif extraordinary == 2:
        weekdays_file = "/workspace/extraordinary_time_table/2/dormitory.csv"
    elif extraordinary == 3:
        weekdays_file = "/workspace/extraordinary_time_table/3/dormitory.csv"
    else:
        if is_saturday:
            weekdays_file = "/workspace/app/latest_time_table/dormitory_saturday.csv"
        else:
            weekdays_file = "/workspace/app/latest_time_table/dormitory_weekdays.csv"

    if isWeekdays or is_saturday:
        with open(weekdays_file, "r") as f:
            reader = csv.reader(f)
            try:
                before_row = next(reader)
            except StopIteration:
                # ファイルが空の場合は空のリストを返す
                return isShuttle, next_bus_times, shuttle_distance

            for row in reader:
                hour, minute = row[direction].split(":")
                table_time = datetime(now_date.year, now_date.month, now_date.day, int(hour), int(minute), 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))

                if table_time > now_date:
                    if row[0] != "1":
                        next_bus_times.append([row[direction], row[direction+1]])
                    if len(next_bus_times) > 5:
                        break
                else:
                    before_row = row

    return isShuttle, next_bus_times, shuttle_distance

def get_bus_times_from_db(bus_type: str, direction: int, now_date: datetime):
    """
    データベースから時刻表データを取得する関数
    """
    from app import db
    from app.models.timetable import Timetable
    
    logger.info(f"時刻表データ取得開始: 路線={bus_type}, 方向={direction}, 現在時刻={now_date}")
    
    try:
        # 現在の日付に有効な時刻表を取得
        query = Timetable.query.filter(
            Timetable.route == bus_type,
            Timetable.direction == direction,
            Timetable.valid_from <= now_date.date(),
            (Timetable.valid_to >= now_date.date()) | (Timetable.valid_to == None)
        ).order_by(Timetable.departure_time)
        
        timetables = query.all()
        logger.info(f"取得した時刻表データ数: {len(timetables)}")
        
        next_bus_times = []
        isShuttle = False
        shuttle_distance = None
        
        for timetable in timetables:
            departure_time = datetime.combine(now_date.date(), timetable.departure_time)
            departure_time = departure_time.replace(tzinfo=timezone(timedelta(hours=+9), 'JST'))
            
            if departure_time > now_date:
                if timetable.is_shuttle:
                    isShuttle = True
                    shuttle_distance = [
                        timetable.shuttle_start.strftime('%H:%M') if timetable.shuttle_start else None,
                        timetable.shuttle_end.strftime('%H:%M') if timetable.shuttle_end else None
                    ]
                else:
                    next_bus_times.append([
                        timetable.departure_time.strftime('%H:%M'),
                        timetable.arrival_time.strftime('%H:%M') if timetable.arrival_time else None
                    ])
                
                if len(next_bus_times) >= 5:
                    break
        
        logger.info(f"次のバス時刻数: {len(next_bus_times)}, シャトル運行: {isShuttle}")
        return isShuttle, next_bus_times, shuttle_distance
        
    except Exception as e:
        logger.error(f"時刻表データ取得中にエラーが発生: {str(e)}")
        return False, [["error", None]], None

def format_timetable(timetable, now_date, bus_type, direction, isShuttle, shuttle_distance):
    """
    時刻表データを整形して表示用のテキストを生成する関数
    """
    logger.info(f"時刻表フォーマット開始: 路線={bus_type}, 方向={direction}")
    
    text = f"【バス運行情報 {now_date.strftime('%H:%M:%S')}現在】\n"

    if bus_type == "八王子":
        if direction == 0:
            text += "大学発 八王子駅行\n"
        else:
            text += "八王子駅発 大学行\n"
    elif bus_type == "南野":
        if direction == 0:
            text += "大学発 八王子みなみ野駅行\n"
        else:
            text += "八王子みなみ野駅発 大学行\n"
    elif bus_type == "蒲田":
        if direction == 0:
            text += "大学発 蒲田駅行\n"
        else:
            text += "蒲田駅発 大学行\n"
    text += "\n"

    if isShuttle and shuttle_distance and all(shuttle_distance):
        text += f"{shuttle_distance[0]} ~ {shuttle_distance[1]}の間はシャトル運行しています．\n\n"
        text += "↓シャトル運行外の時刻表はこちら↓\n"

    if len(timetable) == 0:
        text += "本日のバス運行は終了しました。\n"
    elif timetable[0] == "error":
        text += "エラーが発生しました。時間をおいて再度お試しください。"
    else:
        for i, time in enumerate(timetable, 1):
            text += f"{time[0]} --> {time[1] if time[1] else '終点'}\n"

    text += "\n※時刻は目安です。遅れる場合があります。"
    logger.info("時刻表フォーマット完了")
    return text

def get_last_5_bus_times(bus_type: str, direction: int, specified_datetime: datetime = None):
    """
    次の5本のバス時刻を取得する関数
    
    Args:
        bus_type (str): バス路線名（"八王子", "南野", "蒲田"）
        direction (int): 方向（0: 大学発, 1: 駅発）
        specified_datetime (datetime, optional): 指定日時（デバッグ用）
    """
    logger.info(f"バス時刻取得開始: 路線={bus_type}, 方向={direction}, 指定日時={specified_datetime}")
    
    now_date = specified_datetime if specified_datetime else datetime.now(timezone(timedelta(hours=+9), 'JST'))
    isShuttle, next_bus_times, shuttle_distance = get_bus_times_from_db(bus_type, direction, now_date)
    
    formatted_text = format_timetable(next_bus_times, now_date, bus_type, direction, isShuttle, shuttle_distance)
    logger.info("バス時刻取得完了")
    return formatted_text

# For debugging purposes
if __name__ == "__main__":
    # now_date = datetime.now(timezone(timedelta(hours=+9), 'JST'))
    now_date = datetime(2024, 7, 26, 15, 30, 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))
    isWeekdays = now_date.weekday() < 5
    direction = 2
    bus_type = "dormitory"

    # print(f"hachi->shcool : {get_hachioji_bus_times(isWeekdays, now_date, 1)}")
    # print(f"shcool->hachi : {get_hachioji_bus_times(isWeekdays, now_date, 0)}")

    # print(f"minamino->shcool : {get_minamino_bus_times(isWeekdays, now_date, 1)}")
    # print(f"shcool->minamino : {get_minamino_bus_times(isWeekdays, now_date, 0)}")

    # print(f"dormitory->shcool : {get_dormitory_bus_times(isWeekdays, now_date, 1)}")
    # print(f"shcool->dormitory : {get_dormitory_bus_times(isWeekdays, now_date, 0)}")
    
    isShuttle, timetable, shuttle_distance = get_hachioji_bus_times(isWeekdays, now_date, direction, extraordinary = 1)
    # print(format_timetable(timetable,now_date , bus_type, direction, isShuttle, shuttle_distance))
    print(get_last_5_bus_times("hachioji", 1))