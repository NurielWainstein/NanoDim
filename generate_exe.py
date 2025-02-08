import subprocess
import sys


def create_exe():
    """Use PyInstaller to create the executable."""
    print("Creating executable with PyInstaller...")
    pyinstaller_command = [
        sys.executable, "-m", "PyInstaller",
        "--onefile", "--windowed", "init_app.py"
    ]
    subprocess.run(pyinstaller_command, check=True)
    print("Executable created successfully.")


if __name__ == "__main__":
    create_exe()
