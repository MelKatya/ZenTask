from PySide6.QtCore import QRect
from PySide6.QtWidgets import (QDialogButtonBox, QGroupBox, QHBoxLayout, QLabel,
                               QTableWidget, QTableWidgetItem, QWidget)


class ShowTimers:
    def setup_ui(self, Dialog):
        Dialog.resize(422, 409)
        Dialog.setWindowTitle('История')

        self.groupBox = QGroupBox('История работы таймера', Dialog)
        self.groupBox.setGeometry(QRect(10, 10, 401, 351))
        self.tableWidget = QTableWidget(self.groupBox)

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Дата запуска', 'Запланированное время ', 'Отработанное время'])
        self.tableWidget.resizeColumnsToContents()

        self.tableWidget.setGeometry(QRect(8, 30, 385, 311))

        self.horizontalLayoutWidget = QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QRect(10, 360, 401, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)

        self.label = QLabel('Всего отработано времени:', self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.label)

        self.label_2 = QLabel('Всего отработано времени:', self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.label_2)

        self.buttonBox = QDialogButtonBox(self.horizontalLayoutWidget)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close)
        self.buttonBox.rejected.connect(Dialog.close)
        self.horizontalLayout.addWidget(self.buttonBox)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Close).setText("Закрыть")

    def add_row(self, timer_data):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        for row, data in zip((0, 1, 2), timer_data):
            item = QTableWidgetItem(data)
            self.tableWidget.setItem(row_position, row, item)
