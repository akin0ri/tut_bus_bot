import csv
from datetime import datetime, timedelta, timezone

def get_hachioji_bus_times(isWeekdays, now_date, direction):
    next_bus_times = []

    if isWeekdays:
        with open("/workspace/latest_time_table/hachioji_weekdays.csv", "r") as f:
            reader = csv.reader(f)

            for row in reader:
                hour, minute = row[direction].split(":")
                table_time = datetime(now_date.year, now_date.month, now_date.day, int(hour), int(minute), 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))

                if table_time > now_date:
                    next_bus_times.append(row[direction])
                    if len(next_bus_times) > 5:
                        break

    else:
        with open("/workspace/latest_time_table/hachioji_saturday.csv", "r") as f:
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
        with open("/workspace/latest_time_table/minamino_weekdays.csv", "r") as f:
            reader = csv.reader(f)

            for row in reader:
                hour, minute = row[direction].split(":")
                table_time = datetime(now_date.year, now_date.month, now_date.day, int(hour), int(minute), 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))

                if table_time > now_date:
                    next_bus_times.append(row[direction])
                    if len(next_bus_times) > 5:
                        break

    else:
        with open("/workspace/latest_time_table/minamino_saturday.csv", "r") as f:
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
        with open("/workspace/latest_time_table/dormitory_weekdays.csv", "r") as f:
            reader = csv.reader(f)

            for row in reader:
                hour, minute = row[direction].split(":")
                table_time = datetime(now_date.year, now_date.month, now_date.day, int(hour), int(minute), 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))

                if table_time > now_date:
                    next_bus_times.append(row[direction])
                    if len(next_bus_times) > 5:
                        break
    else:
        raise Exception("Dormitory bus does not run on weekends")

    return next_bus_times

# bus_type: "hachioji" or "minamino" or "dormitory"
# direction: "up":1 or "down":0
def get_last_5_bus_times(bus_type : str, direction : int):
    now_date = datetime.now(timezone(timedelta(hours=+9), 'JST'))
    isWeekdays = now_date.weekday() < 5

    if bus_type == "hachioji":
        return get_hachioji_bus_times(isWeekdays, now_date, direction)
    elif bus_type == "minamino":
        return get_minamino_bus_times(isWeekdays, now_date, direction)
    elif bus_type == "dormitory":
        return get_dormitory_bus_times(isWeekdays, now_date, direction)
    else:
        raise Exception("Invalid bus type")


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
