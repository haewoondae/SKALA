"""
간단한 Sentence Embedding 테스트 (PostgreSQL 없이)
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

def main():
    print("=== Sentence Embedding 테스트 시작 ===")
    
    # 1. 모델 로드
    print("모델 로딩 중...")
    try:
        model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
        print("✅ 모델 로드 성공!")
    except Exception as e:
        print(f"❌ 모델 로드 실패: {e}")
        return
    
    # 2. 리뷰 데이터 로드
    try:
        with open("reviews.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            reviews = data["reviews"] if "reviews" in data else data
        print(f"✅ 리뷰 데이터 로드 성공! ({len(reviews)}개)")
    except Exception as e:
        print(f"⚠️ JSON 파일 읽기 실패 ({e}), 샘플 데이터 사용")
        # 파일이 없으면 샘플 데이터 사용
        reviews = [
            "배송이 빠르고 제품도 좋아요.",
            "품질이 기대 이상입니다!",
            "생각보다 배송이 오래 걸렸어요.",
            "배송은 느렸지만 포장은 안전했어요.",
            "아주 만족스러운 제품입니다.",
            "배송이 정말 빨라서 놀랐어요",
            "상품 품질이 좋네요",
            "포장상태가 완벽했습니다"
        ]
        print(f"📝 샘플 데이터 사용 ({len(reviews)}개)")
    
    # 3. 임베딩 생성
    print("임베딩 생성 중...")
    try:
        embeddings = model.encode(reviews, normalize_embeddings=True)
        print(f"✅ 임베딩 생성 완료! 형태: {embeddings.shape}")
    except Exception as e:
        print(f"❌ 임베딩 생성 실패: {e}")
        return
    
    # 4. 유사도 검색 테스트
    query = "배송이 빨라요"
    print(f"\n=== 검색 쿼리: '{query}' ===")
    
    try:
        query_embedding = model.encode([query], normalize_embeddings=True)
        
        # 코사인 유사도 계산
        similarities = cosine_similarity(query_embedding, embeddings)[0]
        
        # 상위 3개 결과
        top_indices = similarities.argsort()[-3:][::-1]
        
        print("🔍 상위 3개 유사한 리뷰:")
        for i, idx in enumerate(top_indices, 1):
            print(f"{i}. 유사도: {similarities[idx]:.4f} | {reviews[idx]}")
            
    except Exception as e:
        print(f"❌ 검색 실패: {e}")
        return
    
    print("\n✅ 테스트 완료!")

if __name__ == "__main__":
    main()
