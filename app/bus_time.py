import csv
from datetime import datetime, timedelta, timezone

def get_hachioji_bus_times(isWeekdays, now_date, direction, extraordinary=0):
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
        weekdays_file = "/workspace/app/latest_time_table/hachioji_weekdays.csv"
        holiday_file = "/workspace/app/latest_time_table/hachioji_holiday.csv"

    if isWeekdays:
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

def get_minamino_bus_times(isWeekdays, now_date, direction, extraordinary=0):
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
        weekdays_file = "/workspace/app/latest_time_table/minamino_weekdays.csv"
        holiday_file = "/workspace/app/latest_time_table/minamino_holiday.csv"


    if isWeekdays:
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

def get_dormitory_bus_times(isWeekdays, now_date, direction, extraordinary=0):
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
        weekdays_file = "/workspace/app/latest_time_table/dormitory_weekdays.csv"

    if isWeekdays:
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

def format_timetable(timetable, now_date, bus_type, direction, isShuttle, shuttle_distance):
    text = f"【バス運行情報 {now_date.strftime('%H:%M:%S')}現在】\n"

    if bus_type == "hachioji":
        if direction == 1:
            text += "大学発 八王子駅行\n"
        else:
            text += "八王子駅発 大学行\n"
    elif bus_type == "minamino":
        if direction == 1:
            text += "大学発 みなみ野駅行\n"
        else:
            text += "みなみ野駅発 大学行\n"
    elif bus_type == "dormitory":
        if direction == 1:
            text += "大学発 学生寮行\n"
        else:
            text += "学生寮発 大学行\n"
    text += "\n"

    if isShuttle:
        text += f"{shuttle_distance[0]} ~ {shuttle_distance[1]}の間はシャトル運行しています．\n\n"
        text += "↓シャトル運行外の時刻表はこちら↓\n"

    if len(timetable) == 0:
        text += "本日のバス運行は終了しました。\n"
    elif timetable[0] == "error":
        text += "エラーが発生しました。時間をおいて再度お試しください。"
    else:
        for i, time in enumerate(timetable, 1):
            text += f"{time[0]} --> {time[1]}\n"

    text += "\n※時刻は目安です。遅れる場合があります。"

    return text

# bus_type: "hachioji" or "minamino" or "dormitory"
# direction: "up":1 or "down":0
def get_last_5_bus_times(bus_type : str, direction : int):
    now_date = datetime.now(timezone(timedelta(hours=+9), 'JST'))
    isWeekdays = now_date.weekday() < 5
    
    # extraordinary setting start
    # extraordinary = 1 に該当する日付を設定
    extraordinary_1_dates = [
        datetime(2024, 7, 27, tzinfo=jst).date(),
        datetime(2024, 7, 28, tzinfo=jst).date(),
        datetime(2024, 8, 3, tzinfo=jst).date(),
        datetime(2024, 8, 4, tzinfo=jst).date(),
        datetime(2024, 8, 17, tzinfo=jst).date(),
        datetime(2024, 8, 18, tzinfo=jst).date(),
        datetime(2024, 8, 19, tzinfo=jst).date(),
        datetime(2024, 8, 24, tzinfo=jst).date(),
        datetime(2024, 8, 25, tzinfo=jst).date(),
        datetime(2024, 9, 1, tzinfo=jst).date(),
        datetime(2024, 9, 16, tzinfo=jst).date()
    ]

    # extraordinary = 2 の条件: 2024年8月7日〜9月10日（除外日を除く）かつ月〜金曜日のみ
    start_date_2 = datetime(2024, 8, 7, tzinfo=jst).date()
    end_date_2 = datetime(2024, 9, 10, tzinfo=jst).date()
    excluded_periods_2 = [
        (datetime(2024, 8, 10, tzinfo=jst).date(), datetime(2024, 8, 18, tzinfo=jst).date()),
        (datetime(2024, 8, 21, tzinfo=jst).date(), datetime(2024, 8, 25, tzinfo=jst).date())
    ]

    extraordinary_2_dates = []
    current_date = start_date_2
    while current_date <= end_date_2:
        if (current_date.weekday() < 5 and  # 月〜金曜日
            not any(start <= current_date <= end for start, end in excluded_periods_2)):
            extraordinary_2_dates.append(current_date)
        current_date += timedelta(days=1)

    # extraordinary = 3 の条件: 2024年8月31日・9月7日
    extraordinary_3_dates = [
        datetime(2024, 8, 31, tzinfo=jst).date(),
        datetime(2024, 9, 7, tzinfo=jst).date()
    ]

    # extraordinary の値を設定
    if now_date.date() in extraordinary_3_dates:
        extraordinary = 3
    elif now_date.date() in extraordinary_1_dates:
        extraordinary = 1
    elif now_date.date() in extraordinary_2_dates:
        extraordinary = 2
    else:
        extraordinary = 0
    # extraordinary setting end
    
    if bus_type == "hachioji":
        isShuttle, timetable, shuttle_distance = get_hachioji_bus_times(isWeekdays, now_date, direction, extraordinary)
    elif bus_type == "minamino":
        isShuttle, timetable, shuttle_distance = get_minamino_bus_times(isWeekdays, now_date, direction, extraordinary)
    elif bus_type == "dormitory":
        isShuttle, timetable, shuttle_distance = get_dormitory_bus_times(isWeekdays, now_date, direction, extraordinary)
    else:
        isShuttle, timetable, shuttle_distance = ["error"]
        
        
    if len(timetable) == 0:
        return "本日の運行は終了しました。"
    if now_date.weekday() == 6 and extraordinary == 0:
        return "本日は運行していません。"
    
    return format_timetable(timetable,now_date , bus_type, direction, isShuttle, shuttle_distance)



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