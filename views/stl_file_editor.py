from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
import pyqtgraph.opengl as gl
import numpy as np
from stl import mesh
from pathlib import Path

from views.stl_file_manager import FileManagerWindow
from widgets.navigation_button import NavigationButton


class EditSTLWindow(QMainWindow):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 700, 900)
        self.setAcceptDrops(True)

        self.zoom_factor = 40  # Initial zoom distance
        self.currentSTL = None
        self.lastDir = None
        self.droppedFilename = None
        self.file_path = file_path  # Store the file path

        self.initUI()
        self.showSTL(file_path)  # Automatically load the STL file on window initialization

    def initUI(self):
        centerWidget = QWidget()
        self.setCentralWidget(centerWidget)

        layout = QVBoxLayout()
        centerWidget.setLayout(layout)

        # 3D Viewer
        self.viewer = gl.GLViewWidget()
        layout.addWidget(self.viewer, 1)

        self.viewer.setWindowTitle('STL Viewer')
        self.viewer.setCameraPosition(distance=self.zoom_factor)

        g = gl.GLGridItem()
        g.setSize(200, 200)
        g.setSpacing(5, 5)
        self.viewer.addItem(g)

        # Bottom buttons
        bottomLayout = QHBoxLayout()  # Layout for the buttons
        layout.addLayout(bottomLayout)

        # Button 1: For example, "Zoom In"
        zoomInButton = QPushButton("Zoom In")
        zoomInButton.clicked.connect(self.zoomIn)
        bottomLayout.addWidget(zoomInButton)

        # Button 2: "Go to File Manager" - Using NavigationButton
        fileManagerButton = NavigationButton(self, FileManagerWindow, "Go to File Manager")
        bottomLayout.addWidget(fileManagerButton)

    def showSTL(self, filename):
        if self.currentSTL:
            self.viewer.removeItem(self.currentSTL)

        points, faces = self.loadSTL(filename)
        meshdata = gl.MeshData(vertexes=points, faces=faces)
        mesh_item = gl.GLMeshItem(meshdata=meshdata, smooth=True, drawFaces=False, drawEdges=True,
                                  edgeColor=(0, 1, 0, 1))
        self.viewer.addItem(mesh_item)

        self.currentSTL = mesh_item

    def loadSTL(self, filename):
        m = mesh.Mesh.from_file(filename)
        points = m.points.reshape(-1, 3)
        faces = np.arange(points.shape[0]).reshape(-1, 3)
        return points, faces

    def dragEnterEvent(self, e):
        mimeData = e.mimeData()
        mimeList = mimeData.formats()
        filename = None

        if "text/uri-list" in mimeList:
            filename = mimeData.data("text/uri-list")
            filename = str(filename, encoding="utf-8")
            filename = filename.replace("file:///", "").replace("\r\n", "").replace("%20", " ")
            filename = Path(filename)

        if filename.exists() and filename.suffix == ".stl":
            e.accept()
            self.droppedFilename = filename
        else:
            e.ignore()
            self.droppedFilename = None

    def dropEvent(self, e):
        if self.droppedFilename:
            self.showSTL(self.droppedFilename)

    def wheelEvent(self, event):
        """Handle mouse wheel zooming"""
        if event.angleDelta().y() > 0:
            self.zoom_factor += 5  # Zoom in
        else:
            self.zoom_factor -= 5  # Zoom out
        self.viewer.setCameraPosition(distance=self.zoom_factor)

    def zoomIn(self):
        """Zoom in when button is clicked"""
        self.zoom_factor += 5
        self.viewer.setCameraPosition(distance=self.zoom_factor)
