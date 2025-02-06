import os
from views.stl_file_editor import EditSTLWindow

from PyQt6.QtWidgets import QMainWindow

class NavigationUtils:
    @staticmethod
    def open_file_manager(current_window: QMainWindow, file_manager_class):
        """Switch to the File Manager window"""
        file_manager_window = file_manager_class()  # Create instance of the FileManager window
        file_manager_window.show()  # Show the new window
        current_window.close()  # Close the current window

    @staticmethod
    def open_stl_editor(item, file_controller, stacked_widget, parent):
        """Opens the STL edit window when a file is double-clicked."""
        stl_file_path = os.path.join(file_controller.save_path, item.text())
        edit_window = EditSTLWindow(stl_file_path, parent)
        stacked_widget.addWidget(edit_window)
        stacked_widget.setCurrentWidget(edit_window)
