from PySide6.QtWidgets import QPushButton, QMenu
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction

class CustomDropdown(QPushButton):
    """
    A custom dropdown widget built from a QPushButton and a QMenu 
    to avoid QComboBox styling issues on macOS.
    """
    currentTextChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = []
        self._current_text = ""
        self.menu = QMenu(self)
        self.menu.aboutToShow.connect(self._update_menu)
        self.setMenu(self.menu)

    def addItem(self, text, data=None):
        """Adds an item to the dropdown. The data is unused but kept for API compatibility."""
        self._items.append(text)
        if not self._current_text:
            self.setCurrentText(text)

    def setCurrentText(self, text):
        """Sets the current text displayed on the button."""
        if text != self._current_text:
            self._current_text = text
            self.setText(text)
            self.currentTextChanged.emit(text)

    def currentText(self):
        """Returns the current text."""
        return self._current_text

    def _update_menu(self):
        """Clears and rebuilds the menu before showing it."""
        self.menu.clear()
        for text in self._items:
            action = QAction(text, self)
            action.triggered.connect(lambda checked=False, t=text: self.setCurrentText(t))
            self.menu.addAction(action) 