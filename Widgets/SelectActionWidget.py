import os.path
import webbrowser
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog, QSizePolicy
from PyQt6.QtGui import QPixmap, QFont, QMouseEvent, QIcon
from PyQt6.QtCore import Qt, QSize

from Widgets.GenericWidget import GenericWidget


class SelectActionWidget(GenericWidget):

    def __init__(self, gui_info, main_window):
        super().__init__(gui_info, main_window)
        self.section = "select_gui"

        # Create layout for Join PDF widget
        self.layout = QHBoxLayout()

        # "Join PDF" Button
        self.join_button = QPushButton()
        self.setup_big_button(
            self.join_button,
            self.get_info("join_msg"),
            self.get_image_path("join_img")
        )
        self.join_button.clicked.connect(self.main_window.switch_to_join_pdf)
        self.layout.addWidget(self.join_button)

        # "Split PDF" Button
        self.split_button = QPushButton()
        self.setup_big_button(
            self.split_button,
            self.get_info("split_msg"),
            self.get_image_path("split_img")
        )
        self.split_button.clicked.connect(self.main_window.switch_to_split_pdf)
        self.layout.addWidget(self.split_button)
        self.main_window.setStyleSheet(f"background-color: {self.get_info("background_color")};")
        self.setLayout(self.layout)

    def setup_big_button(self, button, text, icon_path):
        """Set up a big button with an icon, text, and hover effect."""
        button.setIcon(QIcon(icon_path))  # Set icon for the button
        button.setIconSize(QSize(42, 42))  # Set large icon size
        button.setText(text)
        button.setFont(QFont("Arial", 14))
        button.setFixedSize(200, 200)
        button.setStyleSheet("""
            QPushButton {
                background-color: #caf0f8;
                color: black;
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                border: 2px solid #023e8a;
            }
            QPushButton:hover {
                background-color: #ade8f4;
                color: black;
                border: 2px solid green;
            }
            QPushButton:pressed {
                background-color: #023e8a;
            }
        """)
        # button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

