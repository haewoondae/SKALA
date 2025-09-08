import requests
import streamlit as st
import pandas as pd
from typing import Optional, Dict, List, Any

# API 기본 설정
API_BASE_URL = "http://localhost:8080"

class StockAPI:
    """백엔드 API 통신을 담당하는 클래스"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
    
    # ==================== 인증 관련 ====================
    def login_player(self, player_id: str, password: str) -> Optional[Dict]:
        """플레이어 로그인"""
        try:
            response = requests.post(f"{self.base_url}/api/players/login", 
                                   json={"playerId": player_id, "playerPassword": password})
            if response.status_code == 200:
                return response.json().get('body')
            return None
        except Exception as e:
            st.error(f"로그인 실패: {str(e)}")
            return None
    
    def create_player(self, player_data: Dict) -> bool:
        """플레이어 등록"""
        try:
            response = requests.post(f"{self.base_url}/api/players", json=player_data)
            return response.status_code == 200
        except Exception as e:
            st.error(f"회원가입 실패: {str(e)}")
            return False
    
    # ==================== 플레이어 관련 ====================
    def get_player_info(self, player_id: str) -> Optional[Dict]:
        """플레이어 상세 정보 조회 (보유 주식 포함)"""
        try:
            response = requests.get(f"{self.base_url}/api/players/{player_id}")
            if response.status_code == 200:
                return response.json().get('body')
            return None
        except Exception as e:
            st.error(f"플레이어 정보 조회 실패: {str(e)}")
            return None
    
    def get_all_players(self, offset: int = 0, count: int = 10) -> Optional[Dict]:
        """전체 플레이어 목록 조회 (관리자용)"""
        try:
            response = requests.get(f"{self.base_url}/api/players/list", 
                                  params={"offset": offset, "count": count})
            if response.status_code == 200:
                return response.json().get('body')
            return None
        except Exception as e:
            st.error(f"플레이어 목록 조회 실패: {str(e)}")
            return None
    
    def update_player(self, player_data: Dict) -> bool:
        """플레이어 정보 수정"""
        try:
            response = requests.put(f"{self.base_url}/api/players", json=player_data)
            return response.status_code == 200
        except Exception as e:
            st.error(f"플레이어 정보 수정 실패: {str(e)}")
            return False
    
    def delete_player(self, player_id: str) -> bool:
        """플레이어 삭제"""
        try:
            response = requests.delete(f"{self.base_url}/api/players", 
                                     json={"playerId": player_id})
            return response.status_code == 200
        except Exception as e:
            st.error(f"플레이어 삭제 실패: {str(e)}")
            return False
    
    # ==================== 주식 관련 ====================
    def get_stocks(self, offset: int = 0, count: int = 50) -> Optional[Dict]:
        """주식 목록 조회"""
        try:
            response = requests.get(f"{self.base_url}/api/stocks/list",
                                  params={"offset": offset, "count": count})
            if response.status_code == 200:
                return response.json().get('body')
            return None
        except Exception as e:
            st.error(f"주식 목록 조회 실패: {str(e)}")
            return None
    
    def get_stock_detail(self, stock_id: int) -> Optional[Dict]:
        """주식 상세 정보 조회"""
        try:
            response = requests.get(f"{self.base_url}/api/stocks/{stock_id}")
            if response.status_code == 200:
                return response.json().get('body')
            return None
        except Exception as e:
            st.error(f"주식 정보 조회 실패: {str(e)}")
            return None
    
    def create_stock(self, stock_data: Dict) -> bool:
        """주식 등록 (관리자용)"""
        try:
            response = requests.post(f"{self.base_url}/api/stocks", json=stock_data)
            return response.status_code == 200
        except Exception as e:
            st.error(f"주식 등록 실패: {str(e)}")
            return False
    
    def update_stock(self, stock_data: Dict) -> bool:
        """주식 정보 수정 (관리자용)"""
        try:
            response = requests.put(f"{self.base_url}/api/stocks", json=stock_data)
            return response.status_code == 200
        except Exception as e:
            st.error(f"주식 정보 수정 실패: {str(e)}")
            return False
    
    def delete_stock(self, stock_id: int) -> bool:
        """주식 삭제 (관리자용)"""
        try:
            response = requests.delete(f"{self.base_url}/api/stocks", 
                                     json={"id": stock_id})
            return response.status_code == 200
        except Exception as e:
            st.error(f"주식 삭제 실패: {str(e)}")
            return False
    
    # ==================== 거래 관련 ====================
    def buy_stock(self, stock_id: int, quantity: int) -> bool:
        """주식 매수"""
        try:
            response = requests.post(f"{self.base_url}/api/players/buy",
                                   json={"stockId": stock_id, "quantity": quantity})
            return response.status_code == 200
        except Exception as e:
            st.error(f"주식 매수 실패: {str(e)}")
            return False
    
    def sell_stock(self, stock_id: int, quantity: int) -> bool:
        """주식 매도"""
        try:
            response = requests.post(f"{self.base_url}/api/players/sell",
                                   json={"stockId": stock_id, "quantity": quantity})
            return response.status_code == 200
        except Exception as e:
            st.error(f"주식 매도 실패: {str(e)}")
            return False
    
    def get_transactions(self, player_id: str, count: int = 20) -> Optional[List]:
        """거래 내역 조회"""
        try:
            response = requests.get(f"{self.base_url}/api/players/{player_id}/transactions",
                                  params={"count": count})
            if response.status_code == 200:
                return response.json().get('body')
            return None
        except Exception as e:
            st.error(f"거래 내역 조회 실패: {str(e)}")
            return None
    
    # ==================== 관심종목 관련 ====================
    def get_watchlist(self, player_id: str) -> Optional[List]:
        """관심종목 목록 조회"""
        try:
            response = requests.get(f"{self.base_url}/api/players/{player_id}/watchlist")
            if response.status_code == 200:
                return response.json().get('body')
            return None
        except Exception as e:
            st.error(f"관심종목 조회 실패: {str(e)}")
            return None
    
    def add_to_watchlist(self, player_id: str, stock_id: int) -> bool:
        """관심종목 추가"""
        try:
            response = requests.post(f"{self.base_url}/api/players/{player_id}/watchlist",
                                   json={"stockId": stock_id})
            return response.status_code == 200
        except Exception as e:
            st.error(f"관심종목 추가 실패: {str(e)}")
            return False
    
    def remove_from_watchlist_by_stock(self, player_id: str, stock_id: int) -> bool:
        """관심종목 삭제 (주식 ID로)"""
        try:
            response = requests.delete(f"{self.base_url}/api/players/{player_id}/watchlist/stock/{stock_id}")
            return response.status_code == 200
        except Exception as e:
            st.error(f"관심종목 삭제 실패: {str(e)}")
            return False
    
    def remove_from_watchlist_by_id(self, player_id: str, watchlist_id: int) -> bool:
        """관심종목 삭제 (관심종목 ID로)"""
        try:
            response = requests.delete(f"{self.base_url}/api/players/{player_id}/watchlist/{watchlist_id}")
            return response.status_code == 200
        except Exception as e:
            st.error(f"관심종목 삭제 실패: {str(e)}")
            return False
    
    def check_watchlist(self, player_id: str, stock_id: int) -> bool:
        """관심종목 등록 여부 확인"""
        try:
            response = requests.get(f"{self.base_url}/api/players/{player_id}/watchlist/check/{stock_id}")
            if response.status_code == 200:
                return response.json().get('body', False)
            return False
        except Exception as e:
            return False
    
    def get_watchlist_count(self, player_id: str) -> int:
        """관심종목 개수 조회"""
        try:
            response = requests.get(f"{self.base_url}/api/players/{player_id}/watchlist/count")
            if response.status_code == 200:
                return response.json().get('body', 0)
            return 0
        except Exception as e:
            return 0

# 전역 API 인스턴스
api = StockAPI()

# ==================== 유틸리티 함수들 ====================
def format_currency(amount: int) -> str:
    """통화 포맷팅"""
    return f"{amount:,}원"

def format_percentage(value: float) -> str:
    """퍼센트 포맷팅"""
    return f"{value:.2f}%"

def calculate_profit_rate(current_price: int, avg_price: int) -> float:
    """수익률 계산"""
    if avg_price == 0:
        return 0.0
    return ((current_price - avg_price) / avg_price) * 100

def is_admin(player_id: str) -> bool:
    """관리자 여부 확인"""
    return player_id == "admin"

def require_admin():
    """관리자 권한 체크"""
    if not st.session_state.get('logged_in', False):
        st.error("❌ 로그인이 필요합니다.")
        st.stop()
    
    current_user = st.session_state.get('current_user', {})
    if not is_admin(current_user.get('playerId', '')):
        st.error("❌ 관리자 권한이 필요합니다.")
        st.stop()

def init_session_state():
    """세션 상태 초기화"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = {}
    if 'page' not in st.session_state:
        st.session_state.page = 'dashboard'
    if 'user_role' not in st.session_state:
        st.session_state.user_role = 'user'

def logout():
    """로그아웃"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
