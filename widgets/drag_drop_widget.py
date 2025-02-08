from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QFileDialog, QPushButton

from config.config import DEFAULT_DRAG_DROP_DESIGN


class DragDropWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__("Drag and drop STL files here", parent)
        self.parent_window = parent
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(DEFAULT_DRAG_DROP_DESIGN)
        self.setAcceptDrops(True)

        # Add a "Select STL Files" button
        self.select_button = QPushButton("Select STL Files", self)
        self.select_button.clicked.connect(self.select_files)
        self.select_button.setGeometry(20, 20, 150, 30)  # Adjust size and position as needed

        # Layout to organize the button
        layout = QVBoxLayout(self)
        layout.addWidget(self.select_button)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop event."""
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()
            if file_path.endswith(".stl"):
                self.handle_dropped_file(file_path)

    def handle_dropped_file(self, file_path):
        """Handle the dropped file."""
        file_controller = self.parent_window.file_controller
        file_controller.save_and_add_file(file_path)
        self.parent_window.file_list_panel.update_items()

    def select_files(self):
        """Open a file dialog to select STL files."""
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select STL Files", "", "STL Files (*.stl)")
        if file_paths:
            for file_path in file_paths:
                self.handle_dropped_file(file_path)
                self.parent_window.file_list_panel.update_items()

