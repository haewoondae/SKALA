# -------------------------------------------------------------
# 작성자 : 
# 작성목적 : KDT 교육용 AI 설계안 등록 통합 실습 (FastAPI + Streamlit + PostgreSQL)
# 작성일 : 2025-06
# 본 파일은 KDT 교육을 위한 Sample 코드이므로 작성자에게 모든 저작권이 있습니다.
# 
# 변경사항 내역 (날짜, 변경목적, 변경내용 순으로 기입)
# 
# -------------------------------------------------------------

## FastAPI 서버 (app.py)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import psycopg2

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_db_conn():
    return psycopg2.connect(
        dbname="yourdb", user="youruser", password="yourpass", host="localhost"
    )

class DesignInput(BaseModel):
    title: str
    description: str

@app.post("/register_design")
def register_design(data: DesignInput):
    conn = get_db_conn()
    cur = conn.cursor()
    try:
        embedding = model.encode(data.description).tolist()
        cur.execute("BEGIN;")
        cur.execute("""
            INSERT INTO design (title, description, embedding)
            VALUES (%s, %s, %s);
        """, (data.title, data.description, embedding))
        conn.commit()
        return {"status": "success", "message": "등록 완료"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"등록 실패: {str(e)}")
    finally:
        cur.close()
        conn.close()


## Streamlit 클라이언트 (streamlit_client.py)
import streamlit as st
import requests

st.title("AI 설계안 등록")

title = st.text_input("설계안 제목")
description = st.text_area("설계안 설명")

if st.button("등록 요청"):
    response = requests.post("http://localhost:8000/register_design", json={
        "title": title,
        "description": description
    })
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error(response.json()["detail"])

