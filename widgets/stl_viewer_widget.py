from PyQt6.QtWidgets import QWidget, QVBoxLayout
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class VTKViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """Initialize the VTK Viewer."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.vtk_widget = QVTKRenderWindowInteractor(self)
        layout.addWidget(self.vtk_widget, 1)

        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.vtk_widget.GetRenderWindow().SetSize(700, 900)

        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        style = vtk.vtkInteractorStyleTrackballCamera()  # Improved rotation style
        self.interactor.SetInteractorStyle(style)
        self.interactor.Initialize()  # Ensure interaction starts properly
        self.interactor.Start()

    def load_stl(self, filename):
        """Load and display the STL file in the VTK viewer."""
        self.renderer.RemoveAllViewProps()

        try:
            reader = vtk.vtkSTLReader()
            reader.SetFileName(str(filename))
            reader.Update()

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(reader.GetOutputPort())

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            self.renderer.AddActor(actor)
            self.renderer.ResetCamera()
            self.vtk_widget.GetRenderWindow().Render()
        except Exception as e:
            print(f"Error loading STL file: {str(e)}")  # Logging instead of QLabel dependency

    def get_vtk_widget(self):
        """Return the VTK widget reference."""
        return self.vtk_widget