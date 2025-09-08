import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# api_client.py에서 필요한 함수들 import
from api_client import api, format_currency, format_percentage, calculate_profit_rate, is_admin, require_admin, init_session_state, logout

# 페이지 설정
st.set_page_config(
    page_title="SKALA 주식 거래 시스템",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
init_session_state()

def show_login_page():
    """로그인/회원가입 페이지"""
    st.title("📈 SKALA 주식 거래 시스템")
    
    tab1, tab2 = st.tabs(["🔑 로그인", "👤 회원가입"])
    
    with tab1:
        st.subheader("로그인")
        with st.form("login_form"):
            player_id = st.text_input("아이디")
            password = st.text_input("비밀번호", type="password")
            submit = st.form_submit_button("로그인")
            
            if submit:
                if player_id and password:
                    user_data = api.login_player(player_id, password)
                    if user_data:
                        st.session_state.logged_in = True
                        st.session_state.current_user = user_data
                        st.session_state.user_role = "admin" if is_admin(player_id) else "user"
                        st.success("✅ 로그인 성공!")
                        st.rerun()
                    else:
                        st.error("❌ 로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.")
                else:
                    st.warning("⚠️ 아이디와 비밀번호를 입력해주세요.")
    
    with tab2:
        st.subheader("회원가입")
        with st.form("register_form"):
            new_id = st.text_input("아이디 (영문/숫자)")
            new_password = st.text_input("비밀번호", type="password")
            confirm_password = st.text_input("비밀번호 확인", type="password")
            initial_money = st.number_input("초기 자금", min_value=100000, max_value=100000000, value=1000000, step=100000)
            submit = st.form_submit_button("회원가입")
            
            if submit:
                if not all([new_id, new_password, confirm_password]):
                    st.warning("⚠️ 모든 필드를 입력해주세요.")
                elif new_password != confirm_password:
                    st.error("❌ 비밀번호가 일치하지 않습니다.")
                elif len(new_password) < 4:
                    st.error("❌ 비밀번호는 4자리 이상이어야 합니다.")
                else:
                    player_data = {
                        "playerId": new_id,
                        "playerPassword": new_password,
                        "playerMoney": initial_money
                    }
                    
                    if api.create_player(player_data):
                        st.success("✅ 회원가입이 완료되었습니다! 로그인해주세요.")
                    else:
                        st.error("❌ 회원가입에 실패했습니다. 이미 존재하는 아이디일 수 있습니다.")

def create_sidebar():
    """사이드바 생성"""
    st.sidebar.title("📈 주식 거래 시스템")
    
    user_role = st.session_state.get('user_role', 'user')
    current_user = st.session_state.get('current_user', {})
    
    # 사용자 정보 표시
    if user_role == "admin":
        st.sidebar.markdown("### 👑 관리자 모드")
        st.sidebar.markdown(f"**{current_user.get('playerId', 'Unknown')}** (관리자)")
        st.sidebar.markdown(f"보유 자금: {format_currency(current_user.get('playerMoney', 0))}")
    else:
        st.sidebar.markdown("### 👤 사용자 모드")
        st.sidebar.markdown(f"**{current_user.get('playerId', 'Unknown')}**")
        st.sidebar.markdown(f"보유 자금: {format_currency(current_user.get('playerMoney', 0))}")
    
    st.sidebar.markdown("---")
    
    # 메뉴 구성
    if user_role == "admin":
        # 관리자 메뉴
        if st.sidebar.button("🏠 관리자 대시보드"):
            st.session_state.page = "admin_dashboard"
        if st.sidebar.button("👥 플레이어 관리"):
            st.session_state.page = "admin_players"
        if st.sidebar.button("📊 주식 관리"):
            st.session_state.page = "admin_stocks"
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("**일반 기능**")
        if st.sidebar.button("🔄 사용자 모드"):
            st.session_state.page = "dashboard"
    else:
        # 일반 사용자 메뉴
        if st.sidebar.button("🏠 대시보드"):
            st.session_state.page = "dashboard"
        if st.sidebar.button("📈 주식 거래"):
            st.session_state.page = "trading"
        if st.sidebar.button("💼 내 포트폴리오"):
            st.session_state.page = "portfolio"
        if st.sidebar.button("📊 거래 내역"):
            st.session_state.page = "transactions"
        if st.sidebar.button("⭐ 관심종목"):
            st.session_state.page = "watchlist"
    
    st.sidebar.markdown("---")
    
    # 계정 관리
    if st.sidebar.button("⚙️ 내 정보 수정"):
        st.session_state.page = "profile"
    if st.sidebar.button("🚪 로그아웃"):
        logout()

def show_dashboard():
    """대시보드 페이지"""
    st.title("🏠 대시보드")
    
    current_user = st.session_state.get('current_user', {})
    player_id = current_user.get('playerId', '')
    
    # 최신 플레이어 정보 조회
    player_info = api.get_player_info(player_id)
    if not player_info:
        st.error("❌ 플레이어 정보를 조회할 수 없습니다.")
        return
    
    # 기본 정보 업데이트
    st.session_state.current_user = player_info
    
    # 상단 핵심 정보 카드
    col1, col2, col3, col4 = st.columns(4)
    
    cash = player_info.get('playerMoney', 0)
    player_stocks = player_info.get('playerStockList', [])
    stock_value = sum(stock.get('stockPrice', 0) * stock.get('quantity', 0) for stock in player_stocks)
    total_assets = cash + stock_value
    watchlist_count = api.get_watchlist_count(player_id)
    
    with col1:
        st.metric("💰 총 자산", format_currency(total_assets))
    with col2:
        st.metric("💵 보유 현금", format_currency(cash))
    with col3:
        st.metric("📈 주식 평가액", format_currency(stock_value))
    with col4:
        st.metric("⭐ 관심종목", f"{watchlist_count}개")
    
    # 자산 구성 차트
    if stock_value > 0:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("💼 포트폴리오 현황")
            if player_stocks:
                df_stocks = pd.DataFrame(player_stocks)
                df_stocks['총가치'] = df_stocks['stockPrice'] * df_stocks['quantity']
                
                # 주식별 비중 파이 차트
                fig = px.pie(df_stocks, values='총가치', names='stockName', 
                           title='보유 주식 구성')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 자산 비중")
            asset_data = pd.DataFrame({
                '자산 유형': ['현금', '주식'],
                '금액': [cash, stock_value],
                '비중': [cash/total_assets*100, stock_value/total_assets*100]
            })
            
            for _, row in asset_data.iterrows():
                st.metric(row['자산 유형'], 
                         format_currency(row['금액']),
                         f"{row['비중']:.1f}%")
    
    # 보유 주식 상세
    st.subheader("💼 보유 주식")
    if player_stocks:
        df_stocks = pd.DataFrame(player_stocks)
        df_stocks['총가치'] = df_stocks['stockPrice'] * df_stocks['quantity']
        df_stocks = df_stocks[['stockName', 'quantity', 'stockPrice', '총가치']]
        df_stocks.columns = ['종목명', '보유량', '현재가', '총가치']
        
        # 포맷팅
        df_stocks['현재가'] = df_stocks['현재가'].apply(format_currency)
        df_stocks['총가치'] = df_stocks['총가치'].apply(format_currency)
        
        st.dataframe(df_stocks, use_container_width=True)
    else:
        st.info("📝 보유 중인 주식이 없습니다.")
    
    # 관심종목 미리보기
    st.subheader("⭐ 관심종목")
    watchlist = api.get_watchlist(player_id)
    if watchlist:
        df_watchlist = pd.DataFrame(watchlist[:5])  # 최대 5개만 표시
        if not df_watchlist.empty:
            df_watchlist = df_watchlist[['stockName', 'currentPrice', 'addedTime']]
            df_watchlist.columns = ['종목명', '현재가', '등록일']
            df_watchlist['현재가'] = df_watchlist['현재가'].apply(format_currency)
            st.dataframe(df_watchlist, use_container_width=True)
        
        if len(watchlist) > 5:
            st.info(f"📋 총 {len(watchlist)}개의 관심종목이 있습니다. 전체 보기는 관심종목 메뉴를 이용하세요.")
    else:
        st.info("📝 등록된 관심종목이 없습니다.")
    
    # 최근 거래내역
    st.subheader("📊 최근 거래내역")
    transactions = api.get_transactions(player_id, 5)  # 최근 5건
    if transactions:
        df_trans = pd.DataFrame(transactions)
        df_trans = df_trans[['stockName', 'transactionType', 'quantity', 'price', 'totalAmount', 'transactionTime']]
        df_trans.columns = ['종목명', '거래유형', '수량', '가격', '총액', '거래시간']
        
        # 포맷팅
        df_trans['가격'] = df_trans['가격'].apply(format_currency)
        df_trans['총액'] = df_trans['총액'].apply(format_currency)
        df_trans['거래유형'] = df_trans['거래유형'].map({'BUY': '매수', 'SELL': '매도'})
        
        st.dataframe(df_trans, use_container_width=True)
    else:
        st.info("📝 거래 내역이 없습니다.")

def show_trading():
    """주식 거래 페이지"""
    st.title("📈 주식 거래")
    
    # 주식 목록 조회
    stocks_data = api.get_stocks(0, 100)
    if not stocks_data:
        st.error("❌ 주식 정보를 조회할 수 없습니다.")
        return
    
    stocks = stocks_data.get('data', [])
    
    if not stocks:
        st.warning("📝 등록된 주식이 없습니다.")
        return
    
    # 주식 목록 표시
    st.subheader("📋 주식 목록")
    df_stocks = pd.DataFrame(stocks)
    
    # 주식 선택을 위한 selectbox 생성
    stock_options = {f"{stock['stockName']} ({format_currency(stock['stockPrice'])})" : stock 
                    for stock in stocks}
    
    selected_stock_str = st.selectbox("거래할 주식을 선택하세요", options=list(stock_options.keys()))
    selected_stock = stock_options[selected_stock_str]
    
    # 선택된 주식 정보 표시
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📊 {selected_stock['stockName']}")
        st.metric("현재가", format_currency(selected_stock['stockPrice']))
        
        # 관심종목 등록/해제 버튼
        current_user = st.session_state.get('current_user', {})
        player_id = current_user.get('playerId', '')
        
        is_in_watchlist = api.check_watchlist(player_id, selected_stock['id'])
        
        if is_in_watchlist:
            if st.button("⭐ 관심종목에서 제거"):
                if api.remove_from_watchlist_by_stock(player_id, selected_stock['id']):
                    st.success("✅ 관심종목에서 제거되었습니다.")
                    st.rerun()
        else:
            if st.button("⭐ 관심종목에 추가"):
                if api.add_to_watchlist(player_id, selected_stock['id']):
                    st.success("✅ 관심종목에 추가되었습니다.")
                    st.rerun()
    
    with col2:
        # 거래 폼
        st.subheader("💰 거래하기")
        
        tab1, tab2 = st.tabs(["매수", "매도"])
        
        with tab1:
            with st.form("buy_form"):
                buy_quantity = st.number_input("매수 수량", min_value=1, value=1)
                total_cost = buy_quantity * selected_stock['stockPrice']
                st.write(f"총 비용: {format_currency(total_cost)}")
                
                buy_submit = st.form_submit_button("매수 주문")
                
                if buy_submit:
                    if api.buy_stock(selected_stock['id'], buy_quantity):
                        st.success("✅ 매수 주문이 완료되었습니다!")
                        st.rerun()
        
        with tab2:
            # 보유 수량 확인
            player_info = api.get_player_info(player_id)
            player_stocks = player_info.get('playerStockList', []) if player_info else []
            
            owned_stock = next((ps for ps in player_stocks if ps['stockId'] == selected_stock['id']), None)
            max_sell = owned_stock['quantity'] if owned_stock else 0
            
            with st.form("sell_form"):
                if max_sell > 0:
                    sell_quantity = st.number_input(f"매도 수량 (보유: {max_sell}주)", 
                                                  min_value=1, max_value=max_sell, value=1)
                    total_revenue = sell_quantity * selected_stock['stockPrice']
                    st.write(f"총 수익: {format_currency(total_revenue)}")
                    
                    sell_submit = st.form_submit_button("매도 주문")
                    
                    if sell_submit:
                        if api.sell_stock(selected_stock['id'], sell_quantity):
                            st.success("✅ 매도 주문이 완료되었습니다!")
                            st.rerun()
                else:
                    st.info("보유 중인 주식이 없습니다.")
                    st.form_submit_button("매도 주문", disabled=True)
    
    # 전체 주식 목록 테이블
    st.subheader("📋 전체 주식 목록")
    df_display = df_stocks[['stockName', 'stockPrice']].copy()
    df_display.columns = ['종목명', '현재가']
    df_display['현재가'] = df_display['현재가'].apply(format_currency)
    st.dataframe(df_display, use_container_width=True)

def show_portfolio():
    """포트폴리오 페이지"""
    st.title("💼 내 포트폴리오")
    
    current_user = st.session_state.get('current_user', {})
    player_id = current_user.get('playerId', '')
    
    # 최신 정보 조회
    player_info = api.get_player_info(player_id)
    if not player_info:
        st.error("❌ 플레이어 정보를 조회할 수 없습니다.")
        return
    
    player_stocks = player_info.get('playerStockList', [])
    cash = player_info.get('playerMoney', 0)
    
    if not player_stocks:
        st.info("📝 보유 중인 주식이 없습니다.")
        return
    
    # 포트폴리오 요약
    df_stocks = pd.DataFrame(player_stocks)
    df_stocks['총가치'] = df_stocks['stockPrice'] * df_stocks['quantity']
    total_stock_value = df_stocks['총가치'].sum()
    total_assets = cash + total_stock_value
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 총 자산", format_currency(total_assets))
    with col2:
        st.metric("📈 주식 평가액", format_currency(total_stock_value))
    with col3:
        st.metric("💵 보유 현금", format_currency(cash))
    
    # 포트폴리오 차트
    col1, col2 = st.columns(2)
    
    with col1:
        # 종목별 비중 파이 차트
        fig_pie = px.pie(df_stocks, values='총가치', names='stockName', 
                        title='보유 주식 구성 비중')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # 자산 구성 (현금 vs 주식)
        asset_comp = pd.DataFrame({
            '구분': ['현금', '주식'],
            '금액': [cash, total_stock_value]
        })
        fig_bar = px.bar(asset_comp, x='구분', y='금액', title='자산 구성')
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # 상세 포트폴리오 테이블
    st.subheader("📊 보유 주식 상세")
    df_display = df_stocks.copy()
    df_display = df_display[['stockName', 'quantity', 'stockPrice', '총가치']]
    df_display.columns = ['종목명', '보유량', '현재가', '총가치']
    
    # 포맷팅
    df_display['현재가'] = df_display['현재가'].apply(format_currency)
    df_display['총가치'] = df_display['총가치'].apply(format_currency)
    
    st.dataframe(df_display, use_container_width=True)

def show_transactions():
    """거래 내역 페이지"""
    st.title("📊 거래 내역")
    
    current_user = st.session_state.get('current_user', {})
    player_id = current_user.get('playerId', '')
    
    # 거래 내역 조회
    count = st.selectbox("조회할 건수", [10, 20, 50, 100], index=1)
    transactions = api.get_transactions(player_id, count)
    
    if not transactions:
        st.info("📝 거래 내역이 없습니다.")
        return
    
    # 거래 내역 분석
    df_trans = pd.DataFrame(transactions)
    
    # 거래 통계
    col1, col2, col3, col4 = st.columns(4)
    
    total_transactions = len(df_trans)
    buy_count = len(df_trans[df_trans['transactionType'] == 'BUY'])
    sell_count = len(df_trans[df_trans['transactionType'] == 'SELL'])
    total_amount = df_trans['totalAmount'].sum()
    
    with col1:
        st.metric("총 거래 건수", f"{total_transactions}건")
    with col2:
        st.metric("매수 건수", f"{buy_count}건")
    with col3:
        st.metric("매도 건수", f"{sell_count}건")
    with col4:
        st.metric("총 거래 금액", format_currency(total_amount))
    
    # 거래 유형별 차트
    col1, col2 = st.columns(2)
    
    with col1:
        # 거래 유형별 건수
        type_counts = df_trans['transactionType'].value_counts()
        type_counts.index = type_counts.index.map({'BUY': '매수', 'SELL': '매도'})
        fig_pie = px.pie(values=type_counts.values, names=type_counts.index, 
                        title='거래 유형별 건수')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # 일별 거래 금액
        df_trans['date'] = pd.to_datetime(df_trans['transactionTime']).dt.date
        daily_amount = df_trans.groupby('date')['totalAmount'].sum().reset_index()
        fig_line = px.line(daily_amount, x='date', y='totalAmount', 
                          title='일별 거래 금액')
        st.plotly_chart(fig_line, use_container_width=True)
    
    # 거래 내역 테이블
    st.subheader("📋 거래 내역 상세")
    
    # 필터
    col1, col2 = st.columns(2)
    with col1:
        type_filter = st.selectbox("거래 유형", ["전체", "매수", "매도"])
    with col2:
        stock_filter = st.selectbox("종목", ["전체"] + list(df_trans['stockName'].unique()))
    
    # 필터링
    filtered_df = df_trans.copy()
    if type_filter != "전체":
        filter_type = "BUY" if type_filter == "매수" else "SELL"
        filtered_df = filtered_df[filtered_df['transactionType'] == filter_type]
    
    if stock_filter != "전체":
        filtered_df = filtered_df[filtered_df['stockName'] == stock_filter]
    
    # 테이블 표시
    if not filtered_df.empty:
        display_df = filtered_df[['stockName', 'transactionType', 'quantity', 'price', 'totalAmount', 'transactionTime']].copy()
        display_df.columns = ['종목명', '거래유형', '수량', '가격', '총액', '거래시간']
        
        # 포맷팅
        display_df['거래유형'] = display_df['거래유형'].map({'BUY': '매수', 'SELL': '매도'})
        display_df['가격'] = display_df['가격'].apply(format_currency)
        display_df['총액'] = display_df['총액'].apply(format_currency)
        
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("📝 필터 조건에 맞는 거래 내역이 없습니다.")

def show_watchlist():
    """관심종목 페이지"""
    st.title("⭐ 관심종목")
    
    current_user = st.session_state.get('current_user', {})
    player_id = current_user.get('playerId', '')
    
    # 관심종목 조회
    watchlist = api.get_watchlist(player_id)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 내 관심종목")
        
        if watchlist:
            df_watchlist = pd.DataFrame(watchlist)
            
            # 관심종목 테이블
            for idx, stock in enumerate(watchlist):
                col_name, col_price, col_action = st.columns([2, 1, 1])
                
                with col_name:
                    st.write(f"**{stock['stockName']}**")
                with col_price:
                    st.write(format_currency(stock['currentPrice']))
                with col_action:
                    if st.button("삭제", key=f"remove_{stock['id']}"):
                        if api.remove_from_watchlist_by_id(player_id, stock['id']):
                            st.success("✅ 관심종목에서 제거되었습니다.")
                            st.rerun()
                
                # 빠른 거래 버튼
                col_buy, col_sell = st.columns(2)
                with col_buy:
                    if st.button(f"매수", key=f"buy_{stock['stockId']}"):
                        st.session_state.quick_trade_stock = stock['stockId']
                        st.session_state.page = "trading"
                        st.rerun()
                with col_sell:
                    if st.button(f"매도", key=f"sell_{stock['stockId']}"):
                        st.session_state.quick_trade_stock = stock['stockId']
                        st.session_state.page = "trading"
                        st.rerun()
                
                st.markdown("---")
        else:
            st.info("📝 등록된 관심종목이 없습니다.")
    
    with col2:
        st.subheader("➕ 관심종목 추가")
        
        # 전체 주식 목록 조회
        stocks_data = api.get_stocks(0, 100)
        if stocks_data:
            stocks = stocks_data.get('data', [])
            
            # 이미 관심종목에 등록된 주식 제외
            watchlist_stock_ids = [w['stockId'] for w in watchlist] if watchlist else []
            available_stocks = [s for s in stocks if s['id'] not in watchlist_stock_ids]
            
            if available_stocks:
                stock_options = {f"{stock['stockName']} ({format_currency(stock['stockPrice'])})" : stock 
                               for stock in available_stocks}
                
                selected_stock_str = st.selectbox("추가할 주식", options=list(stock_options.keys()))
                selected_stock = stock_options[selected_stock_str]
                
                if st.button("⭐ 관심종목에 추가"):
                    if api.add_to_watchlist(player_id, selected_stock['id']):
                        st.success("✅ 관심종목에 추가되었습니다.")
                        st.rerun()
            else:
                st.info("📝 추가할 수 있는 주식이 없습니다.")

def show_profile():
    """프로필 수정 페이지"""
    st.title("⚙️ 내 정보 수정")
    
    current_user = st.session_state.get('current_user', {})
    
    with st.form("profile_form"):
        st.subheader("기본 정보")
        st.text_input("아이디", value=current_user.get('playerId', ''), disabled=True)
        
        new_password = st.text_input("새 비밀번호 (변경시에만 입력)", type="password")
        confirm_password = st.text_input("새 비밀번호 확인", type="password")
        
        submit = st.form_submit_button("정보 수정")
        
        if submit:
            if new_password:
                if new_password != confirm_password:
                    st.error("❌ 비밀번호가 일치하지 않습니다.")
                elif len(new_password) < 4:
                    st.error("❌ 비밀번호는 4자리 이상이어야 합니다.")
                else:
                    update_data = {
                        "playerId": current_user.get('playerId'),
                        "playerPassword": new_password,
                        "playerMoney": current_user.get('playerMoney')
                    }
                    
                    if api.update_player(update_data):
                        st.success("✅ 비밀번호가 변경되었습니다.")
                    else:
                        st.error("❌ 정보 수정에 실패했습니다.")
            else:
                st.info("📝 변경할 정보가 없습니다.")

# 관리자 페이지들
def show_admin_dashboard():
    """관리자 대시보드"""
    require_admin()
    
    st.title("👑 관리자 대시보드")
    
    # 시스템 통계
    players_data = api.get_all_players(0, 1000)  # 전체 조회
    stocks_data = api.get_stocks(0, 1000)  # 전체 조회
    
    if players_data and stocks_data:
        players = players_data.get('data', [])
        stocks = stocks_data.get('data', [])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 총 플레이어 수", f"{len(players)}명")
        with col2:
            st.metric("📊 총 주식 종목 수", f"{len(stocks)}개")
        with col3:
            total_money = sum(p.get('playerMoney', 0) for p in players)
            st.metric("💰 총 보유 자금", format_currency(total_money))
        with col4:
            avg_money = total_money / len(players) if players else 0
            st.metric("📊 평균 보유 자금", format_currency(int(avg_money)))
        
        # 플레이어 자산 분포 차트
        if players:
            df_players = pd.DataFrame(players)
            fig_hist = px.histogram(df_players, x='playerMoney', title='플레이어 자산 분포')
            st.plotly_chart(fig_hist, use_container_width=True)

def show_admin_players():
    """플레이어 관리 페이지"""
    require_admin()
    
    st.title("👥 플레이어 관리")
    
    # 플레이어 목록 조회
    players_data = api.get_all_players(0, 100)
    
    if not players_data:
        st.error("❌ 플레이어 목록을 조회할 수 없습니다.")
        return
    
    players = players_data.get('data', [])
    
    if players:
        df_players = pd.DataFrame(players)
        
        # 플레이어 목록 표시
        st.subheader("📋 플레이어 목록")
        
        # 편집 가능한 데이터프레임
        edited_df = st.data_editor(
            df_players[['playerId', 'playerMoney']],
            column_config={
                'playerId': st.column_config.TextColumn('플레이어 ID', disabled=True),
                'playerMoney': st.column_config.NumberColumn('보유 자금', format='%d'),
            },
            use_container_width=True
        )
        
        # 변경사항 저장
        if st.button("💾 변경사항 저장"):
            for idx, row in edited_df.iterrows():
                original_money = df_players.iloc[idx]['playerMoney']
                new_money = row['playerMoney']
                
                if original_money != new_money:
                    update_data = {
                        'playerId': row['playerId'],
                        'playerMoney': new_money
                    }
                    
                    if api.update_player(update_data):
                        st.success(f"✅ {row['playerId']}의 자금이 업데이트되었습니다.")
                    else:
                        st.error(f"❌ {row['playerId']} 업데이트 실패")
        
        # 플레이어 삭제
        st.subheader("🗑️ 플레이어 삭제")
        delete_player_id = st.selectbox("삭제할 플레이어", 
                                       options=[p['playerId'] for p in players if p['playerId'] != 'admin'])
        
        if st.button("🗑️ 플레이어 삭제", type="secondary"):
            if delete_player_id and delete_player_id != 'admin':
                if api.delete_player(delete_player_id):
                    st.success(f"✅ {delete_player_id} 플레이어가 삭제되었습니다.")
                    st.rerun()
                else:
                    st.error("❌ 플레이어 삭제에 실패했습니다.")
    else:
        st.info("📝 등록된 플레이어가 없습니다.")

def show_admin_stocks():
    """주식 관리 페이지"""
    require_admin()
    
    st.title("📊 주식 관리")
    
    tab1, tab2 = st.tabs(["📋 주식 목록", "➕ 주식 추가"])
    
    with tab1:
        # 주식 목록 조회
        stocks_data = api.get_stocks(0, 100)
        
        if stocks_data:
            stocks = stocks_data.get('data', [])
            
            if stocks:
                df_stocks = pd.DataFrame(stocks)
                
                # 편집 가능한 데이터프레임
                edited_df = st.data_editor(
                    df_stocks[['id', 'stockName', 'stockPrice']],
                    column_config={
                        'id': st.column_config.NumberColumn('ID', disabled=True),
                        'stockName': st.column_config.TextColumn('종목명'),
                        'stockPrice': st.column_config.NumberColumn('가격', format='%d'),
                    },
                    use_container_width=True
                )
                
                # 변경사항 저장
                if st.button("💾 변경사항 저장"):
                    for idx, row in edited_df.iterrows():
                        original = df_stocks.iloc[idx]
                        
                        if (original['stockName'] != row['stockName'] or 
                            original['stockPrice'] != row['stockPrice']):
                            
                            update_data = {
                                'id': row['id'],
                                'stockName': row['stockName'],
                                'stockPrice': row['stockPrice']
                            }
                            
                            if api.update_stock(update_data):
                                st.success(f"✅ {row['stockName']} 정보가 업데이트되었습니다.")
                            else:
                                st.error(f"❌ {row['stockName']} 업데이트 실패")
                
                # 주식 삭제
                st.subheader("🗑️ 주식 삭제")
                delete_stock = st.selectbox("삭제할 주식", 
                                          options=[(s['id'], s['stockName']) for s in stocks],
                                          format_func=lambda x: x[1])
                
                if st.button("🗑️ 주식 삭제", type="secondary"):
                    if delete_stock:
                        if api.delete_stock(delete_stock[0]):
                            st.success(f"✅ {delete_stock[1]} 주식이 삭제되었습니다.")
                            st.rerun()
                        else:
                            st.error("❌ 주식 삭제에 실패했습니다.")
            else:
                st.info("📝 등록된 주식이 없습니다.")
    
    with tab2:
        # 새 주식 추가
        st.subheader("➕ 새 주식 추가")
        
        with st.form("add_stock_form"):
            stock_name = st.text_input("종목명")
            stock_price = st.number_input("주식 가격", min_value=1000, max_value=1000000, value=10000, step=1000)
            
            submit = st.form_submit_button("주식 추가")
            
            if submit:
                if stock_name and stock_price:
                    stock_data = {
                        'stockName': stock_name,
                        'stockPrice': stock_price
                    }
                    
                    if api.create_stock(stock_data):
                        st.success(f"✅ {stock_name} 주식이 추가되었습니다.")
                        st.rerun()
                    else:
                        st.error("❌ 주식 추가에 실패했습니다.")
                else:
                    st.warning("⚠️ 종목명과 가격을 모두 입력해주세요.")

# 메인 애플리케이션
def main():
    if not st.session_state.get('logged_in', False):
        show_login_page()
    else:
        create_sidebar()
        
        # 페이지 라우팅
        page = st.session_state.get('page', 'dashboard')
        
        if page == 'dashboard':
            show_dashboard()
        elif page == 'trading':
            show_trading()
        elif page == 'portfolio':
            show_portfolio()
        elif page == 'transactions':
            show_transactions()
        elif page == 'watchlist':
            show_watchlist()
        elif page == 'profile':
            show_profile()
        elif page == 'admin_dashboard':
            show_admin_dashboard()
        elif page == 'admin_players':
            show_admin_players()
        elif page == 'admin_stocks':
            show_admin_stocks()
        else:
            show_dashboard()

if __name__ == "__main__":
    main()
