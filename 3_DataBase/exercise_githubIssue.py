import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubIssueProcessor:
    def __init__(self):
        load_dotenv()
        self.model = None
        self.conn = None
        
    def load_embedding_model(self):
        """임베딩 모델 로드"""
        try:
            logger.info("임베딩 모델 로딩 중...")
            self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            logger.info("임베딩 모델 로딩 완료")
        except Exception as e:
            logger.error(f"모델 로딩 실패: {e}")
            raise
    
    def connect_db(self):
        """데이터베이스 연결"""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME', 'postgres'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', '')
            )
            logger.info("데이터베이스 연결 성공")
        except Exception as e:
            logger.error(f"데이터베이스 연결 실패: {e}")
            raise
    
    def load_csv_data(self, file_path):
        """CSV 파일 로드 및 전처리"""
        try:
            logger.info(f"CSV 파일 로딩: {file_path}")
            df = pd.read_csv(file_path)
            
            # 기본 정보 출력
            logger.info(f"데이터 shape: {df.shape}")
            logger.info(f"컬럼: {df.columns.tolist()}")
            
            # 결측값 처리
            df = df.dropna(subset=['title', 'description'])
            
            # 텍스트 전처리
            df['title'] = df['title'].astype(str).str.strip()
            df['description'] = df['description'].astype(str).str.strip()
            
            # 빈 문자열 제거
            df = df[(df['title'] != '') & (df['description'] != '')]
            
            logger.info(f"전처리 후 데이터 shape: {df.shape}")
            
            return df
            
        except Exception as e:
            logger.error(f"CSV 로딩 실패: {e}")
            raise
    
    def create_embeddings(self, df):
        """이슈 데이터에 대한 임베딩 생성"""
        try:
            logger.info("임베딩 생성 시작...")
            
            # 제목과 설명을 결합하여 임베딩 생성
            combined_text = df['title'] + ' ' + df['description']
            
            # 배치 처리로 임베딩 생성 (메모리 효율성)
            batch_size = 32
            embeddings = []
            
            for i in range(0, len(combined_text), batch_size):
                batch = combined_text[i:i+batch_size].tolist()
                batch_embeddings = self.model.encode(batch, show_progress_bar=True)
                embeddings.extend(batch_embeddings)
            
            df['embedding'] = embeddings
            logger.info(f"임베딩 생성 완료: {len(embeddings)}개")
            
            return df
            
        except Exception as e:
            logger.error(f"임베딩 생성 실패: {e}")
            raise
    
    def setup_database(self):
        """데이터베이스 테이블 설정"""
        try:
            with self.conn.cursor() as cur:
                # pgvector 확장 활성화
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                
                # 기존 테이블 삭제 및 재생성
                cur.execute("DROP TABLE IF EXISTS issues;")
                
                cur.execute("""
                CREATE TABLE issues (
                    id SERIAL PRIMARY KEY,
                    issue_id VARCHAR(50),
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    tags TEXT,
                    embedding vector(384),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """)
                
                # 벡터 유사도 검색을 위한 인덱스 생성
                cur.execute("""
                CREATE INDEX ON issues 
                USING ivfflat (embedding vector_cosine_ops);
                """)
                
                self.conn.commit()
                logger.info("데이터베이스 테이블 설정 완료")
                
        except Exception as e:
            logger.error(f"데이터베이스 설정 실패: {e}")
            self.conn.rollback()
            raise
    
    def save_to_database(self, df):
        """데이터베이스에 이슈 데이터 저장"""
        try:
            logger.info("데이터베이스에 데이터 저장 중...")
            
            with self.conn.cursor() as cur:
                # 데이터 준비
                data_to_insert = []
                for _, row in df.iterrows():
                    data_to_insert.append((
                        row.get('issue_id', ''),
                        row['title'],
                        row['description'],
                        row.get('tags', ''),
                        row['embedding'].tolist()  # 벡터를 리스트로 변환
                    ))
                
                # 배치 삽입
                execute_values(
                    cur,
                    """
                    INSERT INTO issues (issue_id, title, description, tags, embedding)
                    VALUES %s
                    """,
                    data_to_insert,
                    template=None,
                    page_size=100
                )
                
                self.conn.commit()
                logger.info(f"데이터베이스에 {len(data_to_insert)}개 레코드 저장 완료")
                
        except Exception as e:
            logger.error(f"데이터베이스 저장 실패: {e}")
            self.conn.rollback()
            raise
    
    def process_issues(self, csv_file_path):
        """전체 이슈 처리 파이프라인"""
        try:
            # 1. 모델 로드
            self.load_embedding_model()
            
            # 2. 데이터베이스 연결
            self.connect_db()
            
            # 3. 데이터베이스 설정
            self.setup_database()
            
            # 4. CSV 데이터 로드
            df = self.load_csv_data(csv_file_path)
            
            # 5. 임베딩 생성
            df = self.create_embeddings(df)
            
            # 6. 데이터베이스 저장
            self.save_to_database(df)
            
            logger.info("이슈 처리 파이프라인 완료!")
            
            return df
            
        except Exception as e:
            logger.error(f"이슈 처리 실패: {e}")
            raise
        finally:
            if self.conn:
                self.conn.close()

def main():
    """메인 실행 함수"""
    processor = GitHubIssueProcessor()
    
    # CSV 파일 경로 (실제 파일 위치에 맞게 수정)
    csv_file_path = "github_issues_large.csv"
    
    try:
        # 이슈 처리 실행
        df = processor.process_issues(csv_file_path)
        
        print("\n=== 처리 결과 요약 ===")
        print(f"총 처리된 이슈 수: {len(df)}")
        print(f"임베딩 차원: {len(df['embedding'].iloc[0])}")
        print("\n처리 완료!")
        
    except Exception as e:
        print(f"처리 중 오류 발생: {e}")

if __name__ == "__main__":
    main()