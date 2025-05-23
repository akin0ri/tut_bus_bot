import os
from os import environ
from dotenv import load_dotenv
from flask import Flask, request, abort, Blueprint, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from app.bus_status import get_bus_status
from app.bus_time import get_last_5_bus_times
from app.food_status import get_food_status
from .blueprints.main_routes import main_blueprint
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_class)

    # SECRET_KEYの表示
    print(f"現在使用中のSECRET_KEY: {app.config['SECRET_KEY']}")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Blueprint登録
    from app.blueprints.api import api_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.auth import auth_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_blueprint)

    # set LINE channel secret and access token
    if not (access_token := environ.get("LINE_CHANNEL_ACCESS_TOKEN")):
        raise Exception("access token is not set as an environment variable")
    if not (channel_secret := environ.get("LINE_CHANNEL_SECRET")):
        raise Exception("channel secret is not set as an environment variable")

    # WebhookエンドポイントはBlueprintで管理
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
