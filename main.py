import sys
from main_window import MainWindow
from PySide6.QtWidgets import QApplication
from database import create_tables



if __name__ == "__main__":
    create_tables()

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

