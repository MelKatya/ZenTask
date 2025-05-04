import sys
import time

from PySide6.QtWidgets import (QApplication, QWidget, QDialog, QMainWindow, QMessageBox, QDialogButtonBox,
                               QDateTimeEdit, QAbstractButton, QPushButton, QVBoxLayout, QLabel, QDockWidget,
                               QRadioButton, QButtonGroup, QGridLayout, QGroupBox)
from forms.ui_main_form import MainForm, Base, Note
from forms.ui_add_category import NewCategory
from forms.ui_add_timer import AddTimer
from forms.ui_show_history import ShowTimers
from forms.ui_add_replay import AddReplay
from utils import (upload_priority, upload_category, save_new_category, save_task, save_timer,
                   stop_timer, show_history_time, save_note_to_db, download_noticed_from_db, add_new_repeat)
from PySide6.QtCore import Signal, Qt
from psycopg2 import errors
import psycopg2
from datetime import datetime, timedelta
import threading
from database import Note as No, Task


class DialogReplay(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = AddReplay()
        self.ui.setup_ui(self)

        self.ui.tree_view.itemClicked.connect(self.the_button_was_clicked)

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def the_button_was_clicked(self):
        """Обрабатывает нажатие на дерево выбора"""
        val = ''
        for sel in self.ui.tree_view.selectedIndexes():
            val_2 = " / " + sel.data()
            while sel.parent().isValid():
                sel = sel.parent()
                val += sel.data() + val_2 + '\n'

        self.ui.label_2.setText(val)


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
    def __init__(self, toolBox_not, page_number, functions, text='', note=None):
        super().__init__(toolBox_not, page_number)
        self.tb_not = toolBox_not
        self.page_number = page_number
        self.note = note

        self.text_edit_note.setText(text)
        self.save, self.delete, self.attach, self.change = functions
        self.pushButton_save_not.clicked.connect(lambda: self.save(text=self.text_edit_note.toPlainText()))
        # print(self.pushButton_save_not.emit())
        self.pushButton_del_not.clicked.connect(lambda: self.delete(page_number=self.page_number))
        self.pushButton_attach_not.clicked.connect(lambda: self.attach(page_number=self.page_number))
        self.pushButton_change_not.clicked.connect(lambda: self.change(page_number=self.page_number,
                                                                       text=self.text_edit_note.toPlainText()))


class MainWindow(MainForm):
    timer_finished = Signal()

    def __init__(self):
        super().__init__()
        Task.check_overdue()

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
        # потоки для таймера задач
        self.thread_dict = {}
        self.flag_time_task = {}
        self.pushButton_21.clicked.connect(self.open_history_form)
        self.upload_all_tasks_with_data()
        self.lower_bar_buttons()
        self.search_load()
        self.grid_layout_new_task.check_box_repeat.checkStateChanged.connect(self.on_checkbox_state_changed_reply)
        self.replay = None

    def on_checkbox_state_changed_reply(self, state):
        """Изменение состояния чекбокса с заданием повторения задач"""
        if state == Qt.CheckState.Checked:
            dialog = DialogReplay()
            result = dialog.exec()

            self.replay = None
            if result == QDialog.DialogCode.Accepted:
                if not dialog.ui.label_2.text():
                    self.grid_layout_new_task.check_box_repeat.setCheckState(Qt.CheckState.Unchecked)
                    return

                self.grid_layout_new_task.label_repeat.setText(dialog.ui.label_2.text())
                self.replay = dialog.ui.label_2.text().splitlines()

            elif result == QDialog.DialogCode.Rejected:
                self.grid_layout_new_task.check_box_repeat.setCheckState(Qt.CheckState.Unchecked)

        elif state == Qt.CheckState.Unchecked:
            self.grid_layout_new_task.label_repeat.setText('')
            self.grid_layout_new_task.datetime_edit.setVisible(False)

    def search_load(self):
        """Обновляет процесс-бар выполненных задач"""
        if self.done_tasks or self.planned_tasks or self.doing_tasks:
            value = len(self.done_tasks) * 100 / (len(self.planned_tasks) + len(self.doing_tasks) + len(self.done_tasks))
            self.progressBar.setValue(value)

    def lower_bar_buttons(self):
        """Обрабатывает кнопки нижней панели у поставленных задач"""
        self.pushButton_mt_plan_change_task.clicked.connect(lambda: self.change_task(
            push_button=self.pushButton_mt_plan_change_task,
            combobox=self.comboBox_mt_plan_all,
            frame=self.frame_mt_plan,
            grid_layout=self.grid_layout_plan))

        self.pushButton_mt_proc_change_task.clicked.connect(lambda: self.change_task(
            push_button=self.pushButton_mt_proc_change_task,
            combobox=self.comboBox_mt_proc_all,
            frame=self.frame_mt_proc,
            grid_layout=self.grid_layout_proc))

        self.pushButton_mt_plan_del.clicked.connect(lambda: self.del_task(
            combobox=self.comboBox_mt_plan_all,
            func_update=self.upload_planned_task))

        self.pushButton_mt_proc_del_task.clicked.connect(lambda: self.del_task(
            combobox=self.comboBox_mt_proc_all,
            func_update=self.upload_doing_task))

        self.pushButton_mt_done_del_task.clicked.connect(lambda: self.del_task(
            combobox=self.comboBox_mt_done_all,
            func_update=self.upload_done_task))

        self.grid_layout_plan.check_box_add_time.checkStateChanged.connect(lambda: self.on_checkbox_deadline(
            grid_layout=self.grid_layout_plan))

        self.grid_layout_proc.check_box_add_time.checkStateChanged.connect(lambda: self.on_checkbox_deadline(
            grid_layout=self.grid_layout_proc))

        self.pushButton_mt_plan_start.clicked.connect(self.start_task)
        self.pushButton_mt_proc_finish.clicked.connect(self.finish_task)
        self.pushButton_mt_done_recover_task.clicked.connect(self.recover_task)

        self.pushButton_mt_proc_start_timer.clicked.connect(self.start_task_timer)
        self.pushButton_mt_proc_stop_timer.clicked.connect(self.stop_task_timer)
        self.pushButton_mt_proc_rem_timer.clicked.connect(self.remove_task_timer)

    def start_task_timer(self):
        """Запускает таймера задачи"""
        current_task = self.comboBox_mt_proc_all.currentData()
        if not isinstance(current_task.timer, datetime):
            current_task.timer = datetime.now().replace(hour=current_task.timer.hour,
                                                        minute=current_task.timer.minute,
                                                        second=current_task.timer.second)
        self.flag_time_task[current_task.id] = True
        self.thread_dict[current_task.id] = threading.Thread(target=self.timer_task_thread, args=(current_task,), daemon=True)
        self.pushButton_mt_proc_start_timer.setEnabled(False)
        self.pushButton_mt_proc_stop_timer.setEnabled(True)
        self.pushButton_mt_proc_rem_timer.setEnabled(False)
        self.thread_dict[current_task.id].start()

    def timer_task_thread(self, current_task):
        """Запускает поток таймера задачи"""
        while self.flag_time_task[current_task.id]:
            if self.flag_time_task[current_task.id] == False:
                break
            time.sleep(1)
            current_task.timer += timedelta(seconds=1)

            if current_task == self.comboBox_mt_proc_all.currentData():
                self.label_mt_proc_timer.setText(str(current_task.timer.replace(microsecond=0).time()))

    def stop_task_timer(self):
        """Останавливает таймер задачи"""
        current_task = self.comboBox_mt_proc_all.currentData()
        self.pushButton_mt_proc_start_timer.setEnabled(True)
        self.pushButton_mt_proc_stop_timer.setEnabled(False)
        self.pushButton_mt_proc_rem_timer.setEnabled(True)
        self.flag_time_task[current_task.id] = False
        self.thread_dict[current_task.id].join()
        current_task.stop_timer()

    def remove_task_timer(self):
        """Обнуляет таймер работы над задачей"""
        current_task = self.comboBox_mt_proc_all.currentData()
        current_task.remove_timer()
        self.label_mt_proc_timer.setText('00:00:00')

    def finish_task(self):
        """Обрабатывает кнопку окончания работы над задачей"""
        current_task = self.comboBox_mt_proc_all.currentData()
        current_task.change_status(status_id=3)
        self.upload_doing_task()
        self.upload_done_task()

    def start_task(self):
        """Обрабатывает кнопку начала работы над задачей"""
        current_task = self.comboBox_mt_plan_all.currentData()
        current_task.change_status(status_id=2)
        self.upload_planned_task()
        self.upload_doing_task()

    def recover_task(self):
        """Восстановление задачи"""
        current_task = self.comboBox_mt_done_all.currentData()

        ms_box = QDialog()
        ms_box.resize(312, 142)
        verticalLayoutWidget = QWidget(ms_box)
        verticalLayoutWidget.setGeometry(10, 10, 291, 121)
        verticalLayout = QVBoxLayout(verticalLayoutWidget)
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        groupBox = QGroupBox('Куда перенести задачу:', verticalLayoutWidget)
        rad_but_planned = QRadioButton('Запланировано', groupBox)
        rad_but_planned.setChecked(True)
        rad_but_planned.setGeometry(10, 25, 150, 20)
        rad_but_doing = QRadioButton('В процессе', groupBox)
        rad_but_doing.setGeometry(10, 55, 150, 20)
        verticalLayout.addWidget(groupBox)
        buttonBox = QDialogButtonBox(verticalLayoutWidget)
        buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        verticalLayout.addWidget(buttonBox)
        buttonBox.accepted.connect(ms_box.accept)
        buttonBox.rejected.connect(ms_box.reject)

        result = ms_box.exec()
        if result:
            if rad_but_planned.isChecked():
                current_task.change_status(status_id=1)
                self.upload_planned_task()
                self.upload_done_task()
            elif rad_but_doing.isChecked():
                current_task.change_status(status_id=2)
                self.upload_doing_task()
                self.upload_done_task()

    def del_task(self, combobox, func_update):
        """Обрабатывает кнопку удаления задачи"""
        current_task = combobox.currentData()

        msgBox = QMessageBox()
        msgBox.setWindowTitle('Удаление')
        msgBox.setText(f"Задача {current_task.name} будет удалена.")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        msgBox.setButtonText(QMessageBox.StandardButton.Yes, 'Удалить')
        msgBox.setButtonText(QMessageBox.StandardButton.Cancel, 'Отмена')
        result = msgBox.exec()

        if result == QMessageBox.StandardButton.Yes:
            combobox.setCurrentIndex(1)
            current_task.delete_task()
            time.sleep(0.5)
            func_update()
            self.search_load()

    def change_task(self, push_button, combobox, frame, grid_layout):
        """Обрабатывает кнопку изменения задачи"""
        if push_button.text() == 'Сохранить изменения':
            current_task = combobox.currentData()
            self.change_task_button(grid_layout=grid_layout, task=current_task)
            frame.setEnabled(False)
            push_button.setText('Изменить задачу')

        else:
            frame.setEnabled(True)
            push_button.setText('Сохранить изменения')

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
                if deadline > datetime.now():
                    task.overdue = False
                    grid_layout.task_fire_widget.setVisible(False)
                else:
                    task.overdue = True
                    grid_layout.task_fire_widget.setVisible(True)
            else:
                grid_layout.task_fire_widget.setVisible(False)
                task.overdue = False
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

        #  Заполняет форму с задачей при изменении задачи в комбобоксе
        self.comboBox_mt_plan_all.setCurrentIndex(-1)
        self.comboBox_mt_plan_all.currentIndexChanged.connect(lambda: self.upload_data_to_form(
            grid_layout=self.grid_layout_plan,
            combo_box=self.comboBox_mt_plan_all))

        self.comboBox_mt_proc_all.setCurrentIndex(-1)
        self.comboBox_mt_proc_all.currentIndexChanged.connect(lambda: self.upload_data_to_form(
            grid_layout=self.grid_layout_proc,
            combo_box=self.comboBox_mt_proc_all))

        self.comboBox_mt_done_all.setCurrentIndex(-1)
        self.comboBox_mt_done_all.currentIndexChanged.connect(lambda: self.upload_data_to_form(
            grid_layout=self.grid_layout_done,
            combo_box=self.comboBox_mt_done_all))

    def upload_data_to_form(self, grid_layout, combo_box):
        """Подставляет данные выбранной задачи в чекбоксе"""
        current_task = combo_box.currentData()

        # изменяет видимость всех полей
        if grid_layout == self.grid_layout_plan:
            self.change_visible_planned()

        elif grid_layout == self.grid_layout_proc:
            self.groupBox_mt_proc_timer.setEnabled(True)
            if isinstance(current_task.timer, datetime):
                current_time = str(current_task.timer.replace(microsecond=0).time())
            else:
                current_time = str(current_task.timer)
            if self.flag_time_task.get(current_task.id):
                self.pushButton_mt_proc_rem_timer.setEnabled(False)
                self.pushButton_mt_proc_stop_timer.setEnabled(True)
                self.pushButton_mt_proc_start_timer.setEnabled(False)
            else:
                self.pushButton_mt_proc_rem_timer.setEnabled(True)
                self.pushButton_mt_proc_stop_timer.setEnabled(False)
                self.pushButton_mt_proc_start_timer.setEnabled(True)
            self.label_mt_proc_timer.setText(current_time)
            self.change_visible_doing()

        else:
            self.pushButton_mt_done_del_task.setEnabled(True)
            self.pushButton_mt_done_recover_task.setEnabled(True)
            self.label_mt_done_timer.setText(str(current_task.timer.replace(microsecond=0).time()))
            if current_task.overdue:
                grid_layout.label_task_fire.setVisible(True)

        grid_layout.line_edit_name.setText(current_task.name)
        grid_layout.combo_box_prior.setCurrentIndex(current_task.priority - 1)
        grid_layout.combo_box_category.setCurrentIndex(current_task.category - 1)
        grid_layout.text_edit_description.setText(current_task.description)

        # проверяем, есь и у текущей задачи deadline
        if current_task.deadline:

            grid_layout.check_box_add_time.setChecked(True)
            if isinstance(current_task.deadline, str):
                date = datetime.strptime(current_task.deadline, "%Y-%m-%d %H:%M:%S")
                grid_layout.datetime_edit.setDateTime(date)
            else:
                grid_layout.datetime_edit.setDateTime(current_task.deadline)
            grid_layout.datetime_edit.setVisible(True)

            if current_task.overdue:
                grid_layout.task_fire_widget.setVisible(True)

        else:
            grid_layout.check_box_add_time.setChecked(False)
            grid_layout.task_fire_widget.setVisible(False)

    def on_checkbox_deadline(self, grid_layout):
        """Изменение состояния чекбокса с заданием дедлайна"""
        state = grid_layout.check_box_add_time.checkState()
        if state == Qt.CheckState.Checked:
            if grid_layout.datetime_edit.text() == '01.01.2000 0:00':
                grid_layout.datetime_edit.setDateTime(datetime.now())
            grid_layout.datetime_edit.setVisible(True)
        elif state == Qt.CheckState.Unchecked:
            grid_layout.datetime_edit.setVisible(False)

    def change_visible_planned(self):
        self.pushButton_mt_plan_change_task.setEnabled(True)
        self.frame_mt_plan.setEnabled(False)
        self.pushButton_mt_plan_start.setEnabled(True)
        self.pushButton_mt_plan_del.setEnabled(True)
        self.pushButton_mt_plan_change_task.setText('Изменить задачу')

    def change_visible_doing(self):
        self.pushButton_mt_proc_change_task.setEnabled(True)
        self.frame_mt_plan.setEnabled(False)
        self.pushButton_mt_proc_finish.setEnabled(True)
        self.pushButton_mt_proc_del_task.setEnabled(True)
        self.pushButton_mt_proc_change_task.setText('Изменить задачу')

    def upload_planned_task(self):
        """Загружает все запланированные задачи в комбобокс"""
        self.planned_tasks = Task.download_planned_tasks()

        # Отключает обработку сигналов перед очищением комбобокса
        self.comboBox_mt_plan_all.blockSignals(True)
        self.comboBox_mt_plan_all.clear()
        self.comboBox_mt_plan_all.blockSignals(False)

        if not self.planned_tasks:
            self.pushButton_mt_plan_change_task.setEnabled(False)
            self.pushButton_mt_plan_start.setEnabled(False)
            self.pushButton_mt_plan_del.setEnabled(False)

        for task in self.planned_tasks:
            self.comboBox_mt_plan_all.addItem(task.name, task)

    def upload_doing_task(self):
        """Загружает все выполняемые задачи в комбобокс"""
        self.doing_tasks = Task.download_doing_tasks()

        self.comboBox_mt_proc_all.blockSignals(True)
        self.comboBox_mt_proc_all.clear()
        self.comboBox_mt_proc_all.blockSignals(False)

        if not self.doing_tasks:
            self.pushButton_mt_proc_change_task.setEnabled(False)
            self.pushButton_mt_proc_finish.setEnabled(False)
            self.pushButton_mt_proc_del_task.setEnabled(False)
            self.groupBox_mt_proc_timer.setEnabled(False)

        for task in self.doing_tasks:
            self.comboBox_mt_proc_all.addItem(task.name, task)

    def upload_done_task(self):
        """Загружает все выполненные задачи в комбобокс"""
        self.done_tasks = Task.download_done_tasks()

        self.comboBox_mt_done_all.blockSignals(True)
        self.comboBox_mt_done_all.clear()
        self.comboBox_mt_done_all.blockSignals(False)

        if not self.done_tasks:
            self.pushButton_mt_done_recover_task.setEnabled(False)
            self.pushButton_mt_done_del_task.setEnabled(False)

        for task in self.done_tasks:
            self.comboBox_mt_done_all.addItem(task.name, task)

        self.search_load()

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
            priority = self.grid_layout_new_task.combo_box_prior.currentIndex() + 1
            category = self.grid_layout_new_task.combo_box_category.currentIndex() + 1
            descrirton = self.grid_layout_new_task.text_edit_description.toPlainText()

            if self.grid_layout_new_task.check_box_add_time.checkState() == Qt.CheckState.Checked:
                deadline = self.grid_layout_new_task.datetime_edit.dateTime()
                deadline = deadline.toPython()
            else:
                deadline = None

            recording_result = save_task(name, priority, category, descrirton, deadline)

            if isinstance(recording_result, psycopg2.errors.UniqueViolation):
                QMessageBox.warning(self, "Ошибка", "Задача с таким именем уже есть.")

            elif recording_result:
                if self.replay:
                    for repl in self.replay:
                        add_new_repeat(recording_result, repl)

                self.upload_planned_task()
                self.search_load()
                QMessageBox.about(self, 'Успех', f'задача {name} сохранена')



# __________________ TotalTimer_______________________________
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
        """Обрабатывает кнопку остановки таймера"""
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

# __________________ Note_______________________________

    def download_note(self):
        """Выгружает заметки из бд"""
        self.functions_for_note = (self.save_note, self.del_note, self.attache_note, self.change_note)

        all_notes = download_noticed_from_db()
        index = 0
        self.notes = {}

        for note in all_notes:
            index += 1
            self.notes[index] = NoteTask(self.toolBox_not, index, self.functions_for_note, text=note[1],
                                         note=No(id=note[0], text=note[1]))
            if note[2]:
                self.dockWidget_notice.setVisible(True)
                self.label_atached_note.setText(f"{self.notes[index].note.text}")

            self.notes[index].pushButton_del_not.setEnabled(True)
            self.notes[index].pushButton_attach_not.setEnabled(True)
            self.notes[index].pushButton_change_not.setEnabled(True)
            self.notes[index].pushButton_save_not.setEnabled(False)

        self.notes[index + 1] = NoteTask(self.toolBox_not, index + 1, self.functions_for_note)

    def save_note(self, text):
        """Сохраняет заметки"""
        page_number = max(self.notes)
        note = save_note_to_db(text)

        self.notes[page_number].note = note
        self.notes[page_number + 1] = NoteTask(self.toolBox_not, page_number + 1, self.functions_for_note)

        self.notes[page_number].pushButton_del_not.setEnabled(True)
        self.notes[page_number].pushButton_attach_not.setEnabled(True)
        self.notes[page_number].pushButton_change_not.setEnabled(True)
        self.notes[page_number].pushButton_save_not.setEnabled(False)

    def del_note(self, page_number):
        """Удаляет заметки"""
        self.notes[page_number].note.delete_note()
        self.toolBox_not.removeItem(self.toolBox_not.currentIndex())
        self.notes.pop(page_number)

    def attache_note(self, page_number):
        """Прикрепляет заметку справа"""
        self.dockWidget_notice.setVisible(True)
        self.label_atached_note.setText(f"{self.notes[page_number].note.text}")
        self.notes[page_number].note.attach_note()

    def change_note(self, page_number, text):
        self.notes[page_number].note.change_note(text=text)
