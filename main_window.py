import sys
import time

from PySide6.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QMessageBox, QDialogButtonBox
from forms.ui_main_form import MainForm, Base, Note
from forms.ui_add_category import NewCategory
from forms.ui_add_timer import AddTimer
from forms.ui_show_history import ShowTimers
from utils import (upload_priority, upload_category, save_new_category, save_task, save_timer,
                   stop_timer, show_history_time, save_note_to_db)
from PySide6.QtCore import Signal, Qt
from psycopg2 import errors
import psycopg2
from datetime import datetime, timedelta
import threading


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

        self.id_timer = None
        self.ui.timeEdit.timeChanged.connect(self.change_time)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def change_time(self):
        start = datetime.now()
        self.data = self.ui.timeEdit.text().split(':')
        th1, tm1 = map(int, self.data)
        self.res = (start + timedelta(hours=th1, minutes=tm1))
        self.ui.label_3.setText(str(self.res.strftime('%m.%d в %H:%M')))


class NoteTask(Note):
    def __init__(self, toolBox_not, page_number, functons):
        super().__init__(toolBox_not, page_number)
        self.tb_not = toolBox_not
        self.page_number = page_number
        self.save, self.delete = functons
        self.pushButton_save_not.clicked.connect(lambda: self.save(text=self.text_edit_note.toPlainText()))
        # print(self.pushButton_save_not.emit())
        self.pushButton_del_not.clicked.connect(lambda: self.delete(page_number=self.page_number))

class MainWindow(MainForm):
    timer_finished = Signal()

    def __init__(self):
        super().__init__()

        self.timer_finished.connect(self.finsh_timer)
        self.upload_priority()
        self.upload_category()
        self.change_page_buttons()
        self.grid_layout_new_task.push_button_new_cat.clicked.connect(self.open_category_form)
        self.grid_layout_new_task.check_box_add_time.checkStateChanged.connect(self.on_checkbox_state_changed)
        self.pushButton_nt_create_task.clicked.connect(self.save_task_button)
        self.grid_layout_new_task.datetime_edit.setDateTime(datetime.now())
        self.pushButton_set_timer.clicked.connect(self.open_timer_form)
        self.pushButton_20.clicked.connect(self.stop_timer)
        self.pushButton_20.setEnabled(False)
        self.pushButton_21.clicked.connect(self.open_history_form)
        first_note = NoteTask(self.toolBox_not, 1, (self.save_note, self.del_note))
        self.notes = {1: [first_note]}

    # todo если удалить все заметки, то как добавить еще? номер заметок должен меняться?
    #  выгружать заметки из бд?

    def save_note(self, text):
        """Сохраняет заметки"""
        page_number = len(self.notes)
        note = save_note_to_db(text, page_number)
        self.notes[page_number].append(note)
        self.notes[page_number + 1] = [NoteTask(self.toolBox_not, page_number + 1, (self.save_note, self.del_note))]
        self.notes[page_number][0].pushButton_del_not.setEnabled(True)
        self.notes[page_number][0].pushButton_save_not.setEnabled(False)

    def del_note(self, page_number):
        """Удаляет заметки"""
        print(page_number)
        print(self.notes[page_number])
        self.notes[page_number][1].delete_note()
        self.toolBox_not.removeItem(page_number - 1)

    def attache_notice(self):
        """Прикрепляет заметку справа"""
        ...


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

    def open_timer_form(self):
        """Открывает форму добавления нового таймера"""
        dialog = DialogTimer()
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            if dialog.ui.timeEdit.text() == '0:00':
                QMessageBox.warning(self, "Ошибка", "Необходимо указать время.")
            else:
                self.total_timer = save_timer(dialog.ui.timeEdit.text())
                time_1 = dialog.ui.timeEdit.dateTime().toPython()
                self.label_main_timer_passed.setText('00:00')
                self.label_main_timer_last.setText(time_1.strftime('%H:%M'))
                # self.pushButton_set_timer.setVisible(False)
                self.pushButton_set_timer.setEnabled(False)
                self.run_time = True
                self.pushButton_20.setEnabled(True)
                self.thread_timer = threading.Thread(target=self.strat_timer,
                                                     args=(self.label_main_timer_passed,
                                                           self.label_main_timer_last, time_1), daemon=True)
                self.thread_timer.start()
        else:
            print("Пользователь отменил")

    def strat_timer(self, label_passed, label_last, timer):
        """Запускает таймер"""
        pass_time = (timer - timedelta(minutes=1)).strftime('%H:%M')
        self.rest_time = datetime.now().replace(hour=0, minute=0, second=0)
        while pass_time != '00:00' and self.run_time:
            time.sleep(1)
            if self.run_time == False:
                break
            timer -= timedelta(minutes=1)
            self.rest_time += timedelta(minutes=1)
            pass_time = timer.strftime('%H:%M')
            label_last.setText(pass_time)
            label_passed.setText(self.rest_time.strftime('%H:%M'))
        self.timer_finished.emit()

    def finsh_timer(self):
        """Действия после завершения работы таймера"""
        stop_timer(self.total_timer, self.rest_time)
        self.pushButton_set_timer.setEnabled(True)
        self.pushButton_20.setEnabled(False)
        QMessageBox.about(self, 'Таймер', f'Таймер закончил работу')

    def stop_timer(self):
        """Обрабаотывает кнопку остановки таймера"""
        self.run_time = False
        self.thread_timer.join()

    def open_history_form(self):
        """Открывает форму с историей работы по таймеру"""
        dialog = QDialog()
        ui = ShowTimers()
        ui.setup_ui(dialog)
        total_time, result = show_history_time()
        ui.label_2.setText(str(total_time))
        for timer_data in result:
            ui.add_row(timer_data)
        dialog.exec()








