import os
import inspect
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow
)

from config.config import FILE_MANAGER_WINDOW, SCREENSHOTS_DIR, BATCH_FUNCTIONS_CONFIG_FILE, DEFAULT_BUTTON_DESIGN
from utils import custom_functions
from utils.custom_functions import _process_files_in_directory
from widgets.navigation_button import NavigationButton
from widgets.dropdown_widget import DropdownWidget
from widgets.file_tree_widget import FileTreeWidget
from widgets.config_editor_widget import JsonEditorDialog

class FileViewerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Viewer")
        self.setGeometry(100, 100, 600, 400)

        self.folder_path = os.path.abspath(SCREENSHOTS_DIR)
        self.config_editor_widget = JsonEditorDialog(BATCH_FUNCTIONS_CONFIG_FILE)
        self.function_args = self.config_editor_widget.getJsonData()  # Load saved config

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()  # Create a central widget for QMainWindow
        main_layout = QVBoxLayout(central_widget)  # Apply layout to central widget

        # Top Bar Layout (Function Dropdown + Config Button + Navigation Button)
        top_bar_layout = QHBoxLayout()

        # Navigation Button (top right)
        self.nav_button = NavigationButton(self, FILE_MANAGER_WINDOW, "Go to Main App")

        # Button to open Config Editor
        self.config_button = QPushButton("Edit Config")
        self.config_button.setStyleSheet(DEFAULT_BUTTON_DESIGN)
        self.config_button.clicked.connect(self.config_editor_widget.openConfigEditor)

        # Dropdown for functions using the new DropdownWidget
        self.function_dropdown = DropdownWidget(self)
        self.function_dropdown.update_items(self.getCustomFunctions())  # Populate functions
        self.function_dropdown.currentIndexChanged.connect(self.runSelectedFunction)

        top_bar_layout.addWidget(self.function_dropdown)
        top_bar_layout.addWidget(self.config_button)
        top_bar_layout.addWidget(self.nav_button)

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

    def runSelectedFunction(self):
        """Executes the selected function from custom_functions.py with arguments, using multithreading."""
        # update the function args
        self.function_args = self.config_editor_widget.getJsonData()

        selected_function = self.function_dropdown.currentText()
        if selected_function != "Select Function":
            func = getattr(custom_functions, selected_function, None)
            if callable(func):
                directory = SCREENSHOTS_DIR  # Adjust as necessary
                _process_files_in_directory(directory, func, **self.function_args)
