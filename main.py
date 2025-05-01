import sys
from database import create_tables
import resources_rc
create_tables()
from main_window import MainWindow
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

