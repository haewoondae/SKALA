-- 누가 누구를 막고 있는가
SELECT
  bl.pid       AS waiting_pid,
  wl.pid       AS blocking_pid,
  bl.query     AS waiting_query,
  wl.query     AS blocking_query,
  now() - bl.query_start AS waiting_for
FROM pg_catalog.pg_locks l1
JOIN pg_catalog.pg_stat_activity bl ON bl.pid = l1.pid
JOIN pg_catalog.pg_locks l2 ON l1.locktype = l2.locktype
  AND l1.DATABASE IS NOT DISTINCT FROM l2.DATABASE
  AND l1.relation IS NOT DISTINCT FROM l2.relation
  AND l1.page IS NOT DISTINCT FROM l2.page
  AND l1.tuple IS NOT DISTINCT FROM l2.tuple
  AND l1.virtualxid IS NOT DISTINCT FROM l2.virtualxid
  AND l1.transactionid IS NOT DISTINCT FROM l2.transactionid
  AND l1.classid IS NOT DISTINCT FROM l2.classid
  AND l1.objid IS NOT DISTINCT FROM l2.objid
  AND l1.objsubid IS NOT DISTINCT FROM l2.objsubid
  AND l1.pid <> l2.pid
JOIN pg_catalog.pg_stat_activity wl ON wl.pid = l2.pid
WHERE NOT l1.granted AND l2.granted
ORDER BY waiting_for DESC;

