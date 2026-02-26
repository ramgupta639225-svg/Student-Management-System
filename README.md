# Student Management System

A desktop-based Student Management System built using PyQt6 and MySQL.  
The application performs full CRUD operations (Create, Read, Update, Delete) through a user-friendly GUI.

---

## 🚀 Features

- Add new student
- View all students
- Update student record
- Delete student record
- Search student by name
- Secure database configuration using environment variables

---

## 🛠 Technologies Used

- Python
- PyQt6
- MySQL
- mysql-connector-python
- python-dotenv

---

## 🗄 Database Setup

Run the following SQL script:

```sql
CREATE DATABASE student_management;

USE student_management;

CREATE TABLE student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    course VARCHAR(100),
    mobile VARCHAR(20)
);
