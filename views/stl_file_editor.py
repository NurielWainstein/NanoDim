from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from widgets.navigation_button import NavigationButton
import os
import time


class EditSTLWindow(QMainWindow):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 700, 900)
        self.setAcceptDrops(True)

        self.file_path = file_path  # Store the file path
        self.initUI()
        self.showSTL(file_path)  # Automatically load the STL file

    def initUI(self):
        centerWidget = QWidget()
        self.setCentralWidget(centerWidget)

        layout = QVBoxLayout()
        centerWidget.setLayout(layout)

        # 3D Viewer with VTK
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        layout.addWidget(self.vtk_widget, 1)

        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.vtk_widget.GetRenderWindow().SetSize(700, 900)

        # Improve rotation by using trackball interaction
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        style = vtk.vtkInteractorStyleTrackballCamera()  # Improved rotation style
        self.interactor.SetInteractorStyle(style)
        self.interactor.Initialize()  # Ensure interaction starts properly
        self.interactor.Start()

        # Bottom buttons
        bottomLayout = QHBoxLayout()
        layout.addLayout(bottomLayout)

        # Button: Screenshot
        screenshotButton = QPushButton("Take Screenshot")
        screenshotButton.clicked.connect(self.takeScreenshot)
        bottomLayout.addWidget(screenshotButton)

        # Button: Go to File Manager
        fileManagerButton = NavigationButton(self, "FileManagerWindow", "Go to File Manager")
        bottomLayout.addWidget(fileManagerButton)

        # Temporary message label
        self.messageLabel = QLabel("")
        layout.addWidget(self.messageLabel)

    def showSTL(self, filename):
        # Clear previous STL file if any
        self.renderer.RemoveAllViewProps()

        # Read STL file
        reader = vtk.vtkSTLReader()
        reader.SetFileName(str(filename))
        reader.Update()

        # Map STL data
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        # Create 3D model actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        self.renderer.AddActor(actor)
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

    def takeScreenshot(self):
        """Capture and save a screenshot of the VTK render window with a unique filename"""
        screenshot_dir = "local_files/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")

        # Get the render window as an image
        window_to_image_filter = vtk.vtkWindowToImageFilter()
        window_to_image_filter.SetInput(self.vtk_widget.GetRenderWindow())
        window_to_image_filter.Update()

        writer = vtk.vtkPNGWriter()
        writer.SetFileName(filename)
        writer.SetInputConnection(window_to_image_filter.GetOutputPort())
        writer.Write()

        self.messageLabel.setText(f"Screenshot saved: {filename}")
        self.messageLabel.repaint()

        # Hide the message after a short delay
        QTimer.singleShot(2000, lambda: self.messageLabel.setText(""))

        print(f"Screenshot saved to {filename}")
