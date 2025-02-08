from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QTreeView, QMessageBox
from PyQt6.QtCore import QDir, Qt
import sys
import os
import subprocess

class FileTreeWidget(QTreeView):
    def __init__(self, root_path, parent=None):
        super().__init__(parent)
        self.model = QFileSystemModel()
        self.model.setRootPath(root_path)
        self.model.setFilter(QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)
        self.setModel(self.model)
        self.setRootIndex(self.model.index(root_path))

        # Allow multiple file selections
        self.setSelectionMode(QTreeView.SelectionMode.MultiSelection)

        # Connect double click signal to open selected files
        self.doubleClicked.connect(self.open_files)

    def get_selected_files(self):
        """Returns a list of selected file paths."""
        indexes = self.selectionModel().selectedIndexes()
        return [self.model.filePath(index) for index in indexes if not self.model.isDir(index)]

    def open_files(self, index):
        """Open selected files (dummy function, you can replace it with your file-opening logic)."""
        selected_files = self.get_selected_files()

        if selected_files:
            self.open_selected_files(selected_files)
        else:
            QMessageBox.warning(self, "No Files Selected", "Please select files to open.")

    def open_selected_files(self, files):
        """Opens the selected files based on OS."""
        for file_path in files:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", file_path])
            elif sys.platform == "win32":  # Windows
                os.startfile(file_path)
            elif sys.platform == "linux":  # Linux
                subprocess.run(["xdg-open", file_path])

