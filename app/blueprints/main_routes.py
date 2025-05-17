from flask import Blueprint, render_template_string

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return render_template_string('''
    <h2>TUT Bus Bot 管理画面へようこそ</h2>
    <ul>
        <li><a href="{{ url_for('auth.login') }}">ログイン</a></li>
        <li><a href="{{ url_for('auth.register') }}">ユーザー登録</a></li>
        <li><a href="{{ url_for('admin.timetable') }}">時刻表管理</a></li>
        <li><a href="{{ url_for('admin.upload') }}">CSVアップロード</a></li>
        <li><a href="{{ url_for('admin.history') }}">臨時ダイヤ・履歴管理</a></li>
        <li><a href="{{ url_for('admin.user_list') }}">ユーザー管理</a></li>
    </ul>
    ''') 