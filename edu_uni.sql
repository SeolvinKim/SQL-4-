DROP SCHEMA IF EXISTS edu_uni CASCADE;

CREATE SCHEMA edu_uni;

=================================

CREATE TABLE edu_uni.students (
    student_id      INTEGER PRIMARY KEY,
    student_name    VARCHAR(30) NOT NULL,
    birth_year      INTEGER,
    gender          VARCHAR(10) NOT NULL,
    department_id   INTEGER NOT NULL,
    email           VARCHAR(50) UNIQUE NOT NULL,
    phone_number    VARCHAR(30) UNIQUE NOT NULL,
    address         VARCHAR(80) NOT NULL,
    
    constraint fk_grades
        foreign key (student_id)
        references edu_uni.grades(student_id),
    constraint fk_departments
        foreign key (department_id)
        references edu_uni.departments(department_id)
);


--자료추가--

INSERT into edu_uni.students values
(1, '김예린', 2001, 'F', 1, '1111@naver.com', '010-1111-1111', 'SEOUL'),
(2, '염지유', 2004, 'F', 2, '2222@gmail.com', '010-2222-2222', 'INCHEON'),
(3, '김설빈', 1997, 'F', 3, '3333@naver.com', '010-3333-3333', 'BUSAN'),
(4, '박혜준', 1999, 'M', 1, '4444@gmail.com', '010-4444-4444', 'SEOUL'),
(5, '노재희', 1999, 'F', 2, '5555@daum.net', '010-5555-5555', 'BUSAN');




CREATE TABLE edu_uni.departments (
		department_id INTEGER PRIMARY KEY,
		department_name VARCHAR(20) NOT NULL,
		location_id INTEGER NOT NULL,
		contact_number VARCHAR(15) NOT NULL,
		student_count INTEGER
);



/*자료추가*/
 
INSERT INTO edu_uni.departments
    (department_id, department_name, location_id, contact_number, student_count)
VALUES
    (1, '기계공학과', 1, '02-5614-1875', 120),
    (2, '화학공학과', 2, '02-2757-2222', 95),
    (3, '전기전자공학부', 3, '02-5888-7923', 150);



CREATE TABLE edu_uni.classes (
		class_id INTEGER PRIMARY KEY,
		class_name VARCHAR(100) NOT NULL,
		class_type VARCHAR(20) NOT NULL,
		max_students INTEGER NOT NULL,
		semester VARCHAR(20) NOT NULL
		CHECK (semester IN ('1학기','2학기','여름','겨울'))
);


/*자료추가*/

INSERT INTO edu_uni.classes VALUES
    (1, '기계설계','전공', 40, '1학기'),
    (2, '열역학','전공', 35, '1학기'),
    (3, '재료역학','전공', 40, '2학기'),

    (4, '유기화학','전공', 35, '1학기'),
    (5, '화공양론','전공', 30, '2학기'),
    (6, '반응공학','전공', 30, '2학기'),

    (7, '회로이론','전공', 45, '1학기'),
    (8, '전자회로','전공', 40, '2학기'),
    (9, '디지털공학','전공', 40, '1학기'),

    (10, '공학수학','교양', 50, '여름');



CREATE TABLE edu_uni.professors (
		professor_id INTEGER PRIMARY KEY,
		professor_name VARCHAR(50) NOT NULL,
		age INTEGER,
		department_id INTEGER NOT NULL,
		email VARCHAR(100) UNIQUE,
		gender VARCHAR(2) CHECK (gender IN ('M', 'F')),

CONSTRAINT fk_departments 
    FOREIGN KEY (department_id) 
    REFERENCES edu_uni.departments(department_id)
);


/*자료추가*/

INSERT INTO edu_uni.professors VALUES
(1, '김병철', 30,1, 'kim@gmail.com','F'),
(2, '김찬영', 35,3,  'young@naver.com', 'M'),
(3, '이정수', 35,2, 'jsjs@gmail.com','M');



CREATE TABLE edu_uni.grades (
    grade VARCHAR(4) CHECK (grade IN ('A+','A','B+', 'B','C+', 'C','D+','D','F')),
    lecture_name VARCHAR(100) PRIMARY KEY,
    professor_name VARCHAR(50) NOT NULL,
    class_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,


CONSTRAINT fk_classes
	FOREIGN KEY (class_id)
	REFERENCES edu_uni.classes(class_id)
);




INSERT INTO edu_uni.grades (grade, lecture_name, professor_name, class_id, student_id) VALUES

('A+', '기계설계', '김병철', 1, 1),
('B+', '열역학', '김병철', 2, 2),
('A', '유기화학', '이정수', 4,2),
('C+', '회로이론', '김찬영', 7, 3),
('A+', '디지털공학', '김찬영', 9, 3),


('B', '재료역학', '김병철', 3,3),
('A+', '화공양론', '이정수', 5,4),
('F', '반응공학', '이정수', 6,5),
('A', '전자회로', '김찬영', 8,4),


('B+', '공학수학', '김찬영', 10,1);




/*1. 학생의 나이를 많은 사람부터*/


SELECT *
	FROM edu_uni.students
	ORDER BY birth_year;


/*2. 서울 사는 학생들의 이름과 학번 조회*/

SELECT student_id, student_name
	FROM edu_uni.students
	WHERE address = 'SEOUL';

/*3. 1학기에만 열리는 과목 조회 */


SELECT *
	FROM edu_uni.classes
	WHERE semester = '1학기';


/*4. 성적이 A 이상인 학생*/


select
    s.student_id,
    s.student_name,
    g.lecture_name,
    g.grade
from edu_uni.grades g
join edu_uni.students s using(student_id)
where g.grade = 'A' or g.grade = 'A+'
order by g.grade DESC;


/*5. 이메일 도메인이 [naver.com](http://naver.com) 인 학생*/
SELECT *
	FROM edu_uni.students
	WHERE email ILIKE '%@naver.com';
