from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
import re

# 환경변수 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(title="GitHub Issue Similarity Search API")

# 전역 모델 (앱 시작시 한번만 로드)
model = SentenceTransformer('all-MiniLM-L6-v2')

# DB 연결 정보
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'postgres'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'port': os.getenv('DB_PORT', '5432')
}

# 요청/응답 모델
class IssueSearchRequest(BaseModel):
    title: str
    description: str = ""
    top_k: int = 5

class SimilarIssue(BaseModel):
    id: int
    title: str
    description: str
    similarity: float

class IssueSearchResponse(BaseModel):
    query: str
    results: list[SimilarIssue]

def connect_db():
    """데이터베이스 연결"""
    try:
        return psycopg2.connect(**db_config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB 연결 실패: {e}")

def clean_text(text):
    """텍스트 정제"""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', str(text))
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

@app.get("/")
async def root():
    """API 상태 확인"""
    return {"message": "GitHub Issue Similarity Search API", "status": "running"}

@app.post("/search", response_model=IssueSearchResponse)
async def search_similar_issues(request: IssueSearchRequest):
    """유사 이슈 검색 API"""
    
    # 1. 텍스트 정제 및 결합
    title = clean_text(request.title)
    description = clean_text(request.description)
    combined_text = title + ' ' + description
    
    if not combined_text.strip():
        raise HTTPException(status_code=400, detail="제목 또는 설명을 입력해주세요")
    
    # 2. 임베딩 생성
    try:
        embedding = model.encode([combined_text])[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"임베딩 생성 실패: {e}")
    
    # 3. 유사도 검색
    conn = connect_db()
    try:
        cursor = conn.cursor()
        
        # 임베딩을 문자열로 변환
        embedding_str = '[' + ','.join(map(str, embedding.tolist())) + ']'
        
        # pgvector 코사인 유사도 검색
        query = """
            SELECT id, title, description, 
                   1 - (embedding <=> %s::vector) as similarity
            FROM issues
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
        """
        
        cursor.execute(query, (embedding_str, embedding_str, request.top_k))
        results = cursor.fetchall()
        
        # 결과 변환
        similar_issues = [
            SimilarIssue(
                id=row[0],
                title=row[1],
                description=row[2],
                similarity=round(float(row[3]), 4)
            )
            for row in results
        ]
        
        return IssueSearchResponse(
            query=combined_text,
            results=similar_issues
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 실패: {e}")
    finally:
        cursor.close()
        conn.close()

@app.get("/health")
async def health_check():
    """헬스 체크"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM issues;")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "total_issues": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"헬스 체크 실패: {e}")

if __name__ == "__main__":
    import uvicorn
    
    # 환경변수에서 호스트와 포트 읽기
    host = os.getenv('API_HOST', '127.0.0.1')
    port = int(os.getenv('API_PORT', '8000'))
    
    uvicorn.run(app, host=host, port=port)