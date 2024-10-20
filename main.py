import sys
import tomllib
from PyQt6.QtWidgets import QApplication
from SelectGui import SelectGui

if __name__ == '__main__':
    with open('gui.toml', 'rb') as toml_config:
        gui_info = tomllib.load(toml_config)
    app = QApplication(sys.argv)
    window = SelectGui(gui_info)
    window.show()
    sys.exit(app.exec())
