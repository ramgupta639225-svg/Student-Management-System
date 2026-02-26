CREATE DATABASE student_management;

USE student_management;

CREATE TABLE student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    course VARCHAR(100),
    mobile VARCHAR(20)
);
