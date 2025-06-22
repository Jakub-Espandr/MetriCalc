import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

# Suppress Qt threading warnings on macOS
os.environ['QT_MAC_WANTS_LAYER'] = '1'
os.environ['QT_LOGGING_RULES'] = 'qt.qpa.*=false'

# Import local modules
from utils.resources import get_app_icon, load_custom_fonts
from ui.main_window import MetriCalcApp

if __name__ == "__main__":
    # Add the project root to the Python path to allow for absolute imports
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)

    app = QApplication(sys.argv)
    app.setApplicationName("MetriCalc")
    app.setApplicationVersion("1.0")

    # Load and set the application icon
    app_icon = get_app_icon()
    if app_icon:
        app.setWindowIcon(app_icon)

    # Load custom fonts and set default for the application
    load_custom_fonts()
    app.setFont(QFont("fccTYPO", 11))
    
    window = MetriCalcApp(app_icon=app_icon)
    window.show()
    
    sys.exit(app.exec())