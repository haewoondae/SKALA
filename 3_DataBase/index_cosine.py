"""
AI 설계안 벡터 검색 시스템 - 메인 실행 파일
PostgreSQL pgvector + FastAPI 기반 384차원 벡터 검색
"""

import uvicorn
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

def main():
    # 환경변수에서 설정 로드
    api_host = os.getenv("API_HOST", "127.0.0.1")
    api_port = int(os.getenv("API_PORT", 8000))
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "postgres")
    
    print("=" * 60)
    print("🚀 AI 설계안 벡터 검색 시스템 시작")
    print("=" * 60)
    print(f"📍 API 서버: http://{api_host}:{api_port}")
    print(f"📚 API 문서: http://{api_host}:{api_port}/docs")
    print(f"🔍 데이터베이스: {db_host}:{db_port}/{db_name}")
    print(f"🎯 최적화: lists=10, L2 거리 권장")
    print("=" * 60)
    print("\n주요 엔드포인트:")
    print(f"  • 기본 검색:     POST http://{api_host}:{api_port}/search/vector")
    print(f"  • 정확도 우선:   POST http://{api_host}:{api_port}/search/vector/accurate")
    print(f"  • 샘플 벡터:     GET  http://{api_host}:{api_port}/test/sample-vector")
    print(f"  • 시스템 상태:   GET  http://{api_host}:{api_port}/health")
    print(f"  • 성능 정보:     GET  http://{api_host}:{api_port}/info/performance")
    print("\n" + "=" * 60)
    
    try:
        # FastAPI 서버 시작
        uvicorn.run(
            "api_index_cosine:app",  # 모듈명:앱변수명
            host=api_host,
            port=api_port,
            reload=True,  # 개발환경에서 자동 리로드
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 서버 종료됨")
    except Exception as e:
        print(f"❌ 서버 시작 오류: {str(e)}")

if __name__ == "__main__":
    main()
