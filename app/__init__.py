import os
from os import environ
from dotenv import load_dotenv
from flask import Flask, request, abort, Blueprint, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from app.bus_status import get_bus_status
from app.food_status import get_food_status
from .config import Config

# ログ設定
def setup_logger(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/bus_bot.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Bus Bot startup')

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'このページにアクセスするにはログインが必要です。'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ログ設定の初期化
    setup_logger(app)

    # SECRET_KEYの表示
    app.logger.info(f"現在使用中のSECRET_KEY: {app.config['SECRET_KEY']}")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    login_manager.init_app(app)

    # Blueprint登録
    from app.blueprints.api import bp as api_bp
    from app.blueprints.admin import bp as admin_bp
    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.main import bp as main_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    # set LINE channel secret and access token
    if not (access_token := environ.get("LINE_CHANNEL_ACCESS_TOKEN")):
        app.logger.error("LINE_CHANNEL_ACCESS_TOKENが設定されていません")
        raise Exception("access token is not set as an environment variable")
    if not (channel_secret := environ.get("LINE_CHANNEL_SECRET")):
        app.logger.error("LINE_CHANNEL_SECRETが設定されていません")
        raise Exception("channel secret is not set as an environment variable")

    app.logger.info("アプリケーションの初期化が完了しました")
    return app

def is_valid_secret_key(input_key: str) -> bool:
    current_app.logger.info(f"入力されたSECRET_KEY: '{input_key}'")
    secret_key = current_app.config.get('SECRET_KEY')
    if not secret_key:
        current_app.logger.error('SECRET_KEYが設定されていません')
        return False
    if input_key.strip() != secret_key:
        current_app.logger.warning(f"SECRET_KEY不一致: 入力='{input_key}', 設定='{secret_key}'")
        return False
    return True

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

from app import models
