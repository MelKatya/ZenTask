from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QAbstractItemView, QDialogButtonBox, QGroupBox, QLabel, QTreeWidget, QTreeWidgetItem


class AddReplay:
    def setup_ui(self, Dialog):
        Dialog.setWindowTitle('Повтор')
        Dialog.resize(389, 301)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(30, 260, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setTitle('Добавить повтор')
        self.groupBox.setGeometry(QRect(10, 10, 361, 241))


        self.tree_view = QTreeWidget(self.groupBox)
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.tree_view.setAnimated(True)
        self.tree_view.setAllColumnsShowFocus(True)
        self.tree_view.setGeometry(QRect(10, 30, 141, 201))

        month = QTreeWidgetItem(self.tree_view, ["Месяц"])
        week = QTreeWidgetItem(self.tree_view, ["Неделя"])
        day = QTreeWidgetItem(self.tree_view, ["День"])

        for day_of_month in range(1, 32):
            QTreeWidgetItem(month, [str(day_of_month)])

        for day_of_week in ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"):
            QTreeWidgetItem(week, [day_of_week])

        for hour in range(0, 24):
            QTreeWidgetItem(day, [f'{hour:02d}:00'])


        self.label = QLabel(self.groupBox)
        self.label.setText("Задача будет повторяться каждый:")
        self.label.setGeometry(QRect(160, 30, 191, 31))
        self.label_2 = QLabel(self.groupBox)

        self.label_2.setGeometry(QRect(160, 60, 191, 160))
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_2.setText('')







