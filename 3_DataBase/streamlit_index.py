import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import pandas as pd

# 환경변수 로드
load_dotenv()

# API 서버 설정
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8000))
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"

# 페이지 설정
st.set_page_config(
    page_title="AI 설계안 벡터 검색",
    page_icon="🔍",
    layout="wide"
)

# 메인 제목
st.title("🔍 AI 설계안 벡터 검색 시스템")
st.markdown(f"**API 서버:** `{API_BASE_URL}`")

# API 연결 상태 확인
@st.cache_data(ttl=10)
def check_api_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.json() if response.status_code == 200 else None
    except:
        return None

# 샘플 벡터 가져오기
@st.cache_data(ttl=300)
def get_sample_vector(record_id):
    try:
        response = requests.get(f"{API_BASE_URL}/test/sample-vector?record_id={record_id}")
        return response.json() if response.status_code == 200 else None
    except:
        return None

# 벡터 검색 함수
def search_vectors(query_vector, limit, distance_function, accurate_mode=False):
    endpoint = "/search/vector/accurate" if accurate_mode else "/search/vector"
    
    payload = {
        "query_vector": query_vector,
        "limit": limit,
        "distance_function": distance_function
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=payload, timeout=30)
        return response.json() if response.status_code == 200 else {"error": response.text}
    except Exception as e:
        return {"error": str(e)}

# 사이드바 - 시스템 상태
with st.sidebar:
    st.header("🖥️ 시스템 상태")
    
    health = check_api_health()
    if health and health.get("status") == "healthy":
        st.success("✅ API 서버 연결됨")
        st.info(f"📊 데이터: {health['config_info']['data_count']}건")
        st.info(f"🗂️ 인덱스: {len(health['config_info']['indexes'])}개")
    else:
        st.error("❌ API 서버 연결 실패")
        st.stop()

# 메인 컨테이너
col1, col2 = st.columns([1, 2])

with col1:
    st.header("⚙️ 검색 설정")
    
    # 샘플 벡터 선택
    sample_id = st.selectbox("샘플 데이터 선택", range(1, 11), index=0)
    
    if st.button("📥 샘플 벡터 로드"):
        sample_data = get_sample_vector(sample_id)
        if sample_data:
            st.session_state.vector = sample_data["vector"]
            st.session_state.sample_title = sample_data["title"]
            st.success(f"✅ 로드 완료: {sample_data['title'][:30]}...")
    
    # 검색 파라미터
    limit = st.slider("검색 결과 수", 1, 50, 10)
    distance_function = st.selectbox(
        "거리 함수", 
        ["l2", "cosine"],
        help="L2: 더 높은 정확도 (46%), Cosine: 빠른 속도 (18%)"
    )
    accurate_mode = st.checkbox("정확도 우선 모드 (probes=3)", help="속도는 느리지만 더 정확한 결과")
    
    # 검색 실행
    search_button = st.button("🔍 벡터 검색 실행", type="primary")

with col2:
    st.header("📋 검색 결과")
    
    if search_button:
        if "vector" not in st.session_state:
            st.error("⚠️ 먼저 샘플 벡터를 로드해주세요!")
        else:
            with st.spinner("검색 중..."):
                results = search_vectors(
                    st.session_state.vector, 
                    limit, 
                    distance_function, 
                    accurate_mode
                )
            
            if "error" in results:
                st.error(f"❌ 검색 오류: {results['error']}")
            else:
                # 검색 정보 표시
                if results and "search_info" in results[0]:
                    info = results[0]["search_info"]
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("요청/반환", f"{info['requested_limit']}/{info['actual_returned']}")
                    with col_b:
                        st.metric("정확도", info['accuracy_rate'])
                    with col_c:
                        st.metric("거리 함수", info['distance_function'].upper())
                
                # 결과 테이블
                if results:
                    df = pd.DataFrame([
                        {
                            "ID": r["id"],
                            "제목": r["title"][:40] + "..." if len(r["title"]) > 40 else r["title"],
                            "거리": f"{r['distance']:.6f}",
                            "내용 미리보기": r["content"][:50] + "..." if len(r["content"]) > 50 else r["content"]
                        }
                        for r in results
                    ])
                    
                    st.dataframe(df, use_container_width=True, height=400)
                    
                    # 상세 결과 (확장 가능)
                    with st.expander("📝 상세 검색 결과"):
                        for i, result in enumerate(results, 1):
                            st.subheader(f"{i}. [{result['id']}] {result['title']}")
                            st.write(f"**거리:** {result['distance']:.6f}")
                            st.write(f"**내용:** {result['content']}")
                            st.divider()
                else:
                    st.warning("📭 검색 결과가 없습니다.")

# 하단 정보 탭
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["📊 성능 정보", "🔧 API 문서", "ℹ️ 사용 가이드"])

with tab1:
    if st.button("📊 성능 정보 새로고침"):
        try:
            perf_response = requests.get(f"{API_BASE_URL}/info/performance")
            if perf_response.status_code == 200:
                perf_data = perf_response.json()
                
                st.subheader("테스트 결과")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**L2 거리 (권장)**")
                    st.json(perf_data["test_results"]["performance_comparison"]["l2_distance"])
                
                with col2:
                    st.write("**Cosine 거리**")
                    st.json(perf_data["test_results"]["performance_comparison"]["cosine_distance"])
                
                st.subheader("사용 권장사항")
                for rec in perf_data["usage_recommendations"]:
                    st.write(f"• {rec}")
        except:
            st.error("성능 정보를 가져올 수 없습니다.")

with tab2:
    st.subheader("🔧 API 엔드포인트")
    
    endpoints = [
        {"method": "POST", "url": "/search/vector", "desc": "기본 벡터 검색 (빠른 속도)"},
        {"method": "POST", "url": "/search/vector/accurate", "desc": "정확도 우선 검색 (느린 속도)"},
        {"method": "GET", "url": "/test/sample-vector", "desc": "샘플 벡터 가져오기"},
        {"method": "GET", "url": "/health", "desc": "시스템 상태 확인"},
        {"method": "GET", "url": "/info/performance", "desc": "성능 정보 조회"}
    ]
    
    df_endpoints = pd.DataFrame(endpoints)
    st.dataframe(df_endpoints, use_container_width=True)
    
    st.markdown(f"**API 문서:** {API_BASE_URL}/docs")

with tab3:
    st.subheader("ℹ️ 사용 방법")
    
    st.markdown("""
    ### 1단계: 샘플 벡터 로드
    - 좌측에서 샘플 데이터 ID 선택 (1-10)
    - "샘플 벡터 로드" 버튼 클릭
    
    ### 2단계: 검색 설정
    - **검색 결과 수:** 1-50개 선택
    - **거리 함수:** L2 권장 (더 높은 정확도)
    - **정확도 우선 모드:** 체크 시 더 정확하지만 느린 검색
    
    ### 3단계: 검색 실행
    - "벡터 검색 실행" 버튼 클릭
    - 결과 테이블에서 유사 문서 확인
    
    ### 💡 팁
    - **LIMIT 5-10:** 두 거리 함수 모두 정확
    - **LIMIT 20-50:** L2 거리 함수 권장
    - **빠른 검색:** 기본 모드 사용
    - **정확한 검색:** 정확도 우선 모드 사용
    """)

# 현재 로드된 벡터 정보 표시
if "vector" in st.session_state:
    with st.sidebar:
        st.markdown("---")
        st.subheader("📁 로드된 벡터")
        st.write(f"**제목:** {st.session_state.get('sample_title', 'Unknown')}")
        st.write(f"**차원:** 384")
        st.write(f"**첫 5개 값:** {st.session_state.vector[:5]}")

# 푸터
st.markdown("---")
st.markdown(
    f"""
    <div style="text-align: center; color: gray;">
    PostgreSQL pgvector + FastAPI + Streamlit | API: {API_BASE_URL}
    </div>
    """, 
    unsafe_allow_html=True
)
