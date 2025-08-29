-- 현재 역할(Roles) 목록 및 속성
SELECT rolname, rolsuper, rolcreatedb, rolcreaterole, rolcanlogin
FROM pg_roles
ORDER BY rolname;


-- 사용자별 테이블 권한 확인 (information_schema 기준)
SELECT grantee, table_schema, table_name, privilege_type
FROM information_schema.role_table_grants
WHERE grantee IN ('data_engineer', 'data_analyst', 'api_user')
ORDER BY grantee, table_name;


-- 특정 사용자가 가진 함수 권한
SELECT grantee, routine_schema, routine_name, privilege_type
FROM information_schema.role_routine_grants
WHERE grantee = 'data_analyst';


-- 특정 테이블에 대해 어떤 권한이 부여되었는지
-- 테이블 명은 원하는 테이블명으로 (Comment 지우고 확인!!!)
SELECT *
FROM information_schema.role_table_grants
-- WHERE table_name = '원하는 테이블명';


-- 현재 세션의 사용자 정보 확인
SELECT current_user, session_user;
