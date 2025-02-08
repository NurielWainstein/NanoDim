import os
from shutil import copy2

from config.config import STL_FILES_DIR

class FileController:
    def __init__(self):
        self.save_path = STL_FILES_DIR
        os.makedirs(self.save_path, exist_ok=True)
        self.stl_files = self.load_existing_files()

    def load_existing_files(self):
        """Load existing STL files from the directory."""
        return [os.path.join(self.save_path, f) for f in os.listdir(self.save_path) if f.endswith('.stl')]

    def save_and_add_file(self, file_path):
        """Save STL file and update the list."""
        dest_path = os.path.join(self.save_path, os.path.basename(file_path))
        if dest_path not in self.stl_files:
            copy2(file_path, dest_path)
            self.stl_files.append(dest_path)
            print(f"Added: {dest_path}")
        else:
            print(f"File already exists: {dest_path}")

    def get_files(self):
        """Return the list of STL files."""
        return self.stl_files

    def get_basename_files(self):
        """Returns a list of STL file basenames (without full paths)."""
        return [os.path.basename(file) for file in self.get_files()]

