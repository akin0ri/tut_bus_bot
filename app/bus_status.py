import csv
from datetime import datetime, timedelta, timezone

def get_weekday_jst(jst_time):
    english_weekday = jst_time.strftime('%A')
    
    # 曜日を英語から日本語に変換するための辞書
    weekday_translation = {
        'Monday': '月',
        'Tuesday': '火',
        'Wednesday': '水',
        'Thursday': '木',
        'Friday': '金',
        'Saturday': '土',
        'Sunday': '日'
    }
    
    # 英語の曜日を日本語に変換
    return weekday_translation[english_weekday]

def get_bus_status(num):
    text_date = datetime.now(timezone(timedelta(hours=+9), 'JST'))
    reply_text_list = f"【運行予定 {text_date.strftime('%H:%M:%S')}現在】\n\n"
    for i in range(num):
        now_date = datetime.now(timezone(timedelta(hours=+9), 'JST')) + timedelta(days=int(i))
        # now_date = datetime(2024, 9, 29, 12, 30, 0, 0, tzinfo=timezone(timedelta(hours=+9), 'JST'))
        isWeekdays = now_date.weekday() < 5

        # extraordinary setting start
        # extraordinary = 1 に該当する日付を設定
        extraordinary_1_dates = [
            datetime(2024, 10, 12, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 10, 15, tzinfo=timezone(timedelta(hours=+9), 'JST')).date()
        ]

        # extraordinary = 2 に該当する日付を設定
        extraordinary_2_dates = [
            datetime(2024, 10, 13, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 10, 14, tzinfo=timezone(timedelta(hours=+9), 'JST')).date()
        ]

        # extraordinary = 3 に該当する日付を設定
        extraordinary_3_dates = [
            datetime(2024, 10, 16, tzinfo=timezone(timedelta(hours=+9), 'JST')).date()
        ]

        # 紅華祭終了後戻す
        # if (extraordinary == 0 and now_date.weekday() == 7) or (extraordinary == 2 and now_date.weekday() == 7):
        #     return "本日は運行していません．"

        # extraordinary の値を設定
        if now_date.date() in extraordinary_1_dates:
            text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：紅華祭 臨時ダイヤ(準備等)"
        elif now_date.date() in extraordinary_2_dates:
            if isWeekdays:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：紅華祭 臨時ダイヤ"
            elif now_date.weekday() == 6:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：紅華祭 臨時ダイヤ"
            else:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：紅華祭 臨時ダイヤ"
        elif now_date.date() in extraordinary_3_dates:
            if isWeekdays:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：専門休み 臨時ダイヤ"
            elif now_date.weekday() == 6:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：専門休み 臨時ダイヤ"
            else:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：専門休み 臨時ダイヤ"
        else:
            if isWeekdays:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：通常(平日)ダイヤ"
            elif now_date.weekday() == 6:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：運行なし"
            else:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：通常(土曜)ダイヤ"

        reply_text_list += text + "\n"

    return reply_text_list
        
if __name__ == "__main__":
    print(get_bus_status(7))