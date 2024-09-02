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
    reply_text_list = f"【運行予定 {text_date.strftime('%H:%M:%S')}現在】\n】\n\n"
    for i in range(num):
        now_date = datetime.now(timezone(timedelta(hours=+9), 'JST')) + timedelta(days=int(i))
        
        # extraordinary setting start
        # extraordinary = 1 に該当する日付を設定
        extraordinary_1_dates = [
            datetime(2024, 7, 27, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 7, 28, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 3, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 4, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 17, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 18, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 19, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 24, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 25, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 9, 1, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 9, 16, tzinfo=timezone(timedelta(hours=+9), 'JST')).date()
        ]

        # extraordinary = 2 の条件: 2024年8月7日〜9月10日（除外日を除く）かつ月〜金曜日のみ
        extraordinary_2_dates = [
            datetime(2024, 8, 7, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 8, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 9, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 19, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 20, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 26, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 27, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 28, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 8, 29, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 9, 2, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 9, 3, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 9, 4, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 9, 5, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 9, 6, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 9, 9, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 9, 10, tzinfo=timezone(timedelta(hours=+9), 'JST')).date()
        ]

        # extraordinary = 3 の条件: 2024年8月31日・9月7日
        extraordinary_3_dates = [
            datetime(2024, 8, 31, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(),
            datetime(2024, 9, 7, tzinfo=timezone(timedelta(hours=+9), 'JST')).date()
        ]

        # extraordinary = 4 の条件: 2024年8月10日～18日、8月21日～25日
        extraordinary_4_periods = [
            (datetime(2024, 8, 10, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(), datetime(2024, 8, 18, tzinfo=timezone(timedelta(hours=+9), 'JST')).date()),
            (datetime(2024, 8, 21, tzinfo=timezone(timedelta(hours=+9), 'JST')).date(), datetime(2024, 8, 25, tzinfo=timezone(timedelta(hours=+9), 'JST')).date())
        ]
        print(now_date)

        # extraordinary の値を設定
        if now_date.date() in extraordinary_3_dates:
            text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：臨時時刻表(土曜)での運行"
        elif now_date.date() in extraordinary_1_dates:
            text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：臨時時刻(オーキャンなど)での運行"
        elif now_date.date() in extraordinary_2_dates:
            text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：臨時時刻(平日)での運行"
        elif any(start <= now_date.date() <= end for start, end in extraordinary_4_periods):
            text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：運行なし"
        else:
            if now_date.weekday() == 6:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：運行なし"
            else:
                text = f"{now_date.month}月{now_date.day}日({get_weekday_jst(now_date)})：通常時刻での運行"            
            
        reply_text_list += text + "\n"

    reply_text_list += "詳しいバス運行情報は公式サイトをご確認ください。(https://www.teu.ac.jp/campus/access/006644.html)"
    return reply_text_list
        
if __name__ == "__main__":
    print(get_bus_status(7))