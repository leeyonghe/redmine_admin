# Redmine Admin

[한국어](README.md) | [English](README_EN.md) | [Japanese] | [Chinese](README_ZH.md)

Redmine Adminは、Redmineプロジェクト管理システムのデータを分析・管理するためのDjangoベースのWebアプリケーションです。プロジェクト、課題、工数記録などのデータを可視化し、高度なレポート機能を備えた包括的なパフォーマンス分析を提供します。

## 🚀 主要機能

### 📊 高度なダッシュボード
- **リアルタイム統計**: 全体的なプロジェクトと課題の統計をライブ更新
- **アクティビティタイムライン**: 詳細な追跡による最近のアクティビティ履歴
- **プロジェクト概要**: プロジェクト固有の課題ステータスと進捗の可視化
- **パフォーマンス指標**: 一目で確認できる主要パフォーマンス指標（KPI）

### 📈 包括的なパフォーマンス分析
- **個人パフォーマンス**: ユーザー別の詳細な作業時間と課題処理状況
- **プロジェクトパフォーマンス**: プロジェクト固有のパフォーマンス統計とトレンド
- **チーム分析**: チームパフォーマンスの比較とベンチマーク
- **高度な指標**: 履歴データを含む平均パフォーマンス指標

### 📋 高度なレポートシステム
- **週次レポート**: 今週の課題と作業状況のトレンド分析
- **月次レポート**: 月次パフォーマンスと前月との比較
- **年次レポート**: 予測を含む包括的な年間パフォーマンス分析
- **カスタム日付範囲**: カスタム日付選択による柔軟なレポート
- **エクスポート機能**: 複数形式でのレポートエクスポート

### 👥 強化されたユーザー管理
- **Redmine統合**: シームレスなRedmineユーザー情報管理
- **セキュア認証**: 高度なログインと認証システム
- **ユーザープロファイル**: パフォーマンス履歴を含む詳細なユーザープロファイル
- **アバターサポート**: ユーザーアバターの表示と管理

### 🔍 高度な検索・フィルタリング
- **スマート検索**: 全データにわたる高度な検索機能
- **動的フィルタリング**: ステータス、優先度、担当者によるリアルタイムフィルタリング
- **日付範囲フィルター**: 柔軟な日付ベースのフィルタリングオプション

## 🛠 技術スタック

- **バックエンド**: Django 4.2.7 (LTS)
- **データベース**: MySQL 8.0.42
- **フロントエンド**: HTML5, CSS3, JavaScript (ES6+)
- **コンテナ**: Docker 20.10+ & Docker Compose 2.0+
- **環境**: django-environ 0.11.2
- **画像処理**: Pillow 10.1.0
- **データベースドライバ**: mysqlclient 2.2.0

## 📦 インストールとセットアップ

### 前提条件
- Docker 20.10+ と Docker Compose 2.0+
- Git
- 4GB以上のRAM
- 10GB以上のディスク容量

### 1. Dockerでのクイックスタート（推奨）

#### クローンと実行
```bash
# リポジトリをクローン
git clone <repository-url>
cd redmine_admin

# 全サービスを起動
docker-compose up --build -d

# サービスステータスを確認
docker-compose ps

# ログを表示
docker-compose logs -f web
```

#### サービス管理
```bash
# サービスを起動
docker-compose up -d

# サービスを停止
docker-compose down

# サービスを再起動
docker-compose restart

# 更新とリビルド
docker-compose up --build -d
```

### 2. 個別サービス管理

#### データベースのみ
```bash
# MySQLデータベースを起動
docker-compose up redmine_mysql -d

# MySQLに直接アクセス
docker-compose exec redmine_mysql mysql -u root -p
```

#### アプリケーションのみ
```bash
# Djangoアプリケーションを起動
docker-compose up web -d

# Djangoコマンドを実行
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
```

### 3. 開発環境セットアップ

#### 前提条件
- Python 3.8+
- MySQL 8.0+
- pip
- virtualenv

#### インストール手順
```bash
# 仮想環境を作成してアクティベート
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt

# 環境変数を設定
cp .env.example .env
# .envファイルをデータベース設定で編集

# データベースセットアップ
python manage.py migrate
python manage.py collectstatic --noinput

# スーパーユーザーを作成（オプション）
python manage.py createsuperuser

# 開発サーバーを実行
python manage.py runserver 0.0.0.0:8000
```

## 🌐 アクセス情報

- **Webアプリケーション**: http://localhost:8000
- **管理インターフェース**: http://localhost:8000/admin/
- **MySQLデータベース**: localhost:3310
  - データベース: redmine
  - ユーザー: root
  - パスワード: aqwsde123!
  - 文字セット: utf8

## 📁 プロジェクト構造

```
redmine_admin/
├── redmine/                 # メインDjangoアプリケーション
│   ├── models.py           # データモデル（Project, Issue, TimeEntry等）
│   ├── views.py            # ビューロジック（ダッシュボード、レポート、分析）
│   ├── urls.py             # URLルーティング設定
│   ├── admin.py            # Django管理インターフェース設定
│   ├── backends.py         # カスタム認証バックエンド
│   └── apps.py             # アプリ設定
├── templates/              # HTMLテンプレート
│   ├── base.html          # ナビゲーション付きベーステンプレート
│   ├── dashboard.html     # メインダッシュボードページ
│   ├── login.html         # 認証ページ
│   ├── performance.html   # パフォーマンス分析ページ
│   └── *_report.html      # レポートテンプレート
├── static/                 # 静的アセット
│   ├── css/               # スタイルシート
│   ├── js/                # JavaScriptファイル
│   └── images/            # 画像アセット
├── media/                  # ユーザーアップロードファイル
├── docker-compose.yml     # Docker Compose設定
├── Dockerfile             # Dockerイメージ定義
├── requirements.txt       # Python依存関係
└── manage.py             # Django管理スクリプト
```

## 📊 データモデル

### コアモデル
- **Project**: プロジェクト情報とメタデータ
- **Issue**: 完全なライフサイクル追跡を備えた課題と作業項目
- **TimeEntry**: 時間追跡と作業ログ
- **RedmineUser**: ユーザー情報とプロファイル
- **IssueStatus**: 課題ステータス定義
- **Tracker**: 課題追跡カテゴリ
- **RedmineUserAvatar**: ユーザーアバター管理

### 課題ステータスワークフロー
- **新規 (1)**: 初期課題状態
- **進行中 (2)**: アクティブ開発
- **解決済み (3)**: 課題解決完了
- **フィードバック (4)**: フィードバック/レビュー待ち
- **終了 (5)**: 課題完全完了
- **却下 (6)**: 課題却下/キャンセル

### 優先度レベル
- **低 (1)**: 低優先度課題
- **通常 (2)**: 標準優先度
- **高 (3)**: 高優先度課題
- **緊急 (4)**: 緊急課題
- **即座 (5)**: 重要課題

## 🔧 環境設定

### 必要な環境変数
プロジェクトルートに`.env`ファイルを作成：

```env
# Django設定
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SECRET_KEY=your-secret-key-here

# データベース設定
DATABASE_URL=mysql://root:aqwsde123!@localhost:3310/redmine

# オプション設定
TIME_ZONE=UTC
LANGUAGE_CODE=en-us
```

### Docker環境変数
以下はDockerで自動的に設定されます：

```env
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DATABASE_URL=mysql://root:aqwsde123!@redmine_mysql:3306/redmine
```

## 📈 使用ガイド

### 1. ダッシュボード概要
- http://localhost:8000 に移動
- リアルタイムプロジェクト統計を表示
- 最近のアクティビティとトレンドを監視
- 全機能へのクイックナビゲーションにアクセス

### 2. パフォーマンス分析
- 詳細な分析のために `/performance/` にアクセス
- 個人とチームのパフォーマンス指標を表示
- プロジェクト固有の統計を分析
- 時間経過によるパフォーマンストレンドを追跡

### 3. レポート生成
- **週次レポート**: `/weekly-report/` または `/weekly-report/<year>/<week>/`
- **月次レポート**: `/monthly-report/` または `/monthly-report/<year>/<month>/`
- **年次レポート**: `/yearly-report/` または `/yearly-report/<year>/`

### 4. ユーザー管理
- ユーザープロファイルとパフォーマンスデータにアクセス
- ユーザーアバターと連絡先情報を表示
- ユーザーアクティビティと貢献を追跡

## 🐛 トラブルシューティング

### 一般的な問題と解決策

#### 1. データベース接続問題
```bash
# MySQLコンテナステータスを確認
docker-compose ps redmine_mysql

# MySQLログを表示
docker-compose logs redmine_mysql

# データベース接続をテスト
docker-compose exec web python manage.py dbshell
```

#### 2. Djangoマイグレーション問題
```bash
# マイグレーションをリセット
docker-compose exec web python manage.py migrate --fake-initial

# 新しいマイグレーションを作成
docker-compose exec web python manage.py makemigrations

# マイグレーションを適用
docker-compose exec web python manage.py migrate
```

#### 3. 静的ファイル問題
```bash
# 静的ファイルを再収集
docker-compose exec web python manage.py collectstatic --noinput --clear

# 静的ファイルの場所を確認
docker-compose exec web python manage.py findstatic admin/css/base.css
```

#### 4. パフォーマンス問題
```bash
# コンテナリソースを確認
docker stats

# アプリケーションログを表示
docker-compose logs -f web

# サービスを再起動
docker-compose restart
```

### パフォーマンス最適化
- データベースクエリキャッシュを有効化
- 静的ファイル配信を最適化
- データベース接続プールを使用
- 適切なインデックスを実装

## 🔒 セキュリティ考慮事項

### 認証
- Redmine統合のためのカスタム認証バックエンド
- 設定可能な有効期限によるセッション管理
- パスワードハッシュ化とセキュリティ

### データ保護
- データベース接続暗号化
- 入力検証とサニタイゼーション
- SQLインジェクション防止
- XSS保護

### アクセス制御
- ロールベースアクセス制御
- ユーザー権限管理
- 監査ログ機能

## 🚀 デプロイメント

### 本番デプロイメント
```bash
# 本番環境を設定
export DJANGO_SETTINGS_MODULE=redmine_admin.settings.production

# 本番イメージをビルド
docker build -t redmine-admin:production .

# 本番設定で実行
docker-compose -f docker-compose.prod.yml up -d
```

### スケーリング考慮事項
- 高可用性のためのデータベースレプリケーション
- 複数アプリケーションインスタンスのロードバランシング
- キャッシュレイヤーの実装
- 監視とログ設定

## 🤝 貢献

貢献を歓迎します！以下の手順に従ってください：

1. **プロジェクトをフォーク**
2. **機能ブランチを作成**: `git checkout -b feature/AmazingFeature`
3. **変更をコミット**: `git commit -m 'Add some AmazingFeature'`
4. **ブランチにプッシュ**: `git push origin feature/AmazingFeature`
5. **プルリクエストを開く**

### 開発ガイドライン
- PEP 8コーディング標準に従う
- 包括的なテストを書く
- ドキュメントを更新
- 後方互換性を確保

## 📄 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 📞 サポートとコミュニティ

### ヘルプの取得
- **ドキュメント**: このREADMEとインラインコードコメントを確認
- **問題**: バグや機能リクエストの場合はGitHubでissueを作成
- **ディスカッション**: 質問やアイデアにはGitHub Discussionsを使用

### バージョン履歴
- **v2.0.0**: パフォーマンス分析とレポート機能の強化
- **v1.5.0**: ユーザーアバターサポートとUI改善を追加
- **v1.0.0**: 基本的なダッシュボードとレポートを含む初期リリース

## 🔮 ロードマップ

### 今後の機能
- [ ] リアルタイム通知
- [ ] 高度なチャートと可視化
- [ ] 外部統合のためのAPIエンドポイント
- [ ] モバイルレスポンシブデザインの改善
- [ ] 多言語サポート
- [ ] 高度なエクスポートオプション（PDF、Excel）

### 計画された改善
- [ ] パフォーマンス最適化
- [ ] セキュリティ機能の強化
- [ ] より良いエラーハンドリング
- [ ] 包括的なテストスイート

---

**Redmine Admin v2.0.0** - 高度なプロジェクト管理とパフォーマンス分析ツール

*DjangoとモダンなWeb技術で❤️と共に構築*