/* ============================================================
   0. 공통 스키마(public) ─ 교수 · 공통 강좌
   ============================================================ */
-- 교수(강사) 카탈로그
CREATE TABLE IF NOT EXISTS public.professor (
    professor_id  SERIAL PRIMARY KEY,
    name          VARCHAR(50)  NOT NULL,
    email         VARCHAR(100) UNIQUE
);

-- 과정(강좌) 마스터
CREATE TABLE IF NOT EXISTS public.course_master (
    master_course_id SERIAL PRIMARY KEY,
    title            VARCHAR(100) NOT NULL,
    default_desc     TEXT
);

/* ============================================================
   1. 서울 캠퍼스 = public
   ============================================================ */
-- 1-1 강사 매핑(공통 professor ↔ 서울 instructor_id)
CREATE TABLE IF NOT EXISTS public.instructor_map (
    instructor_id SERIAL PRIMARY KEY,
    professor_id  INT NOT NULL
        REFERENCES public.professor(professor_id) ON DELETE RESTRICT
);

-- 1-2 과정
CREATE TABLE IF NOT EXISTS public.course (
    course_id        SERIAL PRIMARY KEY,
    master_course_id INT  NOT NULL
        REFERENCES public.course_master(master_course_id) ON DELETE RESTRICT,
    instructor_id    INT  NOT NULL
        REFERENCES public.instructor_map(instructor_id)   ON DELETE RESTRICT,
    title_override   VARCHAR(100),
    start_date       DATE,
    end_date         DATE
);

-- 1-3 수강생
CREATE TABLE IF NOT EXISTS public.learner (
    student_id SERIAL PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    major      VARCHAR(50)
);

-- 1-4 과정 설명(1:1)
CREATE TABLE IF NOT EXISTS public.course_description (
    course_id   INT PRIMARY KEY
        REFERENCES public.course(course_id) ON DELETE CASCADE,
    description TEXT
);

-- 1-5 수강(N:M)
CREATE TABLE IF NOT EXISTS public.enrollment (
    enrollment_id SERIAL PRIMARY KEY,
    course_id  INT NOT NULL
        REFERENCES public.course(course_id)   ON DELETE CASCADE,
    student_id INT NOT NULL
        REFERENCES public.learner(student_id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (course_id, student_id)
);

-- 1-6 리뷰
CREATE TABLE IF NOT EXISTS public.review (
    review_id  SERIAL PRIMARY KEY,
    course_id  INT NOT NULL
        REFERENCES public.course(course_id)   ON DELETE CASCADE,
    student_id INT NOT NULL
        REFERENCES public.learner(student_id) ON DELETE CASCADE,
    rating     INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    UNIQUE (course_id, student_id)
);

/* ============================================================
   2. 제주 캠퍼스 = jeju    (구조는 서울(public)과 동일)
   ============================================================ */
CREATE SCHEMA IF NOT EXISTS jeju;

-- 2-1 강사 매핑
CREATE TABLE IF NOT EXISTS jeju.instructor_map (
    instructor_id SERIAL PRIMARY KEY,
    professor_id  INT NOT NULL
        REFERENCES public.professor(professor_id) ON DELETE RESTRICT
);

-- 2-2 과정
CREATE TABLE IF NOT EXISTS jeju.course (
    course_id        SERIAL PRIMARY KEY,
    master_course_id INT  NOT NULL
        REFERENCES public.course_master(master_course_id) ON DELETE RESTRICT,
    instructor_id    INT  NOT NULL
        REFERENCES jeju.instructor_map(instructor_id)     ON DELETE RESTRICT,
    title_override   VARCHAR(100),
    start_date       DATE,
    end_date         DATE
);

-- 2-3 수강생
CREATE TABLE IF NOT EXISTS jeju.learner (
    student_id SERIAL PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    major      VARCHAR(50)
);

-- 2-4 과정 설명
CREATE TABLE IF NOT EXISTS jeju.course_description (
    course_id   INT PRIMARY KEY
        REFERENCES jeju.course(course_id) ON DELETE CASCADE,
    description TEXT
);

-- 2-5 수강
CREATE TABLE IF NOT EXISTS jeju.enrollment (
    enrollment_id SERIAL PRIMARY KEY,
    course_id  INT NOT NULL
        REFERENCES jeju.course(course_id)   ON DELETE CASCADE,
    student_id INT NOT NULL
        REFERENCES jeju.learner(student_id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (course_id, student_id)
);

-- 2-6 리뷰
CREATE TABLE IF NOT EXISTS jeju.review (
    review_id  SERIAL PRIMARY KEY,
    course_id  INT NOT NULL
        REFERENCES jeju.course(course_id)   ON DELETE CASCADE,
    student_id INT NOT NULL
        REFERENCES jeju.learner(student_id) ON DELETE CASCADE,
    rating     INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    UNIQUE (course_id, student_id)
);
