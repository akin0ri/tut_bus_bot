# TUT Bus Bot（リファクタリング・拡張版）

## 概要
TUT Bus Botは東京工科大学・日本工学院八王子専門学校のスクールバス時刻をLINE BotおよびWeb管理画面で提供・管理できるシステムです。

- Flaskベストプラクティスに準拠した構成
- バス時刻表はSQLiteデータベースで管理
- 管理画面から時刻表の直接編集・CSVアップロード・適用日付設定が可能
- シークレットキーによる簡易認証・ユーザー登録
- Azure Functionsまたはdocker-compose+ngrokでデプロイ可能

---

## ディレクトリ構成

```
app/
  ├── __init__.py           # アプリケーションファクトリ
  ├── config.py             # 設定
  ├── models/               # SQLAlchemyモデル
  ├── schemas/              # Marshmallowスキーマ
  ├── blueprints/           # Blueprint（api, admin, auth）
  ├── templates/            # Jinja2テンプレート
  ├── static/               # 静的ファイル
  ├── utils/                # 補助関数
  └── migrations/           # DBマイグレーション
function_app.py             # Azure Functions用
wsgi.py                     # WSGIサーバ用
infra/terraform/            # Azure用Terraformファイル
Dockerfile                  # Dockerビルド用
```

---

## セットアップ・開発手順

1. 依存パッケージのインストール
```sh
pip install -r requirements.txt
```

2. .envファイルの作成（LINE, DB, JWT, シークレットキー等を記載）

例:
```
SECRET_KEY=your-flask-secret
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///timetable.db
LINE_CHANNEL_ACCESS_TOKEN=...
LINE_CHANNEL_SECRET=...
```

3. DBマイグレーション初期化
```sh
flask db init
flask db migrate
flask db upgrade
```

4. 開発サーバ起動
```sh
flask run --host=0.0.0.0 --port=5050
```

---

## 管理画面機能
- /admin/timetable : 時刻表の一覧・直接編集・適用日付設定
- /admin/timetable/add : 新規時刻表追加
- /admin/timetable/edit/<id> : 時刻表編集
- /admin/timetable/delete/<id> : 時刻表削除
- /admin/upload : CSVファイルから時刻表一括登録
- /admin/download : 時刻表CSVダウンロード
- /admin/template : CSVテンプレートダウンロード
- /admin/history : 臨時ダイヤ・履歴管理
- /admin/user : ユーザー管理
- ログイン後のみ編集可能

---

## 認証
- /auth/register : シークレットキー入力でユーザー登録
- /auth/login : ユーザー名・パスワードでログイン
- JWT/セッションによる認証
- /auth/logout : ログアウト

---

## API
- RESTful APIはFlask-RESTfulで実装（今後拡充予定）
- JWT認証でAPI保護

---

## デプロイ
### Azure Functions
- `function_app.py`をエントリポイントに設定
- 必要なAzureリソースは`infra/terraform/`でIaC管理
- Azure App Service, DB, Storage等をTerraformで構築

#### デプロイ手順
以下のコマンドを実行して、Terraform でインフラを作成し、Flask アプリを Azure Functions にデプロイします。

```sh
# Azure CLI でログイン
az login

# Terraform でインフラ構築
cd infra
terraform init
terraform apply \
  -var="line_channel_access_token=${LINE_CHANNEL_ACCESS_TOKEN}" \
  -var="line_channel_secret=${LINE_CHANNEL_SECRET}" \
  -var="secret_key=${SECRET_KEY}" \
  -auto-approve

# アプリパッケージの作成とデプロイ
cd ..
zip -r function_package.zip host.json function_app.py HttpTrigger/ app/ requirements.txt
az functionapp deployment source config-zip \
  --resource-group tutbusbotG \
  --name tutbusbotAPP \
  --src function_package.zip
```

### docker-compose + ngrok
- `docker-compose up`でローカル起動
- ngrokでLINE Webhookを外部公開
- .envファイルで各種キー・DBパスを管理

---

## テスト
- pytestによるユニットテスト・統合テスト
- Flaskのテストクライアント利用
- テスト用DB・テスト用.envを用意

---

## その他
- DBスキーマやAPI仕様は`models/`・`schemas/`を参照
- バス時刻表の履歴管理・臨時ダイヤ適用・CSVテンプレートDL等も順次実装予定
- エラーハンドラ・ログ出力・キャッシュ・パフォーマンス最適化も順次対応

---

## お問い合わせ
不明点・バグ報告は [4kin0ri.dev@gmail.com](mailto:4kin0ri.dev@gmail.com) まで
