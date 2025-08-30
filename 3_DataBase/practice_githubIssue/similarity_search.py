import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
import re

# 환경변수 로드
load_dotenv()

class IssueSimilaritySearch:
    def __init__(self):
        # 임베딩 모델 초기화 (1단계와 동일한 모델 사용)
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
    
    def clean_text(self, text):
        """텍스트 정제 (1단계와 동일)"""
        if not text:
            return ""
        
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', str(text))
        # 연속된 공백 제거
        text = re.sub(r'\s+', ' ', text)
        # 앞뒤 공백 제거
        return text.strip()
    
    def generate_query_embedding(self, title, description=""):
        """새로운 이슈의 임베딩 생성"""
        # 텍스트 정제
        title = self.clean_text(title)
        description = self.clean_text(description)
        
        # title과 description 결합 (1단계와 동일한 방식)
        combined_text = title + ' ' + description
        
        print(f"검색 쿼리: {combined_text[:100]}...")
        
        # 임베딩 생성
        embedding = self.model.encode([combined_text])
        return embedding[0]
    
    def find_similar_issues(self, query_embedding, top_k=5, similarity_threshold=0.3):
        """유사한 이슈 검색 (수정된 버전)"""
        conn = self.connect_db()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            # 임베딩을 문자열로 변환하여 vector 타입으로 캐스팅
            embedding_str = '[' + ','.join(map(str, query_embedding.tolist())) + ']'
            
            # pgvector의 코사인 유사도 검색 사용 (명시적 타입 캐스팅)
            query = """
                SELECT id, title, description, 
                       1 - (embedding <=> %s::vector) as similarity
                FROM issues
                WHERE 1 - (embedding <=> %s::vector) >= %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
            """
            
            cursor.execute(query, (embedding_str, embedding_str, similarity_threshold, embedding_str, top_k))
            results = cursor.fetchall()
            
            return results
            
        except Exception as e:
            print(f"유사도 검색 실패: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def search_similar_issues(self, title, description="", top_k=5, similarity_threshold=0.3):
        """전체 검색 과정 (유연한 검색)"""
        print("=== 유사 이슈 검색 시작 ===")
        
        # 1. 쿼리 임베딩 생성
        query_embedding = self.generate_query_embedding(title, description)
        
        # 2. 유사한 이슈 검색 (임계값 적용)
        similar_issues = self.find_similar_issues(query_embedding, top_k, similarity_threshold)
        
        # 3. 결과가 없으면 임계값을 낮춰서 재검색
        if not similar_issues and similarity_threshold > 0.1:
            print(f"임계값 {similarity_threshold}에서 결과 없음. 임계값을 낮춰서 재검색...")
            similar_issues = self.find_similar_issues(query_embedding, top_k, 0.1)
        
        # 4. 그래도 결과가 없으면 임계값 없이 검색
        if not similar_issues:
            print("임계값 없이 상위 결과 검색...")
            similar_issues = self.find_similar_issues_no_threshold(query_embedding, top_k)
        
        # 5. 결과 출력
        if similar_issues:
            print(f"\n상위 {len(similar_issues)}개 유사 이슈:")
            print("-" * 80)
            
            for i, (issue_id, issue_title, issue_desc, similarity) in enumerate(similar_issues, 1):
                print(f"{i}. [ID: {issue_id}] 유사도: {similarity:.4f}")
                print(f"   제목: {issue_title}")
                print(f"   설명: {issue_desc[:100]}{'...' if len(issue_desc) > 100 else ''}")
                print("-" * 80)
        else:
            print("유사한 이슈를 찾을 수 없습니다.")
        
        return similar_issues
    
    def find_similar_issues_no_threshold(self, query_embedding, top_k=5):
        """임계값 없이 상위 결과만 반환"""
        conn = self.connect_db()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            # 임베딩을 문자열로 변환
            embedding_str = '[' + ','.join(map(str, query_embedding.tolist())) + ']'
            
            # 임계값 없이 상위 결과만
            query = """
                SELECT id, title, description, 
                       1 - (embedding <=> %s::vector) as similarity
                FROM issues
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
            """
            
            cursor.execute(query, (embedding_str, embedding_str, top_k))
            results = cursor.fetchall()
            
            return results
            
        except Exception as e:
            print(f"유사도 검색 실패: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def interactive_search(self):
        """대화형 검색 (개선된 버전)"""
        print("=== GitHub 이슈 유사도 검색 ===")
        print("종료하려면 'quit' 또는 'exit'를 입력하세요.")
        print("옵션: 임계값 설정 가능 (기본값: 0.3)\n")
        
        while True:
            try:
                # 사용자 입력 받기
                title = input("이슈 제목을 입력하세요: ").strip()
                
                if title.lower() in ['quit', 'exit', '종료']:
                    print("검색을 종료합니다.")
                    break
                
                if not title:
                    print("제목을 입력해주세요.")
                    continue
                
                description = input("이슈 설명을 입력하세요 (선택사항): ").strip()
                
                # 임계값 입력 (선택사항)
                threshold_input = input("유사도 임계값 (0.1-0.9, 기본값 0.3): ").strip()
                try:
                    threshold = float(threshold_input) if threshold_input else 0.3
                    threshold = max(0.1, min(0.9, threshold))  # 0.1-0.9 범위로 제한
                except:
                    threshold = 0.3
                
                # 검색 실행
                self.search_similar_issues(title, description, similarity_threshold=threshold)
                print("\n" + "="*80 + "\n")
                
            except KeyboardInterrupt:
                print("\n검색을 종료합니다.")
                break
            except Exception as e:
                print(f"오류 발생: {e}")

# 실행 코드
if __name__ == "__main__":
    searcher = IssueSimilaritySearch()
    
    # 예시 검색
    print("=== 예시 검색 ===")
    searcher.search_similar_issues(
        title="permission bugs", 
        description="access denied error",
        similarity_threshold=0.2  # 낮은 임계값으로 더 많은 결과
    )
    
    print("\n" + "="*80 + "\n")
    
    # 대화형 검색 시작
    searcher.interactive_search()