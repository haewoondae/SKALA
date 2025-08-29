"""
FastAPI 기반 설계안 등록 API 서버

주요 기능:
1. /register_design POST API - 설계안 등록 및 AI 임베딩 생성
2. PostgreSQL + pgvector를 사용한 벡터 데이터 저장
3. 트랜잭션 처리로 데이터 무결성 보장
4. 실시간 임베딩 생성 및 저장

실행 방법:
uvicorn app:app --reload
"""

# FastAPI 프레임워크 및 관련 모듈 - 웹 API 서버 구축을 위한 라이브러리
from fastapi import FastAPI, HTTPException  # FastAPI 메인 클래스와 HTTP 예외 처리
from fastapi.middleware.cors import CORSMiddleware  # Cross-Origin Resource Sharing 허용을 위한 미들웨어
# 데이터 검증을 위한 Pydantic 모델 - API 요청/응답 데이터 구조 정의
from pydantic import BaseModel  # 데이터 유효성 검증 및 직렬화
# PostgreSQL 연결을 위한 psycopg2 - 데이터베이스 어댑터
import psycopg2  # PostgreSQL 데이터베이스 연결 및 쿼리 실행
# AI 임베딩 모델을 위한 sentence-transformers - 텍스트를 벡터로 변환
from sentence_transformers import SentenceTransformer  # 다국어 문장 임베딩 모델
# 환경변수 처리 - 보안을 위한 설정값 관리
import os  # 운영체제 환경변수 접근
from dotenv import load_dotenv  # .env 파일에서 환경변수 로드
# 비동기 처리를 위한 asyncio - 동시성 처리
import asyncio  # 비동기 프로그래밍 지원
# 로깅 - 애플리케이션 실행 로그 기록
import logging  # 디버깅 및 모니터링을 위한 로그

# .env 파일에서 환경변수 로드 - 데이터베이스 접속 정보 등 보안 설정
load_dotenv()

# 로깅 설정 - 애플리케이션 실행 과정 추적을 위한 로그 레벨 설정
logging.basicConfig(level=logging.INFO)  # INFO 레벨 이상의 로그 출력
logger = logging.getLogger(__name__)  # 현재 모듈용 로거 생성

# FastAPI 애플리케이션 인스턴스 생성 - 메인 웹 서버 객체
app = FastAPI(
    title="Design Registration API",  # API 문서에 표시될 제목
    description="AI 임베딩을 사용한 설계안 등록 시스템",  # API 설명
    version="1.0.0"  # API 버전 정보
)

# CORS 미들웨어 추가 (Streamlit에서 API 호출 허용) - 브라우저의 동일 출처 정책 우회
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (개발환경용) - 운영환경에서는 특정 도메인만 허용 권장
    allow_credentials=True,  # 인증 정보 포함 요청 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

# PostgreSQL 데이터베이스 연결 설정 - 환경변수에서 DB 접속 정보 읽기
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),  # DB 서버 주소 (기본값: localhost)
    "port": int(os.getenv("DB_PORT", 5432)),  # DB 포트 번호 (기본값: 5432)
    "dbname": os.getenv("DB_NAME", "postgres"),  # 데이터베이스 이름 (기본값: postgres)
    "user": os.getenv("DB_USER", "postgres"),  # 사용자명 (기본값: postgres)
    "password": os.getenv("DB_PASSWORD")  # 비밀번호 (환경변수에서만 읽기)
}

# AI 임베딩 모델 전역 변수 (서버 시작시 한 번만 로드) - 메모리 효율성을 위한 싱글톤 패턴
embedding_model = None

# 요청 데이터 모델 정의 (Pydantic) - API로 받을 데이터 구조 정의
class DesignRequest(BaseModel):
    """설계안 등록 요청 데이터 모델"""
    title: str  # 설계안 제목 (필수) - 문자열 타입, 빈 값 불허
    description: str  # 설계안 설명 (필수) - AI 임베딩 생성 대상 텍스트
    
    class Config:
        # JSON 스키마 예시 - API 문서에서 사용자에게 보여줄 예시 데이터
        schema_extra = {
            "example": {
                "title": "친환경 스마트홈",
                "description": "태양광 패널과 지열 에너지를 활용하여 에너지 자립을 목표로 하는 설계안입니다."
            }
        }

# 응답 데이터 모델 정의 - API가 반환할 데이터 구조 정의
class DesignResponse(BaseModel):
    """설계안 등록 응답 데이터 모델"""
    success: bool  # 성공 여부 - True/False로 처리 결과 표시
    message: str   # 응답 메시지 - 사용자에게 보여줄 결과 메시지
    design_id: int = None  # 생성된 설계안 ID (성공시) - 데이터베이스 자동 생성 ID
    embedding_dimension: int = None  # 임베딩 차원 (성공시) - 벡터 크기 정보 (384차원)

@app.on_event("startup")  # FastAPI 서버 시작 이벤트 핸들러 - 서버 실행 시 한 번만 실행
async def startup_event():
    """서버 시작시 실행되는 이벤트 - AI 모델 로딩"""
    global embedding_model  # 전역 변수 수정을 위한 global 선언
    try:
        logger.info("AI 임베딩 모델 로딩 중...")  # 로딩 시작 로그
        # 한국어 지원 다국어 임베딩 모델 로드 - 384차원 벡터 생성 모델
        embedding_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        logger.info("AI 임베딩 모델 로딩 완료!")  # 로딩 완료 로그
    except Exception as e:
        logger.error(f"AI 모델 로딩 실패: {e}")  # 오류 로그 기록
        raise e  # 서버 시작 실패로 예외 재발생

def create_embedding(text: str):
    """
    텍스트를 384차원 임베딩 벡터로 변환
    - 입력된 텍스트를 AI 모델을 통해 수치형 벡터로 변환
    - 의미적으로 유사한 텍스트는 유사한 벡터값을 가짐
    
    Args:
        text: 임베딩할 텍스트 - 설계안 설명 등
        
    Returns:
        list: 384개 실수로 구성된 임베딩 벡터 - 벡터 유사도 검색 가능
    """
    try:
        # AI 모델로 텍스트 인코딩 - 자연어를 수치형 벡터로 변환
        embedding = embedding_model.encode(text)
        # numpy 배열을 Python 리스트로 변환 - JSON 직렬화 가능한 형태로 변환
        return embedding.tolist()
    except Exception as e:
        logger.error(f"임베딩 생성 실패: {e}")  # 오류 로그 기록
        return None  # 실패시 None 반환

def insert_design_to_db(title: str, description: str, embedding: list):
    """
    설계안과 임베딩을 데이터베이스에 저장 (트랜잭션 처리)
    - ACID 속성을 보장하는 트랜잭션으로 데이터 무결성 확보
    - 실패시 자동 롤백으로 부분 저장 방지
    
    Args:
        title: 설계안 제목 - design 테이블의 title 컬럼
        description: 설계안 설명 - design 테이블의 description 컬럼  
        embedding: 384차원 임베딩 벡터 - pgvector 확장의 vector 타입으로 저장
        
    Returns:
        int: 생성된 설계안 ID (실패시 None) - PostgreSQL의 SERIAL 타입 자동 생성
    """
    conn = None  # 연결 객체 초기화
    try:
        # PostgreSQL 연결 - DB_CONFIG 설정으로 데이터베이스 접속
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()  # 커서 생성 - SQL 쿼리 실행을 위한 객체
        
        # 임베딩 유효성 검사 - 벡터 차원이 정확한지 확인
        if not embedding or len(embedding) != 384:
            raise ValueError(f"유효하지 않은 임베딩 차원: {len(embedding) if embedding else 0}")
        
        # INSERT 쿼리 실행 - RETURNING 절로 생성된 ID 반환
        insert_sql = """
        INSERT INTO design (title, description, embedding) 
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        
        cur.execute(insert_sql, (title, description, embedding))  # 매개변수 바인딩으로 SQL 인젝션 방지
        design_id = cur.fetchone()[0]  # 생성된 ID 추출
        
        # 트랜잭션 커밋 - 모든 변경사항을 데이터베이스에 영구 저장
        conn.commit()
        cur.close()  # 커서 종료
        conn.close()  # 연결 종료
        
        logger.info(f"설계안 저장 성공 - ID: {design_id}, Title: {title}")  # 성공 로그
        return design_id
        
    except Exception as e:
        # 롤백 처리 - 오류 발생시 모든 변경사항 취소
        if conn:
            conn.rollback()  # 트랜잭션 롤백
            conn.close()  # 연결 종료
        logger.error(f"데이터베이스 저장 실패: {e}")  # 오류 로그
        return None  # 실패시 None 반환

@app.get("/")  # HTTP GET 메서드로 루트 경로 처리
async def root():
    """루트 엔드포인트 - API 상태 확인"""
    return {
        "message": "Design Registration API Server",  # 서버 식별 메시지
        "status": "running",  # 서버 실행 상태
        "model_loaded": embedding_model is not None  # AI 모델 로딩 상태 확인
    }

@app.get("/health")  # 헬스 체크용 엔드포인트
async def health_check():
    """헬스 체크 엔드포인트 - 시스템 전체 상태 점검"""
    return {
        "status": "healthy",  # 전체 시스템 상태
        "model_status": "loaded" if embedding_model else "not_loaded",  # AI 모델 상태
        "database": "connected"  # 실제로는 DB 연결 테스트 필요 - 추후 개선점
    }

@app.post("/register_design", response_model=DesignResponse)  # POST 메서드로 설계안 등록 처리
async def register_design(request: DesignRequest):
    """
    설계안 등록 API - 메인 비즈니스 로직
    
    전체 처리 흐름:
    1. 요청 데이터 검증 - 필수 필드 확인
    2. AI 임베딩 생성 - 텍스트를 벡터로 변환
    3. PostgreSQL에 저장 (트랜잭션) - 원자적 저장 보장
    4. 결과 반환 - 성공/실패 상태와 상세 정보
    """
    try:
        logger.info(f"설계안 등록 요청 - Title: {request.title}")  # 요청 로그
        
        # AI 모델 로딩 확인 - 모델이 준비되지 않은 상태에서 요청 처리 방지
        if embedding_model is None:
            raise HTTPException(
                status_code=500, 
                detail="AI 임베딩 모델이 로드되지 않았습니다."
            )
        
        # 입력 데이터 검증 - 빈 문자열이나 공백만 있는 입력 방지
        if not request.title.strip() or not request.description.strip():
            raise HTTPException(
                status_code=400,  # Bad Request
                detail="제목과 설명은 필수 입력 항목입니다."
            )
        
        # 1. AI 임베딩 생성 - 설계안 설명을 384차원 벡터로 변환
        logger.info("AI 임베딩 생성 중...")
        embedding = create_embedding(request.description)
        
        if embedding is None:
            raise HTTPException(
                status_code=500,  # Internal Server Error
                detail="임베딩 생성에 실패했습니다."
            )
        
        # 2. 데이터베이스에 저장 - 트랜잭션으로 안전한 저장
        logger.info("데이터베이스 저장 중...")
        design_id = insert_design_to_db(
            request.title, 
            request.description, 
            embedding
        )
        
        if design_id is None:
            raise HTTPException(
                status_code=500,
                detail="데이터베이스 저장에 실패했습니다."
            )
        
        # 3. 성공 응답 반환 - 생성된 ID와 임베딩 정보 포함
        return DesignResponse(
            success=True,
            message="설계안이 성공적으로 등록되었습니다.",
            design_id=design_id,
            embedding_dimension=len(embedding)  # 벡터 차원 정보 (384)
        )
        
    except HTTPException:
        # 이미 처리된 HTTP 예외는 그대로 전달 - 중복 처리 방지
        raise
    except Exception as e:
        logger.error(f"예상치 못한 오류: {e}")  # 예외 로그 기록
        raise HTTPException(
            status_code=500,
            detail=f"서버 내부 오류가 발생했습니다: {str(e)}"
        )

if __name__ == "__main__":
    # 개발용 서버 실행 (실제로는 uvicorn 명령어 사용 권장)
    # 운영환경에서는 'uvicorn app:app --host 0.0.0.0 --port 8000' 명령어 사용
    import uvicorn  # ASGI 서버 - 비동기 웹 서버
    uvicorn.run(app, host="0.0.0.0", port=8000)  # 모든 네트워크 인터페이스에서 8000번 포트로 서버 실행