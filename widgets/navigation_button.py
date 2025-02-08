from PyQt6.QtWidgets import QPushButton

from config.config import CLASS_NAVIGATION_MAP, DEFAULT_BUTTON_DESIGN
from utils.navigation_transit import NavigationUtils

class NavigationButton(QPushButton):
    def __init__(self, parent, target_screen_name: str, label=""):
        super().__init__(label, parent)

        self.parent_window = parent
        self.target_screen_name = target_screen_name
        self.setStyleSheet(DEFAULT_BUTTON_DESIGN)

        # Connect the button's click event to the navigation action
        self.clicked.connect(self.navigate_to_screen)

    def navigate_to_screen(self):
        # Check if the target screen name exists in the mapping
        if self.target_screen_name in CLASS_NAVIGATION_MAP:
            method_name = CLASS_NAVIGATION_MAP[self.target_screen_name]
            if hasattr(self, method_name):
                target_class = getattr(self, method_name)()  # Call the method to get the class
                if target_class:
                    NavigationUtils.open_screen(self.parent_window, target_class)
                else:
                    print(f"Error: {method_name} did not return a valid class.")
            else:
                print(f"Error: Method '{method_name}' not found.")
        else:
            print(f"Error: No navigation function mapped for '{self.target_screen_name}'.")

    def navigate_to_file_manager_window(self):
        from views.stl_file_manager import FileManagerWindow
        return FileManagerWindow

    def navigate_to_file_viewer_window(self):
        from views.image_folder import FileViewerWindow
        return FileViewerWindow

