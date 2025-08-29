# AI 설계안 등록 시스템

AI 임베딩을 활용한 설계안 등록 및 관리 시스템입니다. FastAPI 백엔드와 Streamlit 프론트엔드로 구성되어 있습니다.

## 🏗️ 시스템 아키텍처

- **Backend**: FastAPI + PostgreSQL + pgvector
- **Frontend**: Streamlit 웹 애플리케이션
- **AI Model**: sentence-transformers (다국어 임베딩)
- **Database**: PostgreSQL with pgvector extension

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 환경변수 파일 생성
cp .env.example .env

# .env 파일을 편집하여 실제 데이터베이스 정보 입력
# DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD 설정
```

### 2. 의존성 설치

```bash
# Python 패키지 설치
pip install fastapi uvicorn psycopg2-binary python-multipart
pip install streamlit sentence-transformers python-dotenv
```

### 3. 데이터베이스 설정

```bash
# PostgreSQL 실행 (macOS)
brew services start postgresql

# 데이터베이스 접속 및 pgvector 확장 설치
psql -U postgres -d postgres
CREATE EXTENSION vector;
```

### 4. 서버 실행

```bash
# Terminal 1: FastAPI 백엔드 서버 실행
uvicorn app:app --reload

# Terminal 2: Streamlit 프론트엔드 실행
streamlit run streamlit_client.py
```

### 5. 접속

- **Streamlit 웹 앱**: http://localhost:8501
- **FastAPI 문서**: http://localhost:8000/docs
- **API 헬스체크**: http://localhost:8000/health

## 📁 파일 구조

```
3_DataBase/
├── app.py                 # FastAPI 백엔드 서버
├── streamlit_client.py    # Streamlit 프론트엔드
├── .env                   # 환경변수 (로컬 설정)
├── .env.example          # 환경변수 템플릿
├── .gitignore            # Git 무시 파일 목록
└── README.md             # 프로젝트 설명서
```

## 🔧 주요 기능

### FastAPI 백엔드 (`app.py`)
- **설계안 등록 API**: `/register_design` (POST)
- **AI 임베딩 생성**: sentence-transformers 활용
- **데이터베이스 저장**: PostgreSQL + pgvector
- **트랜잭션 처리**: ACID 속성 보장

### Streamlit 프론트엔드 (`streamlit_client.py`)
- **사용자 친화적 UI**: 설계안 입력 폼
- **실시간 상태 체크**: API 서버 연결 상태
- **진행 상태 표시**: 등록 과정 시각화
- **결과 확인**: 등록 성공/실패 피드백

## 🔐 보안 설정

### 환경변수 관리
- `.env` 파일은 Git에 커밋하지 않음
- `.env.example`을 템플릿으로 제공
- 민감한 정보(비밀번호 등)는 환경변수로 관리

### 데이터베이스 보안
- 매개변수 바인딩으로 SQL 인젝션 방지
- 최소 권한 원칙 적용
- 트랜잭션 기반 데이터 무결성 보장

## 🤖 AI 모델 정보

- **모델명**: `paraphrase-multilingual-MiniLM-L12-v2`
- **지원 언어**: 한국어 포함 104개 언어
- **벡터 차원**: 384차원
- **용도**: 텍스트 의미 유사도 검색

## 📊 데이터베이스 스키마

```sql
CREATE TABLE design (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    embedding VECTOR(384),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 벡터 유사도 검색을 위한 인덱스
CREATE INDEX ON design USING ivfflat (embedding vector_cosine_ops);
```

## 🛠️ 개발 환경 설정

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pgvector extension

### 개발 모드 실행
```bash
# 개발용 FastAPI 서버 (자동 리로드)
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# 개발용 Streamlit (자동 리로드)
streamlit run streamlit_client.py --server.runOnSave true
```

## 🔍 API 문서

FastAPI 서버 실행 후 다음 URL에서 자동 생성된 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 주요 엔드포인트

| 메서드 | 경로 | 설명 | 응답 |
|--------|------|------|------|
| GET | `/` | 서버 상태 확인 | 서버 정보 |
| GET | `/health` | 헬스 체크 | 시스템 상태 |
| POST | `/register_design` | 설계안 등록 | 등록 결과 |

## 🚨 문제 해결

### 일반적인 오류

1. **AI 모델 로딩 실패**
   ```bash
   # 인터넷 연결 확인 후 재시도
   pip install --upgrade sentence-transformers
   ```

2. **데이터베이스 연결 실패**
   ```bash
   # PostgreSQL 서비스 상태 확인
   brew services list | grep postgresql
   
   # pgvector 확장 설치 확인
   psql -U postgres -c "SELECT * FROM pg_extension WHERE extname='vector';"
   ```

3. **포트 충돌**
   ```bash
   # 다른 포트 사용
   uvicorn app:app --port 8001
   streamlit run streamlit_client.py --server.port 8502
   ```

## 📝 개발 노트

- 모든 API 요청은 JSON 형태로 처리
- 임베딩 생성은 서버 시작시 모델 로딩 필요
- 대용량 텍스트 처리시 타임아웃 고려 필요
- 벡터 검색 성능 최적화를 위한 인덱스 활용

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.
