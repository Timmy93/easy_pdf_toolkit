import os

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedWidget

from Widgets.JoinPdfWidget import JoinPdfWidget
from Widgets.SelectActionWidget import SelectActionWidget
from Widgets.SplitPdfWidget import SplitPdfWidget


class SelectGui(QWidget):

    def __init__(self, gui_info):
        super().__init__()
        self.info = gui_info
        self.setWindowTitle(self.info["gui"]["title"])
        self.setWindowIcon(QIcon(os.path.join("icons", self.info["gui"]["icon_img"])))
        self.setGeometry(300, 300, 600, 200)
        self.main_layout = QVBoxLayout()

        # Add the buttons layout (Join PDF, Split PDF)
        self.stacked_widget = QStackedWidget()
        self.select_action_widget = SelectActionWidget(self.info, self)
        self.stacked_widget.addWidget(self.select_action_widget)
        self.join_pdf_widget = JoinPdfWidget(self.info, self)
        self.stacked_widget.addWidget(self.join_pdf_widget)
        self.split_pdf_widget = SplitPdfWidget(self.info, self)
        self.stacked_widget.addWidget(self.split_pdf_widget)

        self.stacked_widget.setCurrentWidget(self.select_action_widget)
        self.main_layout.addWidget(self.stacked_widget)
        self.setLayout(self.main_layout)

    def switch_to_split_pdf(self):
        """Switch to the Split PDF layout."""
        self.stacked_widget.setCurrentWidget(self.split_pdf_widget)

    def switch_to_join_pdf(self):
        """Switch to the Join PDF layout."""
        self.stacked_widget.setCurrentWidget(self.join_pdf_widget)

    def get_image_path(self, section, name):
        return os.path.join("icons", self.info[section][name])