#!/usr/bin/env python3
import csv
import io
from datetime import datetime, date
import logging

# Flaskアプリケーションのインポート
from app import create_app, db
from app.models.timetable import Timetable

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_csv_upload(csv_file_path):
    """実際のFlaskアプリケーションコンテキストでCSVアップロードをテスト"""
    app = create_app()
    
    with app.app_context():
        logger.info("CSVアップロードテスト開始")
        
        # 既存のhachioji路線データを削除
        Timetable.query.filter_by(route='hachioji').delete()
        db.session.commit()
        logger.info("既存のhachioji路線データを削除")
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                stream = io.StringIO(f.read())
                reader = csv.DictReader(stream)
                
                success_count = 0
                error_count = 0
                
                for row_num, row in enumerate(reader, 1):
                    try:
                        logger.info(f"=== 行 {row_num} ===")
                        logger.info(f"生データ: {row}")
                        
                        # 英語カラム名の処理
                        if 'route' in row:
                            logger.info("英語カラム名を検出")
                            
                            route = str(row['route']) if row['route'] is not None else ''
                            direction = int(row['direction']) if row['direction'] is not None else 0
                            timetable_type = int(row.get('timetable_type', 1)) if row.get('timetable_type') is not None else 1
                            departure_time_str = str(row['departure_time']) if row['departure_time'] is not None else ''
                            arrival_time_str = str(row['arrival_time']) if row['arrival_time'] is not None else ''
                            
                            # is_shuttleの詳細処理
                            is_shuttle_value = str(row.get('is_shuttle', '0')).strip()
                            is_shuttle = is_shuttle_value == '1'
                            logger.info(f"is_shuttle_value: '{is_shuttle_value}', is_shuttle: {is_shuttle}")
                            
                            shuttle_start_str = str(row.get('shuttle_start', '')) if row.get('shuttle_start') is not None else ''
                            shuttle_end_str = str(row.get('shuttle_end', '')) if row.get('shuttle_end') is not None else ''
                            valid_from_str = str(row.get('valid_from', '')) if row.get('valid_from') is not None else ''
                            valid_to_str = str(row.get('valid_to', '')) if row.get('valid_to') is not None else ''
                            
                            logger.info(f"解析結果: route={route}, direction={direction}, is_shuttle={is_shuttle}")
                            logger.info(f"時刻: departure={departure_time_str}, arrival={arrival_time_str}")
                            logger.info(f"シャトル: start={shuttle_start_str}, end={shuttle_end_str}")
                            logger.info(f"有効期間: from={valid_from_str}, to={valid_to_str}")
                            
                            # valid_fromが空欄の場合は今日の日付を設定
                            valid_from_date = datetime.strptime(valid_from_str, '%Y-%m-%d').date() if valid_from_str else date.today()
                            logger.info(f"valid_from_date: {valid_from_date}")
                            
                            timetable = Timetable(
                                route=route,
                                direction=direction,
                                timetable_type=timetable_type,
                                departure_time=datetime.strptime(departure_time_str, '%H:%M:%S').time() if departure_time_str else None,
                                arrival_time=datetime.strptime(arrival_time_str, '%H:%M:%S').time() if arrival_time_str else None,
                                is_shuttle=is_shuttle,
                                shuttle_start=datetime.strptime(shuttle_start_str, '%H:%M:%S').time() if shuttle_start_str else None,
                                shuttle_end=datetime.strptime(shuttle_end_str, '%H:%M:%S').time() if shuttle_end_str else None,
                                valid_from=valid_from_date,
                                valid_to=datetime.strptime(valid_to_str, '%Y-%m-%d').date() if valid_to_str else None
                            )
                            
                            logger.info(f"Timetableオブジェクト作成:")
                            logger.info(f"  route: {timetable.route}")
                            logger.info(f"  direction: {timetable.direction}")
                            logger.info(f"  is_shuttle: {timetable.is_shuttle}")
                            logger.info(f"  shuttle_start: {timetable.shuttle_start}")
                            logger.info(f"  shuttle_end: {timetable.shuttle_end}")
                            
                            db.session.add(timetable)
                            success_count += 1
                            logger.info(f"行 {row_num}: 正常に追加")
                            
                    except Exception as row_error:
                        error_count += 1
                        logger.error(f"行 {row_num} でエラー: {str(row_error)}")
                        logger.error(f"問題のある行データ: {row}")
                        continue
                
                # コミット前の確認
                logger.info("コミット前のセッション内容確認:")
                for obj in db.session.new:
                    if isinstance(obj, Timetable):
                        logger.info(f"  新規追加予定: route={obj.route}, is_shuttle={obj.is_shuttle}")
                
                db.session.commit()
                logger.info(f"アップロード完了: 成功 {success_count}件, エラー {error_count}件")
                
                # コミット後の確認
                logger.info("コミット後のDB確認:")
                timetables = Timetable.query.filter_by(route='hachioji').all()
                for t in timetables:
                    logger.info(f"  DB内容: ID={t.id}, route={t.route}, departure={t.departure_time}, is_shuttle={t.is_shuttle}, shuttle_start={t.shuttle_start}, shuttle_end={t.shuttle_end}")
                
        except Exception as e:
            logger.error(f"アップロード処理全体でエラー: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    test_csv_upload('shuttle_test.csv') 