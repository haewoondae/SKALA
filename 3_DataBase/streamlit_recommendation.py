import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="사용자 추천 시스템", layout="wide")

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

@st.cache_data
def load_users():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        df = pd.read_sql("""
            SELECT ub.user_id, ub.age, ub.income, ub.gender, ub.spending_score, ub.visit_count
            FROM user_behavior ub
            JOIN user_embeddings ue ON ub.user_id = ue.user_id
            ORDER BY ub.user_id
        """, conn)
        return df
    finally:
        conn.close()

def get_recommendations(user_id, method, limit):
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        if method == "euclidean":
            query = """
                SELECT ub.user_id, 
                       1 / (1 + (ue1.embedding <-> ue2.embedding)) AS similarity,
                       ub.age, ub.income, ub.gender, ub.spending_score, ub.visit_count
                FROM user_embeddings ue1
                CROSS JOIN user_embeddings ue2
                JOIN user_behavior ub ON ue1.user_id = ub.user_id
                WHERE ue2.user_id = %s AND ue1.user_id != %s
                ORDER BY ue1.embedding <-> ue2.embedding
                LIMIT %s;
            """
        else:
            query = """
                SELECT ub.user_id,
                       1 - (ue1.embedding <=> ue2.embedding) AS similarity,
                       ub.age, ub.income, ub.gender, ub.spending_score, ub.visit_count
                FROM user_embeddings ue1
                CROSS JOIN user_embeddings ue2
                JOIN user_behavior ub ON ue1.user_id = ub.user_id
                WHERE ue2.user_id = %s AND ue1.user_id != %s
                ORDER BY ue1.embedding <=> ue2.embedding
                LIMIT %s;
            """
        
        df = pd.read_sql(query, conn, params=(user_id, user_id, limit))
        return df
    except Exception as e:
        st.error(f"오류: {str(e)}")
        return pd.DataFrame()
    finally:
        conn.close()

# 메인
st.title("🎯 사용자 추천 시스템")

df_users = load_users()
if df_users.empty:
    st.error("데이터를 불러올 수 없습니다.")
    st.stop()

# 사이드바
selected_user = st.sidebar.selectbox("사용자 선택", df_users['user_id'].tolist())
method = st.sidebar.radio("유사도 방법", ["euclidean", "cosine"])
limit = st.sidebar.slider("추천 수", 1, 10, 5)

user_info = df_users[df_users['user_id'] == selected_user].iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"선택된 사용자: {selected_user}")
    st.write(f"나이: {user_info['age']}세")
    st.write(f"소득: {user_info['income']:,}원") 
    st.write(f"성별: {user_info['gender']}")
    st.write(f"소비점수: {user_info['spending_score']}")

with col2:
    st.subheader("추천 결과")
    recommendations = get_recommendations(selected_user, method, limit)
    
    for idx, row in recommendations.iterrows():
        st.write(f"**{idx+1}. {row['user_id']}** (유사도: {row['similarity']:.3f})")
        st.write(f"나이: {row['age']}세, 소득: {row['income']:,}원")