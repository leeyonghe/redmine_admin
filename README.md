# Redmine Admin

Redmine Admin은 Redmine 프로젝트 관리 시스템의 데이터를 분석하고 관리하기 위한 Django 기반 웹 애플리케이션입니다. 프로젝트, 이슈, 시간 기록 등의 데이터를 시각화하고 성과 분석을 제공합니다.

## 🚀 주요 기능

### 📊 대시보드
- 전체 프로젝트 및 이슈 통계
- 최근 활동 내역
- 프로젝트별 이슈 현황

### 📈 성과 분석
- 개인별 작업 시간 및 이슈 처리 현황
- 프로젝트별 성과 통계
- 평균 성과 지표

### 📋 보고서 시스템
- **주간 보고서**: 현재 주의 이슈 및 작업 현황
- **월간 보고서**: 월별 성과 및 전월 대비 비교
- **연간 보고서**: 연도별 종합 성과 분석

### 👥 사용자 관리
- Redmine 사용자 정보 관리
- 로그인 및 인증 시스템

## 🛠 기술 스택

- **Backend**: Django 4.2.7
- **Database**: MySQL 8.0
- **Frontend**: HTML, CSS, JavaScript
- **Container**: Docker & Docker Compose
- **Environment**: django-environ

## 📦 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd redmine_admin
```

### 2. Docker를 사용한 실행 (권장)

#### Docker Compose로 실행
```bash
# 컨테이너 빌드 및 실행
docker-compose up --build

# 백그라운드에서 실행
docker-compose up -d
```

#### 개별 서비스 실행
```bash
# MySQL 데이터베이스만 실행
docker-compose up redmine_mysql

# Django 애플리케이션만 실행
docker-compose up web
```

### 3. 로컬 환경에서 실행

#### 필수 요구사항
- Python 3.8+
- MySQL 8.0
- pip

#### 설치 단계
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 데이터베이스 설정

# 데이터베이스 마이그레이션
python manage.py migrate

# 정적 파일 수집
python manage.py collectstatic

# 개발 서버 실행
python manage.py runserver
```

## 🌐 접속 정보

- **웹 애플리케이션**: http://localhost:8000
- **MySQL 데이터베이스**: localhost:3310
  - 데이터베이스: redmine
  - 사용자: root
  - 비밀번호: aqwsde123!

## 📁 프로젝트 구조

```
redmine_admin/
├── redmine/                 # 메인 Django 앱
│   ├── models.py           # 데이터 모델 (Project, Issue, TimeEntry 등)
│   ├── views.py            # 뷰 로직 (대시보드, 보고서 등)
│   ├── urls.py             # URL 라우팅
│   └── admin.py            # Django 관리자 설정
├── templates/              # HTML 템플릿
│   ├── base.html          # 기본 템플릿
│   ├── dashboard.html     # 대시보드 페이지
│   ├── login.html         # 로그인 페이지
│   └── *_report.html      # 보고서 페이지들
├── static/                 # 정적 파일 (CSS, JS)
├── docker-compose.yml     # Docker Compose 설정
├── Dockerfile             # Docker 이미지 설정
└── requirements.txt       # Python 의존성
```

## 📊 데이터 모델

### 주요 모델
- **Project**: 프로젝트 정보
- **Issue**: 이슈 및 작업 항목
- **TimeEntry**: 시간 기록
- **RedmineUser**: 사용자 정보
- **IssueStatus**: 이슈 상태
- **Tracker**: 이슈 추적기

### 이슈 상태
- 신규 (1)
- 진행중 (2)
- 해결됨 (3)
- 피드백 (4)
- 종료 (5)
- 거부됨 (6)

### 우선순위
- 낮음 (1)
- 보통 (2)
- 높음 (3)
- 긴급 (4)
- 즉시 (5)

## 🔧 환경 변수

`.env` 파일에서 다음 환경 변수를 설정하세요:

```env
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DATABASE_URL=mysql://root:password@localhost:3310/redmine
```

## 📈 사용법

### 1. 대시보드 접속
- http://localhost:8000 으로 접속
- 전체 프로젝트 현황 및 최근 활동 확인

### 2. 성과 분석
- `/performance/` 페이지에서 개인별 및 프로젝트별 성과 확인
- 작업 시간, 처리된 이슈 수, 평균 성과 지표 제공

### 3. 보고서 확인
- **주간 보고서**: `/weekly-report/`
- **월간 보고서**: `/monthly-report/`
- **연간 보고서**: `/yearly-report/`

## 🐛 문제 해결

### 일반적인 문제들

1. **데이터베이스 연결 오류**
   ```bash
   # MySQL 컨테이너 상태 확인
   docker-compose ps
   
   # 로그 확인
   docker-compose logs redmine_mysql
   ```

2. **Django 마이그레이션 오류**
   ```bash
   # 컨테이너 내부에서 마이그레이션 실행
   docker-compose exec web python manage.py migrate
   ```

3. **정적 파일 문제**
   ```bash
   # 정적 파일 재수집
   docker-compose exec web python manage.py collectstatic --noinput
   ```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해 주세요.

---

**Redmine Admin** - 효율적인 프로젝트 관리와 성과 분석을 위한 도구