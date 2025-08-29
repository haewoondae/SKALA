-- 현재 잠금 보유/대기 중인 세션 확인
-- pg_locks – 잠금 정보 모니터링
SELECT 
    pid,
    mode,
    relation::regclass AS table_name,
    granted,
    now() - pg_stat_activity.query_start AS query_duration,
    pg_stat_activity.query
FROM pg_locks
JOIN pg_stat_activity USING (pid)
WHERE relation IS NOT NULL
ORDER BY granted DESC;
