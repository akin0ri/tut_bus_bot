import csv
from datetime import datetime, timedelta, timezone

def get_hachioji_bus_times(isWeekdays, now_date, direction):
    next_bus_times = []

    if isWeekdays:
        with open("/workspace/app/latest_time_table/hachioji_weekdays.csv", "r") as f:
            reader = csv.reader(f)

            for row in reader:
                hour, minute = row[direction].split(":")
                table_time = datetime(now_date.year, now_date.month, now_date.day, int(hour), int(minute), 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))

                if table_time > now_date:
                    next_bus_times.append(row[direction])
                    if len(next_bus_times) > 5:
                        break

    else:
        with open("/workspace/app/latest_time_table/hachioji_holiday.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                hour, minute = row[direction].split(":")
                table_time = datetime(now_date.year, now_date.month, now_date.day, int(hour), int(minute), 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))

                if table_time > now_date:
                    next_bus_times.append(row[direction])
                    if len(next_bus_times) > 5:
                        break

    return next_bus_times

def get_minamino_bus_times(isWeekdays, now_date, direction):
    next_bus_times = []

    if isWeekdays:
        with open("/workspace/app/latest_time_table/minamino_weekdays.csv", "r") as f:
            reader = csv.reader(f)

            for row in reader:
                hour, minute = row[direction].split(":")
                table_time = datetime(now_date.year, now_date.month, now_date.day, int(hour), int(minute), 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))

                if table_time > now_date:
                    next_bus_times.append(row[direction])
                    if len(next_bus_times) > 5:
                        break

    else:
        with open("/workspace/app/latest_time_table/minamino_holiday.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                hour, minute = row[direction].split(":")
                table_time = datetime(now_date.year, now_date.month, now_date.day, int(hour), int(minute), 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))

                if table_time > now_date:
                    next_bus_times.append(row[direction])
                    if len(next_bus_times) > 5:
                        break

    return next_bus_times

def get_dormitory_bus_times(isWeekdays, now_date, direction):
    next_bus_times = []

    if isWeekdays:
        with open("/workspace/app/latest_time_table/dormitory_weekdays.csv", "r") as f:
            reader = csv.reader(f)

            for row in reader:
                hour, minute = row[direction].split(":")
                table_time = datetime(now_date.year, now_date.month, now_date.day, int(hour), int(minute), 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))

                if table_time > now_date:
                    next_bus_times.append(row[direction])
                    if len(next_bus_times) > 5:
                        break

    return next_bus_times

def format_timetable(timetable, bus_type, direction):
    text = "【バス運行情報】\n\n"

    if len(timetable) == 0:
        text += "本日のバス運行は終了しました。\n"
    elif timetable[0] == "error":
        text += "エラーが発生しました。時間をおいて再度お試しください。"
    else:
        for i, time in enumerate(timetable, 1):
            text += f"{time}\n"

    text += "\n※時刻は目安です。遅れる場合があります。"

    return text

# bus_type: "hachioji" or "minamino" or "dormitory"
# direction: "up":1 or "down":0
def get_last_5_bus_times(bus_type : str, direction : int):
    now_date = datetime.now(timezone(timedelta(hours=+9), 'JST'))
    isWeekdays = now_date.weekday() < 5

    if bus_type == "hachioji":
        timetable = get_hachioji_bus_times(isWeekdays, now_date, direction)
    elif bus_type == "minamino":
        timetable = get_minamino_bus_times(isWeekdays, now_date, direction)
    elif bus_type == "dormitory":
        timetable = get_dormitory_bus_times(isWeekdays, now_date, direction)
    else:
        timetable = ["error"]

    return format_timetable(timetable, bus_type, direction)


# For debugging purposes
if __name__ == "__main__":
    now_date = datetime.now(timezone(timedelta(hours=+9), 'JST'))
    isWeekdays = now_date.weekday() < 5

    # print(f"hachi->shcool : {get_hachioji_bus_times(isWeekdays, now_date, 1)}")
    # print(f"shcool->hachi : {get_hachioji_bus_times(isWeekdays, now_date, 0)}")

    # print(f"minamino->shcool : {get_minamino_bus_times(isWeekdays, now_date, 1)}")
    # print(f"shcool->minamino : {get_minamino_bus_times(isWeekdays, now_date, 0)}")

    # print(f"dormitory->shcool : {get_dormitory_bus_times(isWeekdays, now_date, 1)}")
    # print(f"shcool->dormitory : {get_dormitory_bus_times(isWeekdays, now_date, 0)}")

    print(get_last_5_bus_times("hachioji", 0))
