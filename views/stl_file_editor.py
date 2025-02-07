from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from pathlib import Path
from views.stl_file_manager import FileManagerWindow
from widgets.navigation_button import NavigationButton


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

        # Button 1: Zoom In
        zoomInButton = QPushButton("Zoom In")
        zoomInButton.clicked.connect(self.zoomIn)
        bottomLayout.addWidget(zoomInButton)

        # Button 2: Go to File Manager
        fileManagerButton = NavigationButton(self, FileManagerWindow, "Go to File Manager")
        bottomLayout.addWidget(fileManagerButton)

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

    def zoomIn(self):
        """Zoom in the camera"""
        camera = self.renderer.GetActiveCamera()
        camera.Zoom(1.2)
        self.vtk_widget.GetRenderWindow().Render()
