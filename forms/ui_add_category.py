from PySide6.QtWidgets import QDialogButtonBox, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout


class NewCategory:
    def setup_ui(self, Dialog):

        Dialog.setWindowTitle("Добавить новую категорию")
        Dialog.resize(318, 124)

        self.verticalLayout = QVBoxLayout(Dialog)
        self.groupBox = QGroupBox("Новая категория", Dialog)
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout = QHBoxLayout()

        self.label = QLabel("Название:", self.groupBox)
        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.groupBox)
        self.horizontalLayout.addWidget(self.lineEdit)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(Dialog)

        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText("ОК")
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText("Отмена")

        self.verticalLayout.addWidget(self.buttonBox)
