#!/usr/bin/env python3
import csv
import io
from datetime import datetime, date
import logging

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def debug_csv_processing(csv_file_path):
    """CSVファイルの処理をデバッグする"""
    logger.info(f"CSVファイル処理開始: {csv_file_path}")
    
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        logger.info(f"ファイル内容:\n{content}")
    
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row_num, row in enumerate(reader, 1):
            logger.info(f"=== 行 {row_num} ===")
            logger.info(f"生データ: {row}")
            
            # 英語カラム名の処理をシミュレート
            if 'route' in row:
                logger.info("英語カラム名を検出")
                
                route = str(row['route']) if row['route'] is not None else ''
                direction = int(row['direction']) if row['direction'] is not None else 0
                timetable_type = int(row.get('timetable_type', 1)) if row.get('timetable_type') is not None else 1
                departure_time_str = str(row['departure_time']) if row['departure_time'] is not None else ''
                arrival_time_str = str(row['arrival_time']) if row['arrival_time'] is not None else ''
                
                # is_shuttleの詳細デバッグ
                is_shuttle_raw = row.get('is_shuttle')
                logger.info(f"is_shuttle_raw: {repr(is_shuttle_raw)} (type: {type(is_shuttle_raw)})")
                
                is_shuttle_value = str(row.get('is_shuttle', '0')).strip()
                logger.info(f"is_shuttle_value: '{is_shuttle_value}' (type: {type(is_shuttle_value)})")
                
                is_shuttle = is_shuttle_value == '1'
                logger.info(f"is_shuttle: {is_shuttle} (type: {type(is_shuttle)})")
                
                shuttle_start_str = str(row.get('shuttle_start', '')) if row.get('shuttle_start') is not None else ''
                shuttle_end_str = str(row.get('shuttle_end', '')) if row.get('shuttle_end') is not None else ''
                valid_from_str = str(row.get('valid_from', '')) if row.get('valid_from') is not None else ''
                valid_to_str = str(row.get('valid_to', '')) if row.get('valid_to') is not None else ''
                
                logger.info(f"解析結果:")
                logger.info(f"  route: {route}")
                logger.info(f"  direction: {direction}")
                logger.info(f"  timetable_type: {timetable_type}")
                logger.info(f"  departure_time_str: {departure_time_str}")
                logger.info(f"  arrival_time_str: {arrival_time_str}")
                logger.info(f"  is_shuttle: {is_shuttle}")
                logger.info(f"  shuttle_start_str: {shuttle_start_str}")
                logger.info(f"  shuttle_end_str: {shuttle_end_str}")
                logger.info(f"  valid_from_str: {valid_from_str}")
                logger.info(f"  valid_to_str: {valid_to_str}")
                
                # 時刻変換のテスト
                try:
                    departure_time = datetime.strptime(departure_time_str, '%H:%M:%S').time() if departure_time_str else None
                    arrival_time = datetime.strptime(arrival_time_str, '%H:%M:%S').time() if arrival_time_str else None
                    shuttle_start = datetime.strptime(shuttle_start_str, '%H:%M:%S').time() if shuttle_start_str else None
                    shuttle_end = datetime.strptime(shuttle_end_str, '%H:%M:%S').time() if shuttle_end_str else None
                    valid_from_date = datetime.strptime(valid_from_str, '%Y-%m-%d').date() if valid_from_str else date.today()
                    valid_to_date = datetime.strptime(valid_to_str, '%Y-%m-%d').date() if valid_to_str else None
                    
                    logger.info(f"変換後の時刻:")
                    logger.info(f"  departure_time: {departure_time}")
                    logger.info(f"  arrival_time: {arrival_time}")
                    logger.info(f"  shuttle_start: {shuttle_start}")
                    logger.info(f"  shuttle_end: {shuttle_end}")
                    logger.info(f"  valid_from_date: {valid_from_date}")
                    logger.info(f"  valid_to_date: {valid_to_date}")
                    
                except Exception as e:
                    logger.error(f"時刻変換エラー: {e}")

if __name__ == "__main__":
    debug_csv_processing('shuttle_test.csv') 