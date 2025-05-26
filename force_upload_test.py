#!/usr/bin/env python3
import csv
import io
from datetime import datetime, date
import logging
from werkzeug.datastructures import FileStorage

# Flaskアプリケーションのインポート
from app import create_app, db
from app.models.timetable import Timetable

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def force_upload_test():
    """管理画面のアップロード処理を強制的にテスト"""
    app = create_app()
    
    with app.app_context():
        logger.info("強制アップロードテスト開始")
        
        # 既存のhachioji路線データを削除
        Timetable.query.filter_by(route='hachioji').delete()
        db.session.commit()
        logger.info("既存のhachioji路線データを削除")
        
        # CSVファイルを読み込み
        with open('shuttle_test.csv', 'rb') as f:
            file_content = f.read()
        
        # FileStorageオブジェクトを作成（Flaskのファイルアップロードをシミュレート）
        file_storage = FileStorage(
            stream=io.BytesIO(file_content),
            filename='shuttle_test.csv',
            content_type='text/csv'
        )
        
        # 管理画面のアップロード処理を直接呼び出し
        from app.routes.admin import upload
        
        # Flaskのリクエストコンテキストをシミュレート
        with app.test_request_context('/admin/timetable/upload', method='POST', 
                                      data={'file': file_storage}):
            try:
                result = upload()
                logger.info(f"アップロード結果: {result}")
            except Exception as e:
                logger.error(f"アップロード処理でエラー: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
        
        # 結果確認
        logger.info("アップロード後のDB確認:")
        timetables = Timetable.query.filter_by(route='hachioji').all()
        for t in timetables:
            logger.info(f"  DB内容: ID={t.id}, route={t.route}, departure={t.departure_time}, is_shuttle={t.is_shuttle}, shuttle_start={t.shuttle_start}, shuttle_end={t.shuttle_end}")

if __name__ == "__main__":
    force_upload_test() 