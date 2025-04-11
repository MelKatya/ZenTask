import sys
from PySide6.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QMessageBox, QDialogButtonBox
from forms.ui_main_form import MainForm, Base
from forms.ui_add_category import NewCategory
from forms.ui_add_timer import AddTimer
from utils import upload_priority, upload_category, save_new_category, save_task
from PySide6.QtCore import Qt
from psycopg2 import errors
import psycopg2
from datetime import datetime


class DialogCategory(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = NewCategory()
        self.ui.setup_ui(self)

        self.ui.buttonBox.accepted.connect(self.the_button_was_clicked)
        # self.buttonBox.accepted.connect(Dialog.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def the_button_was_clicked(self):
        user_input = self.ui.lineEdit.text()
        if user_input:
            QMessageBox.about(self, 'Успех', f'Категория {user_input} сохранена')

            # msgBox = QMessageBox()
            # msgBox.setText("The document has been modified.")
            # msgBox.setInformativeText("Do you want to save your changes?")
            # msgBox.setStandardButtons(QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
            # msgBox.setDefaultButton(QMessageBox.StandardButton.Save)
            # ret = msgBox.exec()

            # QMessageBox.information(self, 'Успех', f'Категория {user_input} сохранена', QDialogButtonBox.StandardButton.Ok)
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Необходимо ввести новую категорию.")


class DialogTimer(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = AddTimer()
        self.ui.setup_ui(self)


class MainWindow(MainForm):
    def __init__(self):
        super().__init__()

        self.upload_priority()
        self.upload_category()
        self.change_page_buttons()
        self.grid_layout_new_task.push_button_new_cat.clicked.connect(self.open_category_form)
        self.grid_layout_new_task.check_box_add_time.checkStateChanged.connect(self.on_checkbox_state_changed)
        self.pushButton_nt_create_task.clicked.connect(self.save_task_button)
        self.grid_layout_new_task.datetime_edit.setDateTime(datetime.now())
        # добавить таймер
        # self.pushButton_set_timer.clicked.connect()

    def upload_category(self):
        """Загружает категории из бд"""
        upload_category(self.grid_layout_new_task.combo_box_category)

        upload_category(self.grid_layout_plan.combo_box_category)

        upload_category(self.grid_layout_proc.combo_box_category)

        upload_category(self.grid_layout_done.combo_box_category)

    def upload_priority(self):
        """Загружает приоритет из бд"""
        upload_priority(self.grid_layout_new_task.combo_box_prior)

        upload_priority(self.grid_layout_plan.combo_box_prior)

        upload_priority(self.grid_layout_proc.combo_box_prior)

        upload_priority(self.grid_layout_done.combo_box_prior)

    def change_page_buttons(self):
        """Обрабатывает кнопки перехода на другие страницы"""
        self.pushButton_nt_my_task.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_nt_not.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        self.pushButton_mt_not.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButton_mt_crete_task.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        self.pushButton_cret_tsk_not.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_my_task_not.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

    def open_category_form(self):
        """Открывает форму создания новой категории"""
        dialog = DialogCategory()

        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            new_category_name = dialog.ui.lineEdit.text()
            save_new_category(new_category_name)
            self.upload_category()
            print("Данные получены:", new_category_name)
        else:
            print("Пользователь отменил")

    def on_checkbox_state_changed(self, state):
        """Изменение состояния чекбокса с заданием дедлайна"""
        if state == Qt.CheckState.Checked:
            self.grid_layout_new_task.datetime_edit.setEnabled(True)
        elif state == Qt.CheckState.Unchecked:
            self.grid_layout_new_task.datetime_edit.setEnabled(False)

    def save_task_button(self):
        """Обрабатывает кнопку 'Создать задачу' - создает задачу"""
        flag = True
        if not self.grid_layout_new_task.line_edit_name.text():
            QMessageBox.warning(self, "Ошибка", "Необходимо ввести название задачи.")
            flag = False

        if not self.grid_layout_new_task.text_edit_description.toPlainText():
            QMessageBox.warning(self, "Ошибка", "Необходимо ввести описание задачи.")
            flag = False

        if flag:
            name = self.grid_layout_new_task.line_edit_name.text()
            priority = self.grid_layout_new_task.combo_box_prior.currentText()
            category = self.grid_layout_new_task.combo_box_category.currentText()
            descrirton = self.grid_layout_new_task.text_edit_description.toPlainText()

            deadline = None
            if self.grid_layout_new_task.check_box_add_time.checkState() == Qt.CheckState.Checked:
                deadline = self.grid_layout_new_task.datetime_edit.dateTime()
                deadline = deadline.toPython()

            recording_result = save_task(name, priority, category, descrirton, deadline)
            if not recording_result:
                QMessageBox.about(self, 'Успех', f'задача {name} сохранена')
            elif isinstance(recording_result, psycopg2.errors.UniqueViolation):
                QMessageBox.warning(self, "Ошибка", "Задача с таким именем уже есть.")


