from idlelib.help_about import AboutDialog
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QLabel, QWidget, QGridLayout, QLineEdit,
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem,
    QDialog, QMessageBox, QVBoxLayout, QComboBox,
    QToolBar, QStatusBar
)
from PyQt6.QtGui import QAction
import sys
import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env")

DB_HOST = os.getenv("DB_HOST")

DB_USER = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction("Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Id", "Name", "Course", "Mobile"])
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.table.cellClicked.connect(self.cell_clicked)

        self.edit_button = QPushButton("Edit record")
        self.edit_button.clicked.connect(self.edit)

        self.delete_button = QPushButton("Delete record")
        self.delete_button.clicked.connect(self.delete_record)

        self.statusbar.addWidget(self.edit_button)
        self.statusbar.addWidget(self.delete_button)

        self.edit_button.hide()
        self.delete_button.hide()

    def cell_clicked(self, row, column):
        self.edit_button.show()
        self.delete_button.show()

    def load_data(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM student")
        result = cursor.fetchall()

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table.setItem(
                    row_number, column_number,
                    QTableWidgetItem(str(column_data))
                )

        cursor.close()
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDiolog()
        dialog.exec()

    def delete_record(self):
        dialog = DeleteDiolog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setText(
            "This app was created during the course. "
            "'The Python Mega Course'."
        )


class EditDiolog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = main_window.table.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Error", "Please select a record first")
            self.close()
            return

        self.student_id = main_window.table.item(index, 0).text()
        student_name = main_window.table.item(index, 1).text()
        course_name = main_window.table.item(index, 2).text()
        mobile = main_window.table.item(index, 3).text()

        self.student_name = QLineEdit(student_name)
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        self.course_name.addItems(["Biology", "Math", "Physics", "Science"])
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit(mobile)
        layout.addWidget(self.mobile)

        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE student SET name=%s, course=%s, mobile=%s WHERE id=%s",
            (
                self.student_name.text(),
                self.course_name.currentText(),
                self.mobile.text(),
                self.student_id
            )
        )
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()


class DeleteDiolog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student")

        layout = QGridLayout()

        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)

        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)
        no.clicked.connect(self.close)

    def delete_student(self):
        index = main_window.table.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Error", "Please select a record first")
            return

        student_id = main_window.table.item(index, 0).text()

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM student WHERE id=%s", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_data()
        QMessageBox.information(self, "Success", "Record deleted successfully")
        self.close()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        self.course_name.addItems(["Biology", "Math", "Physics", "Science"])
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit()
        layout.addWidget(self.mobile)

        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO student (name, course, mobile) VALUES (%s, %s, %s)",
            (
                self.student_name.text(),
                self.course_name.currentText(),
                self.mobile.text()
            )
        )
        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_data()
        self.close()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        layout.addWidget(self.student_name)

        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        if not name:
            QMessageBox.warning(self, "Error", "Please enter a name")
            return

        main_window.table.clearSelection()
        items = main_window.table.findItems(
            name, Qt.MatchFlag.MatchContains
        )

        if not items:
            QMessageBox.information(self, "Result", "Student not found")
        else:
            for item in items:
                item.setSelected(True)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
