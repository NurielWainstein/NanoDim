import os
from PyQt6.QtWidgets import QMainWindow

class NavigationUtils:
    @staticmethod
    def open_screen(current_window: QMainWindow, target_window):
        """Load a new screen inside the existing QMainWindow."""
        new_widget = target_window()

        # Ensure the current window is a QMainWindow
        if isinstance(current_window, QMainWindow):
            current_window.setCentralWidget(new_widget)

    @staticmethod
    def open_stl_editor(item, file_controller, stacked_widget, parent):
        """Opens the STL edit window when a file is double-clicked."""
        from views.stl_file_editor import EditSTLWindow

        stl_file_path = os.path.join(file_controller.save_path, item.text())
        edit_window = EditSTLWindow(stl_file_path, parent)
        stacked_widget.addWidget(edit_window)
        stacked_widget.setCurrentWidget(edit_window)
