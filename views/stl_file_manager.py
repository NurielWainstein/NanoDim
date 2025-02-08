from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget
)

from config.config import FILE_VIEWER_WINDOW
from widgets.file_list_widget import FileListWidget
from widgets.drag_drop_widget import DragDropWidget
from utils.file_controller import FileController
from widgets.navigation_button import NavigationButton

class FileManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("STL File Manager")
        self.setGeometry(100, 100, 800, 400)

        self.file_controller = FileController()
        self.stl_files = self.file_controller.load_existing_files()

        self.stacked_widget = QStackedWidget(self)
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface components."""
        # Create the main container widget
        self.file_manager_widget = QWidget(self)
        self.file_manager_layout = QVBoxLayout()

        # Create the top bar layout
        self.top_bar_layout = QHBoxLayout()

        # Navigation button (top right)
        self.nav_button = NavigationButton(self, FILE_VIEWER_WINDOW, "Screenshots Manager")
        self.top_bar_layout.addStretch()  # Push button to the right
        self.top_bar_layout.addWidget(self.nav_button)

        # Create file manager panel layout
        self.main_content_layout = QHBoxLayout()

        # File list panel
        self.file_list_panel = FileListWidget(self.file_controller, self.stacked_widget, self)
        self.file_list_layout = QVBoxLayout()
        self.file_list_layout.addWidget(self.file_list_panel)

        # Drag and drop panel
        self.drag_drop_panel = DragDropWidget(self)
        self.drag_drop_layout = QVBoxLayout()
        self.drag_drop_layout.addWidget(self.drag_drop_panel)

        # Add panels to the main content layout
        self.main_content_layout.addLayout(self.file_list_layout, 1)
        self.main_content_layout.addLayout(self.drag_drop_layout, 3)

        # Combine layouts
        self.file_manager_layout.addLayout(self.top_bar_layout)  # Add the top bar
        self.file_manager_layout.addLayout(self.main_content_layout)  # Add main content

        self.file_manager_widget.setLayout(self.file_manager_layout)
        self.stacked_widget.addWidget(self.file_manager_widget)
        self.setCentralWidget(self.stacked_widget)

        self.file_list_panel.update_items()

    def show_file_manager(self):
        self.stacked_widget.setCurrentWidget(self.file_manager_widget)