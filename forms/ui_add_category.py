from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QDialogButtonBox, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout,)


class UiDialog:
    def setup_ui(self, Dialog):
        # if not Dialog.objectName():
        #     Dialog.setObjectName(u"MyDialog")

        Dialog.setWindowTitle("Добавить новую категорию")

        Dialog.resize(318, 124)

        self.verticalLayout = QVBoxLayout(Dialog)
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setTitle("Новая категория")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout = QHBoxLayout()
        self.label = QLabel(self.groupBox)
        self.label.setText("Название:")
        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.groupBox)
        self.horizontalLayout.addWidget(self.lineEdit)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(Dialog)
        # self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStyleSheet("""
                            QPushButton {
                                background-color: #4CAF50;
                                color: white;
                                padding: 10px 20px;
                                border-radius: 5px;
                            }
                            
                            QPushButton:hover {
                                background-color: #45a049;
                            }
                """)
        # self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText("ОК")
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText("Отмена")

        self.verticalLayout.addWidget(self.buttonBox)

        # lambda создает "обертку", которая вызывает метод только когда сигнал сработает.
        # self.buttonBox.accepted.connect(lambda: self.the_button_was_clicked(Dialog))
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        # автоматизация нажатия кнопок без вызова connect()
        # QMetaObject.connectSlotsByName(Dialog)

    def the_button_was_clicked(self, Dialog):
        user_input = self.lineEdit.text()

        Dialog.accept()


