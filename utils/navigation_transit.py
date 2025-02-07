import os
from PyQt6.QtWidgets import QMainWindow

class NavigationUtils:
    @staticmethod
    def open_screen(current_window: QMainWindow, target_window):
        """Navigate to any screen given current and target windows"""
        file_manager_window = target_window()
        file_manager_window.show()  # Show the new window
        current_window.close()  # Close the current window

    @staticmethod
    def open_stl_editor(item, file_controller, stacked_widget, parent):
        """Opens the STL edit window when a file is double-clicked."""
        from views.stl_file_editor import EditSTLWindow

        stl_file_path = os.path.join(file_controller.save_path, item.text())
        edit_window = EditSTLWindow(stl_file_path, parent)
        stacked_widget.addWidget(edit_window)
        stacked_widget.setCurrentWidget(edit_window)
