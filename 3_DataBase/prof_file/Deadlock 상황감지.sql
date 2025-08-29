-- 로그 기반 데드락 메시지 확인 (로그 설정 필요)
-- log_lock_waits = on / log_min_messages = notice
SELECT * FROM pg_catalog.pg_logs WHERE message LIKE '%deadlock%';
