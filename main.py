import sys
import tomllib
from PyQt6.QtWidgets import QApplication
from DragDropWindow import DragDropWindow
from PdfEditor import PdfEditor

if __name__ == '__main__':
    with open('gui.toml', 'rb') as toml_config:
        gui_info = tomllib.load(toml_config)
    pdf_editor = PdfEditor()
    app = QApplication(sys.argv)
    window = DragDropWindow(gui_info, pdf_editor)
    window.show()
    sys.exit(app.exec())
