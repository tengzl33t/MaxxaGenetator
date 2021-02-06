"""Maxa text generator."""
import random
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QCheckBox, QLineEdit


class ResultWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = "Result"
        self.top = 100
        self.left = 100
        self.width = 1000
        self.height = 500
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.text_out = QLabel(self)
        self.text_out.move(10, 10)
        self.text_out.setStyleSheet("background-color: white")


class FirstWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.show_result = None

        self.title = "MaxxaGenetator 0.9"
        self.top = 100
        self.left = 100
        self.width = 400
        self.height = 200

        self.button = QPushButton("Start", self)
        self.button.move(10, 100)
        self.button.clicked.connect(self.go)

        self.all_phrases_label = QLabel("All Phrases count:", self)
        self.all_phrases_label.move(10, 10)
        self.all_phrases = QLineEdit(self)
        self.all_phrases.move(100, 10)
        self.all_phrases.resize(50, 25)

        self.line_phrases_label = QLabel("Line Phrases count:", self)
        self.line_phrases_label.move(10, 40)
        self.line_phrases = QLineEdit(self)
        self.line_phrases.move(110, 40)
        self.line_phrases.resize(50, 25)

        self.cap = QCheckBox("Capitalize first letters?", self)
        self.cap.move(10, 70)
        self.cap.resize(200, 25)

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def go(self):
        text = union_random(int(self.all_phrases.text()), int(self.line_phrases.text()), self.cap.isChecked())

        self.show_result = ResultWindow()
        self.show_result.text_out.setText(text)
        self.show_result.text_out.adjustSize()
        self.show_result.text_out.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.show_result.show()


def read_from_file() -> list:
    """Read file with phrases."""
    phrases = []
    with open("phrases.txt", encoding="utf-8") as file:
        for line in file:
            phrases.append(line.strip())

    return phrases


def get_random_from_list():
    """IDK why i need this."""
    return random.choice(read_from_file())


def union_random(all_count, line_count, capitalize):
    """Make text from phrases."""
    res_str = ""
    counter = 0
    line_counter = 0
    while counter != all_count:
        counter += 1

        if line_counter == line_count:
            res_str += "\n" + (get_random_from_list().capitalize() if capitalize else get_random_from_list()) + " "
            line_counter = 1
        else:
            res_str += (get_random_from_list().capitalize() if len(
                res_str) == 0 and capitalize else get_random_from_list()) + " "
            line_counter += 1

    return res_str


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = FirstWindow()
    sys.exit(app.exec())
