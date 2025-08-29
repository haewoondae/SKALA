import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

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
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

# SQLAlchemy 엔진 생성
connection_string = f"postgresql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
engine = create_engine(connection_string)

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

# 3단계: 테이블 생성 및 데이터 적재
print("\n3단계: 테이블 생성 및 PostgreSQL에 데이터 적재 중...")

try:
    # 테이블 생성
    with engine.connect() as conn:
        conn.execute(text(create_table_sql))
        conn.commit()
        print("✅ user_behavior 테이블이 생성되었습니다.")
    
    # DataFrame을 PostgreSQL 테이블로 적재
    df.to_sql(
        name='user_behavior',
        con=engine,
        if_exists='append',  # 테이블이 이미 존재하므로 데이터만 추가
        index=False,  # 인덱스 컬럼 제외
        method='multi'  # 빠른 삽입을 위한 멀티 인서트
    )
    
    print(f"✅ 성공적으로 {len(df)}개 레코드가 'user_behavior' 테이블에 적재되었습니다.")
    
    # 4단계: 적재 결과 확인
    print("\n4단계: 적재 결과 확인...")
    
    # 적재된 데이터 개수 확인
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM user_behavior"))
        count = result.fetchone()[0]
        print(f"PostgreSQL 테이블 'user_behavior'의 총 레코드 수: {count}")
        
        # 샘플 데이터 조회
        result = conn.execute(text("SELECT * FROM user_behavior LIMIT 5"))
        sample_data = result.fetchall()
        print("\n샘플 데이터:")
        for row in sample_data:
            print(row)

except Exception as e:
    print(f"❌ 오류 발생: {e}")
    
finally:
    # 연결 종료
    engine.dispose()
    print("\n✅ 데이터베이스 연결이 종료되었습니다.")