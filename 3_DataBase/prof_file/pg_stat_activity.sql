-- 현재 실행 중인 쿼리 확인 (Idle 제외)
-- pg_stat_activity – 세션 활동 실시간 보기 
SELECT pid, usename, state, wait_event_type, wait_event, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY backend_start DESC;
