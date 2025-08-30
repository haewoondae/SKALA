import pandas as pd
import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer
import re
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

class IssueEmbeddingProcessor:
    def __init__(self):
        # 임베딩 모델 초기화 (384차원)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # DB 연결 정보
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password'),
            'port': os.getenv('DB_PORT', '5432')
        }
    
    def connect_db(self):
        """데이터베이스 연결"""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except Exception as e:
            print(f"DB 연결 실패: {e}")
            return None
    
    def setup_database(self):
        """데이터베이스 및 테이블 설정"""
        conn = self.connect_db()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            print("pgvector 확장 프로그램 설치 중...")
            # pgvector 확장 프로그램 설치
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            
            print("기존 테이블 삭제 및 새 테이블 생성 중...")
            # 기존 테이블 삭제
            cursor.execute("DROP TABLE IF EXISTS issues;")
            
            # 새 테이블 생성
            cursor.execute("""
                CREATE TABLE issues (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    embedding vector(384)
                );
            """)
            
            conn.commit()
            print("데이터베이스 설정 완료")
            return True
            
        except Exception as e:
            print(f"데이터베이스 설정 실패: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def load_csv_data(self, csv_path):
        """CSV 파일 로드"""
        print("CSV 파일 로딩 중...")
        try:
            df = pd.read_csv(csv_path)
            print(f"총 {len(df)}개의 이슈 로드 완료")
            return df
        except Exception as e:
            print(f"CSV 파일 로드 실패: {e}")
            return None
    
    def clean_text(self, text):
        """텍스트 정제"""
        if pd.isna(text):
            return ""
        
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', str(text))
        # 연속된 공백 제거
        text = re.sub(r'\s+', ' ', text)
        # 앞뒤 공백 제거
        return text.strip()
    
    def preprocess_data(self, df):
        """데이터 전처리"""
        print("데이터 전처리 중...")
        
        # 필수 컬럼 확인
        required_columns = ['title', 'description']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"필수 컬럼이 없습니다: {missing_columns}")
            return None
        
        # 텍스트 정제
        df['title'] = df['title'].apply(self.clean_text)
        df['description'] = df['description'].apply(self.clean_text)
        
        # title과 description 결합
        df['combined_text'] = df['title'] + ' ' + df['description']
        
        # 빈 텍스트 제거
        df = df[df['combined_text'].str.strip() != '']
        
        print(f"전처리 후 {len(df)}개의 이슈 남음")
        return df
    
    def generate_embeddings(self, texts):
        """텍스트 임베딩 생성"""
        print("임베딩 생성 중...")
        try:
            embeddings = self.model.encode(texts, show_progress_bar=True)
            print(f"임베딩 생성 완료: {embeddings.shape}")
            return embeddings
        except Exception as e:
            print(f"임베딩 생성 실패: {e}")
            return None
    
    def save_to_db(self, df, embeddings):
        """데이터베이스에 저장"""
        conn = self.connect_db()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            print("데이터베이스에 저장 중...")
            for i, (_, row) in enumerate(df.iterrows()):
                # 임베딩을 리스트로 변환
                embedding_list = embeddings[i].tolist()
                
                cursor.execute(
                    "INSERT INTO issues (title, description, embedding) VALUES (%s, %s, %s)",
                    (row['title'], row['description'], embedding_list)
                )
                
                if (i + 1) % 100 == 0:
                    print(f"{i + 1}개 저장 완료...")
            
            conn.commit()
            print(f"총 {len(df)}개 이슈 저장 완료")
            return True
            
        except Exception as e:
            print(f"저장 실패: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def verify_data(self):
        """저장된 데이터 확인"""
        conn = self.connect_db()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM issues;")
            count = cursor.fetchone()[0]
            print(f"데이터베이스에 저장된 이슈 개수: {count}")
            
            # 첫 번째 이슈 샘플 출력
            cursor.execute("SELECT id, title, description FROM issues LIMIT 1;")
            sample = cursor.fetchone()
            if sample:
                print(f"샘플 데이터 - ID: {sample[0]}, Title: {sample[1][:50]}...")
        
        except Exception as e:
            print(f"데이터 확인 실패: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def process_issues(self, csv_path):
        """전체 처리 과정"""
        print("=== GitHub 이슈 임베딩 처리 시작 ===")
        
        # 1. 데이터베이스 설정
        if not self.setup_database():
            print("데이터베이스 설정 실패")
            return
        
        # 2. CSV 로드
        df = self.load_csv_data(csv_path)
        if df is None:
            return
        
        # 3. 데이터 전처리
        df_cleaned = self.preprocess_data(df)
        if df_cleaned is None:
            return
        
        # 4. 임베딩 생성
        embeddings = self.generate_embeddings(df_cleaned['combined_text'].tolist())
        if embeddings is None:
            return
        
        # 5. DB 저장
        success = self.save_to_db(df_cleaned, embeddings)
        
        if success:
            # 6. 데이터 확인
            self.verify_data()
            print("=== 1단계 처리 완료! ===")
        else:
            print("=== 처리 중 오류 발생 ===")

# 실행 코드
if __name__ == "__main__":
    processor = IssueEmbeddingProcessor()
    
    # CSV 파일 경로 (파일이 있는 경로로 수정 필요)
    csv_path = "github_issues_large.csv"
    
    # CSV 파일 존재 확인
    if not os.path.exists(csv_path):
        print(f"CSV 파일을 찾을 수 없습니다: {csv_path}")
        print("github_issues_large.csv 파일을 현재 디렉토리에 위치시켜주세요.")
    else:
        processor.process_issues(csv_path)