from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget
from widgets.file_list_widget import FileListWidget
from widgets.drag_drop_widget import DragDropWidget
from controllers.file_controller import FileController

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
        # add main screen panel file manager
        self.file_manager_widget = QWidget(self)
        self.file_manager_layout = QHBoxLayout()

        self.file_manager_widget.setLayout(self.file_manager_layout)
        self.stacked_widget.addWidget(self.file_manager_widget)

        # add file list panel
        self.file_list_panel = FileListWidget(self.file_controller, self.stacked_widget, self)

        self.file_list_layout = QVBoxLayout()
        self.file_list_layout.addWidget(self.file_list_panel)

        # add drag and drop panel
        self.drag_drop_panel = DragDropWidget(self)

        self.drag_drop_layout = QVBoxLayout()
        self.drag_drop_layout.addWidget(self.drag_drop_panel)

        # set panels in main screen
        self.file_manager_layout.addLayout(self.file_list_layout, 1)
        self.file_manager_layout.addLayout(self.drag_drop_layout, 3)

        self.setCentralWidget(self.stacked_widget)

        self.file_list_panel.update_items()

    def show_file_manager(self):
        self.stacked_widget.setCurrentWidget(self.file_manager_widget)