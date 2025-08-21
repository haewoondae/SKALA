from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer

import psycopg2
import json
import os

# .env 파일 자동 로드
load_dotenv()

"""
I_WANT_TO_FIND 에 원하는 리뷰 문장을 넣으면 비슷한 리뷰를 찾아줍니다.
"""
# ===== 아래 입력 =====

I_WANT_TO_FIND = "배송이 빨라요"   # 원하는 질의 문장


# ===== 설정 =====


DB = dict(
    host=os.environ.get("PG_HOST"),
    port=int(os.environ.get("PG_PORT")),
    dbname=os.environ.get("PG_DBNAME"),
    user=os.environ.get("PG_USER"),
    password=os.environ.get("PG_PASSWORD"),
)

# 예시처럼 SQL을 문자열로 정의
SQL_CREATE_EXT = "CREATE EXTENSION IF NOT EXISTS vector;"
SQL_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS review_vectors (
  id        SERIAL PRIMARY KEY,
  review    TEXT,
  embedding VECTOR(384)      -- MiniLM-L6-v2 차원
);
"""

TRUNCATE_BEFORE_INSERT =True # 데모 반복 시 중복 방지용 

SQL_TRUNCATE = "TRUNCATE review_vectors;"

SQL_INSERT = "INSERT INTO review_vectors (review, embedding) VALUES (%s, %s)"
SQL_SEARCH_TOP3 = """
SELECT review,
       embedding <=> %s::vector AS distance,          -- 코사인 '거리'(작을수록 유사)
       1 - (embedding <=> %s::vector) AS similarity   -- 보기 좋은 '유사도'
FROM review_vectors
ORDER BY distance
LIMIT 3;
"""


# ===== 1) 모델 로드 + 데이터 로드 =====

model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")

with open("reviews.json", "r", encoding="utf-8") as f:
    reviews = json.load(f)["reviews"]

# 코사인 거리 안정화를 위해 정규화 권장
embs = model.encode(reviews, normalize_embeddings=True)  # (N, 384)

# ===== 2) DB 연결 및 스키마 준비 → 적재 =====

conn = psycopg2.connect(**DB)
cur = conn.cursor()

# 확장/테이블 생성 (예시 형식)
cur.execute(SQL_CREATE_EXT)
cur.execute(SQL_CREATE_TABLE)

if TRUNCATE_BEFORE_INSERT:
    cur.execute(SQL_TRUNCATE)

# 대량 입력은 executemany 사용
cur.executemany(SQL_INSERT, [(r, e.tolist()) for r, e in zip(reviews, embs)])
conn.commit()
print(f"Inserted {len(reviews)} rows into review_vectors.")

# ====== 3) 유사도 검색 (예시 형식) =====

query_text = I_WANT_TO_FIND              # 단어보다 문장형이 성능 좋음
qvec = model.encode([query_text], normalize_embeddings=True)[0].tolist()

cur.execute(SQL_SEARCH_TOP3, (qvec, qvec))

print(f"\n[쿼리] {query_text}")
for i, (rev, dist, sim) in enumerate(cur.fetchall(), 1):
    print(f"{i}. dist={dist:.4f} | sim={sim:.4f} | {rev}")

cur.close()
conn.close()