-- ===== 1. 사용자·강사·관리자 역할 분리 =====
CREATE TABLE Instructor (
    instructor_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE Admin (
    admin_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE Learner (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    major VARCHAR(50)
);

-- ===== 2. 교육과정 =====
CREATE TABLE Course (
    course_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    instructor_id INT REFERENCES Instructor(instructor_id) ON DELETE RESTRICT,
    admin_id INT REFERENCES Admin(admin_id) ON DELETE RESTRICT
);

-- ===== 3. 과정 설명 1:1 =====
CREATE TABLE CourseDescription (
    course_id INT PRIMARY KEY REFERENCES Course(course_id) ON DELETE CASCADE,
    description TEXT
);

-- ===== 4. 교차 테이블: 수강 정보 =====
CREATE TABLE Enrollment (
    enrollment_id SERIAL PRIMARY KEY,
    course_id INT REFERENCES Course(course_id) ON DELETE CASCADE,
    student_id INT REFERENCES Learner(student_id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (course_id, student_id)
);

-- ===== 5. 리뷰 =====
CREATE TABLE Review (
    review_id SERIAL PRIMARY KEY,
    course_id INT REFERENCES Course(course_id) ON DELETE CASCADE,
    student_id INT REFERENCES Learner(student_id) ON DELETE CASCADE,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    posted_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (course_id, student_id)
);
