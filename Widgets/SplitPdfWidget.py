import os.path
import webbrowser
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog
from PyQt6.QtGui import QPixmap, QFont, QMouseEvent, QIcon
from PyQt6.QtCore import Qt
from PdfEditor import PdfEditor


class SplitPdfWidget(QWidget):

    def __init__(self, gui_info, main_window):
        super().__init__()
        self.main_window = main_window
        self.file = {}
        self.pdf_editor = PdfEditor()
        self.info = gui_info

        self.setAcceptDrops(True)
        self.setStyleSheet(f"background-color: {self.info["split_pdf_gui"]["background_color"]};")

        # Layout for the window
        self.layout = QVBoxLayout()

        #Title
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont('Arial', 24))
        self.layout.addWidget(self.title)

        # Placeholder label for dropped file image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)

        # Label to show file name
        self.file_name_label = QLabel("")
        self.file_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.file_name_label.setFont(QFont('Arial', 14))
        self.layout.addWidget(self.file_name_label)

        self.button_layout = QHBoxLayout()
        # Button to show after file is dropped
        self.go_button = QPushButton(self.info["split_pdf_gui"]["action_btn"])
        self.go_button.clicked.connect(self.elaborate_pdf)  # Connect button click to clear function
        self.button_layout.addWidget(self.go_button)
        # Button to reset status
        self.restart_button = QPushButton(self.info["split_pdf_gui"]["cancel_btn"])
        self.restart_button.clicked.connect(self.clear_and_reset)
        self.button_layout.addWidget(self.restart_button)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        #Start with a clean status
        self.clear_and_reset()

    def open_dialog(self, event: QMouseEvent):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("PDF files (*.pdf)")
        if file_dialog.exec():
            print("Selezionato!")
            selected_file = file_dialog.selectedFiles()[0]  # Get the selected file path
            print(f"Selezionato {selected_file}")
            self.file = {"name": selected_file.split('/')[-1], "path": selected_file}
            self.show_file()

    def set_button_style(self, button, color):
        """Sets the style for the button"""
        button.setStyleSheet("""
            QPushButton {
                background-color: """ + color + """;
                color: white;
                font-size: 20px;
                padding: 15px 30px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: white;
                color: """ + color + """;
                border: 2px solid """ + color + """;
            }
        """)

    def set_image(self, image_path):
        """Set the image to the given file."""
        image_path = os.path.join("../icons", image_path)
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))

    def clear_and_reset(self):
        """Clear everything and reset to the initial empty folder state."""
        self.file = {}
        self.title.setText(self.info["split_pdf_gui"]["empty_msg"])
        self.title.mousePressEvent = self.do_nothing
        self.file_name_label.setText("")
        self.set_image(self.info["split_pdf_gui"]["empty_img"])
        self.image_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.image_label.mousePressEvent = self.open_dialog
        self.restart_button.setText(self.info["split_pdf_gui"]["cancel_btn"])
        self.set_button_style(self.restart_button, self.info["split_pdf_gui"]["cancel_color"])
        self.restart_button.setVisible(False)
        self.go_button.setText(self.info["split_pdf_gui"]["action_btn"])
        self.set_button_style(self.go_button, self.info["split_pdf_gui"]["action_color"])
        self.go_button.setVisible(False)

    def show_file(self):
        """Displays the selected file."""
        self.file["ext"] = os.path.splitext(self.file["name"])[-1]
        print(self.file)
        if self.file["ext"].lower() == ".pdf":
            self.file["pages"] = self.pdf_editor.count_pages(self.file["path"])
            # Load and display the file_present image
            self.title.setText(self.info["split_pdf_gui"]["ready_msg"])
            self.set_image(self.info["split_pdf_gui"]["ready_img"])
            self.image_label.setCursor(Qt.CursorShape.ArrowCursor)
            self.image_label.mousePressEvent = self.do_nothing
            # Display the file name
            self.file_name_label.setText(f"<br>File: <b>{self.file['name']}</b><br>Pagine: <b>{self.file["pages"]}</b>")
            #Show buttons
            self.go_button.setVisible(True)
            self.restart_button.setVisible(True)
        else:
            self.title.setText(self.info["split_pdf_gui"]["invalid_msg"])
            self.set_image(self.info["split_pdf_gui"]["invalid_img"])

    def elaborate_pdf(self):
        split_dir = self.pdf_editor.split_pdf(self.file["path"])
        if split_dir:
            self.file["result_dir"] = split_dir
            self.title.setText(self.info["split_pdf_gui"]["done_msg"])
            self.set_image(self.info["split_pdf_gui"]["done_img"])
            self.image_label.setCursor(Qt.CursorShape.PointingHandCursor)
            self.image_label.mousePressEvent = self.open_directory
            self.title.mousePressEvent = self.open_directory
            self.go_button.setVisible(False)
            self.restart_button.setText(self.info["split_pdf_gui"]["restart_btn"])
        else:
            print("Error - Cannot split pdf")
            self.clear_and_reset()

    def open_directory(self, event: QMouseEvent):
        """Open the browser to the split file location"""
        if "result_dir" in self.file:
            file_dir = self.file["result_dir"]
            webbrowser.open(file_dir)

    def do_nothing(self, event: QMouseEvent):
        pass

    # Overriding dragEnterEvent to allow drag and drop
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.title.setText(self.info["split_pdf_gui"]["drag_and_drop_msg"])
            self.set_image(self.info["split_pdf_gui"]["drag_and_drop_img"])  # Show open folder while dragging

    # Overriding dropEvent to handle the dropped file
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_url = event.mimeData().urls()[0]
            file_path = file_url.toLocalFile()
            self.file = {"name": file_path.split('/')[-1], "path": file_path}
            self.show_file()

    # Overriding dragLeaveEvent to reset the folder image when nothing is dropped
    def dragLeaveEvent(self, event):
        if not self.file:
            self.clear_and_reset()
        else:
            self.show_file()

