from PyQt6.QtWidgets import QPushButton
from utils.navigation_transit import NavigationUtils

class NavigationButton(QPushButton):
    def __init__(self, parent, target_screen, label=""):
        super().__init__(label, parent)

        self.parent_window = parent
        self.target_screen = target_screen
        self.setStyleSheet("font-size: 14px; padding: 10px;")

        # Connect the button's click event to the navigation action
        self.clicked.connect(self.navigate_to_screen)

    def navigate_to_screen(self):
        """Ensure the OpenGL context is cleaned before navigating."""
        if hasattr(self.parent_window, "viewer") and self.parent_window.viewer is not None:
            self.parent_window.close()  # Close the window (triggers cleanup)

        NavigationUtils.open_screen(self.parent_window, self.target_screen)
