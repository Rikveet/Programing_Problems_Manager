import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Programing problems github Readme Manager")
        # set size
        self.setFixedSize(QSize(400, 300))

        main_Background_layout = QHBoxLayout()

        github_link_section_layout = QVBoxLayout()
        github_link_label = QLabel("Github Link")
        github_link_input = QLineEdit()
        github_link_input.setMaxLength(10)
        github_link_input.setPlaceholderText("https://github.com/Rikveet")
        github_link_section_layout.addWidget(github_link_label)
        github_link_section_layout.addWidget(github_link_input)

        main_Background_layout.addWidget(github_link_section_layout)

        widget = QWidget()
        widget.setLayout(main_Background_layout)

        self.setCentralWidget(widget)

    @staticmethod
    def alignCenter(widget):
        try:
            widget.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        except Exception as e:
            print(e)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
