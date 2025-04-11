from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtWidgets import (QDialogButtonBox, QGroupBox, QHBoxLayout, QLabel, QSizePolicy,
                               QSpacerItem, QTimeEdit, QVBoxLayout, QWidget)
import datetime


class AddTimer:
    def setup_ui(self, Dialog):

        Dialog.resize(248, 211)
        Dialog.setWindowTitle('Добавление таймера')

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(0, 170, 231, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.groupBox = QGroupBox('Добавить таймер', Dialog)
        self.groupBox.setGeometry(QRect(10, 10, 221, 151))

        self.verticalLayoutWidget = QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 171, 51))

        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel('Планируемое время работы:', self.verticalLayoutWidget)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.timeEdit = QTimeEdit(self.verticalLayoutWidget)
        self.timeEdit.setMinimumSize(QSize(75, 0))
        self.timeEdit.timeChanged.connect(self.onSelectionChanged)

        self.horizontalLayout.addWidget(self.timeEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayoutWidget_2 = QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 80, 160, 51))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.label_2 = QLabel('Окончание работы:', self.verticalLayoutWidget_2)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setText('')

        self.verticalLayout_2.addWidget(self.label_3)


        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

    def onSelectionChanged(self):
        start = datetime.datetime.now()
        data = self.timeEdit.text().split(':')
        th1, tm1 = map(int, data)
        res = (start + datetime.timedelta(hours=th1, minutes=tm1)).strftime('%m.%d в %H:%M')
        self.label_3.setText(str(res))


