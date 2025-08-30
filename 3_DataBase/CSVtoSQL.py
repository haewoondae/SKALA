import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np

# .env 파일 로드
load_dotenv()

# 1단계: CSV 데이터 로드 및 DataFrame 정제
print("1단계: CSV 파일 로드 중...")
df = pd.read_csv('/Users/ichangmin/MyDrive/SKALA/SKALA/3_DataBase/file/user_behavior.csv')

# 데이터 기본 정보 확인
print(f"데이터 형태: {df.shape}")
print(f"컬럼명: {df.columns.tolist()}")
print("\n데이터 미리보기:")
print(df.head())

# 데이터 정제 (필요시)
df = df.dropna()  # 결측값 제거
print(f"정제 후 데이터 형태: {df.shape}")

# 2단계: PostgreSQL 연결 설정
print("\n2단계: PostgreSQL 연결 설정...")

# .env 파일에서 DB 연결 정보 가져오기
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

# 테이블 생성 SQL
create_table_sql = """
CREATE TABLE IF NOT EXISTS user_behavior (
    user_id VARCHAR(10) PRIMARY KEY,
    age INTEGER,
    income INTEGER,
    gender VARCHAR(1),
    spending_score INTEGER,
    visit_count INTEGER
);
"""

# 임베딩 테이블 생성 SQL (pgvector 확장 포함)
create_embedding_table_sql = """
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS user_embeddings (
    user_id VARCHAR(10) PRIMARY KEY,
    embedding vector(2)
);
"""

# INSERT 쿼리 정의
insert_sql = """
INSERT INTO user_behavior (user_id, age, income, gender, spending_score, visit_count)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO NOTHING;
"""

# 3단계: 테이블 생성 및 데이터 적재
print("\n3단계: 테이블 생성 및 PostgreSQL에 데이터 적재 중...")

conn = None
try:
    # psycopg2로 직접 연결
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # pgvector 확장 및 임베딩 테이블 생성
    cur.execute(create_embedding_table_sql)
    print("✅ pgvector 확장 및 user_embeddings 테이블이 생성되었습니다.")
    
    # user_behavior 테이블 생성
    cur.execute(create_table_sql)
    print("✅ user_behavior 테이블이 생성되었습니다.")
    
    # 데이터 삽입 카운터
    success_count = 0
    fail_count = 0
    
    # DataFrame의 각 행을 순회하며 INSERT 실행
    for index, row in df.iterrows():
        try:
            # 각 행의 데이터를 튜플로 변환
            data = (
                str(row['user_id']),
                int(row['age']),
                int(row['income']),
                str(row['gender']),
                int(row['spending_score']),
                int(row['visit_count'])
            )
            
            # INSERT 쿼리 실행
            cur.execute(insert_sql, data)
            success_count += 1
            
            # 100개마다 진행상황 출력
            if (index + 1) % 100 == 0:
                print(f"진행중... {index + 1}/{len(df)} 레코드 처리 완료")
                
        except Exception as row_error:
            print(f"❌ 행 {index} 처리 실패: {row_error}")
            fail_count += 1
    
    # 모든 변경사항 커밋
    conn.commit()
    print(f"✅ 성공적으로 {success_count}개 레코드가 'user_behavior' 테이블에 적재되었습니다.")
    if fail_count > 0:
        print(f"⚠️  {fail_count}개 레코드 적재 실패")
    
    # 4단계: PostgreSQL에서 AI 분석에 필요한 필드 추출
    print("\n4단계: PostgreSQL에서 AI 분석에 필요한 필드 추출 중...")
    
    # 수치형 데이터만 추출하는 쿼리
    cur.execute("""
        SELECT user_id, age, income, spending_score, visit_count 
        FROM user_behavior 
        ORDER BY user_id
    """)
    
    # 결과를 DataFrame으로 변환
    columns = ['user_id', 'age', 'income', 'spending_score', 'visit_count']
    extracted_data = cur.fetchall()
    df_extracted = pd.DataFrame(extracted_data, columns=columns)
    
    print(f"추출된 데이터 형태: {df_extracted.shape}")
    print("추출된 데이터 미리보기:")
    print(df_extracted.head())
    
    # 5단계: PCA, 클러스터링, pgvector 처리
    print("\n5단계: PCA로 벡터화 및 임베딩 테이블에 저장 중...")
    
    # 수치형 컬럼만 선택 (user_id 제외)
    X = df_extracted[['age', 'income', 'spending_score', 'visit_count']].values
    
    # 표준화 (StandardScaler)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print("✅ 데이터 표준화 완료")
    
    # PCA로 2차원 임베딩 생성
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    print("✅ PCA 2차원 변환 완료")
    print(f"PCA 설명 가능 분산비: {pca.explained_variance_ratio_}")
    print(f"총 설명 가능 분산: {sum(pca.explained_variance_ratio_):.3f}")
    
    # 임베딩을 리스트 형태로 변환
    df_extracted['embedding'] = [list(v) for v in X_pca]
    
    print("\nPCA 결과 미리보기:")
    print(df_extracted[['user_id', 'embedding']].head())
    
    # 임베딩 데이터를 user_embeddings 테이블에 저장
    print("\n임베딩 데이터를 user_embeddings 테이블에 저장 중...")
    embedding_insert_count = 0
    embedding_fail_count = 0
    
    for uid, vec in zip(df_extracted['user_id'], df_extracted['embedding']):
        try:
            cur.execute("""
                INSERT INTO user_embeddings (user_id, embedding)
                VALUES (%s, %s)
                ON CONFLICT (user_id) DO UPDATE SET embedding = EXCLUDED.embedding;
            """, (uid, vec))
            embedding_insert_count += 1
            
            # 100개마다 진행상황 출력
            if embedding_insert_count % 100 == 0:
                print(f"임베딩 저장 진행중... {embedding_insert_count}/{len(df_extracted)} 완료")
                
        except Exception as e:
            print(f"❌ 임베딩 저장 실패 (user_id: {uid}): {e}")
            embedding_fail_count += 1
    
    # 임베딩 저장 커밋
    conn.commit()
    print(f"✅ 성공적으로 {embedding_insert_count}개 사용자 임베딩이 저장되었습니다.")
    if embedding_fail_count > 0:
        print(f"⚠️  {embedding_fail_count}개 임베딩 저장 실패")
    
    # 최종 결과 확인
    print("\n=== 최종 결과 확인 ===")
    
    # user_behavior 테이블 데이터 개수 확인
    cur.execute("SELECT COUNT(*) FROM user_behavior")
    behavior_count = cur.fetchone()[0]
    print(f"user_behavior 테이블의 총 레코드 수: {behavior_count}")
    
    # user_embeddings 테이블 데이터 개수 확인
    cur.execute("SELECT COUNT(*) FROM user_embeddings")
    embedding_count = cur.fetchone()[0]
    print(f"user_embeddings 테이블의 총 레코드 수: {embedding_count}")
    
    # 샘플 데이터 조회
    cur.execute("SELECT * FROM user_behavior LIMIT 3")
    sample_behavior = cur.fetchall()
    print("\n샘플 user_behavior 데이터:")
    for row in sample_behavior:
        print(row)
    
    # 샘플 임베딩 데이터 조회
    cur.execute("SELECT user_id, embedding FROM user_embeddings LIMIT 3")
    sample_embeddings = cur.fetchall()
    print("\n샘플 user_embeddings 데이터:")
    for row in sample_embeddings:
        print(f"User ID: {row[0]}, Embedding: {row[1]}")
    
    # 벡터 유사도 검색 예시 (더 의미 있는 방식들)
    print("\n=== 벡터 유사도 검색 예시 ===")
    
    # 1) 특정 사용자(U0001)와 가장 유사한 사용자들 (유클리디안 거리)
    cur.execute("""
        SELECT u1.user_id, u1.embedding,
               u1.embedding <-> u2.embedding AS euclidean_distance
        FROM user_embeddings u1, user_embeddings u2
        WHERE u2.user_id = 'U0001'
          AND u1.user_id != 'U0001'
        ORDER BY euclidean_distance
        LIMIT 3;
    """)
    similar_to_u0001 = cur.fetchall()
    print("📏 U0001과 가장 유사한 사용자들 (유클리디안 거리 기준):")
    for row in similar_to_u0001:
        print(f"User ID: {row[0]}, Euclidean Distance: {row[2]:.4f}")
    
    # 2) 특정 사용자(U0001)와 가장 유사한 사용자들 (코사인 유사도)
    cur.execute("""
        SELECT u1.user_id, u1.embedding,
               u1.embedding <=> u2.embedding AS cosine_distance,
               1 - (u1.embedding <=> u2.embedding) AS cosine_similarity
        FROM user_embeddings u1, user_embeddings u2
        WHERE u2.user_id = 'U0001'
          AND u1.user_id != 'U0001'
        ORDER BY cosine_distance
        LIMIT 3;
    """)

    cosine_similar_to_u0001 = cur.fetchall()
    print("\n📐 U0001과 가장 유사한 사용자들 (코사인 유사도 기준):")
    for row in cosine_similar_to_u0001:
        print(f"User ID: {row[0]}, Cosine Similarity: {row[3]:.4f}, Cosine Distance: {row[2]:.4f}")

    
    # 커서 및 연결 종료
    cur.close()

except Exception as e:
    print(f"❌ 오류 발생: {e}")
    if conn:
        conn.rollback()  # 오류 시 롤백
    
finally:
    # 연결 종료
    if conn:
        conn.close()
    print("\n✅ 모든 작업이 완료되었습니다. 데이터베이스 연결이 종료되었습니다.")