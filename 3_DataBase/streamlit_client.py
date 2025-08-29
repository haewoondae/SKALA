"""
Streamlit 기반 설계안 등록 웹 UI

주요 기능:
1. 사용자 친화적인 설계안 입력 폼
2. FastAPI 서버와 연동하여 설계안 등록
3. 실시간 등록 결과 확인
4. 임베딩 정보 표시

실행 방법:
streamlit run streamlit_client.py
"""

# Streamlit 웹 UI 프레임워크 - 파이썬으로 웹 애플리케이션 구축
import streamlit as st  # 대화형 웹 인터페이스 생성을 위한 메인 라이브러리
# HTTP 요청을 위한 requests 라이브러리 - FastAPI 서버와 통신
import requests  # RESTful API 호출을 위한 HTTP 클라이언트
# JSON 데이터 처리 - API 응답 데이터 파싱 및 직렬화
import json  # JavaScript Object Notation 형식 데이터 처리
# 시간 처리 - 진행 상태 표시용 대기 시간 구현
import time  # 시간 지연 및 측정 기능
# 날짜/시간 표시 - 현재 시간 표시 및 로그 타임스탬프
from datetime import datetime  # 날짜와 시간 객체 생성 및 포맷팅

# FastAPI 서버 URL 설정 - 백엔드 API 서버 주소
API_BASE_URL = "http://localhost:8000"  # 로컬 개발환경의 FastAPI 서버 주소

# Streamlit 페이지 설정 - 웹 페이지 메타데이터 및 레이아웃 구성
st.set_page_config(
    page_title="AI 설계안 등록 시스템",  # 브라우저 탭에 표시될 제목
    page_icon="🏗️",  # 브라우저 탭 아이콘 (이모지)
    layout="wide",  # 페이지 레이아웃을 넓게 설정 (전체 화면 활용)
    initial_sidebar_state="expanded"  # 사이드바 초기 상태를 펼쳐진 상태로 설정
)

def check_api_health():
    """
    FastAPI 서버 상태 확인
    - 백엔드 서버의 정상 작동 여부를 실시간 체크
    - 연결 실패시 사용자에게 적절한 안내 메시지 표시
    
    Returns:
        dict: API 상태 정보 (연결 실패시 None) - 서버 상태, 모델 로딩 상태 등
    """
    try:
        # FastAPI 헬스 체크 엔드포인트 호출 - /health API로 서버 상태 확인
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)  # 5초 타임아웃 설정
        if response.status_code == 200:  # HTTP 200 OK 응답 확인
            return response.json()  # JSON 형태의 상태 정보 반환
        else:
            return None  # 오류 응답시 None 반환
    except requests.exceptions.RequestException:  # 네트워크 오류 등 예외 처리
        return None  # 연결 실패시 None 반환

def register_design_api(title: str, description: str):
    """
    FastAPI를 통해 설계안 등록
    - 사용자 입력 데이터를 JSON 형태로 변환하여 백엔드로 전송
    - AI 임베딩 생성 및 데이터베이스 저장 과정을 API를 통해 처리
    
    Args:
        title: 설계안 제목 - 사용자가 입력한 설계안 이름
        description: 설계안 설명 - AI 임베딩 생성 대상 텍스트
        
    Returns:
        dict: API 응답 데이터 - 성공/실패 상태와 상세 정보
    """
    try:
        # POST 요청 데이터 준비 - JSON 형태로 데이터 구성
        payload = {
            "title": title,        # 설계안 제목
            "description": description  # 설계안 설명 (임베딩 대상)
        }
        
        # FastAPI /register_design 엔드포인트 호출 - 설계안 등록 API 호출
        response = requests.post(
            f"{API_BASE_URL}/register_design",  # POST 요청 URL
            json=payload,  # JSON 데이터로 전송
            headers={"Content-Type": "application/json"},  # JSON 콘텐츠 타입 헤더
            timeout=30  # 임베딩 생성 시간을 고려한 타임아웃 (30초)
        )
        
        return {
            "status_code": response.status_code,  # HTTP 상태 코드 (200, 400, 500 등)
            "data": response.json()  # 응답 데이터 (성공시 design_id, 실패시 오류 메시지)
        }
        
    except requests.exceptions.Timeout:  # 요청 시간 초과 처리
        return {
            "status_code": 408,  # Request Timeout
            "data": {"detail": "요청 시간이 초과되었습니다. 서버가 응답하지 않습니다."}
        }
    except requests.exceptions.RequestException as e:  # 기타 네트워크 오류 처리
        return {
            "status_code": 500,  # Internal Server Error
            "data": {"detail": f"네트워크 오류: {str(e)}"}
        }

def main():
    """메인 Streamlit 애플리케이션 - 전체 UI 구성 및 사용자 상호작용 처리"""
    
    # 페이지 헤더 - 메인 제목과 구분선
    st.title("🏗️ AI 설계안 등록 시스템")  # 페이지 메인 제목
    st.markdown("---")  # 구분선 추가
    
    # 사이드바 - API 서버 상태 표시 영역
    st.sidebar.header("📊 시스템 상태")  # 사이드바 제목
    
    # API 서버 상태 확인 - 실시간으로 백엔드 서버 연결 상태 체크
    with st.sidebar:
        with st.spinner("API 서버 상태 확인 중..."):  # 로딩 스피너 표시
            health_status = check_api_health()  # 서버 헬스 체크 함수 호출
        
        if health_status:  # 서버 연결 성공시
            st.success("✅ API 서버 연결됨")  # 성공 메시지 표시
            st.json({  # 서버 상태 정보를 JSON 형태로 표시
                "상태": health_status.get("status", "unknown"),  # 전체 시스템 상태
                "모델": health_status.get("model_status", "unknown"),  # AI 모델 로딩 상태
                "데이터베이스": health_status.get("database", "unknown")  # DB 연결 상태
            })
        else:  # 서버 연결 실패시
            st.error("❌ API 서버 연결 실패")  # 오류 메시지 표시
            st.warning("FastAPI 서버가 실행 중인지 확인하세요:\n`uvicorn app:app --reload`")  # 해결 방법 안내
    
    # 메인 콘텐츠 영역 - 2열 레이아웃으로 구성 (입력폼:정보 = 2:1 비율)
    col1, col2 = st.columns([2, 1])  # 첫 번째 열은 2배, 두 번째 열은 1배 크기
    
    with col1:  # 왼쪽 열 - 설계안 입력 폼
        st.header("📝 새 설계안 등록")  # 입력 섹션 제목
        
        # 설계안 입력 폼 - Streamlit 폼 컨테이너로 사용자 입력 관리
        with st.form("design_form"):  # 폼 ID 지정으로 상태 관리
            # 설계안 제목 입력 - 필수 입력 필드
            title = st.text_input(
                "설계안 제목 *",  # 라벨 (* 표시로 필수 항목 표시)
                placeholder="예: 친환경 스마트홈 설계",  # 입력 예시 텍스트
                help="설계안의 간단하고 명확한 제목을 입력하세요."  # 도움말 툴팁
            )
            
            # 설계안 설명 입력 - AI 임베딩 생성 대상 텍스트
            description = st.text_area(
                "설계안 설명 *",  # 라벨
                placeholder="예: 태양광 패널과 지열 에너지를 활용하여 에너지 자립을 목표로 하는 친환경 주택 설계안입니다. 스마트 홈 시스템을 통해 실시간 에너지 관리가 가능하며...",
                height=200,  # 텍스트 영역 높이 설정
                help="설계안의 상세한 설명을 입력하세요. 이 텍스트는 AI 임베딩으로 변환됩니다."  # 임베딩 용도 설명
            )
            
            # 등록 버튼 - 폼 제출 트리거
            submitted = st.form_submit_button(
                "🚀 설계안 등록",  # 버튼 텍스트 (이모지로 시각적 효과)
                type="primary",  # 기본 액션 버튼으로 강조 표시
                use_container_width=True  # 컨테이너 전체 너비 사용
            )
        
        # 폼 제출 처리 - 사용자가 등록 버튼을 클릭했을 때 실행
        if submitted:
            # 입력 검증 - 필수 필드 확인 및 유효성 검사
            if not title.strip():  # 제목이 비어있거나 공백만 있는 경우
                st.error("❌ 설계안 제목을 입력하세요.")
            elif not description.strip():  # 설명이 비어있거나 공백만 있는 경우
                st.error("❌ 설계안 설명을 입력하세요.")
            elif not health_status:  # API 서버 연결 상태 확인
                st.error("❌ API 서버에 연결할 수 없습니다. 서버 상태를 확인하세요.")
            else:
                # 설계안 등록 진행 - 모든 유효성 검사 통과시 실행
                st.info("🔄 설계안을 등록하는 중입니다...")  # 진행 상태 표시
                
                # 진행 상태 표시 - 사용자 경험 향상을 위한 시각적 피드백
                progress_bar = st.progress(0)  # 진행률 바 초기화 (0%)
                status_text = st.empty()  # 상태 텍스트 플레이스홀더
                
                # 단계별 진행 표시 - 3단계로 나누어 진행 상황 시각화
                status_text.text("1/3 API 서버에 연결 중...")  # 1단계: 서버 연결
                progress_bar.progress(33)  # 33% 진행
                time.sleep(0.5)  # 사용자가 인지할 수 있도록 잠시 대기
                
                status_text.text("2/3 AI 임베딩 생성 중...")  # 2단계: 임베딩 생성
                progress_bar.progress(67)  # 67% 진행
                
                # API 호출 - 실제 백엔드 처리 요청
                result = register_design_api(title, description)
                
                progress_bar.progress(100)  # 100% 완료
                status_text.text("3/3 완료!")  # 3단계: 완료
                time.sleep(0.5)  # 완료 상태 잠시 표시
                
                # 결과 처리 - API 응답에 따른 성공/실패 메시지 표시
                if result["status_code"] == 200:  # HTTP 200 OK - 성공
                    # 성공 - 설계안 등록 완료
                    data = result["data"]  # 응답 데이터 추출
                    st.success("✅ 설계안이 성공적으로 등록되었습니다!")  # 성공 메시지
                    
                    # 등록 결과 정보 표시 - 사용자에게 생성된 정보 제공
                    st.info(f"📋 **등록 정보**\n"
                           f"- 설계안 ID: {data.get('design_id')}\n"  # 데이터베이스에서 생성된 고유 ID
                           f"- 임베딩 차원: {data.get('embedding_dimension')}차원\n"  # AI 벡터 차원 정보
                           f"- 등록 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")  # 현재 시간 표시
                    
                    # 입력 데이터 확인 - 등록된 내용 재확인 가능한 확장 가능 섹션
                    with st.expander("📄 등록된 설계안 정보"):
                        st.write("**제목:**", title)  # 입력한 제목 표시
                        st.write("**설명:**", description)  # 입력한 설명 표시
                else:
                    # 실패 - 오류 메시지 표시
                    error_detail = result["data"].get("detail", "알 수 없는 오류")  # 오류 상세 내용 추출
                    st.error(f"❌ 설계안 등록에 실패했습니다.\n\n**오류 내용:** {error_detail}")  # 오류 메시지 표시
                
                # 진행 표시 제거 - UI 정리
                progress_bar.empty()  # 진행률 바 제거
                status_text.empty()  # 상태 텍스트 제거
    
    with col2:  # 오른쪽 열 - 시스템 정보 및 사용법 안내
        st.header("ℹ️ 시스템 정보")  # 정보 섹션 제목
        
        # 시스템 정보 카드 - 사용된 기술 스택 및 AI 모델 정보
        st.info("""
        **🤖 AI 모델 정보**
        - 모델: paraphrase-multilingual-MiniLM-L12-v2  # 다국어 지원 경량 모델
        - 지원 언어: 한국어 포함 104개 언어  # 다국어 임베딩 지원 범위
        - 벡터 차원: 384차원  # 생성되는 임베딩 벡터 크기
        
        **💾 데이터베이스**
        - PostgreSQL + pgvector 확장  # 벡터 저장 및 검색 지원 DB
        - 트랜잭션 기반 안전한 저장  # ACID 속성 보장
        
        **🔧 기술 스택**
        - FastAPI (백엔드)  # 고성능 Python 웹 프레임워크
        - Streamlit (프론트엔드)  # 파이썬 기반 웹 UI
        - sentence-transformers (AI)  # 문장 임베딩 라이브러리
        """)
        
        # 사용법 안내 - 단계별 사용 방법 설명
        st.info("""
        **📖 사용법**
        1. 설계안 제목을 간단명료하게 입력  # 검색 키워드 역할
        2. 설계안 설명을 상세히 작성  # AI 임베딩 생성 원본 텍스트
        3. '설계안 등록' 버튼 클릭  # 처리 시작 트리거
        4. AI가 자동으로 임베딩 생성  # 텍스트 → 벡터 변환
        5. 데이터베이스에 안전하게 저장  # 트랜잭션 기반 저장
        """)
        
        # 현재 시간 표시 - 실시간 정보 제공
        st.markdown("---")  # 구분선
        st.caption(f"⏰ 현재 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")  # 현재 시각 표시

if __name__ == "__main__":
    main()  # 메인 함수 실행 - 스크립트가 직접 실행될 때만 웹 앱 시작