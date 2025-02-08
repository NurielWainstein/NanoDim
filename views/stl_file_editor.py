from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from widgets.stl_viewer_widget import VTKViewerWidget

from widgets.navigation_button import NavigationButton
import os
import time
import weakref
from PyQt6.QtCore import QTimer
import vtk

class EditSTLWindow(QMainWindow):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 700, 900)
        self.setAcceptDrops(True)

        self.file_path = file_path  # Store the file path
        self._init_ui()
        self.vtk_viewer.load_stl(file_path)  # Automatically load the STL file

    def _init_ui(self):
        """Initialize the user interface components"""
        centerWidget = QWidget()
        self.setCentralWidget(centerWidget)

        layout = QVBoxLayout()
        centerWidget.setLayout(layout)

        self._setup_vtk_widget(layout)
        self._setup_bottom_buttons(layout)
        self._setup_message_label(layout)

    def _setup_vtk_widget(self, layout):
        """Set up the custom VTK 3D viewer widget"""
        self.vtk_viewer = VTKViewerWidget(self)
        layout.addWidget(self.vtk_viewer, 1)

    def _setup_bottom_buttons(self, layout):
        """Set up the bottom buttons for screenshot and navigation"""
        bottomLayout = QHBoxLayout()
        layout.addLayout(bottomLayout)

        screenshotButton = QPushButton("Take Screenshot")
        screenshotButton.clicked.connect(self._take_screenshot)
        bottomLayout.addWidget(screenshotButton)

        fileManagerButton = NavigationButton(self, "FileManagerWindow", "Go to File Manager")
        bottomLayout.addWidget(fileManagerButton)

    def _setup_message_label(self, layout):
        """Set up the temporary message label"""
        self.messageLabel = QLabel("")
        layout.addWidget(self.messageLabel)

    def _take_screenshot(self):
        """Capture and save a screenshot of the VTK render window with a unique filename"""
        screenshot_dir = self._get_screenshot_directory()
        os.makedirs(screenshot_dir, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")

        try:
            self._save_screenshot(filename)
            self.messageLabel.setText(f"Screenshot saved: {filename}")
            self.messageLabel.repaint()

            # Hide the message after a short delay using weakref to ensure QLabel is still valid
            QTimer.singleShot(2000, weakref.ref(self.messageLabel, self._hide_message))
        except Exception as e:
            self.messageLabel.setText(f"Error taking screenshot: {str(e)}")
            self.messageLabel.repaint()

    def _get_screenshot_directory(self):
        """Return the directory to save screenshots"""
        return "local_files/screenshots"

    def _save_screenshot(self, filename):
        """Save the screenshot using VTK"""
        window_to_image_filter = vtk.vtkWindowToImageFilter()
        window_to_image_filter.SetInput(self.vtk_viewer.get_vtk_widget().GetRenderWindow())
        window_to_image_filter.Update()

        writer = vtk.vtkPNGWriter()
        writer.SetFileName(filename)
        writer.SetInputConnection(window_to_image_filter.GetOutputPort())
        writer.Write()

        print(f"Screenshot saved to {filename}")

    def _hide_message(self, ref):
        """Clear the message label after a delay"""
        label = ref()
        if label:
            label.setText("")