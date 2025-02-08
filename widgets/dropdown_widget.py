from PyQt6.QtWidgets import QComboBox

class DropdownWidget(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItem("Select Option")

    def update_items(self, items):
        """Update dropdown items dynamically."""
        self.clear()
        self.addItem("Select Option")
        self.addItems(items)
