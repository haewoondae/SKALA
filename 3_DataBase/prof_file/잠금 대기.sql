-- 잠금 대기 상태인 세션만 보기
SELECT pid, mode, relation::regclass, granted, query
FROM pg_locks
JOIN pg_stat_activity USING (pid)
WHERE NOT granted;
