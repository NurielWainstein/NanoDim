import os
import inspect
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow
)

from utils import custom_functions
from utils.custom_functions import _process_files_in_directory
from widgets.navigation_button import NavigationButton
from widgets.dropdown_widget import DropdownWidget
from widgets.file_tree_widget import FileTreeWidget
from widgets.config_editor_widget import JsonEditorDialog

CONFIG_FILE = "config.json"


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

        # Top Bar Layout (Function Dropdown + Config Button + Navigation Button)
        top_bar_layout = QHBoxLayout()

        # Navigation Button (top right)
        self.nav_button = NavigationButton(self, "FileManagerWindow", "Go to Main App")
        top_bar_layout.addStretch()  # Push button to the right
        top_bar_layout.addWidget(self.nav_button)

        # Dropdown for functions using the new DropdownWidget
        self.function_dropdown = DropdownWidget(self)
        self.function_dropdown.update_items(self.getCustomFunctions())  # Populate functions
        self.function_dropdown.currentIndexChanged.connect(self.runSelectedFunction)

        # Button to open Config Editor
        self.config_button = QPushButton("Edit Config")
        self.config_button.clicked.connect(self.openConfigEditor)

        top_bar_layout.addWidget(self.function_dropdown)
        top_bar_layout.addWidget(self.config_button)

        main_layout.addLayout(top_bar_layout)

        # Use FileTreeWidget to show files
        self.file_tree_widget = FileTreeWidget(self.folder_path)
        main_layout.addWidget(self.file_tree_widget)

        # Set central widget for QMainWindow
        self.setCentralWidget(central_widget)

    def getCustomFunctions(self):
        """Gets all functions from the custom_functions module, excluding those that start with an underscore."""
        return [name for name, obj in inspect.getmembers(custom_functions, inspect.isfunction) if
                not name.startswith('_')]

    def openConfigEditor(self):
        """Opens the ConfigEditorWidget to edit function arguments."""
        editor_widget = JsonEditorDialog(config_file=CONFIG_FILE, parent=self)
        editor_widget.show()
        editor_widget.loadJsonConfig()

    def runSelectedFunction(self):
        """Executes the selected function from custom_functions.py with arguments, using multithreading."""
        selected_function = self.function_dropdown.currentText()
        if selected_function != "Select Function":
            func = getattr(custom_functions, selected_function, None)
            if callable(func):
                directory = "local_files/screenshots"  # Adjust as necessary
                _process_files_in_directory(directory, func, **self.function_args)

    def loadJsonConfig(self):
        """Loads JSON configuration from a file."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}
