
-- 클러스터별 고객 수 및 평균 소득
SELECT 
  cluster,
  COUNT(*) AS customer_count,
  ROUND(AVG(annual_income)) AS avg_income,
  ROUND(AVG(spending_score), 1) AS avg_spending_score
FROM clustered_segments
GROUP BY cluster
ORDER BY cluster;

-- 시간 흐름별(예: 고객 가입 일자 컬럼이 있는 경우) 이탈 예측률 트렌드 예시
-- SELECT join_date::date, ROUND(AVG(churn_probability), 2) AS avg_churn
-- FROM clustered_segments
-- GROUP BY join_date::date
-- ORDER BY join_date::date;

-- 클러스터별 특성 평균 비교
SELECT
  cluster,
  ROUND(AVG(age), 1) AS avg_age,
  ROUND(AVG(annual_income)) AS avg_income,
  ROUND(AVG(spending_score), 1) AS avg_score,
  ROUND(AVG(visits_per_month), 1) AS avg_visits
FROM clustered_segments
GROUP BY cluster
ORDER BY cluster;
