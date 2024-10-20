from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from Widgets.GenericWidget import GenericWidget


class ActionWidget(GenericWidget):

    def __init__(self, gui_info, main_window):
        super().__init__(gui_info, main_window)
        self.section = "generic_action_gui"
        self.parent_section = self.section

        # Layout for the window
        self.layout = QVBoxLayout()

        # Title
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont('Arial', 24))
        self.layout.addWidget(self.title)

        # The main image section
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)

        # The description section
        self.file_name_label = QLabel("")
        self.file_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.file_name_label.setFont(QFont('Arial', 14))
        self.file_name_label.setStyleSheet(
            """
            padding: 15px;
            margin: 10px;
            """
        )
        self.layout.addWidget(self.file_name_label)

        # The action buttons to show
        self.button_layout = QHBoxLayout()
        self.go_button = QPushButton(self.get_info("action_btn"))
        self.button_layout.addWidget(self.go_button)
        # Button to reset status
        self.restart_button = QPushButton(self.get_info("cancel_btn"))
        self.button_layout.addWidget(self.restart_button)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def set_image(self, name):
        """Set the image to the given file."""
        image_path = self.get_image_path(name)
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))

    def change_background(self):
        self.main_window.setStyleSheet(f"background-color: {self.get_info("background_color")};")