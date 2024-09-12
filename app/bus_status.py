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
            datetime(2024, 9, 16, tzinfo=timezone(timedelta(hours=+9), 'JST')).date()
        ]

        # extraordinary = 2 の条件: 2024年9月11日(水) ～ 9月21日(土)
        extraordinary_2_start = datetime(2024, 9, 11, tzinfo=timezone(timedelta(hours=+9), 'JST')).date()
        extraordinary_2_end = datetime(2024, 9, 21, tzinfo=timezone(timedelta(hours=+9), 'JST')).date()

        # extraordinary の値を設定
        if now_date.date() in extraordinary_1_dates:
            text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：臨時(オーキャン等)ダイヤ"
        elif extraordinary_2_start <= now_date.date() <= extraordinary_2_end:
            if isWeekdays:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：長期休暇(平日)ダイヤ"
            elif now_date.weekday() == 6:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：運行なし"
            else:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：長期休暇(土曜)ダイヤ"
        else:
            if isWeekdays:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：通常(平日)ダイヤ"
            elif now_date.weekday() == 6:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：運行なし"
            else:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：通常(土曜)ダイヤ"

        reply_text_list += text + "\n"

    reply_text_list += "\n詳しいバス運行情報は公式サイトをご確認ください。(https://www.teu.ac.jp/campus/access/006644.html)"
    return reply_text_list
        
if __name__ == "__main__":
    print(get_bus_status(7))