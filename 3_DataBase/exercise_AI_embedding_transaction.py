"""
AI 임베딩 + PostgreSQL 트랜잭션 시스템

실습 시나리오:
1. 사용자가 설계안 텍스트(CSV의 description)를 입력
2. 해당 텍스트에 대해 Python에서 AI 임베딩을 수행
3. 임베딩 결과가 유효할 경우 design 테이블에 등록 (COMMIT)
4. 실패하면 아무 데이터도 등록하지 않음 (ROLLBACK)
5. PostgreSQL + pgvector 확장 사용
6. Python에서 psycopg2 + 임베딩 처리

기술 스택:
- AI 모델: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (한국어 지원)
- 데이터베이스: PostgreSQL + pgvector 확장
- Python 라이브러리: psycopg2, sentence-transformers, pandas, python-dotenv
- 데이터: sample_designs_500.csv (500개 설계안)
- 환경변수: .env 파일로 데이터베이스 연결 정보 관리

설치 요구사항:
1. pip install psycopg2-binary sentence-transformers torch pandas python-dotenv
2. PostgreSQL + pgvector 확장 설치
3. .env 파일에 데이터베이스 연결 정보 설정

.env 파일 예시:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
"""

# PostgreSQL 데이터베이스 연결을 위한 라이브러리
import psycopg2
# CSV 파일 읽기 및 데이터 조작을 위한 pandas 라이브러리
import pandas as pd
# AI 임베딩 모델을 사용하기 위한 sentence-transformers 라이브러리
from sentence_transformers import SentenceTransformer
# JSON 데이터 처리를 위한 라이브러리 (사용하지 않지만 임포트됨)
import json
# 수치 연산을 위한 NumPy 라이브러리 (사용하지 않지만 임포트됨)
import numpy as np
# 정규 표현식 처리를 위한 re 라이브러리 (사용하지 않지만 임포트됨)
import re
# 운영체제 환경변수 접근을 위한 os 라이브러리
import os
# .env 파일에서 환경변수를 로드하기 위한 python-dotenv 라이브러리
from dotenv import load_dotenv

# .env 파일에서 환경변수를 시스템 환경변수로 로드
# 이 함수는 .env 파일의 KEY=VALUE 형태를 읽어 os.getenv()로 접근 가능하게 함
load_dotenv()

# PostgreSQL 데이터베이스 연결 설정 정보를 환경변수에서 가져오기
# 보안상 민감한 정보(비밀번호 등)는 코드에 직접 하드코딩하지 않고 .env 파일에서 관리
DB_CONFIG = {
    # DB_HOST 환경변수 값, 없으면 기본값 "localhost" 사용
    "host": os.getenv("DB_HOST", "localhost"),
    # DB_PORT 환경변수 값을 정수로 변환, 없으면 기본값 5432 사용
    "port": int(os.getenv("DB_PORT", 5432)),
    # DB_NAME 환경변수 값, 없으면 기본값 "postgres" 사용
    "dbname": os.getenv("DB_NAME", "postgres"),
    # DB_USER 환경변수 값, 없으면 기본값 "postgres" 사용
    "user": os.getenv("DB_USER", "postgres"),
    # DB_PASSWORD 환경변수 값 (기본값 없음 - 반드시 .env에서 설정해야 함)
    "password": os.getenv("DB_PASSWORD")
}

class AIEmbeddingProcessor:
    """
    AI 임베딩과 PostgreSQL 트랜잭션을 처리하는 메인 클래스
    
    주요 기능:
    1. 한국어 지원 임베딩 모델 로딩
    2. PostgreSQL + pgvector 확장을 사용한 벡터 저장
    3. 각 설계안마다 개별 트랜잭션 처리 (COMMIT/ROLLBACK)
    4. 에러 발생시 자동 재시도 및 폴백 처리
    """
    
    def __init__(self):
        # 한국어 지원 임베딩 모델 로드 (첫 실행시 자동 다운로드됨)
        # 384차원 벡터 생성, 다국어 지원 모델 사용
        print("임베딩 모델을 로딩 중입니다...")  # 사용자에게 로딩 시작 알림
        # sentence-transformers 라이브러리로 사전 훈련된 다국어 임베딩 모델 로드
        # 'paraphrase-multilingual-MiniLM-L12-v2': 한국어 포함 104개 언어 지원 모델
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        print("모델 로딩 완료!")  # 사용자에게 로딩 완료 알림
        
    def create_database_table(self):
        """
        PostgreSQL 데이터베이스에 design 테이블 생성
        
        주요 기능:
        - pgvector 확장 활성화 (벡터 데이터 타입 지원)
        - design 테이블 생성 (id, title, description, embedding, created_at)
        - embedding 컬럼은 384차원 vector 타입으로 정의
        """
        try:
            # psycopg2를 사용하여 PostgreSQL 데이터베이스에 연결 시도
            conn = psycopg2.connect(**DB_CONFIG)  # DB_CONFIG 딕셔너리를 언패킹하여 연결 정보 전달
            cur = conn.cursor()  # SQL 쿼리 실행을 위한 커서 객체 생성
            
            # pgvector 확장 생성 (벡터 데이터 타입 지원을 위해 필요)
            # IF NOT EXISTS: 이미 존재하면 무시하고 계속 진행
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            
            # design 테이블 생성 SQL 쿼리 정의
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS design (
                id SERIAL PRIMARY KEY,           -- 자동 증가하는 기본키
                title VARCHAR(255) NOT NULL,     -- 설계안 제목 (최대 255자, 필수값)
                description TEXT NOT NULL,       -- 설계안 설명 (긴 텍스트, 필수값)
                embedding vector(384),           -- 384차원 벡터 (pgvector 확장 타입)
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 생성 시간 (기본값: 현재 시간)
            );
            """
            # 테이블 생성 쿼리 실행
            cur.execute(create_table_sql)
            
            # 트랜잭션 커밋 (변경사항을 데이터베이스에 영구 저장)
            conn.commit()
            # 커서 닫기 (메모리 해제)
            cur.close()
            # 연결 닫기 (연결 해제)
            conn.close()
            
            # 성공 메시지 출력
            print("✅ design 테이블 생성 완료 (pgvector 확장 포함)")
            return True  # 성공 시 True 반환
            
        except Exception as e:
            # 오류 발생시 에러 메시지 출력
            print(f"❌ 테이블 생성 실패: {e}")
            return False  # 실패 시 False 반환
    
    def insert_design_with_transaction(self, title, description, embedding):
        """
        개별 설계안을 트랜잭션으로 DB에 저장
        
        트랜잭션 처리:
        - 임베딩 유효성 검사 (384차원 확인)
        - 유효한 경우: INSERT 후 COMMIT
        - 실패한 경우: 자동 ROLLBACK
        - 각 설계안마다 독립적인 트랜잭션 처리
        """
        conn = None  # 연결 객체 초기화 (finally 블록에서 안전하게 닫기 위함)
        try:
            # PostgreSQL 데이터베이스에 연결
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()  # SQL 실행을 위한 커서 생성
            
            # 임베딩 벡터의 유효성 검사
            # embedding이 None이 아니고 정확히 384차원인지 확인
            if not embedding or len(embedding) != 384:
                # 유효하지 않으면 ValueError 예외 발생시켜 롤백 유도
                raise ValueError(f"유효하지 않은 임베딩: 차원={len(embedding) if embedding else 0}")
            
            # INSERT 쿼리 정의 (RETURNING id로 생성된 ID 반환받음)
            insert_sql = """
            INSERT INTO design (title, description, embedding) 
            VALUES (%s, %s, %s)
            RETURNING id;
            """
            
            # 매개변수화된 쿼리 실행 (SQL 인젝션 방지)
            # %s는 psycopg2가 안전하게 값을 바인딩함
            cur.execute(insert_sql, (title, description, embedding))
            # INSERT 결과로 반환된 ID 값 가져오기
            design_id = cur.fetchone()[0]
            
            # 트랜잭션 커밋 (데이터를 영구 저장)
            conn.commit()
            cur.close()  # 커서 닫기
            conn.close()  # 연결 닫기
            
            # 성공 메시지 출력 (COMMIT 완료 알림)
            print(f"✅ COMMIT: 설계안 '{title}' 저장 완료 (ID: {design_id})")
            return design_id  # 생성된 ID 반환
            
        except Exception as e:
            # 오류 발생시 롤백 처리
            if conn:
                conn.rollback()  # 트랜잭션 롤백 (변경사항 취소)
                conn.close()     # 연결 닫기
            # 실패 메시지 출력 (ROLLBACK 완료 알림)
            print(f"❌ ROLLBACK: 설계안 '{title}' 저장 실패 - {e}")
            return None  # 실패시 None 반환
    
    def create_embedding(self, text):
        """
        AI 모델을 사용하여 텍스트를 384차원 임베딩 벡터로 변환
        
        처리 과정:
        1. sentence-transformers 모델로 텍스트 인코딩
        2. numpy array를 Python list로 변환
        3. 384차원 벡터 반환
        
        사용 모델: paraphrase-multilingual-MiniLM-L12-v2 (한국어 지원)
        """
        try:
            # sentence-transformers 모델을 사용하여 텍스트를 벡터로 인코딩
            # 입력: 문자열 텍스트, 출력: 384차원 numpy 배열
            embedding = self.model.encode(text)
            
            # numpy array를 Python list로 변환 (JSON 직렬화 가능하게 만듦)
            # PostgreSQL에 저장하기 위해서는 list 형태여야 함
            embedding_list = embedding.tolist()
            
            return embedding_list  # 384개 실수로 구성된 리스트 반환
            
        except Exception as e:
            # 임베딩 생성 중 오류 발생시 에러 메시지 출력
            print(f"임베딩 생성 실패: {e}")
            return None  # 실패시 None 반환
    
    def load_csv_data(self):
        """
        설계안 데이터가 담긴 CSV 파일을 pandas DataFrame으로 로드
        
        파일 정보:
        - 파일명: sample_designs_500.csv
        - 컬럼: title, description, embedding
        - 총 500개의 설계안 데이터
        """
        try:
            # pandas 라이브러리를 사용하여 CSV 파일을 DataFrame으로 읽기
            # 절대 경로로 파일 위치 지정
            df = pd.read_csv('/Users/ichangmin/MyDrive/SKALA/SKALA/3_DataBase/file/sample_designs_500.csv')
            # 성공 메시지와 함께 로드된 데이터의 행 개수 출력
            print(f"CSV 파일 로딩 완료 - 총 {len(df)}개 행")
            return df  # DataFrame 객체 반환
            
        except Exception as e:
            # 파일 읽기 실패시 오류 메시지 출력
            print(f"CSV 파일 로딩 실패: {e}")
            return None  # 실패시 None 반환
    
    def process_and_save_all_designs(self, limit=None):
        """
        전체 프로세스의 메인 함수 - CSV 데이터를 읽어 임베딩 생성 후 DB 저장
        
        처리 단계:
        1. CSV 파일에서 설계안 데이터 로드
        2. PostgreSQL 테이블 생성 (pgvector 확장 포함)
        3. 각 설계안에 대해 순차 처리:
           - description을 AI 임베딩으로 변환
           - 성공시 DB에 저장 후 COMMIT
           - 실패시 ROLLBACK
        4. 최종 통계 출력 (성공/실패 개수, 성공률)
        
        Args:
            limit: 처리할 데이터 개수 제한 (None이면 전체 처리)
        """
        # CSV 데이터 로드 함수 호출
        df = self.load_csv_data()
        # 데이터 로드 실패시 함수 종료
        if df is None:
            return
        
        # PostgreSQL 테이블 생성 함수 호출
        # pgvector 확장과 design 테이블 생성
        if not self.create_database_table():
            return  # 테이블 생성 실패시 함수 종료
        
        # 처리할 데이터 개수 결정
        # limit이 None이면 전체 데이터 처리, 아니면 제한된 개수만 처리
        total_count = len(df) if limit is None else min(limit, len(df))
        
        # 처리 시작 알림 메시지
        print(f"\n=== {total_count}개 설계안 처리 및 DB 저장 시작 ===")
        
        # 성공/실패 카운터 초기화
        success_count = 0  # 성공적으로 저장된 설계안 개수
        fail_count = 0     # 실패한 설계안 개수
        
        # 각 설계안을 순차적으로 처리하는 반복문
        for i in range(total_count):
            # 현재 처리 중인 설계안 번호 출력
            print(f"\n--- 처리 중: {i+1}/{total_count} ---")
            
            try:
                # DataFrame에서 i번째 행의 'title' 컬럼 값을 문자열로 변환 후 공백 제거
                title = str(df.iloc[i]['title']).strip()
                # DataFrame에서 i번째 행의 'description' 컬럼 값을 문자열로 변환 후 공백 제거
                description = str(df.iloc[i]['description']).strip()
                
                # 처리 중인 설계안 정보 출력
                print(f"Title: {title}")
                # description의 처음 100자만 출력 (너무 길면 ...으로 표시)
                print(f"Description: {description[:100]}...")
                
                # 1. AI 임베딩 생성 (description 텍스트를 384차원 벡터로 변환)
                embedding = self.create_embedding(description)
                
                # 임베딩 생성 성공 여부 확인
                if embedding:
                    # 임베딩이 성공적으로 생성된 경우
                    print(f"임베딩 생성 성공 (차원: {len(embedding)})")
                    
                    # 2. DB에 저장 (개별 트랜잭션 처리)
                    # 성공시 COMMIT, 실패시 자동 ROLLBACK
                    design_id = self.insert_design_with_transaction(title, description, embedding)
                    
                    # DB 저장 결과에 따라 카운터 증가
                    if design_id:
                        success_count += 1  # 저장 성공
                    else:
                        fail_count += 1     # 저장 실패
                else:
                    # 임베딩 생성이 실패한 경우
                    print("❌ 임베딩 생성 실패 - DB 저장 건너뛰기")
                    fail_count += 1  # 실패 카운터 증가
                    
            except Exception as row_error:
                # 특정 행 처리 중 예상치 못한 오류 발생시
                print(f"❌ 행 처리 실패: {row_error}")
                fail_count += 1  # 실패 카운터 증가
            
            # 각 설계안 처리 완료 후 구분선 출력
            print("-" * 60)
        
        # 최종 처리 결과 통계 출력
        print(f"\n=== 전체 처리 완료 ===")
        print(f"✅ 성공: {success_count}개")  # 성공적으로 저장된 설계안 개수
        print(f"❌ 실패: {fail_count}개")    # 실패한 설계안 개수
        # 성공률 계산 및 출력 (소수점 첫째자리까지)
        print(f"📊 성공률: {success_count/total_count*100:.1f}%")

def main():
    """
    메인 실행 함수
    
    전체 실행 흐름:
    1. AIEmbeddingProcessor 초기화 (AI 모델 로딩)
    2. CSV 파일의 모든 설계안 처리 (500개)
    3. 각 설계안마다 임베딩 생성 및 DB 저장
    4. 트랜잭션 방식으로 데이터 무결성 보장
    
    최종 결과: PostgreSQL DB에 임베딩이 포함된 설계안 데이터 저장
    """
    # 사용자에게 프로그램 시작을 알리는 메시지 출력
    print("=== AI 임베딩 + PostgreSQL 트랜잭션 시스템 ===\n")
    
    # 환경변수 로딩 상태 확인 및 출력
    print("📋 환경변수 로딩 상태 확인:")
    print(f"  - DB Host: {os.getenv('DB_HOST', 'localhost')}")
    print(f"  - DB Port: {os.getenv('DB_PORT', '5432')}")
    print(f"  - DB Name: {os.getenv('DB_NAME', 'postgres')}")
    print(f"  - DB User: {os.getenv('DB_USER', 'postgres')}")
    # 보안상 비밀번호는 마스킹하여 표시 (실제 값이 있는지만 확인)
    db_password = os.getenv('DB_PASSWORD')
    if db_password:
        print(f"  - DB Password: {'*' * len(db_password)} (로딩됨)")
    else:
        print("  - DB Password: ❌ 설정되지 않음")
    print()
    
    # AIEmbeddingProcessor 클래스의 인스턴스 생성
    # 이때 __init__ 메서드가 호출되어 AI 모델이 로딩됨
    processor = AIEmbeddingProcessor()
    
    # 모든 설계안 처리 및 DB 저장 메서드 호출 (전체 500개 처리)
    # limit 매개변수 제거로 전체 데이터 처리
    processor.process_and_save_all_designs()
    
    # 전체 프로세스 완료 메시지 출력
    print("\n🎉 전체 프로세스 완료!")
    # 사용자에게 결과 확인 방법 안내
    print("📋 결과 확인: pgAdmin4에서 design 테이블 조회 가능")

if __name__ == "__main__":
    # 스크립트가 직접 실행될 때만 main() 함수 호출
    # 모듈로 import될 때는 실행되지 않음
    main()