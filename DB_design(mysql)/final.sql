-- drop database dummy;
create database dummy;
use dummy;

CREATE TABLE faculty (
    Teacher_Id VARCHAR(50) not null PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Course_Id VARCHAR(10),
    Expertise VARCHAR(100),
    YearsOfExperience INT,
    Gender ENUM('male', 'female'),
    Recognitions VARCHAR(100),
    Email VARCHAR(100) not null CHECK (Email LIKE '%@%'),
    OfficeHours ENUM('Mon-Fri: 9am-5pm', 'Thu-Sat: 9am-5pm', 'Mon-Wed: 8am-4pm', 'Tue-Sat: 10am-6pm')
--     FOREIGN KEY (Teacher_Id) REFERENCES User(UsernameId) ON DELETE CASCADE
);

-- Add the department column to the faculty table
ALTER TABLE faculty
ADD COLUMN Department ENUM('Computer Science', 'Data Science', 'Statistics', 'Chemistry', 'Admin', 'Intelligent Systems');

#ALTER TABLE faculty
#DROP COLUMN Department;

ALTER TABLE faculty
ADD COLUMN status VARCHAR(10) NOT NULL DEFAULT 'teacher';

CREATE TABLE students (
    StudentId VARCHAR(50) not null PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100) not null CHECK (Email LIKE '%@%'),
    Phone VARCHAR(10),
    Gender ENUM('male', 'female'),
    CoursesTaken TEXT,
    AdmissionNo VARCHAR(20),
    Address VARCHAR(255),
    ClassId VARCHAR(10),
    Stream ENUM('Graduate', 'Undergraduate'),
    Department ENUM('Computer Science', 'Data Science', 'Statistics', 'Chemistry'),
    AdmissionDate TIMESTAMP,
    AcademicYear VARCHAR(10)
);

ALTER TABLE students
ADD COLUMN status VARCHAR(10) NOT NULL DEFAULT 'student';

-- ALTER TABLE faculty
-- ADD COLUMN OfficeHours ENUM('Mon-Fri: 9am-5pm', 'Thu-Sat: 9am-5pm', 'Mon-Wed: 8am-4pm', 'Tue-Sat: 10am-6pm'); 

-- Adding classteacher column to students table
ALTER TABLE students
ADD COLUMN classteacher VARCHAR(10);  

-- Adding foreign key constraint for classteacher referencing Teacher_Id in faculty table
ALTER TABLE students
ADD CONSTRAINT fk_students_faculty FOREIGN KEY (classteacher) REFERENCES faculty(Teacher_Id);

-- Adding the foreign key constraint for students table referencing user table
-- ALTER TABLE students
-- ADD CONSTRAINT fk_students_user FOREIGN KEY (StudentId) REFERENCES user(usernameId);


INSERT INTO faculty (Teacher_Id, FirstName, LastName, Course_Id, Expertise, YearsOfExperience, Recognitions, Email, Gender, OfficeHours, Department, Status)
VALUES 
('101_Mark', 'Mark', 'Taylor', 'CSE101', 'Computer Science', 4, 'Best Teacher Award 2020', 'mark.taylor@example.com','male', 
'Thu-Sat: 9am-5pm', 'Computer Science', 'Teacher'),
('102_Veda', 'Veda', 'Vyas', 'IE201', 'Administration', 3, 'IT Developer Award', 'veda@example.com', 'male',
'Mon-Wed: 8am-4pm', 'Admin', 'Teacher'),
('103_Vyas', 'Vyas', 'Sayvadev', 'STAT101', 'IT tools', 7, 'Outstanding Admin Award', 'vyas@example.com', 'male',
'Tue-Sat: 10am-6pm', 'Admin', 'Teacher'),
('104_Emily', 'Emily', 'Clark', 'DS201', 'Data Analysis', 3, 'Research Excellence Award', 'emily.clark@example.com', 'female',
'Mon-Wed: 8am-4pm', 'Data Science', 'Teacher'),
('105_David', 'David', 'Wilson', 'STAT101', 'Statistical Models', 7, 'Outstanding Educator Award', 'david.wilson@example.com', 'male',
'Tue-Sat: 10am-6pm', 'Statistics', 'Teacher'),
('106_Sophia', 'Sophia', 'Brown', 'CHEM101', 'Organic Chemistry', 2, 'Innovative Teaching Award', 'sophia.brown@example.com', 'female',
'Mon-Fri: 9am-5pm', 'Chemistry', 'Teacher'),
('107_Nasim', 'Nasim', 'Anousheh', 'IS101', 'Intelligent Sysytems I', 2, 'Best Researcher Award', 'nasim.anousheh@example.com', 'female',
'Mon-Fri: 9am-5pm', 'Intelligent Systems', 'Teacher');

INSERT INTO students (StudentId, FirstName, LastName, Email, Phone,Gender, CoursesTaken, AdmissionNo, Address, ClassId,
Stream, Department, AdmissionDate, AcademicYear, classteacher, status)
VALUES 
('1001_Michael', 'Michael', 'Johnson', 'michael.johnson@example.com', '9876543210', 'male',
'CSE101, MATH101', 'ADM001', '123 Main St, City',
 'CLASS_101', 'Graduate',  'Computer Science', '2022-01-15', '2022-2023', '101_Mark', 'Student'),
('1002_Emma', 'Emma', 'Wilson', 'emma.wilson@example.com', '1234567890', 'female',
'DS201, STAT101', 'ADM002', '456 Elm St, Town',
 'CLASS_102',  'Undergraduate', 'Data Science', '2021-09-10', '2021-2022', '104_Emily', 'Student'),
('1003_Oliver', 'Oliver', 'Taylor', 'oliver.taylor@example.com', '7890123456', 'male',
'CHEM101, BIO101', 'ADM003', '789 Oak St, Village',
 'CLASS_103', 'Undergraduate',  'Chemistry', '2020-08-20', '2020-2021', '106_Sophia', 'Student'),
('1004_Sophia', 'Sophia', 'Moore', 'sophia.moore@example.com', '2345678901', 'female',
'STAT101, CSE101', 'ADM004', '345 Pine St, County',
 'CLASS_104', 'Graduate',  'Statistics', '2019-12-05', '2019-2020', '105_David', 'Student'),
 ('1005_Vedavyas', 'Vedavyas', 'Chakkirala', 'vedavyas.chakkirala@example.com', '2345678901', 'male',
'STAT101, CSE101, IS101', 'ADM004', '345 Pine St, County',
 'CLASS_104', 'Graduate',  'Statistics', '2019-12-05', '2019-2020', '107_Nasim', 'Student');
 
select * from students;
select * from faculty;

-- Created by Vedavyas, Sumit
CREATE TABLE IF NOT EXISTS user (
    UsernameId VARCHAR(50) not null PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100) not null CHECK (Email LIKE '%@%'),
    Password VARCHAR(100) not null,
    PhoneNumber VARCHAR(10) CHECK (CHAR_LENGTH(PhoneNumber) = 10),
    Gender ENUM('male', 'female')
);
ALTER TABLE user
ADD COLUMN status VARCHAR(10) NOT NULL DEFAULT 'Admin';

INSERT INTO user (UsernameId, FirstName, LastName, Email, Password, PhoneNumber, Gender, Status)
VALUES 
-- ('101_Mark', 'Mark', 'Taylor', 'mark.taylor@example.com', 'password123', '1234567890', 'male', 'Teacher'),
-- ('104_Emily', 'Emily', 'Clark', 'emily.clark@example.com', 'password456', '9876543210', 'female', 'Teacher'),
-- ('105_David', 'David', 'Wilson', 'david.wilson@example.com', 'password789', '4567890123', 'male', 'Teacher'),
-- ('106_Sophia', 'Sophia', 'Brown', 'sophia.brown@example.com', 'passwordabc', '7890123456', 'female', 'Teacher'),
('102_Veda', 'Veda', 'Vyas', 'veda@example.com','password123', '1234567790', 'male','Admin'),
('103_Vyas', 'VyasVyas', 'Sayvadev', 'vyas@example.com','password456', '9876544210', 'female','Admin');
-- ('1003_Oliver', 'Oliver', 'Taylor', 'oliver.taylor@example.com','password789', '4566890123', 'male','Student'),
-- ('1004_Sophia', 'Sophia', 'Moore', 'sophia.moore@example.com','passwordabc', '7890123456', 'female','Student');

select * from user;

CREATE TABLE IF NOT EXISTS courses (
    course_id VARCHAR(50) not null PRIMARY KEY,
    faculty_id VARCHAR(50) not null,
    course_name VARCHAR(100),
    topics_covered TEXT,
    rating FLOAT CHECK (rating >= 0 AND rating <= 5),
    FOREIGN KEY (faculty_id) REFERENCES faculty(Teacher_Id)
);

-- Add foreign key constraint for faculty_id in courses table
ALTER TABLE courses
ADD CONSTRAINT fk_courses_faculty FOREIGN KEY (faculty_id) REFERENCES faculty(Teacher_Id);

-- Add foreign key constraint for course_id in faculty table
ALTER TABLE faculty
ADD CONSTRAINT fk_faculty_courses FOREIGN KEY (Course_Id) REFERENCES courses(course_id);

-- Created by Vedavyas
INSERT INTO courses (course_id, faculty_id, course_name, topics_covered, rating)
VALUES 
  ('STAT101', '105_David', 'Statistics 101', 'Descriptive Statistics, Probability Distributions, Hypothesis Testing', 4.5),
  ('CSE101', '101_Mark', 'Computer Science 101', 'Introduction to Programming, Data Structures, Algorithms', 4.8),
  ('IE201', '102_Veda', 'Data Adminstration 201', 'Data Engineering, Data Visualization', 4.9),
  ('IS101', '107_Nasim', 'Intelligent Sysytems 101', 'Atomic Structure, Chemical Reactions, Periodic Table', 5.0),
  ('DS201', '104_Emily', 'Data Science 201', 'Data Preprocessing, Machine Learning Algorithms, Data Visualization', 4.6),
  ('CHEM101', '106_Sophia', 'Chemistry 101', 'Atomic Structure, Chemical Reactions, Periodic Table', 4.3);
  
-- Created by Sumit
CREATE TABLE classes (
    class_id VARCHAR(50) not null PRIMARY KEY,
    class_name VARCHAR(100),
    class_teacher_id VARCHAR(10) not null,
    Department ENUM('Computer Science', 'Data Science', 'Statistics', 'Chemistry', 'Administration')
);

-- Adding foreign key constraint for class_teacher_id referencing Teacher_Id in faculty table
ALTER TABLE classes
ADD CONSTRAINT fk_classes_faculty FOREIGN KEY (class_teacher_id) REFERENCES faculty(Teacher_Id);

-- Adding the foreign key constraint for class_id referencing class_id in students table
ALTER TABLE students
ADD CONSTRAINT fk_students_classes FOREIGN KEY (ClassId) REFERENCES classes(class_id);

-- -- Created by Sumit
INSERT INTO classes (class_id, class_name, class_teacher_id, Department)
VALUES 
    ('CLASS_101', 'Introduction to Computer Science', '101_Mark', 'Computer Science'),
    ('CLASS_102', 'Data Science Fundamentals', '104_Emily', 'Data Science'),
    ('CLASS_104', 'Statistics for Beginners', '105_David', 'Statistics'),
    ('CLASS_103', 'Chemistry Basics', '106_Sophia', 'Chemistry');

-- -- Created by Sumit
CREATE TABLE Faculty_attendance (
    teacher_id VARCHAR(100) not null,
    department ENUM('Computer Science', 'Data Science', 'Statistics','Intelligent Systems', 'Chemistry', 'Administration'),
    Class_id VARCHAR(10) not null,
    Date TIMESTAMP,
    Attendance ENUM('Present', 'Day-Off', 'On-Duty','Half-day'),
    PRIMARY KEY (teacher_id),
    FOREIGN KEY (teacher_id) REFERENCES faculty(Teacher_Id),
    FOREIGN KEY (Class_id) REFERENCES classes(class_id)
);

# alter table Faculty_attendance
# add column  department ENUM('Computer Science', 'Data Science', 'Statistics','Intelligent Systems', 'Chemistry', 'Administration');

-- -- Created by Sumit
INSERT INTO Faculty_attendance (teacher_id, department, Class_id, Date, Attendance)
VALUES 
    ('101_Mark', 'Computer Science', 'CLASS_101', '2024-03-06 09:00:00', 'Present'),
    ('104_Emily', 'Data Science', 'CLASS_102', '2024-03-06 09:00:00', 'Present'),
    ('106_Sophia', 'Chemistry', 'CLASS_103', '2024-03-06 09:00:00', 'Day-Off'),
--     ('103_Vyas', 'Administration', 'CLASS_108', '2024-03-06 09:00:00', 'Half-day'),
    ('105_David', 'Statistics', 'CLASS_104', '2024-03-06 09:00:00', 'On-Duty');
--     ('107_Nasim', 'Intelligent Systems', 'CLASS_107', '2024-03-06 09:00:00', 'Present');
    
select * from Faculty_attendance;

-- Created by Tumul
CREATE TABLE Student_attendance (
    Student_id VARCHAR(100) not null PRIMARY KEY,
    Class_id VARCHAR(10) not null,
    Class_teacher_id VARCHAR(10) not null,
    Date TIMESTAMP,
    Attendance ENUM('Present', 'Absent', 'On-Duty','Half-day'),
    FOREIGN KEY (Student_id) REFERENCES Students(StudentId),
    FOREIGN KEY (Class_id) REFERENCES Classes(class_id),
    FOREIGN KEY (Class_teacher_id) REFERENCES Faculty(Teacher_Id)
);
--
-- -- Created by Tumul
INSERT INTO Student_attendance (Student_id, Class_id, Class_teacher_id, Date, Attendance)
VALUES 
    ('1001_Michael', 'CLASS_101', '101_Mark', '2024-03-15 09:00:00', 'Present'),
    ('1004_Sophia', 'CLASS_104', '105_David', '2024-03-15 10:00:00', 'Absent'),
    ('1003_Oliver', 'CLASS_103', '106_Sophia', '2024-03-15 11:00:00', 'On-Duty'),
    ('1002_Emma', 'CLASS_102', '104_Emily', '2024-03-15 12:00:00', 'Present');

-- truncate table faculty_attendance;
---------------------------------------------------------------
select * from user;
select * from faculty;
select * from students;
select * from courses;
select * from classes;
select * from faculty_attendance;
select * from student_attendance;
select * from classes where Class_id='CLASS_101';
-- ---------------------------------------------------------------
SELECT * FROM user WHERE status="Admin";

create view updateAttendance as
select  s.StudentId, concat(s.FirstName, s.Lastname) as Name, s.CoursesTaken,s.ClassId as Class_id,s.Department, s.classteacher,sa.Date,sa.Attendance
from students s left join student_attendance sa on s.classId=sa.Class_id;

create view updateTeacherAttendance as
select  t.Teacher_Id, concat(t.FirstName, t.Lastname) as Name, t.Course_Id,t.Department,ta.Class_id,ta.Date,ta.Attendance
from faculty t left join faculty_attendance ta on t.Department=ta.Department;

-- drop view updateTeacherAttendance;
select * from faculty;
select * from faculty_attendance;
select * from updateTeacherAttendance;

select * from updateAttendance;
select * from students;
select * from student_attendance;
