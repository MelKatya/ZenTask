import sys
import time

from PySide6.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QMessageBox, QDialogButtonBox, QDateTimeEdit
from forms.ui_main_form import MainForm, Base, Note
from forms.ui_add_category import NewCategory
from forms.ui_add_timer import AddTimer
from forms.ui_show_history import ShowTimers
from utils import (upload_priority, upload_category, save_new_category, save_task, save_timer,
                   stop_timer, show_history_time, save_note_to_db, download_noticed_from_db, download_all_tasks_from_db)
from PySide6.QtCore import Signal, Qt
from psycopg2 import errors
import psycopg2
from datetime import datetime, timedelta
import threading
from database import Note as No, Task


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
    def __init__(self, toolBox_not, page_number, functons, text=''):
        super().__init__(toolBox_not, page_number)
        self.tb_not = toolBox_not
        self.page_number = page_number
        self.text_edit_note.setText(text)
        self.save, self.delete, self.attach = functons
        self.pushButton_save_not.clicked.connect(lambda: self.save(text=self.text_edit_note.toPlainText()))
        # print(self.pushButton_save_not.emit())
        self.pushButton_del_not.clicked.connect(lambda: self.delete(page_number=self.page_number))
        self.pushButton_attach_not.clicked.connect(lambda: self.attach(page_number=self.page_number))


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
        self.download_note()
        self.pushButton_21.clicked.connect(self.open_history_form)
        self.planned_tasks, self.doing_tasks, self.done_tasks = download_all_tasks_from_db()
        self.upload_all_tasks_with_data()
        self.pushButton_mt_plan_change_task.clicked.connect(self.change_task)
        self.pushButton_mt_plan_change_task.setEnabled(False)

    def change_task(self):
        """Обрабатывает кнопку изменения задачи"""
        if self.pushButton_mt_plan_change_task.text() == 'Сохранить изменения':
            print('ggfgf')
            current_task = self.comboBox_mt_plan_all.currentData()
            self.change_task_button(grid_layout=self.grid_layout_plan, task=current_task)
            self.frame_mt_plan.setEnabled(False)
            self.pushButton_mt_plan_change_task.setText('Изменить задачу')

        else:
            print('hdhdhhd')
            self.frame_mt_plan.setEnabled(True)
            self.pushButton_mt_plan_change_task.setText('Сохранить изменения')

    def change_task_button(self, grid_layout, task):
        """Обрабатывает кнопку 'Изменить задачу' - изменяет задачу"""
        flag = True
        if not grid_layout.line_edit_name.text():
            QMessageBox.warning(self, "Ошибка", "Необходимо ввести название задачи.")
            flag = False

        if not grid_layout.text_edit_description.toPlainText():
            QMessageBox.warning(self, "Ошибка", "Необходимо ввести описание задачи.")
            flag = False

        if flag:
            task.name = grid_layout.line_edit_name.text()
            task.priority = grid_layout.combo_box_prior.currentIndex() + 1
            task.category = grid_layout.combo_box_category.currentIndex() + 1
            task.description = grid_layout.text_edit_description.toPlainText()

            if grid_layout.check_box_add_time.checkState() == Qt.CheckState.Checked:
                deadline = grid_layout.datetime_edit.dateTime()
                deadline = deadline.toPython()
            else:
                deadline = None

            task.deadline = deadline
            result = task.change_task()
            if result:
                QMessageBox.about(self, 'Успех', f'Задача {task.name} изменена')
            else:
                QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {result}")

    def upload_all_tasks_with_data(self):
        """Выгружает все задачи в нужные комбобоксы"""
        self.upload_planned_task()
        self.upload_doing_task()
        self.upload_done_task()

        self.comboBox_mt_plan_all.currentIndexChanged.connect(lambda: self.upload_data_to_form(
            value=self.comboBox_mt_plan_all.currentIndex(),
            grid_layout=self.grid_layout_plan,
            combo_box=self.comboBox_mt_plan_all))

        self.comboBox_mt_proc_all.currentIndexChanged.connect(lambda: self.upload_data_to_form(
            value=self.comboBox_mt_proc_all.currentIndex(),
            grid_layout=self.grid_layout_plan,
            combo_box=self.comboBox_mt_proc_all))

        self.comboBox_mt_done_all.currentIndexChanged.connect(lambda: self.upload_data_to_form(
            value=self.comboBox_mt_done_all.currentIndex(),
            grid_layout=self.grid_layout_plan,
            combo_box=self.comboBox_mt_done_all))


    def upload_data_to_form(self, value, grid_layout, combo_box):
        """Подставляет данные выбранной задачи в чекбоксе"""
        print("Значение ComboBox изменено", value)
        # изменяет видимость всех полей
        self.pushButton_mt_plan_change_task.setEnabled(True)
        self.frame_mt_plan.setEnabled(False)
        self.pushButton_mt_plan_change_task.setText('Изменить задачу')

        current_task = combo_box.currentData()
        grid_layout.line_edit_name.setText(current_task.name)
        grid_layout.combo_box_prior.setCurrentIndex(current_task.priority - 1)
        grid_layout.combo_box_category.setCurrentIndex(current_task.category - 1)
        grid_layout.text_edit_description.setText(current_task.description)
        if current_task.deadline:
            grid_layout.check_box_add_time.setChecked(True)
            date = datetime.strptime(current_task.deadline, "%Y-%m-%d %H:%M:%S")
            grid_layout.datetime_edit.setVisible(True)
            grid_layout.datetime_edit.setDateTime(date)
        else:
            grid_layout.check_box_add_time.setChecked(False)
            grid_layout.datetime_edit.setVisible(False)

    def upload_planned_task(self):
        """Загружает все запланированные задачи в комбобокс"""
        self.planned_tasks = Task.download_planned_tasks()
        self.comboBox_mt_plan_all.clear()
        for task in self.planned_tasks:
            self.comboBox_mt_plan_all.addItem(task.name, task)

    def upload_doing_task(self):
        """Загружает все выполняемые задачи в комбобокс"""
        for task in self.doing_tasks:
            self.comboBox_mt_proc_all.addItem(task.name, task)

    def upload_done_task(self):
        """Загружает все выполненные задачи в комбобокс"""
        for task in self.done_tasks:
            self.comboBox_mt_done_all.addItem(task.name, task)

    def download_note(self):
        """Выгружает заметки из бд"""
        self.pages_notes = []
        self.functions_for_note = (self.save_note, self.del_note, self.attache_notice)

        all_notes = download_noticed_from_db()
        if not all_notes:
            self.notes = {}
            self.pages_notes = [0]
        else:
            self.notes = {}
            for note in all_notes:
                self.pages_notes.append(note[3])
                self.notes[note[3]] = [NoteTask(self.toolBox_not, note[3], self.functions_for_note, note[1]),
                                       No(id=note[0], text=note[1], page=note[3])]
                self.notes[note[3]][0].pushButton_del_not.setEnabled(True)
                self.notes[note[3]][0].pushButton_attach_not.setEnabled(True)
                self.notes[note[3]][0].pushButton_save_not.setEnabled(False)

        first_note = NoteTask(self.toolBox_not, self.pages_notes[-1] + 1, self.functions_for_note)
        self.notes[self.pages_notes[-1] + 1] = [first_note]
        self.pages_notes.append(self.pages_notes[-1] + 1)

    def save_note(self, text):
        """Сохраняет заметки"""
        page_number = self.pages_notes[-1]
        note = save_note_to_db(text, page_number)
        self.notes[page_number].append(note)
        self.notes[page_number + 1] = [NoteTask(self.toolBox_not, page_number + 1, self.functions_for_note)]
        self.pages_notes.append(page_number + 1)
        self.notes[page_number][0].pushButton_del_not.setEnabled(True)
        self.notes[page_number][0].pushButton_attach_not.setEnabled(True)
        self.notes[page_number][0].pushButton_save_not.setEnabled(False)

    def del_note(self, page_number):
        """Удаляет заметки"""
        self.notes[page_number][1].delete_note()
        self.toolBox_not.removeItem(self.toolBox_not.currentIndex())
        self.notes.pop(page_number)

    # todo прикрепление выглядит отстойно

    def attache_notice(self, page_number):
        """Прикрепляет заметку справа"""
        self.dockWidget_notice.setVisible(True)
        self.label_atached_note.setText(f"{self.notes[page_number][1].text}")
        self.notes[page_number][1].attach_note()

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
            self.grid_layout_new_task.datetime_edit.setVisible(True)
        elif state == Qt.CheckState.Unchecked:
            self.grid_layout_new_task.datetime_edit.setVisible(False)

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

            if self.grid_layout_new_task.check_box_add_time.checkState() == Qt.CheckState.Checked:
                deadline = self.grid_layout_new_task.datetime_edit.dateTime()
                deadline = deadline.toPython()
            else:
                deadline = None

            recording_result = save_task(name, priority, category, descrirton, deadline)
            if not recording_result:
                self.upload_planned_task()
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
        """Открывает форму с историей работы таймера"""
        dialog = QDialog()
        ui = ShowTimers()
        ui.setup_ui(dialog)
        total_time, result = show_history_time()
        ui.label_2.setText(str(total_time))
        for timer_data in result:
            ui.add_row(timer_data)
        dialog.exec()








