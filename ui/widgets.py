from PySide6.QtWidgets import QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class ModernButton(QPushButton):
    """Custom modern button with hover effects"""
    def __init__(self, text, icon_text="", color="#4CAF50", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(45)
        bold_font = QFont("fccTYPO", 10)
        bold_font.setBold(True)
        self.setFont(bold_font)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self._adjust_color(color, 1.1)};
            }}
            QPushButton:pressed {{
                background-color: {self._adjust_color(color, 0.9)};
            }}
        """)
        
        if icon_text:
            self.setText(f"{icon_text} {text}")
    
    def _adjust_color(self, color, factor):
        """Adjust color brightness"""
        if color.startswith('#'):
            color = color[1:]
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c * factor)) for c in rgb)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

class FileLabel(QLabel):
    """Custom label for displaying file paths"""
    def __init__(self, default_text, parent=None):
        super().__init__(default_text, parent)
        self.setFont(QFont("fccTYPO", 9))
        self.setStyleSheet("""
            QLabel {
                color: #666;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 8px 12px;
                margin: 4px 0;
            }
        """)
        self.setWordWrap(True) 