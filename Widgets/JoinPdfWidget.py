import os.path
import webbrowser
from natsort import natsorted
from PyQt6.QtWidgets import QFileDialog, QListWidget
from PyQt6.QtGui import QMouseEvent, QFont
from PyQt6.QtCore import Qt
from PdfEditor import PdfEditor
from Widgets.ActionWidget import ActionWidget


class JoinPdfWidget(ActionWidget):

    def __init__(self, gui_info, main_window):
        super().__init__(gui_info, main_window)
        self.section = "join_pdf_gui"
        self.files = []
        self.result_dir = None
        self.pdf_editor = PdfEditor()
        self.setAcceptDrops(True)
        self.go_button.clicked.connect(self.join_pdf)  # Connect button click to clear function
        self.restart_button.clicked.connect(self.clear_and_reset)
        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont('Arial', 11))
        # Add the sorted strings to the QListWidget
        self.updateList()
        # Add the QListWidget to the layout
        self.layout.addWidget(self.list_widget)
        #Start with a clean status
        self.clear_and_reset()

    def updateList(self):
        files = [file['name'] for file in self.files]
        self.list_widget.clear()
        self.list_widget.addItems(files)
        self.update_gui()

    def open_dialog(self, event: QMouseEvent):
        file_dialog = QFileDialog(self)
        results = file_dialog.getOpenFileNames(caption="Documenti PDF da unire", filter="Documenti PDF (*.pdf)")
        selected_files = results[0]
        if selected_files:
            self.files = self.files + self.order_files(selected_files)
            self.updateList()

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

    def clear_and_reset(self):
        """Clear everything and reset to the initial empty folder state."""
        self.files = []
        self.title.setText(self.get_info("empty_msg"))
        self.title.mousePressEvent = self.do_nothing
        self.file_name_label.setText("")
        self.set_image("empty_img")
        self.image_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.image_label.mousePressEvent = self.open_dialog
        self.restart_button.setText(self.get_info("cancel_btn"))
        self.set_button_style(self.restart_button, self.get_info("cancel_color"))
        self.restart_button.setVisible(False)
        self.go_button.setText(self.get_info("action_btn"))
        self.set_button_style(self.go_button, self.get_info("action_color"))
        self.go_button.setVisible(False)
        self.updateList()

    def join_pdf(self):
        joined_pdf = self.pdf_editor.join_pdf(self.files)
        if joined_pdf:
            self.result_dir = os.path.dirname(joined_pdf)
            self.title.setText(self.get_info("done_msg"))
            self.set_image("done_img")
            self.file_name_label.setText(
                f"<p><b>Successo!</b></p>" +
                f"<p>Pagine del PDF: <b>{self.pdf_editor.count_pages(joined_pdf)}</b></p>" +
                f"<p>Nome cartella con il risultato: <i>{os.path.basename(self.result_dir)}</i></p>" +
                f"<p>Clicca sull'icona o vai sul Desktop per vedere il risultato</p>"
            )
            self.image_label.setCursor(Qt.CursorShape.PointingHandCursor)
            self.image_label.mousePressEvent = self.open_directory
            self.go_button.setVisible(False)
            self.restart_button.setText(self.get_info("restart_btn"))
        else:
            print("Error - Cannot join pdf")
            self.clear_and_reset()

    def open_directory(self, event: QMouseEvent):
        """Open the browser to the joined file location"""
        if self.result_dir:
            webbrowser.open(self.result_dir)


    # Overriding dropEvent to handle the dropped file
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_urls = event.mimeData().urls()
            file_paths = [file_url.toLocalFile() for file_url in file_urls]
            self.files = self.files + self.order_files(file_paths)
            self.updateList()

    def order_files(self, file_paths):
        """Create an ordered list of files from the given list of filepath"""
        selected_files = []
        for file_path in file_paths:
            file = {
                "name": file_path.split('/')[-1],
                "path": file_path,
                "ext": os.path.splitext(file_path.split('/')[-1])[-1]
            }
            if file["ext"].lower() == ".pdf":
                selected_files.append(file)
        return natsorted(selected_files, key=lambda d: d['name'])

    # Overriding dragEnterEvent to allow drag and drop
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.title.setText(self.get_info("drag_and_drop_msg"))
            self.set_image("drag_and_drop_img")

    # Overriding dragLeaveEvent to reset the folder image when nothing is dropped
    def dragLeaveEvent(self, event):
        self.update_gui()

    def update_gui(self):
        if self.files:
            self.set_image("full_img")
            self.restart_button.setVisible(True)
            self.go_button.setVisible(True)
            self.file_name_label.setText(
                f"<p>{len(self.files)} PDF selezionati</p>"+
                f"<p>Aggiungi altri file o premi <span style='color: {self.get_info("action_color")}; font-weight: bold;'>{self.get_info("action_btn")}</span> per unire</p>"
            )
        else:
            self.set_image("empty_img")
            self.restart_button.setVisible(False)
            self.go_button.setVisible(False)
            self.file_name_label.setText("Nessun PDF selezionato")