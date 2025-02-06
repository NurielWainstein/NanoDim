from PyQt6.QtWidgets import QListWidget
from utils.navigation_transit import NavigationUtils

class FileListWidget(QListWidget):
    def __init__(self, file_controller, stacked_widget, parent=None):
        super().__init__(parent)

        self.parent_window = parent
        self.file_controller = file_controller
        self.stacked_widget = stacked_widget

        self.setAcceptDrops(True)
        self.itemDoubleClicked.connect(self.on_item_double_clicked)

    def on_item_double_clicked(self, item):
        """Handle the double-click event to open the STL editor."""
        NavigationUtils.open_stl_editor(item, self.file_controller, self.stacked_widget, self.parent_window)

    def update_items(self):
        """Update the list with file names."""
        self.clear()
        for file in self.file_controller.get_basename_files():
            self.addItem(file)
