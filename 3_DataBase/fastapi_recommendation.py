from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv
from typing import List, Dict

# 환경변수 로드
load_dotenv()

app = FastAPI(title="User Recommendation System")

# DB 연결 설정
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

# 요청/응답 모델
class RecommendRequest(BaseModel):
    user_id: str
    limit: int = 5

class SimilarUser(BaseModel):
    user_id: str
    similarity: float
    age: int
    income: int
    gender: str
    spending_score: int
    visit_count: int

def get_db():
    return psycopg2.connect(**DB_CONFIG)

@app.get("/")
def root():
    return {"message": "User Recommendation API"}

@app.post("/recommend/euclidean", response_model=List[SimilarUser])
def recommend_euclidean(request: RecommendRequest):
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT u1.user_id,
                   1 / (1 + (u1.embedding <-> u2.embedding)) AS similarity,
                   ub.age, ub.income, ub.gender, ub.spending_score, ub.visit_count
            FROM user_embeddings u1, user_embeddings u2
            JOIN user_behavior ub ON u1.user_id = ub.user_id
            WHERE u2.user_id = %s AND u1.user_id != %s
            ORDER BY u1.embedding <-> u2.embedding
            LIMIT %s;
        """, (request.user_id, request.user_id, request.limit))
        
        results = cur.fetchall()
        return [SimilarUser(
            user_id=row[0], similarity=float(row[1]), age=row[2],
            income=row[3], gender=row[4], spending_score=row[5], visit_count=row[6]
        ) for row in results]
    finally:
        conn.close()

@app.post("/recommend/cosine", response_model=List[SimilarUser])
def recommend_cosine(request: RecommendRequest):
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT u1.user_id,
                   1 - (u1.embedding <=> u2.embedding) AS similarity,
                   ub.age, ub.income, ub.gender, ub.spending_score, ub.visit_count
            FROM user_embeddings u1, user_embeddings u2
            JOIN user_behavior ub ON u1.user_id = ub.user_id
            WHERE u2.user_id = %s AND u1.user_id != %s
            ORDER BY u1.embedding <=> u2.embedding
            LIMIT %s;
        """, (request.user_id, request.user_id, request.limit))
        
        results = cur.fetchall()
        return [SimilarUser(
            user_id=row[0], similarity=float(row[1]), age=row[2],
            income=row[3], gender=row[4], spending_score=row[5], visit_count=row[6]
        ) for row in results]
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    api_host = os.getenv("API_HOST", "127.0.0.1")
    api_port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host=api_host, port=api_port)