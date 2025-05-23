# TUT Bus Bot デプロイメント手順

このドキュメントでは、TUT Bus Botのデプロイメント手順について説明します。

## 前提条件

- Python 3.10以上
- Git
- pip
- データベース（SQLite3）

## 1. リポジトリのクローン

```bash
git clone <repository-url>
cd tut_bus_bot
```

## 2. 環境設定

### 2.1 仮想環境の作成と有効化

```bash
python -m venv venv
source venv/bin/activate  # Linuxの場合
# または
.\venv\Scripts\activate  # Windowsの場合
```

### 2.2 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2.3 環境変数の設定

`.env`ファイルを作成し、以下の環境変数を設定します：

```env
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/timetable.db
JWT_SECRET_KEY=your-jwt-secret-key-here
```

## 3. データベースの初期化

```bash
flask db upgrade
```

## 4. アプリケーションの起動

### 4.1 開発環境での起動

```bash
flask run --host=0.0.0.0 --port=5050
```

### 4.2 本番環境での起動（Gunicorn使用）

```bash
gunicorn -w 4 -b 0.0.0.0:5050 wsgi:app
```

## 5. 初期設定

1. アプリケーションにアクセス（`http://localhost:5050`）
2. ユーザー登録画面（`/auth/register`）にアクセス
3. コンソールに表示される`SECRET_KEY`を使用してユーザー登録
4. 登録したユーザーでログイン

## 6. トラブルシューティング

### 6.1 データベースエラー

データベースに問題がある場合は、以下のコマンドで再初期化できます：

```bash
rm -f instance/timetable.db
flask db upgrade
```

### 6.2 環境変数の確認

環境変数が正しく設定されているか確認：

```bash
flask shell
>>> from app import create_app
>>> app = create_app()
>>> print(app.config['SECRET_KEY'])
```

## 7. セキュリティに関する注意事項

1. 本番環境では必ず強力な`SECRET_KEY`と`JWT_SECRET_KEY`を設定してください
2. `.env`ファイルはGitにコミットしないでください
3. 本番環境では`FLASK_ENV=production`を設定してください
4. 本番環境では適切なWSGIサーバー（Gunicorn等）を使用してください

## 8. バックアップ

定期的に以下のファイルをバックアップすることを推奨します：

- `instance/timetable.db`（データベースファイル）
- `.env`（環境変数ファイル）

## 9. 更新手順

アプリケーションを更新する場合は、以下の手順を実行してください：

```bash
git pull
pip install -r requirements.txt
flask db upgrade
```

## 10. 監視とログ

- アプリケーションのログは`logs/`ディレクトリに保存されます
- エラーが発生した場合は`logs/error.log`を確認してください

## 11. サポート

問題が発生した場合は、以下の情報を確認してください：

1. アプリケーションのログ
2. データベースの状態
3. 環境変数の設定
4. 依存パッケージのバージョン 