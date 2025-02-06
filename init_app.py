import sys
from PyQt6.QtWidgets import QApplication
from views.stl_file_manager import FileManagerWindow

def main():
    app = QApplication(sys.argv)
    window = FileManagerWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
