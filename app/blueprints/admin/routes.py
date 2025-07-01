from flask import render_template, request, redirect, url_for, flash, current_app, send_file
from flask_login import login_required, current_user
from . import bp
from app import db
from app.models.timetable import Timetable
from app.models.user import User
import pandas as pd
from datetime import datetime, date
import os

# Route name mapping from Japanese to romanized
ROUTE_NAME_MAPPING = {
    "八王子みなみ野駅": "minamino",
    "八王子駅南口": "hachioji", 
    "学生会館": "dormitory"
}

def convert_route_name(japanese_name):
    """Convert Japanese route name to romanized version"""
    return ROUTE_NAME_MAPPING.get(japanese_name, japanese_name)

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('このページにアクセスする権限がありません。', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@bp.route('/timetable')
@login_required
@admin_required
def timetable():
    timetables = Timetable.query.order_by(Timetable.route, Timetable.direction, Timetable.departure_time).all()
    return render_template('admin/timetable.html', timetables=timetables)

@bp.route('/timetable/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_timetable():
    if request.method == 'POST':
        timetable = Timetable(
            route=request.form['route'],
            direction=int(request.form['direction']),
            departure_time=datetime.strptime(request.form['departure_time'], '%H:%M:%S').time(),
            arrival_time=datetime.strptime(request.form['arrival_time'], '%H:%M:%S').time() if request.form['arrival_time'] else None,
            valid_from=datetime.strptime(request.form['valid_from'], '%Y-%m-%d').date(),
            valid_to=datetime.strptime(request.form['valid_to'], '%Y-%m-%d').date() if request.form['valid_to'] else None
        )
        db.session.add(timetable)
        db.session.commit()
        flash('時刻表を追加しました。', 'success')
        return redirect(url_for('admin.timetable'))
    return render_template('admin/add_timetable.html')

@bp.route('/timetable/<int:timetable_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_timetable(timetable_id):
    timetable = Timetable.query.get_or_404(timetable_id)
    if request.method == 'POST':
        timetable.route = request.form['route']
        timetable.direction = int(request.form['direction'])
        timetable.departure_time = datetime.strptime(request.form['departure_time'], '%H:%M:%S').time()
        timetable.arrival_time = datetime.strptime(request.form['arrival_time'], '%H:%M:%S').time() if request.form['arrival_time'] else None
        timetable.valid_from = datetime.strptime(request.form['valid_from'], '%Y-%m-%d').date()
        timetable.valid_to = datetime.strptime(request.form['valid_to'], '%Y-%m-%d').date() if request.form['valid_to'] else None
        db.session.commit()
        flash('時刻表を更新しました。', 'success')
        return redirect(url_for('admin.timetable'))
    return render_template('admin/edit_timetable.html', timetable=timetable)

@bp.route('/timetable/delete_all', methods=['POST'])
@login_required
@admin_required
def delete_all_timetables():
    Timetable.query.delete()
    db.session.commit()
    flash('すべての時刻表を削除しました。', 'success')
    return redirect(url_for('admin.timetable'))

@bp.route('/timetable/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがアップロードされていません。', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('ファイルが選択されていません。', 'danger')
            return redirect(request.url)
        
        if not file.filename.endswith('.csv'):
            flash('CSVファイルのみアップロード可能です。', 'danger')
            return redirect(request.url)
        
        try:
            df = pd.read_csv(file)
            required_columns = ['route', 'direction', 'departure_time', 'arrival_time', 'valid_from', 'valid_to']
            if not all(col in df.columns for col in required_columns):
                flash('必要なカラムが不足しています。', 'danger')
                return redirect(request.url)
            
            has_timetable_type = 'timetable_type' in df.columns
            has_is_shuttle = 'is_shuttle' in df.columns
            has_shuttle_start = 'shuttle_start' in df.columns
            has_shuttle_end = 'shuttle_end' in df.columns
            
            for _, row in df.iterrows():
                route_raw = str(row['route']) if not pd.isna(row['route']) else ''
                route = convert_route_name(route_raw)
                direction = int(row['direction']) if not pd.isna(row['direction']) else 0
                departure_time_str = str(row['departure_time']) if not pd.isna(row['departure_time']) else ''
                arrival_time_str = str(row['arrival_time']) if not pd.isna(row['arrival_time']) else ''
                valid_from_str = str(row['valid_from']) if not pd.isna(row['valid_from']) and str(row['valid_from']) != '' and str(row['valid_from']) != 'nan' else None
                valid_to_str = str(row['valid_to']) if not pd.isna(row['valid_to']) and str(row['valid_to']) != '' and str(row['valid_to']) != 'nan' else None
                
                if has_timetable_type and not pd.isna(row['timetable_type']) and str(row['timetable_type']) != '' and str(row['timetable_type']) != 'nan':
                    timetable_type = int(row['timetable_type'])
                else:
                    timetable_type = 1  # デフォルト値

                # is_shuttle処理を追加
                is_shuttle = False
                shuttle_start = None
                shuttle_end = None
                
                if has_is_shuttle and not pd.isna(row['is_shuttle']):
                    is_shuttle_value = str(row['is_shuttle']).strip()
                    is_shuttle = is_shuttle_value == '1'
                    
                    if is_shuttle:
                        if has_shuttle_start and not pd.isna(row['shuttle_start']) and str(row['shuttle_start']) != 'nan':
                            shuttle_start_str = str(row['shuttle_start'])
                            shuttle_start = datetime.strptime(shuttle_start_str, '%H:%M:%S').time()
                        
                        if has_shuttle_end and not pd.isna(row['shuttle_end']) and str(row['shuttle_end']) != 'nan':
                            shuttle_end_str = str(row['shuttle_end'])
                            shuttle_end = datetime.strptime(shuttle_end_str, '%H:%M:%S').time()

                # valid_fromが空欄・nanなら今日の日付をセット
                if not valid_from_str:
                    valid_from_date = date.today()
                else:
                    valid_from_date = datetime.strptime(valid_from_str, '%Y-%m-%d').date()

                valid_to_date = datetime.strptime(valid_to_str, '%Y-%m-%d').date() if valid_to_str else None

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
                db.session.add(timetable)
            
            db.session.commit()
            flash('時刻表のアップロードが完了しました。', 'success')
            return redirect(url_for('admin.timetable'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'アップロード中にエラーが発生しました: {str(e)}', 'danger')
            return redirect(request.url)
    
    return render_template('admin/upload.html')

@bp.route('/timetable/download')
@login_required
@admin_required
def download():
    try:
        timetables = Timetable.query.all()
        data = []
        for t in timetables:
            data.append({
                'route': t.route,
                'direction': t.direction,
                'departure_time': t.departure_time.strftime('%H:%M:%S'),
                'arrival_time': t.arrival_time.strftime('%H:%M:%S') if t.arrival_time else None,
                'valid_from': t.valid_from.strftime('%Y-%m-%d'),
                'valid_to': t.valid_to.strftime('%Y-%m-%d') if t.valid_to else None
            })
        
        df = pd.DataFrame(data)
        csv_path = os.path.join('static', 'downloads', 'timetable.csv')
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df.to_csv(csv_path, index=False)
        
        return send_file(csv_path, as_attachment=True, download_name='timetable.csv')
    
    except Exception as e:
        flash(f'ダウンロード中にエラーが発生しました: {str(e)}', 'danger')
        return redirect(url_for('admin.timetable'))

@bp.route('/timetable/template')
@login_required
@admin_required
def download_template():
    template_path = os.path.join('static', 'templates', 'timetable_template.csv')
    return send_file(template_path, as_attachment=True, download_name='timetable_template.csv')

@bp.route('/users')
@login_required
@admin_required
def user_list():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/user_list.html', users=users)

@bp.route('/users/<int:user_id>/toggle')
@login_required
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    flash(f'ユーザー {user.username} の状態を{"有効" if user.is_active else "無効"}に変更しました。', 'success')
    return redirect(url_for('admin.user_list'))

@bp.route('/users/<int:user_id>/toggle_admin')
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f'ユーザー {user.username} の管理者権限を{"付与" if user.is_admin else "削除"}しました。', 'success')
    return redirect(url_for('admin.user_list'))

@bp.route('/timetable/<int:timetable_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_timetable(timetable_id):
    timetable = Timetable.query.get_or_404(timetable_id)
    try:
        db.session.delete(timetable)
        db.session.commit()
        flash('時刻表を削除しました。', 'success')
    except Exception as e:
        flash(f'エラーが発生しました: {str(e)}', 'danger')
    return redirect(url_for('admin.timetable')) 