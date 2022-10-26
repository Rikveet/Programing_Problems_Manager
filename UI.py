import os
import sys

from PyQt6 import QtGui
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QLineEdit, \
    QPushButton, QFileDialog, QScrollArea, QCheckBox, QMessageBox, QProgressBar

styleSheet = """
MainWindow
{
    background-color: black;
}
QMessageBox
{
    background-color: black;
}
QLineEdit
{
    background-color: black;
    color: grey;
    border: 1px solid white;
    border-radius: 10px;
    font-size: 12px;
    min-height: fit-content;
    min-width: fit-content;
    padding: 5 5 5;
}
QLineEdit::placeholder
{
    color: grey;
}
QLineEdit::hover
{
    border: 2px solid white;
}
QLabel{
    color: white;
    font-size: 12px;
}
QPushButton
{
    background-color: qlineargradient(x1: 0, x2: 1, stop: 0 blue, stop: 1 red);
    border: 0;
    border-radius: 10px;
    box-sizing: border-box;
    font-size: 15px;
    min-height: fit-content;
    min-width: fit-content;
    max-width: 100px;
    padding: 5px;
    text-decoration: none;
    color: white;
}
QPushButton::hover
{
    border: 1px solid white;
}
QPushButton::pressed
{
    background-color : red;
}
QCheckBox{
    color: white;
    min-width: fit-content;
    font-size: 12px;
}
QScrollArea
{
    background-color: black;
    border: 1px solid white;
    border-radius: 10px;
    padding: 10 00 10;
}
QScrollArea::hover
{
    border: 2px solid white;
}
QScrollBar::sub-line{
    background-color: black;
}
"""


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.folders = {}

        self.setWindowTitle("Programing problems github Readme Manager")
        # set size
        self.setMinimumSize(QSize(500, 666))

        # Title
        title_text = QLabel('<a href="">PPGRM</a>')
        title_text.setStyleSheet('font-size: 35px;')
        title_text.setOpenExternalLinks(True)
        title_text.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        title_text.setContentsMargins(0, 0, 0, 10)

        # GitHub link input section
        github_link_section_layout = QHBoxLayout()
        github_link_label = QLabel("Github Link")
        github_link_input = QLineEdit()
        github_link_input.setMaxLength(10)
        github_link_input.setPlaceholderText("https://github.com/Rikveet")
        github_link_input.setProperty("mandatoryField", True)
        github_link_section_layout.addWidget(github_link_label)
        github_link_section_layout.addWidget(github_link_input)

        # Directory selector
        directory_selector_label = QLabel("Select Directory")
        directory_selector_container = QHBoxLayout()
        self.directory_selector_input = QLineEdit()
        self.directory_selector_input.setProperty("mandatoryField", True)
        self.directory_selector_input.setPlaceholderText(os.getcwd())
        directory_selector_button = QPushButton("📁")
        directory_load_folders_button = QPushButton("Load Folders")

        def load_folders():
            try:
                if len(self.directory_selector_input.text()) == 0:
                    self.directory_selector_input.setText(os.getcwd())
                if not os.path.isdir(self.directory_selector_input.text()):
                    raise Exception("Directory does not exists")
                os_walker = os.walk(self.directory_selector_input.text())
                if len(self.folders) != 0:
                    for folder in self.folders.keys():
                        self.select_box_container.removeWidget(self.folders[folder])
                self.folders = dict.fromkeys([folder for folder in next(os_walker)[1]], None)
                for folder in self.folders:
                    self.folders[folder] = QCheckBox(folder, self)
                    self.folders[folder].setChecked(False)
                    self.select_box_container.addWidget(self.folders[folder])
            except Exception as e:
                self.directory_selector_input.setText("")
                self.showPopUpMessage(str(e), QMessageBox.Icon.Critical, "Error while loading folders")

        def directory_selector_button_handler():
            self.directory_selector_input.setText(QFileDialog.getExistingDirectory(self, 'Select Folder'))
            load_folders()

        directory_load_folders_button.clicked.connect(load_folders)
        directory_selector_button.clicked.connect(directory_selector_button_handler)
        directory_selector_container.addWidget(directory_selector_label)
        directory_selector_container.addWidget(self.directory_selector_input)
        directory_selector_container.addWidget(directory_load_folders_button)
        directory_selector_container.addWidget(directory_selector_button)

        # Folders select box
        select_box_main_container = QVBoxLayout()
        select_box = QWidget()
        # select box layout
        self.select_box_container = QVBoxLayout()
        self.select_box_container.setAlignment(Qt.AlignmentFlag.AlignTop)
        select_box.setLayout(self.select_box_container)
        select_box.setStyleSheet("""
            background: black;
            border: 0;
            overflow: hidden;
        """)

        # select box scroll
        select_box_scroll = QScrollArea()
        select_box_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        select_box_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        select_box_scroll.setWidgetResizable(True)
        select_box_scroll.setWidget(select_box)

        # select all option
        def select_all_checkbox_handler():
            value = self.sender().isChecked()
            for key in self.folders.keys():
                self.folders[key].setChecked(value)

        select_all_checkbox = QCheckBox("Select All")
        select_all_checkbox.toggled.connect(select_all_checkbox_handler)
        self.select_box_container.addWidget(select_all_checkbox)

        select_box_main_container.addWidget(QLabel("Select Directories that you want to include on the table:"))
        select_box_main_container.addWidget(select_box_scroll)

        footer_container = QHBoxLayout()
        footer_start_button = QPushButton("Start")
        footer_quit_button = QPushButton("Quit")
        self.footer_progress_bar = QProgressBar()
        footer_container.addWidget(footer_start_button)
        footer_container.addWidget(footer_quit_button)

        # main layout
        main_Background_layout = QVBoxLayout()
        main_Background_layout.setContentsMargins(30, 20, 30, 50)
        main_Background_layout.setSpacing(10)
        # add sections
        main_Background_layout.addWidget(title_text)
        main_Background_layout.addLayout(github_link_section_layout)
        main_Background_layout.addLayout(directory_selector_container)
        main_Background_layout.addLayout(select_box_main_container)
        main_Background_layout.addLayout(footer_container)

        # Set main alignment
        main_Background_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        widget = QWidget()
        widget.setLayout(main_Background_layout)

        self.setCentralWidget(widget)

    @staticmethod
    def showPopUpMessage(text, icon=QMessageBox.Icon.NoIcon, title=""):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setWindowIcon(QtGui.QIcon("content/icons/error.png"))
        msg.exec()


app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon("content/icons/programming-language.png"))
app.setStyleSheet(styleSheet)

window = MainWindow()
window.setMaximumSize(QSize(800, 1066))
window.show()

app.exec()
