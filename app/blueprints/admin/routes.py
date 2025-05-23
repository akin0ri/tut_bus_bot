from . import admin_bp
from flask import render_template, redirect, url_for, request, flash, send_file, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.timetable import Timetable, ExtraTimetable
from app.models.user import User
from app import db
from app.schemas.timetable import TimetableSchema
from app.schemas.extra_timetable import ExtraTimetableSchema
from app.utils.csv_utils import import_timetable_csv, export_timetable_csv, get_csv_template
import io
import datetime

# ここに管理画面用のルートを追加予定 

@admin_bp.route('/timetable', methods=['GET'])
@jwt_required()
def timetable():
    timetables = Timetable.query.order_by(Timetable.valid_from.desc()).all()
    return render_template('admin/timetable.html', timetables=timetables)

@admin_bp.route('/timetable/edit/<int:timetable_id>', methods=['GET', 'POST'])
@jwt_required()
def edit_timetable(timetable_id):
    timetable = Timetable.query.get_or_404(timetable_id)
    if request.method == 'POST':
        # 入力値のバリデーションと更新
        timetable.route = request.form.get('route')
        timetable.direction = request.form.get('direction')
        timetable.departure_time = request.form.get('departure_time')
        timetable.arrival_time = request.form.get('arrival_time')
        timetable.valid_from = request.form.get('valid_from')
        timetable.valid_to = request.form.get('valid_to')
        db.session.commit()
        flash('時刻表を更新しました', 'success')
        return redirect(url_for('admin.timetable'))
    return render_template('admin/edit_timetable.html', timetable=timetable)

@admin_bp.route('/timetable/delete/<int:timetable_id>', methods=['POST'])
@jwt_required()
def delete_timetable(timetable_id):
    timetable = Timetable.query.get_or_404(timetable_id)
    db.session.delete(timetable)
    db.session.commit()
    flash('時刻表を削除しました', 'info')
    return redirect(url_for('admin.timetable'))

@admin_bp.route('/timetable/add', methods=['GET', 'POST'])
@jwt_required()
def add_timetable():
    if request.method == 'POST':
        # 入力値のバリデーションと追加
        new_tt = Timetable(
            route=request.form.get('route'),
            direction=request.form.get('direction'),
            departure_time=request.form.get('departure_time'),
            arrival_time=request.form.get('arrival_time'),
            valid_from=request.form.get('valid_from'),
            valid_to=request.form.get('valid_to')
        )
        db.session.add(new_tt)
        db.session.commit()
        flash('時刻表を追加しました', 'success')
        return redirect(url_for('admin.timetable'))
    return render_template('admin/add_timetable.html')

@admin_bp.route('/upload', methods=['GET', 'POST'])
@jwt_required()
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash('ファイルが選択されていません', 'danger')
            return redirect(url_for('admin.upload'))
        try:
            import_timetable_csv(file)
            flash('CSVをインポートしました', 'success')
        except Exception as e:
            flash(f'インポート失敗: {e}', 'danger')
        return redirect(url_for('admin.upload'))
    return render_template('admin/upload.html')

@admin_bp.route('/download', methods=['GET'])
@jwt_required()
def download():
    output = export_timetable_csv()
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='timetable.csv')

@admin_bp.route('/template', methods=['GET'])
@jwt_required()
def download_template():
    output = get_csv_template()
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='timetable_template.csv')

@admin_bp.route('/history', methods=['GET'])
@jwt_required()
def history():
    # 履歴管理（例: ExtraTimetableの一覧）
    extra = ExtraTimetable.query.order_by(ExtraTimetable.special_date.desc()).all()
    return render_template('admin/history.html', extra=extra)

@admin_bp.route('/user', methods=['GET'])
@jwt_required()
def user_list():
    users = User.query.all()
    return render_template('admin/user_list.html', users=users)

@admin_bp.route('/delete_all', methods=['GET', 'POST'])
@jwt_required()
def delete_all():
    if request.method == 'POST':
        ExtraTimetable.query.delete()
        Timetable.query.delete()
        User.query.delete()
        db.session.commit()
        flash('すべてのデータを削除しました', 'success')
        return redirect(url_for('admin.timetable'))
    return render_template('admin/delete_all.html') 