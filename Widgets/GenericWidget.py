import os

from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget


class GenericWidget(QWidget):

    def __init__(self, gui_info, main_window):
        super().__init__()
        self.section = None
        self.parent_section = self.section
        self.info = gui_info
        self.main_window = main_window

    def do_nothing(self, event: QMouseEvent):
        """Disable the mouse action"""
        pass

    def get_info(self, name):
        """Retrieve the given value for this section."""
        section_info = self.info.get(self.section)
        parent_section_info = self.info.get(self.parent_section)
        if not section_info and not parent_section_info:
            print(f"There is no section {self.section} in the config file")
            raise ValueError("Missing sections info in config file")
        value = section_info.get(name) if section_info else None
        parent_value = parent_section_info.get(name) if parent_section_info else None
        if not value and not parent_value:
            print(f"There is no value for {self.section}/{self.parent_section} --> {name} in the config file")
            raise ValueError("Missing valid value in the config file")
        return value if value else parent_value

    def get_image_path(self, name):
        """Retrieve the requested image path for this section."""
        return os.path.join("icons", self.get_info(name))