#!/usr/bin/env python3
import pandas as pd
from datetime import datetime, date
import logging

# Flaskアプリケーションのインポート
from app import create_app, db
from app.models.timetable import Timetable

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_blueprint_upload():
    """修正されたBlueprint管理画面のアップロード処理をテスト"""
    app = create_app()
    
    with app.app_context():
        logger.info("Blueprint管理画面アップロードテスト開始")
        
        # 既存のhachioji路線データを削除
        Timetable.query.filter_by(route='hachioji').delete()
        db.session.commit()
        logger.info("既存のhachioji路線データを削除")
        
        # CSVファイルを読み込み（Blueprint管理画面と同じ処理）
        try:
            df = pd.read_csv('shuttle_test.csv')
            logger.info(f"CSVファイル読み込み完了: {len(df)}行")
            logger.info(f"カラム: {list(df.columns)}")
            
            required_columns = ['route', 'direction', 'departure_time', 'arrival_time', 'valid_from', 'valid_to']
            if not all(col in df.columns for col in required_columns):
                logger.error("必要なカラムが不足しています")
                return
            
            has_timetable_type = 'timetable_type' in df.columns
            has_is_shuttle = 'is_shuttle' in df.columns
            has_shuttle_start = 'shuttle_start' in df.columns
            has_shuttle_end = 'shuttle_end' in df.columns
            
            logger.info(f"has_timetable_type: {has_timetable_type}")
            logger.info(f"has_is_shuttle: {has_is_shuttle}")
            logger.info(f"has_shuttle_start: {has_shuttle_start}")
            logger.info(f"has_shuttle_end: {has_shuttle_end}")
            
            for index, row in df.iterrows():
                logger.info(f"=== 行 {index + 1} ===")
                logger.info(f"生データ: {dict(row)}")
                
                route = str(row['route']) if not pd.isna(row['route']) else ''
                direction = int(row['direction']) if not pd.isna(row['direction']) else 0
                departure_time_str = str(row['departure_time']) if not pd.isna(row['departure_time']) else ''
                arrival_time_str = str(row['arrival_time']) if not pd.isna(row['arrival_time']) else ''
                valid_from_str = str(row['valid_from']) if not pd.isna(row['valid_from']) and str(row['valid_from']) != '' and str(row['valid_from']) != 'nan' else None
                valid_to_str = str(row['valid_to']) if not pd.isna(row['valid_to']) and str(row['valid_to']) != '' and str(row['valid_to']) != 'nan' else None
                
                if has_timetable_type and not pd.isna(row['timetable_type']) and str(row['timetable_type']) != '' and str(row['timetable_type']) != 'nan':
                    timetable_type = int(row['timetable_type'])
                else:
                    timetable_type = 1  # デフォルト値

                # is_shuttle処理
                is_shuttle = False
                shuttle_start = None
                shuttle_end = None
                
                if has_is_shuttle and not pd.isna(row['is_shuttle']):
                    is_shuttle_value = str(row['is_shuttle']).strip()
                    logger.info(f"is_shuttle_value: '{is_shuttle_value}' (type: {type(is_shuttle_value)})")
                    is_shuttle = is_shuttle_value == '1'
                    logger.info(f"is_shuttle: {is_shuttle}")
                    
                    if is_shuttle:
                        if has_shuttle_start and not pd.isna(row['shuttle_start']) and str(row['shuttle_start']) != 'nan':
                            shuttle_start_str = str(row['shuttle_start'])
                            logger.info(f"shuttle_start_str: {shuttle_start_str}")
                            shuttle_start = datetime.strptime(shuttle_start_str, '%H:%M:%S').time()
                        
                        if has_shuttle_end and not pd.isna(row['shuttle_end']) and str(row['shuttle_end']) != 'nan':
                            shuttle_end_str = str(row['shuttle_end'])
                            logger.info(f"shuttle_end_str: {shuttle_end_str}")
                            shuttle_end = datetime.strptime(shuttle_end_str, '%H:%M:%S').time()

                # valid_fromが空欄・nanなら今日の日付をセット
                if not valid_from_str:
                    valid_from_date = date.today()
                else:
                    valid_from_date = datetime.strptime(valid_from_str, '%Y-%m-%d').date()

                valid_to_date = datetime.strptime(valid_to_str, '%Y-%m-%d').date() if valid_to_str else None

                logger.info(f"解析結果: route={route}, direction={direction}, is_shuttle={is_shuttle}")
                logger.info(f"時刻: departure={departure_time_str}, arrival={arrival_time_str}")
                logger.info(f"シャトル: start={shuttle_start}, end={shuttle_end}")
                logger.info(f"有効期間: from={valid_from_date}, to={valid_to_date}")

                timetable = Timetable(
                    route=route,
                    direction=direction,
                    timetable_type=timetable_type,
                    departure_time=datetime.strptime(departure_time_str, '%H:%M:%S').time() if departure_time_str and departure_time_str != 'nan' else None,
                    arrival_time=datetime.strptime(arrival_time_str, '%H:%M:%S').time() if arrival_time_str and arrival_time_str != 'nan' else None,
                    is_shuttle=is_shuttle,
                    shuttle_start=shuttle_start,
                    shuttle_end=shuttle_end,
                    valid_from=valid_from_date,
                    valid_to=valid_to_date
                )
                
                logger.info(f"Timetableオブジェクト作成:")
                logger.info(f"  route: {timetable.route}")
                logger.info(f"  direction: {timetable.direction}")
                logger.info(f"  is_shuttle: {timetable.is_shuttle} (type: {type(timetable.is_shuttle)})")
                logger.info(f"  shuttle_start: {timetable.shuttle_start}")
                logger.info(f"  shuttle_end: {timetable.shuttle_end}")
                logger.info(f"  departure_time: {timetable.departure_time}")
                logger.info(f"  arrival_time: {timetable.arrival_time}")
                
                db.session.add(timetable)
            
            db.session.commit()
            logger.info("アップロード完了")
            
            # コミット後の確認
            logger.info("コミット後のDB確認:")
            timetables = Timetable.query.filter_by(route='hachioji').all()
            for t in timetables:
                logger.info(f"  DB内容: ID={t.id}, route={t.route}, departure={t.departure_time}, is_shuttle={t.is_shuttle}, shuttle_start={t.shuttle_start}, shuttle_end={t.shuttle_end}")
            
        except Exception as e:
            logger.error(f"アップロード処理でエラー: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            db.session.rollback()

if __name__ == "__main__":
    test_blueprint_upload() 