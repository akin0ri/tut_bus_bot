from . import bp
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        flash('ユーザー名またはパスワードが正しくありません。', 'danger')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。', 'info')
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        secret_key = request.form.get('secret_key')
        
        if User.query.filter_by(username=username).first():
            flash('このユーザー名は既に使用されています。', 'danger')
            return render_template('auth/register.html')
        
        if secret_key != current_app.config['SECRET_KEY']:
            flash('無効なシークレットキーです。', 'danger')
            return render_template('auth/register.html')
        
        user = User(username=username)
        user.set_password(password)
        user.is_admin = True
        db.session.add(user)
        db.session.commit()
        
        flash('登録が完了しました。ログインしてください。', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

# ここに認証用のルートを追加予定 