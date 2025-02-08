import sys
import os
import subprocess
import inspect  # To get functions dynamically
import json
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTreeView, QHBoxLayout, QComboBox, QTextEdit, QDialog, QMainWindow
)
from PyQt6.QtCore import QDir

from utils import custom_functions

CONFIG_FILE = "config.json"


class JsonEditorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Function Arguments")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setText(self.loadJsonConfig())  # Load saved JSON
        self.layout.addWidget(self.text_edit)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.saveJsonConfig)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def loadJsonConfig(self):
        """Loads JSON data from file."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return f.read()
        return "{}"  # Default empty JSON object

    def saveJsonConfig(self):
        """Saves JSON data to file and closes the dialog."""
        with open(CONFIG_FILE, "w") as f:
            f.write(self.text_edit.toPlainText())
        self.accept()

    def getJsonData(self):
        """Returns the JSON data from the editor."""
        try:
            return json.loads(self.text_edit.toPlainText())
        except json.JSONDecodeError:
            return {}  # Return empty dict if invalid JSON


class FileViewerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Viewer")
        self.setGeometry(100, 100, 600, 400)

        self.folder_path = os.path.abspath("local_files/screenshots")
        self.function_args = self.loadJsonConfig()  # Load saved config

        self.initUI()

    def initUI(self):
        central_widget = QWidget()  # Create a central widget for QMainWindow
        main_layout = QVBoxLayout(central_widget)  # Apply layout to central widget

        # Top Bar Layout (Function Dropdown + Config Button)
        top_bar_layout = QHBoxLayout()

        # Dropdown for functions
        self.function_dropdown = QComboBox()
        self.function_dropdown.addItem("Select Function")
        self.function_dropdown.addItems(self.getCustomFunctions())  # Populate functions
        self.function_dropdown.currentIndexChanged.connect(self.runSelectedFunction)

        # Button to open JSON editor
        self.config_button = QPushButton("Edit Config")
        self.config_button.clicked.connect(self.openJsonEditor)

        top_bar_layout.addWidget(self.function_dropdown)
        top_bar_layout.addWidget(self.config_button)

        main_layout.addLayout(top_bar_layout)

        # File system model
        self.model = QFileSystemModel()
        self.model.setRootPath(self.folder_path)
        self.model.setFilter(QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)

        # Tree View
        self.treeView = QTreeView()
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(self.folder_path))
        self.treeView.setSelectionMode(QTreeView.SelectionMode.MultiSelection)
        self.treeView.doubleClicked.connect(self.openFiles)  # Open all selected files on double-click

        main_layout.addWidget(self.treeView)

        # Set central widget for QMainWindow
        self.setCentralWidget(central_widget)

    def getCustomFunctions(self):
        """Gets all functions from the custom_functions module."""
        return [name for name, obj in inspect.getmembers(custom_functions, inspect.isfunction)]

    def openJsonEditor(self):
        """Opens a dialog to edit function arguments as JSON."""
        dialog = JsonEditorDialog(self)
        if dialog.exec():  # If the user clicks Save
            self.function_args = dialog.getJsonData()
            self.saveJsonConfig()

    def runSelectedFunction(self):
        """Executes the selected function from custom_functions.py with arguments."""
        selected_function = self.function_dropdown.currentText()
        if selected_function != "Select Function":
            func = getattr(custom_functions, selected_function, None)
            if callable(func):
                func(**self.function_args)  # Pass kwargs

    def loadJsonConfig(self):
        """Loads JSON configuration from a file."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def saveJsonConfig(self):
        """Saves the current JSON configuration to a file."""
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.function_args, f, indent=4)

    def openFiles(self):
        """Opens all selected files when a file is double-clicked."""
        selected_indexes = self.treeView.selectionModel().selectedIndexes()
        selected_files = [
            self.model.filePath(index) for index in selected_indexes if self.model.isDir(index) is False
        ]
        self.openSelectedFiles(selected_files)

    def openSelectedFiles(self, files):
        """Opens the given list of files based on OS."""
        for file_path in files:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", file_path])
            elif sys.platform == "win32":  # Windows
                os.startfile(file_path)
            elif sys.platform == "linux":  # Linux
                subprocess.run(["xdg-open", file_path])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileViewerWindow()
    window.show()
    sys.exit(app.exec())
