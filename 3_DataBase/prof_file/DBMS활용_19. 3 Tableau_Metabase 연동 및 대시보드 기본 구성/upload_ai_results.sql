
DROP TABLE IF EXISTS clustered_segments;

CREATE TABLE clustered_segments (
    customer_id INTEGER,
    age INTEGER,
    annual_income INTEGER,
    spending_score INTEGER,
    visits_per_month INTEGER,
    pca_x FLOAT,
    pca_y FLOAT,
    cluster INTEGER
);

-- 예시: CSV 업로드 후 COPY 명령어 또는 pandas to_sql 사용
-- COPY clustered_segments FROM '/path/to/clustered_segments.csv' DELIMITER ',' CSV HEADER;
