from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app.models import Timetable, db
from datetime import datetime
import csv
import io

admin = Blueprint('admin', __name__)

@admin.route('/timetable')
@login_required
def timetable():
    timetable_type = request.args.get('timetable_type', type=int)
    query = Timetable.query
    
    if timetable_type:
        query = query.filter_by(timetable_type=timetable_type)
    
    timetables = query.order_by(Timetable.route, Timetable.direction, Timetable.departure_time).all()
    return render_template('admin/timetable.html', timetables=timetables, timetable_type=timetable_type)

@admin.route('/timetable/add', methods=['GET', 'POST'])
@login_required
def add_timetable():
    if request.method == 'POST':
        try:
            timetable = Timetable(
                route=request.form['route'],
                direction=int(request.form['direction']),
                timetable_type=int(request.form['timetable_type']),
                departure_time=datetime.strptime(request.form['departure_time'], '%H:%M').time(),
                arrival_time=datetime.strptime(request.form['arrival_time'], '%H:%M').time() if request.form['arrival_time'] else None,
                is_shuttle=bool(request.form.get('is_shuttle')),
                shuttle_start=datetime.strptime(request.form['shuttle_start'], '%H:%M').time() if request.form.get('is_shuttle') and request.form['shuttle_start'] else None,
                shuttle_end=datetime.strptime(request.form['shuttle_end'], '%H:%M').time() if request.form.get('is_shuttle') and request.form['shuttle_end'] else None,
                valid_from=datetime.strptime(request.form['valid_from'], '%Y-%m-%d').date(),
                valid_to=datetime.strptime(request.form['valid_to'], '%Y-%m-%d').date() if request.form['valid_to'] else None
            )
            db.session.add(timetable)
            db.session.commit()
            flash('時刻表を追加しました', 'success')
            return redirect(url_for('admin.timetable'))
        except Exception as e:
            flash(f'エラーが発生しました: {str(e)}', 'error')
            return render_template('admin/add_timetable.html')
    
    return render_template('admin/add_timetable.html')

@admin.route('/timetable/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_timetable(id):
    timetable = Timetable.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            timetable.route = request.form['route']
            timetable.direction = int(request.form['direction'])
            timetable.timetable_type = int(request.form['timetable_type'])
            timetable.departure_time = datetime.strptime(request.form['departure_time'], '%H:%M').time()
            timetable.arrival_time = datetime.strptime(request.form['arrival_time'], '%H:%M').time() if request.form['arrival_time'] else None
            timetable.is_shuttle = bool(request.form.get('is_shuttle'))
            timetable.shuttle_start = datetime.strptime(request.form['shuttle_start'], '%H:%M').time() if request.form.get('is_shuttle') and request.form['shuttle_start'] else None
            timetable.shuttle_end = datetime.strptime(request.form['shuttle_end'], '%H:%M').time() if request.form.get('is_shuttle') and request.form['shuttle_end'] else None
            timetable.valid_from = datetime.strptime(request.form['valid_from'], '%Y-%m-%d').date()
            timetable.valid_to = datetime.strptime(request.form['valid_to'], '%Y-%m-%d').date() if request.form['valid_to'] else None
            
            db.session.commit()
            flash('時刻表を更新しました', 'success')
            return redirect(url_for('admin.timetable'))
        except Exception as e:
            flash(f'エラーが発生しました: {str(e)}', 'error')
    
    return render_template('admin/edit_timetable.html', timetable=timetable)

@admin.route('/timetable/<int:id>/delete', methods=['POST'])
@login_required
def delete_timetable(id):
    timetable = Timetable.query.get_or_404(id)
    try:
        db.session.delete(timetable)
        db.session.commit()
        flash('時刻表を削除しました', 'success')
    except Exception as e:
        flash(f'エラーが発生しました: {str(e)}', 'error')
    return redirect(url_for('admin.timetable'))

@admin.route('/timetable/delete_all', methods=['POST'])
@login_required
def delete_all_timetables():
    try:
        Timetable.query.delete()
        db.session.commit()
        flash('すべての時刻表を削除しました', 'success')
    except Exception as e:
        flash(f'エラーが発生しました: {str(e)}', 'error')
    return redirect(url_for('admin.timetable'))

@admin.route('/timetable/download')
@login_required
def download():
    timetables = Timetable.query.order_by(Timetable.route, Timetable.direction, Timetable.departure_time).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['路線', '方向', '種類', '出発時刻', '到着時刻', 'シャトル運行', 'シャトル開始', 'シャトル終了', '適用開始日', '適用終了日'])
    
    for t in timetables:
        writer.writerow([
            t.route_japanese,
            '大学発' if t.direction == 0 else '駅発',
            t.timetable_type_name,
            t.departure_time.strftime('%H:%M'),
            t.arrival_time.strftime('%H:%M') if t.arrival_time else '',
            'はい' if t.is_shuttle else 'いいえ',
            t.shuttle_start.strftime('%H:%M') if t.shuttle_start else '',
            t.shuttle_end.strftime('%H:%M') if t.shuttle_end else '',
            t.valid_from.strftime('%Y-%m-%d'),
            t.valid_to.strftime('%Y-%m-%d') if t.valid_to else ''
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'timetable_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@admin.route('/timetable/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルが選択されていません', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('ファイルが選択されていません', 'error')
            return redirect(request.url)
        
        if not file.filename.endswith('.csv'):
            flash('CSVファイルを選択してください', 'error')
            return redirect(request.url)
        
        try:
            stream = io.StringIO(file.stream.read().decode('utf-8-sig'))
            reader = csv.DictReader(stream)
            
            for row in reader:
                timetable = Timetable(
                    route=row['路線'],
                    direction=0 if row['方向'] == '大学発' else 1,
                    timetable_type={
                        '通常平日': 1,
                        '通常土曜日': 2,
                        '特別日': 3
                    }[row['種類']],
                    departure_time=datetime.strptime(row['出発時刻'], '%H:%M').time(),
                    arrival_time=datetime.strptime(row['到着時刻'], '%H:%M').time() if row['到着時刻'] else None,
                    is_shuttle=row['シャトル運行'] == 'はい',
                    shuttle_start=datetime.strptime(row['シャトル開始'], '%H:%M').time() if row['シャトル開始'] else None,
                    shuttle_end=datetime.strptime(row['シャトル終了'], '%H:%M').time() if row['シャトル終了'] else None,
                    valid_from=datetime.strptime(row['適用開始日'], '%Y-%m-%d').date(),
                    valid_to=datetime.strptime(row['適用終了日'], '%Y-%m-%d').date() if row['適用終了日'] else None
                )
                db.session.add(timetable)
            
            db.session.commit()
            flash('時刻表をアップロードしました', 'success')
            return redirect(url_for('admin.timetable'))
        except Exception as e:
            flash(f'エラーが発生しました: {str(e)}', 'error')
            return redirect(request.url)
    
    return render_template('admin/upload.html') 