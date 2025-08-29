"""
FastAPI 기반 설계안 등록 및 유사도 검색 API 서버 (코사인 인덱스 특화)

실행 방법:
uvicorn api_index_cosine:app --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
import logging

# 환경변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="Design Registration & Search API",
    description="AI 임베딩과 코사인 유사도를 사용한 설계안 등록 및 검색 시스템",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 연결 설정
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD")
}

# AI 모델 전역 변수
embedding_model = None

# ========== 요청/응답 모델 ==========
# Pydantic BaseModel을 상속받아 API 요청과 응답의 데이터 구조를 정의
# 자동으로 데이터 검증, 직렬화/역직렬화, API 문서 생성 기능 제공

class DesignRequest(BaseModel):
    """설계안 등록 요청 데이터 모델"""
    title: str          # 설계안 제목 (필수)
    description: str    # 설계안 상세 설명 (필수, AI 임베딩 변환 대상)

class DesignResponse(BaseModel):
    """설계안 등록 응답 데이터 모델"""
    success: bool                    # 등록 성공 여부
    message: str                     # 응답 메시지
    design_id: int = None           # 등록된 설계안의 데이터베이스 ID
    embedding_dimension: int = None  # 생성된 임베딩 벡터의 차원 수 (384차원)

class VectorSearchRequest(BaseModel):
    """벡터 유사도 검색 요청 데이터 모델"""
    query_text: str                     # 검색할 텍스트 (AI가 벡터로 변환)
    limit: int = 10                     # 반환할 검색 결과 개수 (기본값: 10개)
    distance_threshold: float = 2.0     # 코사인 거리 임계값 (작을수록 엄격한 유사도)

class VectorSearchResponse(BaseModel):
    """벡터 유사도 검색 응답 데이터 모델"""
    success: bool           # 검색 성공 여부
    message: str           # 응답 메시지
    results: list = []     # 검색 결과 리스트 (각 항목: id, title, description, cosine_distance, similarity_score)
    total_found: int = 0   # 찾은 결과의 총 개수

# ========== 서버 시작 이벤트 ==========
# FastAPI 서버가 시작될 때 자동으로 실행되는 이벤트 핸들러
# AI 모델 로딩과 데이터베이스 연결 테스트를 수행

@app.on_event("startup")
async def startup_event():
    """서버 시작시 초기화 작업 수행"""
    global embedding_model
    try:
        # 1. AI 임베딩 모델 로딩 (한국어 지원 다국어 모델)
        logger.info("AI 임베딩 모델 로딩 중...")
        embedding_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        logger.info("AI 임베딩 모델 로딩 완료!")
        
        # 2. 데이터베이스 연결 테스트 (연결 가능 여부 확인)
        conn = psycopg2.connect(**DB_CONFIG)
        conn.close()
        logger.info("데이터베이스 연결 성공!")
        
    except Exception as e:
        logger.error(f"서버 시작 실패: {e}")
        raise e

# ========== 유틸리티 함수 ==========
# 핵심 비즈니스 로직을 처리하는 헬퍼 함수들

def create_embedding(text: str):
    """텍스트를 384차원 임베딩 벡터로 변환
    
    Args:
        text (str): 변환할 텍스트 (설계안 설명 또는 검색 쿼리)
    
    Returns:
        list: 384차원 실수 리스트 (임베딩 벡터) 또는 None (실패시)
    """
    try:
        # SentenceTransformer 모델을 사용하여 텍스트를 벡터로 변환
        embedding = embedding_model.encode(text)
        return embedding.tolist()  # numpy 배열을 Python 리스트로 변환
    except Exception as e:
        logger.error(f"임베딩 생성 실패: {e}")
        return None

def insert_design_to_db(title: str, description: str, embedding: list):
    """설계안과 임베딩을 데이터베이스에 저장
    
    Args:
        title (str): 설계안 제목
        description (str): 설계안 상세 설명
        embedding (list): 384차원 임베딩 벡터
    
    Returns:
        int: 저장된 설계안의 ID 또는 None (실패시)
    """
    conn = None
    try:
        # PostgreSQL 연결 생성
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # design_doc 테이블에 데이터 삽입
        # content 컬럼에 description 저장, embedding_vector 컬럼에 벡터 저장
        insert_sql = """
        INSERT INTO design_doc (title, content, embedding_vector) 
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        
        cur.execute(insert_sql, (title, description, embedding))
        design_id = cur.fetchone()[0]  # 생성된 ID 반환
        
        # 트랜잭션 커밋 (데이터 확정 저장)
        conn.commit()
        cur.close()
        conn.close()
        
        logger.info(f"설계안 저장 성공 - ID: {design_id}")
        return design_id
        
    except Exception as e:
        # 오류 발생시 롤백 처리
        if conn:
            conn.rollback()
            conn.close()
        logger.error(f"데이터베이스 저장 실패: {e}")
        return None

# ========== API 엔드포인트 ==========
# 클라이언트 요청을 처리하는 REST API 엔드포인트들

@app.get("/")
async def root():
    """루트 엔드포인트 - 서버 상태 정보 반환"""
    return {
        "message": "Design Registration & Search API Server",
        "status": "running",
        "model_loaded": embedding_model is not None
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트 - 서버와 데이터베이스 연결 상태 확인"""
    try:
        # 데이터베이스 연결 테스트
        conn = psycopg2.connect(**DB_CONFIG)
        conn.close()
        db_status = "connected"
    except:
        db_status = "disconnected"
    
    return {
        "status": "healthy" if embedding_model and db_status == "connected" else "unhealthy",
        "model_status": "loaded" if embedding_model else "not_loaded",
        "database": db_status
    }

@app.post("/register_design", response_model=DesignResponse)
async def register_design(request: DesignRequest):
    """설계안 등록 API
    
    기능 흐름:
    1. 입력 데이터 검증 (제목, 설명 필수)
    2. AI 모델로 설명 텍스트를 384차원 벡터로 변환
    3. 설계안 정보와 임베딩 벡터를 PostgreSQL에 저장
    4. 저장 결과 반환 (ID, 벡터 차원 정보 포함)
    """
    try:
        logger.info(f"설계안 등록 요청 - Title: {request.title}")
        
        # 1. AI 모델 로딩 상태 확인
        if embedding_model is None:
            raise HTTPException(status_code=500, detail="AI 임베딩 모델이 로드되지 않았습니다.")
        
        # 2. 입력 데이터 유효성 검증
        if not request.title.strip() or not request.description.strip():
            raise HTTPException(status_code=400, detail="제목과 설명은 필수 입력 항목입니다.")
        
        # 3. AI 임베딩 생성 (설명 텍스트 → 384차원 벡터)
        embedding = create_embedding(request.description)
        if embedding is None:
            raise HTTPException(status_code=500, detail="임베딩 생성에 실패했습니다.")
        
        # 4. 데이터베이스에 저장 (트랜잭션 처리)
        design_id = insert_design_to_db(request.title, request.description, embedding)
        if design_id is None:
            raise HTTPException(status_code=500, detail="데이터베이스 저장에 실패했습니다.")
        
        # 5. 성공 응답 반환
        return DesignResponse(
            success=True,
            message="설계안이 성공적으로 등록되었습니다.",
            design_id=design_id,
            embedding_dimension=len(embedding)
        )
        
    except HTTPException:
        raise  # HTTP 예외는 그대로 전달
    except Exception as e:
        logger.error(f"예상치 못한 오류: {e}")
        raise HTTPException(status_code=500, detail=f"서버 내부 오류: {str(e)}")

@app.post("/search_similar_designs", response_model=VectorSearchResponse)
async def search_similar_designs(request: VectorSearchRequest):
    """유사한 설계안 검색 API (코사인 유사도 기반)
    
    기능 흐름:
    1. 검색 텍스트를 AI로 384차원 벡터 변환
    2. pgvector의 코사인 거리 연산자(<=>)로 유사도 계산
    3. 거리 임계값 이하의 결과만 필터링
    4. 코사인 거리 기준 오름차순 정렬 (거리가 작을수록 유사)
    5. 지정된 개수만큼 결과 반환
    """
    try:
        logger.info(f"유사도 검색 요청 - Query: {request.query_text}")
        
        # 1. AI 모델 로딩 상태 확인
        if embedding_model is None:
            raise HTTPException(status_code=500, detail="AI 임베딩 모델이 로드되지 않았습니다.")
        
        # 2. 입력 데이터 유효성 검증
        if not request.query_text.strip():
            raise HTTPException(status_code=400, detail="검색할 텍스트를 입력해주세요.")
        
        # 3. 검색 텍스트를 AI로 벡터 변환
        query_embedding = create_embedding(request.query_text)
        if query_embedding is None:
            raise HTTPException(status_code=500, detail="검색 텍스트의 임베딩 생성에 실패했습니다.")
        
        # 4. 데이터베이스에서 유사한 벡터 검색
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # pgvector 코사인 거리 검색 쿼리
        # <=> : 코사인 거리 연산자 (0에 가까울수록 유사)
        # WHERE 절: 거리 임계값으로 결과 필터링
        # ORDER BY: 거리 기준 오름차순 정렬 (가장 유사한 것부터)
        # LIMIT: 반환할 결과 개수 제한
        search_sql = """
        SELECT id, title, content, 
               (embedding_vector <=> %s::vector) AS cosine_distance
        FROM design_doc
        WHERE (embedding_vector <=> %s::vector) <= %s
        ORDER BY embedding_vector <=> %s::vector
        LIMIT %s;
        """
        
        cur.execute(search_sql, (
            query_embedding,           # 검색할 벡터
            query_embedding,           # WHERE 절용 벡터 (동일)
            request.distance_threshold, # 거리 임계값
            query_embedding,           # ORDER BY 절용 벡터 (동일)
            request.limit              # 결과 개수 제한
        ))
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        # 5. 결과 데이터 가공 및 응답 생성
        formatted_results = []
        for row in results:
            # 코사인 거리를 유사도 점수로 변환
            # 코사인 거리: 0~2 범위 (0이 가장 유사)
            # 유사도 점수: 0~1 범위 (1이 가장 유사)
            similarity_score = 1 - float(row[3])
            formatted_results.append({
                "id": row[0],                           # 설계안 ID
                "title": row[1],                        # 설계안 제목
                "description": row[2],                  # 설계안 내용
                "cosine_distance": float(row[3]),       # 원본 코사인 거리
                "similarity_score": round(similarity_score, 4)  # 변환된 유사도 점수
            })
        
        return VectorSearchResponse(
            success=True,
            message=f"유사한 설계안 {len(results)}개를 찾았습니다.",
            results=formatted_results,
            total_found=len(results)
        )
        
    except HTTPException:
        raise  # HTTP 예외는 그대로 전달
    except Exception as e:
        logger.error(f"검색 오류: {e}")
        raise HTTPException(status_code=500, detail=f"검색 중 오류가 발생했습니다: {str(e)}")

@app.get("/database_stats")
async def get_database_stats():
    """데이터베이스 통계 정보 조회 API
    
    반환 정보:
    - 총 설계안 개수
    - 데이터베이스 이름
    - 테이블 이름
    - 생성된 인덱스 목록 (코사인, L2 거리 인덱스 등)
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # design_doc 테이블의 전체 레코드 개수 조회
        cur.execute("SELECT COUNT(*) FROM design_doc;")
        total_designs = cur.fetchone()[0]
        
        # design_doc 테이블에 생성된 모든 인덱스 정보 조회
        # pg_indexes 시스템 테이블에서 인덱스명과 정의 가져오기
        cur.execute("""
        SELECT indexname, indexdef 
        FROM pg_indexes 
        WHERE tablename = 'design_doc';
        """)
        indexes = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return {
            "total_designs": total_designs,                # 총 설계안 개수
            "database_name": DB_CONFIG["dbname"],          # 데이터베이스 이름
            "table_name": "design_doc",                    # 테이블 이름
            "indexes": [{"name": idx[0], "definition": idx[1]} for idx in indexes]  # 인덱스 목록
        }
        
    except Exception as e:
        logger.error(f"통계 조회 오류: {e}")
        raise HTTPException(status_code=500, detail=f"통계 조회 중 오류: {str(e)}")

# ========== 서버 실행 설정 ==========
# 개발 환경에서 직접 실행할 때 사용되는 설정
# 실제 배포시에는 외부에서 uvicorn 명령어로 실행

if __name__ == "__main__":
    import uvicorn
    # .env 파일에서 호스트와 포트 설정 읽기
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host=host, port=port)