# ---------- build backend (Maven) ----------
FROM openjdk:17-jdk-slim
WORKDIR /app
COPY . .
# mvnw가 있으면 mvnw, 없으면 mvn 사용
RUN if [ -f ./mvnw ]; then chmod +x ./mvnw && ./mvnw -q -DskipTests clean package; else mvn -q -DskipTests clean package; fi

# ---------- run: Java + Streamlit ----------
FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-21-jre-headless ca-certificates curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Maven 산출물 복사 (target/*.jar → app.jar)
COPY --from=build /app/target/*.jar /app/app.jar

# Streamlit 프론트
COPY src/main/resources/static/app.py /app/app.py
COPY src/main/resources/static/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# 환경 변수
ENV TZ=Asia/Seoul
ENV BACKEND_BASE_URL=http://127.0.0.1:9080
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

EXPOSE 9080 8501

# 두 프로세스 동시 실행
CMD java -jar /app/app.jar --server.port=9080 & streamlit run /app/app.py --server.port=8501 --server.address=0.0.0.0 && wait