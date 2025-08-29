-- === 변수처럼 사용: 바꿔 넣으세요 ===
-- 데이터베이스: mydb
-- 대상 스키마들: public 만 예시
-- 테이블/함수 등 오브젝트를 만드는 소유자: app_owner

BEGIN;

-- 1) 그룹 역할 생성 (NOLOGIN: 로그인 불가, 권한 묶음으로만 사용)
CREATE ROLE readonly_role  NOLOGIN;
CREATE ROLE analyst_role   NOLOGIN;
CREATE ROLE admin_role     NOLOGIN;

-- 2) 데이터베이스 접속/임시테이블 권한
GRANT CONNECT, TEMP ON DATABASE mydb TO readonly_role, analyst_role;

-- 3) 스키마/오브젝트 권한 (필요한 스키마 목록에 대해 반복)
DO $$
DECLARE s text;
BEGIN
  FOREACH s IN ARRAY ARRAY['public'] LOOP
    -- 스키마 접근
    EXECUTE format('GRANT USAGE ON SCHEMA %I TO readonly_role, analyst_role;', s);

    -- 기존 테이블/뷰 읽기
    EXECUTE format('GRANT SELECT ON ALL TABLES IN SCHEMA %I TO readonly_role, analyst_role;', s);

    -- 시퀀스 읽기(다음값 조회 등)
    EXECUTE format('GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA %I TO readonly_role, analyst_role;', s);

    -- 함수/프로시저 실행은 분석가에게만
    EXECUTE format('GRANT EXECUTE ON ALL FUNCTIONS   IN SCHEMA %I TO analyst_role;', s);
    EXECUTE format('GRANT EXECUTE ON ALL PROCEDURES IN SCHEMA %I TO analyst_role;', s);
  END LOOP;
END $$;

-- 4) 앞으로 생성될 오브젝트의 기본 권한(중요!)
--    기본 권한은 "오브젝트 소유자" 기준으로 설정해야 합니다.
ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA public
  GRANT SELECT ON TABLES TO readonly_role, analyst_role;

ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA public
  GRANT USAGE, SELECT ON SEQUENCES TO readonly_role, analyst_role;

ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA public
  GRANT EXECUTE ON FUNCTIONS TO analyst_role;

ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA public
  GRANT EXECUTE ON PROCEDURES TO analyst_role;

-- 5) 관리자 역할: 슈퍼유저로 쓸지, DB/스키마 단위로 제한할지 선택
-- (A) 진짜 최고관리자
-- ALTER ROLE admin_role WITH SUPERUSER;

-- (B) 제한된 관리자(생성 권한만 예시)
GRANT CREATE ON DATABASE mydb TO admin_role;
GRANT USAGE, CREATE ON SCHEMA public TO admin_role;

COMMIT;

-- 6) 실제 사용자에 부여 예시
-- CREATE ROLE alice LOGIN PASSWORD '***';
-- GRANT readonly_role TO alice;   -- 읽기 전용 부여
-- GRANT analyst_role  TO bob;     -- 분석가 권한 부여
-- GRANT admin_role    TO charlie; -- (선택) 관리자 권한 부여
