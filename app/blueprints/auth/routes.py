from . import auth_bp
from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db
import datetime
import os
from dotenv import load_dotenv

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('ユーザー名とパスワードは必須です', 'danger')
            return redirect(url_for('auth.login'))
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash('ユーザー名またはパスワードが間違っています', 'danger')
            return redirect(url_for('auth.login'))
        access_token = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(hours=6))
        resp = redirect(url_for('admin.timetable'))
        set_access_cookies(resp, access_token)
        flash('ログイン成功', 'success')
        return resp
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        secret_key = request.form.get('secret_key')
        username = request.form.get('username')
        password = request.form.get('password')
        if not secret_key or not username or not password:
            flash('全ての項目を入力してください', 'danger')
            return redirect(url_for('auth.register'))
        
        # .envファイルのSECRET_KEYと比較
        load_dotenv()
        env_secret_key = os.environ.get('SECRET_KEY')
        if not env_secret_key:
            flash('システムエラーが発生しました', 'danger')
            return redirect(url_for('auth.register'))
            
        if secret_key != env_secret_key:
            flash('無効なシークレットキーです', 'danger')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(username=username).first():
            flash('既に登録済みのユーザー名です', 'danger')
            return redirect(url_for('auth.register'))
            
        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('ユーザー登録成功', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    resp = redirect(url_for('auth.login'))
    unset_jwt_cookies(resp)
    flash('ログアウトしました', 'info')
    return resp

# ここに認証用のルートを追加予定 