# Redmine Admin

[한국어] | [English](README_EN.md) | [Japanese](README_JP.md) | [Chinese](README_ZH.md)

Redmine Admin은 Redmine 프로젝트 관리 시스템의 데이터를 분석하고 관리하기 위한 Django 기반 웹 애플리케이션입니다. 프로젝트, 이슈, 시간 기록 등의 데이터를 시각화하고 고급 성과 분석 및 보고서 기능을 제공합니다.

## 🚀 주요 기능

### 📊 고급 대시보드
- **실시간 통계**: 전체 프로젝트 및 이슈 통계의 실시간 업데이트
- **활동 타임라인**: 상세한 추적이 가능한 최근 활동 내역
- **프로젝트 개요**: 프로젝트별 이슈 현황 및 진행률 시각화
- **성과 지표**: 주요 성과 지표(KPI)를 한눈에 확인

### 📈 종합 성과 분석
- **개인별 성과**: 사용자별 상세한 작업 시간 및 이슈 처리 현황
- **프로젝트 성과**: 프로젝트별 성과 통계 및 트렌드 분석
- **팀 분석**: 팀 성과 비교 및 벤치마킹
- **고급 지표**: 과거 데이터를 포함한 평균 성과 지표

### 📋 고급 보고서 시스템
- **주간 보고서**: 현재 주의 이슈 및 작업 현황과 트렌드 분석
- **월간 보고서**: 월별 성과 및 전월 대비 비교
- **연간 보고서**: 예측 기능을 포함한 연도별 종합 성과 분석
- **사용자 정의 기간**: 사용자 정의 날짜 선택이 가능한 유연한 보고서
- **내보내기 기능**: 다양한 형식의 보고서 내보내기

### 👥 향상된 사용자 관리
- **Redmine 통합**: 원활한 Redmine 사용자 정보 관리
- **보안 인증**: 고급 로그인 및 인증 시스템
- **사용자 프로필**: 성과 이력이 포함된 상세한 사용자 프로필
- **아바타 지원**: 사용자 아바타 표시 및 관리

### 🔍 고급 검색 및 필터링
- **스마트 검색**: 모든 데이터에 대한 고급 검색 기능
- **동적 필터링**: 상태, 우선순위, 담당자별 실시간 필터링
- **날짜 범위 필터**: 유연한 날짜 기반 필터링 옵션

## 🛠 기술 스택

- **Backend**: Django 4.2.7 (LTS)
- **Database**: MySQL 8.0.42
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Container**: Docker 20.10+ & Docker Compose 2.0+
- **Environment**: django-environ 0.11.2
- **Image Processing**: Pillow 10.1.0
- **Database Driver**: mysqlclient 2.2.0

## 📦 설치 및 실행

### 필수 요구사항
- Docker 20.10+ 및 Docker Compose 2.0+
- Git
- 4GB+ 사용 가능한 RAM
- 10GB+ 디스크 공간

### 1. Docker를 사용한 빠른 시작 (권장)

#### 클론 및 실행
```bash
# 저장소 클론
git clone <repository-url>
cd redmine_admin

# 모든 서비스 시작
docker-compose up --build -d

# 서비스 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f web
```

#### 서비스 관리
```bash
# 서비스 시작
docker-compose up -d

# 서비스 중지
docker-compose down

# 서비스 재시작
docker-compose restart

# 업데이트 및 재빌드
docker-compose up --build -d
```

### 2. 개별 서비스 관리

#### 데이터베이스만 실행
```bash
# MySQL 데이터베이스 시작
docker-compose up redmine_mysql -d

# MySQL 직접 접속
docker-compose exec redmine_mysql mysql -u root -p
```

#### 애플리케이션만 실행
```bash
# Django 애플리케이션 시작
docker-compose up web -d

# Django 명령어 실행
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
```

### 3. 개발 환경 설정

#### 필수 요구사항
- Python 3.8+
- MySQL 8.0+
- pip
- virtualenv

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

# 데이터베이스 설정
python manage.py migrate
python manage.py collectstatic --noinput

# 슈퍼유저 생성 (선택사항)
python manage.py createsuperuser

# 개발 서버 실행
python manage.py runserver 0.0.0.0:8000
```

## 🌐 접속 정보

- **웹 애플리케이션**: http://localhost:8000
- **관리자 인터페이스**: http://localhost:8000/admin/
- **MySQL 데이터베이스**: localhost:3310
  - 데이터베이스: redmine
  - 사용자: root
  - 비밀번호: aqwsde123!
  - 문자셋: utf8

## 📁 프로젝트 구조

```
redmine_admin/
├── redmine/                 # 메인 Django 애플리케이션
│   ├── models.py           # 데이터 모델 (Project, Issue, TimeEntry 등)
│   ├── views.py            # 뷰 로직 (대시보드, 보고서, 분석)
│   ├── urls.py             # URL 라우팅 설정
│   ├── admin.py            # Django 관리자 인터페이스 설정
│   ├── backends.py         # 커스텀 인증 백엔드
│   └── apps.py             # 앱 설정
├── templates/              # HTML 템플릿
│   ├── base.html          # 네비게이션이 포함된 기본 템플릿
│   ├── dashboard.html     # 메인 대시보드 페이지
│   ├── login.html         # 인증 페이지
│   ├── performance.html   # 성과 분석 페이지
│   └── *_report.html      # 보고서 템플릿들
├── static/                 # 정적 자산
│   ├── css/               # 스타일시트
│   ├── js/                # JavaScript 파일들
│   └── images/            # 이미지 자산
├── media/                  # 사용자 업로드 파일
├── docker-compose.yml     # Docker Compose 설정
├── Dockerfile             # Docker 이미지 정의
├── requirements.txt       # Python 의존성
└── manage.py             # Django 관리 스크립트
```

## 📊 데이터 모델

### 핵심 모델
- **Project**: 프로젝트 정보 및 메타데이터
- **Issue**: 전체 생명주기 추적이 가능한 이슈 및 작업 항목
- **TimeEntry**: 시간 추적 및 작업 로깅
- **RedmineUser**: 사용자 정보 및 프로필
- **IssueStatus**: 이슈 상태 정의
- **Tracker**: 이슈 추적 카테고리
- **RedmineUserAvatar**: 사용자 아바타 관리

### 이슈 상태 워크플로우
- **신규 (1)**: 초기 이슈 상태
- **진행중 (2)**: 활성 개발 중
- **해결됨 (3)**: 이슈 해결 완료
- **피드백 (4)**: 피드백/검토 대기 중
- **종료 (5)**: 이슈 완전 완료
- **거부됨 (6)**: 이슈 거부/취소

### 우선순위 레벨
- **낮음 (1)**: 낮은 우선순위 이슈
- **보통 (2)**: 표준 우선순위
- **높음 (3)**: 높은 우선순위 이슈
- **긴급 (4)**: 긴급 이슈
- **즉시 (5)**: 중요한 이슈

## 🔧 환경 설정

### 필수 환경 변수
프로젝트 루트에 `.env` 파일을 생성하세요:

```env
# Django 설정
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SECRET_KEY=your-secret-key-here

# 데이터베이스 설정
DATABASE_URL=mysql://root:aqwsde123!@localhost:3310/redmine

# 선택적 설정
TIME_ZONE=UTC
LANGUAGE_CODE=ko-kr
```

### Docker 환경 변수
다음은 Docker에서 자동으로 설정됩니다:

```env
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DATABASE_URL=mysql://root:aqwsde123!@redmine_mysql:3306/redmine
```

## 📈 사용 가이드

### 1. 대시보드 개요
- http://localhost:8000 으로 접속
- 실시간 프로젝트 통계 확인
- 최근 활동 및 트렌드 모니터링
- 모든 기능에 대한 빠른 네비게이션 접근

### 2. 성과 분석
- `/performance/` 페이지에서 상세한 분석 확인
- 개인별 및 팀 성과 지표 확인
- 프로젝트별 통계 분석
- 시간에 따른 성과 트렌드 추적

### 3. 보고서 생성
- **주간 보고서**: `/weekly-report/` 또는 `/weekly-report/<year>/<week>/`
- **월간 보고서**: `/monthly-report/` 또는 `/monthly-report/<year>/<month>/`
- **연간 보고서**: `/yearly-report/` 또는 `/yearly-report/<year>/`

### 4. 사용자 관리
- 사용자 프로필 및 성과 데이터 접근
- 사용자 아바타 및 연락처 정보 확인
- 사용자 활동 및 기여도 추적

## 🐛 문제 해결

### 일반적인 문제 및 해결책

#### 1. 데이터베이스 연결 문제
```bash
# MySQL 컨테이너 상태 확인
docker-compose ps redmine_mysql

# MySQL 로그 확인
docker-compose logs redmine_mysql

# 데이터베이스 연결 테스트
docker-compose exec web python manage.py dbshell
```

#### 2. Django 마이그레이션 문제
```bash
# 마이그레이션 초기화
docker-compose exec web python manage.py migrate --fake-initial

# 새 마이그레이션 생성
docker-compose exec web python manage.py makemigrations

# 마이그레이션 적용
docker-compose exec web python manage.py migrate
```

#### 3. 정적 파일 문제
```bash
# 정적 파일 재수집
docker-compose exec web python manage.py collectstatic --noinput --clear

# 정적 파일 위치 확인
docker-compose exec web python manage.py findstatic admin/css/base.css
```

#### 4. 성능 문제
```bash
# 컨테이너 리소스 확인
docker stats

# 애플리케이션 로그 확인
docker-compose logs -f web

# 서비스 재시작
docker-compose restart
```

### 성능 최적화
- 데이터베이스 쿼리 캐싱 활성화
- 정적 파일 서빙 최적화
- 데이터베이스 연결 풀링 사용
- 적절한 인덱싱 구현

## 🔒 보안 고려사항

### 인증
- Redmine 통합을 위한 커스텀 인증 백엔드
- 설정 가능한 만료 시간의 세션 관리
- 비밀번호 해싱 및 보안

### 데이터 보호
- 데이터베이스 연결 암호화
- 입력 검증 및 살균
- SQL 인젝션 방지
- XSS 보호

### 접근 제어
- 역할 기반 접근 제어
- 사용자 권한 관리
- 감사 로깅 기능

## 🚀 배포

### 프로덕션 배포
```bash
# 프로덕션 환경 설정
export DJANGO_SETTINGS_MODULE=redmine_admin.settings.production

# 프로덕션 이미지 빌드
docker build -t redmine-admin:production .

# 프로덕션 설정으로 실행
docker-compose -f docker-compose.prod.yml up -d
```

### 확장 고려사항
- 고가용성을 위한 데이터베이스 복제
- 여러 애플리케이션 인스턴스를 위한 로드 밸런싱
- 캐싱 레이어 구현
- 모니터링 및 로깅 설정

## 🤝 기여하기

기여를 환영합니다! 다음 단계를 따라주세요:

1. **프로젝트 포크**
2. **기능 브랜치 생성**: `git checkout -b feature/AmazingFeature`
3. **변경사항 커밋**: `git commit -m 'Add some AmazingFeature'`
4. **브랜치에 푸시**: `git push origin feature/AmazingFeature`
5. **풀 리퀘스트 열기**

### 개발 가이드라인
- PEP 8 코딩 표준 준수
- 포괄적인 테스트 작성
- 문서 업데이트
- 하위 호환성 보장

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다 - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 지원 및 커뮤니티

### 도움 받기
- **문서**: 이 README와 인라인 코드 주석 확인
- **이슈**: 버그나 기능 요청을 위해 GitHub에 이슈 생성
- **토론**: 질문과 아이디어를 위해 GitHub Discussions 사용

### 버전 히스토리
- **v2.0.0**: 향상된 성과 분석 및 보고서 기능
- **v1.5.0**: 사용자 아바타 지원 및 UI 개선 추가
- **v1.0.0**: 기본 대시보드 및 보고서가 포함된 초기 릴리스

## 🔮 로드맵

### 예정된 기능
- [ ] 실시간 알림
- [ ] 고급 차트 및 시각화
- [ ] 외부 통합을 위한 API 엔드포인트
- [ ] 모바일 반응형 디자인 개선
- [ ] 다국어 지원
- [ ] 고급 내보내기 옵션 (PDF, Excel)

### 계획된 개선사항
- [ ] 성능 최적화
- [ ] 향상된 보안 기능
- [ ] 더 나은 오류 처리
- [ ] 포괄적인 테스트 스위트

---

**Redmine Admin v2.0.0** - 고급 프로젝트 관리 및 성과 분석 도구

*Django와 현대적인 웹 기술로 ❤️을 담아 구축*