from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

app = FastAPI(title="간단한 텍스트 검색 API")

# 데이터베이스 연결 설정
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "0430"),
}

# 요청 모델
class TextSearchRequest(BaseModel):
    query_text: str
    top_k: int = 5

# 응답 모델
class SearchResult(BaseModel):
    id: int
    title: str
    content: str
    distance: float

# 임베딩 생성 함수 (실제 구현 필요한 부분)
def get_embedding(text: str) -> List[float]:
    """
    실제 사용시에는 여기에 임베딩 생성 로직 구현
    예: OpenAI API, sentence-transformers 등
    """
    # 임시로 첫 번째 문서의 임베딩을 반환 (데모용)
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute("SELECT embedding_vector FROM design_doc WHERE id = 1;")
            result = cur.fetchone()
        conn.close()
        
        if result:
            # PostgreSQL 벡터를 리스트로 변환
            vector_str = str(result[0])
            # '[1,2,3]' 형태를 리스트로 변환
            vector_list = eval(vector_str) if vector_str.startswith('[') else list(result[0])
            return vector_list
        else:
            return [0.0] * 384
    except:
        return [0.0] * 384

# PostgreSQL 배열 형태로 변환
def list_to_pg_array(lst: List[float]) -> str:
    return '{' + ','.join(str(x) for x in lst) + '}'

@app.post("/search_text", response_model=List[SearchResult])
async def search_text(request: TextSearchRequest):
    """
    텍스트를 입력받아 가장 유사한 k개 문서 반환
    """
    
    # 1. 텍스트에서 임베딩 생성
    embedding = get_embedding(request.query_text)
    embedding_str = list_to_pg_array(embedding)
    
    # 2. L2 거리로 유사 문서 검색
    sql = """
    SELECT 
        id,
        title,
        content,
        embedding_vector <-> %s::vector AS distance
    FROM design_doc 
    ORDER BY distance
    LIMIT %s;
    """
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # 인덱스 사용 강제
            cur.execute("SET LOCAL enable_seqscan = off;")
            cur.execute(sql, (embedding_str, request.top_k))
            results = cur.fetchall()
        conn.close()
        
        return [
            SearchResult(
                id=row['id'],
                title=row['title'],
                content=row['content'],
                distance=float(row['distance'])
            )
            for row in results
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 오류: {str(e)}")

# 헬스체크
@app.get("/health")
async def health():
    return {"status": "ok", "message": "텍스트 검색 API 정상 동작"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
