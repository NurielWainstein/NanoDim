import os
import json
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton

class JsonEditorDialog(QDialog):
    def __init__(self, config_file, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Function Arguments")
        self.setGeometry(200, 200, 400, 300)

        self.config_file = config_file
        self.layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setText(self.loadJsonConfig())
        self.layout.addWidget(self.text_edit)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.saveJsonConfig)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def loadJsonConfig(self):
        """Loads JSON data from file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return f.read()
        return "{}"  # Default empty JSON object

    def saveJsonConfig(self):
        """Saves JSON data to file and closes the dialog."""
        with open(self.config_file, "w") as f:
            f.write(self.text_edit.toPlainText())
        self.accept()

    def getJsonData(self):
        """Returns the JSON data from the editor."""
        try:
            return json.loads(self.text_edit.toPlainText())
        except json.JSONDecodeError:
            return {}  # Return empty dict if invalid JSON

    def openConfigEditor(self):
        """Opens the ConfigEditorWidget to edit function arguments."""
        self.show()
        self.loadJsonConfig()
