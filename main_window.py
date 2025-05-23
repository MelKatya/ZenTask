import time
from typing import Tuple, Optional, Callable, Any

from PySide6.QtWidgets import (QWidget, QDialog, QMessageBox, QDialogButtonBox, QVBoxLayout, QLabel,
                               QRadioButton, QGroupBox, QComboBox, QToolBox)

from forms.ui_main_form import MainForm, Note
from forms.ui_add_category import NewCategory
from forms.ui_add_timer import AddTimer
from forms.ui_show_history import ShowTimers
from forms.ui_add_replay import AddReplay
from utils import (upload_priority, upload_category, save_new_category, save_task, save_timer,
                   stop_timer, show_history_time, save_note_to_db, add_new_repeat, return_task, load_stylesheet)

from PySide6.QtCore import Signal, Qt
from psycopg2 import errors
import psycopg2
from datetime import datetime, timedelta
import threading
from database import Note as No, Task, TaskRepeat


class DialogReplay(QDialog):
    """
    Диалоговое окно для выбора повтора задачи.
    """
    def __init__(self):
        super().__init__()

        self.setStyleSheet(load_stylesheet())

        self.ui = AddReplay()
        self.ui.setup_ui(self)

        self.ui.tree_view.itemClicked.connect(self.the_button_was_clicked)

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def the_button_was_clicked(self) -> None:
        """
        Обрабатывает нажатие на элемент в дереве.
        """
        val = ''

        for sel in self.ui.tree_view.selectedIndexes():
            val_2 = " / " + sel.data()

            while sel.parent().isValid():
                sel = sel.parent()
                val += sel.data() + val_2 + '\n'

        self.ui.label_2.setText(val)


class DialogCategory(QDialog):
    """
    Диалоговое окно для создания новой категории.
    """
    def __init__(self):
        super().__init__()

        self.setStyleSheet(load_stylesheet())

        self.ui = NewCategory()
        self.ui.setup_ui(self)

        self.ui.buttonBox.accepted.connect(self.the_button_was_clicked)
        # self.buttonBox.accepted.connect(Dialog.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def the_button_was_clicked(self) -> None:
        """
        Обрабатывает кнопку сохранения новой категории.
        Если ввод пустой — показывает предупреждение.
        """
        user_input = self.ui.lineEdit.text()

        if user_input:
            QMessageBox.about(self, 'Успех', f'Категория {user_input} сохранена')
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Необходимо ввести новую категорию.")


class DialogTimer(QDialog):
    """
    Диалоговое окно для установки общего таймера работы.
    Показывает предполагаемое время окончания таймера на основе введенного времени.
    """
    def __init__(self):
        super().__init__()

        self.setStyleSheet(load_stylesheet())

        self.ui = AddTimer()
        self.ui.setup_ui(self)

        self.id_timer = None
        self.ui.timeEdit.timeChanged.connect(self.change_time)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def change_time(self) -> None:
        """
        Обновляет отображение времени завершения таймера
        при изменении пользователем длительности в timeEdit.
        """
        start = datetime.now()
        data = self.ui.timeEdit.text().split(':')
        th1, tm1 = map(int, data)
        res = (start + timedelta(hours=th1, minutes=tm1))
        self.ui.label_3.setText(str(res.strftime('%m.%d в %H:%M')))


class NoteTask(Note):
    """Класс для отображения заметок.

    Args:
        toolBox_not (QToolBox): Виджет QToolBox, к которому прикреплена заметка.
        page_number (int): Номер страницы в QToolBox.
        functions (Tuple[Callable, Callable, Callable, Callable]):
            Кортеж из четырёх функций: (save, delete, attach, change).
        text (str, optional): Начальный текст заметки.
        note (No, optional): Объект заметки, если уже существует.
    """
    def __init__(self, toolBox_not: QToolBox, page_number: int,
                 functions: Tuple[Callable, Callable, Callable, Callable],
                 text: str = '', note: Optional[No] = None) -> None:

        super().__init__(toolBox_not, page_number)
        self.tb_not = toolBox_not
        self.page_number = page_number
        self.note = note

        self.text_edit_note.setText(text)
        self.save, self.delete, self.attach, self.change = functions

        # Подключение кнопок к функциям
        self.pushButton_save_not.clicked.connect(lambda: self.save(text=self.text_edit_note.toPlainText()))
        self.pushButton_del_not.clicked.connect(lambda: self.delete(page_number=self.page_number))
        self.pushButton_attach_not.clicked.connect(lambda: self.attach(page_number=self.page_number))
        self.pushButton_change_not.clicked.connect(lambda: self.change(page_number=self.page_number,
                                                                       text=self.text_edit_note.toPlainText()))


class MainWindow(MainForm):
    """
    Основная форма приложения. Управляет логикой задач, заметок, категорий, таймеров и интерфейсом.
    """
    timer_finished = Signal()

    def __init__(self):
        super().__init__()
        # проверка просроченных задач и загрузка повторяемых
        Task.check_overdue()
        return_task()

        # потоки и флаги для таймера задач
        self.thread_dict = {}
        self.flag_time_task = {}

        # первоначальное состояние статуса чекбокса для повтора
        self.last_check = Qt.CheckState.Unchecked
        # изначально нет повтора у задач
        self.replay = None

        # Загрузка данных из базы данных
        self.download_note()
        self.upload_priority()
        self.upload_category()
        self.upload_all_tasks_with_data()
        self.search_load()

        # Инициализация кнопок и обработчиков
        self.total_timer_buttons()
        self.new_task_buttons()
        self.change_page_buttons()
        self.lower_bar_buttons()

    def search_load(self) -> None:
        """
        Обновляет прогресс-бар выполненных задач,
        рассчитывая процент завершенных относительно общего количества.
        """
        if self.done_tasks or self.planned_tasks or self.doing_tasks:
            value = (len(self.done_tasks) * 100 / (len(self.planned_tasks) +
                                                   len(self.doing_tasks) + len(self.done_tasks)))
            self.progressBar.setValue(value)

    def open_category_form(self) -> None:
        """
        Открывает диалоговое окно добавления новой категории.
        """
        dialog = DialogCategory()

        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            new_category_name = dialog.ui.lineEdit.text()
            save_new_category(new_category_name)
            self.upload_category()

    def upload_all_tasks_with_data(self) -> None:
        """
        Загружает задачи всех состояний (запланированные, выполняемые, выполненные) и
        подключает обработчики событий на изменение выбора и состояния чекбоксов.
        """
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

        self.grid_layout_plan.check_box_repeat.checkStateChanged.connect(lambda: self.on_checkbox_state_changed_reply(
            grid_layout=self.grid_layout_plan))

        self.grid_layout_proc.check_box_repeat.checkStateChanged.connect(lambda: self.on_checkbox_state_changed_reply(
            grid_layout=self.grid_layout_proc))

    def upload_data_to_form(self, grid_layout: Any, combo_box: QComboBox) -> None:
        """
        Подставляет данные выбранной задачи в поля формы.
        """
        current_task = combo_box.currentData()

        # изменяет отображение в зависимости от типа задачи
        if grid_layout == self.grid_layout_plan:
            self.change_visible_planned()

        elif grid_layout == self.grid_layout_proc:
            self.change_visible_proc(current_task)

        else:
            self.change_visible_doing(current_task, grid_layout)

        grid_layout.line_edit_name.setText(current_task.name)
        grid_layout.combo_box_prior.setCurrentIndex(current_task.priority - 1)
        grid_layout.combo_box_category.setCurrentIndex(current_task.category - 1)
        grid_layout.text_edit_description.setText(current_task.description)

        # обработка дедлайна
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

        # обработка повторений
        if current_task.repeats:
            self.last_check = Qt.CheckState.Checked
            grid_layout.check_box_repeat.setChecked(True)
            repeat_text = '\n'.join((f'{rep[0]} / {rep[1]}' for rep in current_task.repeats))
            grid_layout.label_repeat.setText(repeat_text)

        else:
            self.last_check = Qt.CheckState.Unchecked
            grid_layout.check_box_repeat.setChecked(False)
            grid_layout.label_repeat.setText('')

    def change_visible_planned(self) -> None:
        """
        Изменяет видимость полей и кнопок у запланированных задач.
        """
        self.pushButton_mt_plan_change_task.setEnabled(True)
        self.frame_mt_plan.setEnabled(False)
        self.pushButton_mt_plan_start.setEnabled(True)
        self.pushButton_mt_plan_del.setEnabled(True)
        self.pushButton_mt_plan_change_task.setText('Изменить задачу')

    def change_visible_proc(self, current_task: Task) -> None:
        """
        Изменяет видимость полей и кнопок у выполняемых задач.
        """
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
        self.pushButton_mt_proc_change_task.setEnabled(True)
        self.frame_mt_plan.setEnabled(False)
        self.pushButton_mt_proc_finish.setEnabled(True)
        self.pushButton_mt_proc_del_task.setEnabled(True)
        self.pushButton_mt_proc_change_task.setText('Изменить задачу')

    def change_visible_doing(self, current_task: Task, grid_layout: Any) -> None:
        """
        Изменяет видимость полей и кнопок у выполненных задач.
        """
        self.pushButton_mt_done_del_task.setEnabled(True)
        self.pushButton_mt_done_recover_task.setEnabled(True)
        self.label_mt_done_timer.setText(str(current_task.timer.replace(microsecond=0).time()))
        if current_task.overdue:
            grid_layout.label_task_fire.setVisible(True)

    def on_checkbox_state_changed_reply(self, grid_layout: Any) -> None:
        """
        Реакция на изменение состояния чекбокса повтора задач.
        """
        state = grid_layout.check_box_repeat.checkState()
        if state == Qt.CheckState.Checked and grid_layout.check_box_repeat.checkState() != self.last_check:
            self.last_check = Qt.CheckState.Checked
            dialog = DialogReplay()
            result = dialog.exec()

            self.replay = None
            if result == QDialog.DialogCode.Accepted:
                if not dialog.ui.label_2.text():
                    grid_layout.check_box_repeat.setCheckState(Qt.CheckState.Unchecked)
                    return

                grid_layout.label_repeat.setText(dialog.ui.label_2.text())
                self.replay = dialog.ui.label_2.text().splitlines()

            elif result == QDialog.DialogCode.Rejected:
                grid_layout.check_box_repeat.setCheckState(Qt.CheckState.Unchecked)

        elif state == Qt.CheckState.Unchecked:
            self.last_check = Qt.CheckState.Unchecked
            grid_layout.label_repeat.setText('')
            grid_layout.datetime_edit.setVisible(False)

    def on_checkbox_deadline(self, grid_layout: Any) -> None:
        """
        Реакция на изменение чекбокса дедлайна.
        """
        state = grid_layout.check_box_add_time.checkState()
        if state == Qt.CheckState.Checked:
            if grid_layout.datetime_edit.text() == '01.01.2000 0:00':
                grid_layout.datetime_edit.setDateTime(datetime.now())
            grid_layout.datetime_edit.setVisible(True)
        elif state == Qt.CheckState.Unchecked:
            grid_layout.datetime_edit.setVisible(False)

# ___________________New_Task_____________________________
    def new_task_buttons(self) -> None:
        """
        Настраивает кнопки и чекбоксы формы создания задачи (связывает с обработчиками событий).
        """
        self.grid_layout_new_task.push_button_new_cat.clicked.connect(self.open_category_form)
        self.pushButton_nt_create_task.clicked.connect(self.save_task_button)
        self.grid_layout_new_task.check_box_add_time.checkStateChanged.connect(lambda: self.on_checkbox_deadline(
            grid_layout=self.grid_layout_new_task))
        self.grid_layout_new_task.check_box_repeat.checkStateChanged.connect(lambda:
                                                                             self.on_checkbox_state_changed_reply(
                                                                                 grid_layout=self.grid_layout_new_task))

    def save_task_button(self) -> None:
        """
        Создает новую задачу на основе данных из формы, сохраняет ее в базу и показывает результат.
        """

        if not self.grid_layout_new_task.line_edit_name.text():
            QMessageBox.warning(self, "Ошибка", "Необходимо ввести название задачи.")
            return

        if not self.grid_layout_new_task.text_edit_description.toPlainText():
            QMessageBox.warning(self, "Ошибка", "Необходимо ввести описание задачи.")
            return

        name = self.grid_layout_new_task.line_edit_name.text()
        priority = self.grid_layout_new_task.combo_box_prior.currentIndex() + 1
        category = self.grid_layout_new_task.combo_box_category.currentIndex() + 1
        description = self.grid_layout_new_task.text_edit_description.toPlainText()

        if self.grid_layout_new_task.check_box_add_time.checkState() == Qt.CheckState.Checked:
            deadline = self.grid_layout_new_task.datetime_edit.dateTime()
            deadline = deadline.toPython()
        else:
            deadline = None

        recording_result = save_task(name, priority, category, description, deadline)

        if isinstance(recording_result, psycopg2.errors.UniqueViolation):
            QMessageBox.warning(self, "Ошибка", "Задача с таким именем уже есть.")

        elif recording_result:
            if self.replay:
                for repl in self.replay:
                    add_new_repeat(recording_result, repl)

            self.upload_planned_task()
            self.search_load()
            QMessageBox.about(self, 'Успех', f'задача {name} сохранена')

    def change_page_buttons(self) -> None:
        """
        Настраивает переходы между страницами интерфейса по кнопкам.
        """
        self.pushButton_nt_my_task.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_nt_not.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        self.pushButton_mt_not.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButton_mt_crete_task.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        self.pushButton_cret_tsk_not.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_my_task_not.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

# ___________________Upload_data_____________________________
    def upload_planned_task(self) -> None:
        """
        Загружает задачи со статусом "Запланировано" в комбобокс и обновляет состояние кнопок.
        """
        self.planned_tasks = Task.download_tasks_by_status(status_id=1)

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

    def upload_doing_task(self) -> None:
        """
        Загружает задачи со статусом "Выполняется" в комбобокс и обновляет интерфейс.
        """
        self.doing_tasks = Task.download_tasks_by_status(status_id=2)

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

    def upload_done_task(self) -> None:
        """
        Загружает задачи со статусом "Выполнено" в комбобокс, обновляет кнопки и вызывает обновление поиска.
        """
        self.done_tasks = Task.download_tasks_by_status(status_id=3)

        self.comboBox_mt_done_all.blockSignals(True)
        self.comboBox_mt_done_all.clear()
        self.comboBox_mt_done_all.blockSignals(False)

        if not self.done_tasks:
            self.pushButton_mt_done_recover_task.setEnabled(False)
            self.pushButton_mt_done_del_task.setEnabled(False)

        for task in self.done_tasks:
            self.comboBox_mt_done_all.addItem(task.name, task)

        self.search_load()

    def upload_category(self) -> None:
        """
        Загружает список категорий из базы данных во все комбобоксы категорий.
        """
        upload_category(self.grid_layout_new_task.combo_box_category)

        upload_category(self.grid_layout_plan.combo_box_category)

        upload_category(self.grid_layout_proc.combo_box_category)

        upload_category(self.grid_layout_done.combo_box_category)

    def upload_priority(self) -> None:
        """
        Загружает список приоритетов из базы данных во все комбобоксы приоритета.
        """
        upload_priority(self.grid_layout_new_task.combo_box_prior)

        upload_priority(self.grid_layout_plan.combo_box_prior)

        upload_priority(self.grid_layout_proc.combo_box_prior)

        upload_priority(self.grid_layout_done.combo_box_prior)

# ___________________TotalTimer_______________________________
    def total_timer_buttons(self) -> None:
        """
        Подключает обработчики событий для общего таймера: запуск, остановка и история.
        """
        self.pushButton_set_timer.clicked.connect(self.open_timer_form)
        self.pushButton_stop_timer.clicked.connect(self.stop_timer)
        self.pushButton_stop_timer.setEnabled(False)
        self.pushButton_21.clicked.connect(self.open_history_form)
        self.timer_finished.connect(self.finsh_timer)

    def open_timer_form(self) -> None:
        """
        Открывает диалоговое окно для создания таймера.
        При подтверждении запускает таймер в отдельном потоке.
        """
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
                self.pushButton_set_timer.setEnabled(False)
                self.run_time = True
                self.pushButton_stop_timer.setEnabled(True)
                self.thread_timer = threading.Thread(target=self.strat_timer,
                                                     args=(self.label_main_timer_passed,
                                                           self.label_main_timer_last, time_1), daemon=True)
                self.thread_timer.start()

    def strat_timer(self, label_passed: QLabel, label_last: QLabel, timer: datetime) -> None:
        """
        Цикл работы таймера: обновляет оставшееся и прошедшее время каждую минуту.
        Работает в отдельном потоке. Завершается по окончании времени или остановке вручную.
        """
        pass_time = timer.strftime('%H:%M')
        self.rest_time = datetime.now().replace(hour=0, minute=0, second=0)

        while pass_time != '00:00' and self.run_time:
            for sec in range(30):
                time.sleep(2)
                if self.run_time == False:
                    break
            else:
                timer -= timedelta(minutes=1)
                self.rest_time += timedelta(minutes=1)
                pass_time = timer.strftime('%H:%M')
                label_last.setText(pass_time)
                label_passed.setText(self.rest_time.strftime('%H:%M'))

        self.timer_finished.emit()

    def finsh_timer(self) -> None:
        """
        Обновляет интерфейс после завершения таймера, сохраняет результат и уведомляет пользователя.
        """
        stop_timer(self.total_timer, self.rest_time)
        self.pushButton_set_timer.setEnabled(True)
        self.pushButton_stop_timer.setEnabled(False)
        QMessageBox.about(self, 'Таймер', f'Таймер закончил работу')

    def stop_timer(self) -> None:
        """
        Останавливает таймер, завершая поток.
        """
        self.run_time = False
        self.thread_timer.join()

    def open_history_form(self) -> None:
        """
        Открывает окно с историей использования таймера и общим временем.
        Загружает данные из базы и отображает их в таблице.
        """
        dialog = QDialog()
        dialog.setStyleSheet(self.style)
        ui = ShowTimers()
        ui.setup_ui(dialog)
        total_time, result = show_history_time()
        ui.label_2.setText(str(total_time))

        for timer_data in result:
            ui.add_row(timer_data)

        dialog.exec()

# ___________________Task buttons_______________________________
    def lower_bar_buttons(self) -> None:
        """
        Устанавливает обработчики для кнопок управления задачами на нижней панели:
        изменение, удаление, запуск, завершение, восстановление и таймер.
        """
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

    def finish_task(self) -> None:
        """
        Устанавливает обработчик для кнопки окончания работы над задачей.
        """
        current_task = self.comboBox_mt_proc_all.currentData()
        current_task.change_status(status_id=3)
        self.upload_doing_task()
        self.upload_done_task()

    def start_task(self) -> None:
        """
        Устанавливает обработчик для кнопки начала работы над задачей.
        """
        current_task = self.comboBox_mt_plan_all.currentData()
        current_task.change_status(status_id=2)
        self.upload_planned_task()
        self.upload_doing_task()

    def recover_task(self) -> None:
        """
        Восстанавливает задачу.
        """
        current_task = self.comboBox_mt_done_all.currentData()

        ms_box = QDialog()
        ms_box.setStyleSheet(self.style)
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
        buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText("ОК")
        buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText("Отмена")

        verticalLayout.addWidget(buttonBox)
        buttonBox.accepted.connect(ms_box.accept)
        buttonBox.rejected.connect(ms_box.reject)

        result = ms_box.exec()
        if result:
            if rad_but_planned.isChecked():
                current_task.change_status(status_id=1)
                self.upload_planned_task()
                self.upload_done_task()
            else:
                current_task.change_status(status_id=2)
                self.upload_doing_task()
                self.upload_done_task()

    def del_task(self, combobox: QComboBox, func_update: Callable) -> None:
        """
        Устанавливает обработчик для кнопки удаления задачи.
        """
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
            func_update()
            self.search_load()

    def change_task(self, push_button: Any, combobox: Any, frame, grid_layout) -> None:
        """
        Устанавливает обработчик для кнопки изменения задачи.
        """
        if push_button.text() == 'Сохранить изменения':
            current_task = combobox.currentData()
            self.change_task_button(grid_layout=grid_layout, task=current_task)
            frame.setEnabled(False)
            push_button.setText('Изменить задачу')

        else:
            frame.setEnabled(True)
            push_button.setText('Сохранить изменения')

    def change_task_button(self, grid_layout, task: Task) -> None:
        """
        Изменяет данные задачи по введенным пользователем значениям и сохраняет изменения.
        Также обрабатывает дедлайн и параметры повторений.
        """
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

            if self.replay:
                self.last_check = Qt.CheckState.Checked
                for repl in self.replay:
                    add_new_repeat(task.id, repl)
            else:
                self.last_check=Qt.CheckState.Unchecked
                TaskRepeat.del_repeat(task_id=task.id)
                grid_layout.label_repeat.setText('')

            if result:
                QMessageBox.about(self, 'Успех', f'Задача {task.name} изменена')
            else:
                QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {result}")

# ___________________Task timer_______________________________
    def start_task_timer(self) -> None:
        """
        Запускает таймер для выбранной задачи и запускает отдельный поток отсчета времени.
        """
        current_task = self.comboBox_mt_proc_all.currentData()
        if not isinstance(current_task.timer, datetime):
            current_task.timer = datetime.now().replace(hour=current_task.timer.hour,
                                                        minute=current_task.timer.minute,
                                                        second=current_task.timer.second)
        self.flag_time_task[current_task.id] = True
        self.thread_dict[current_task.id] = threading.Thread(target=self.timer_task_thread,
                                                             args=(current_task,),
                                                             daemon=True)
        self.pushButton_mt_proc_start_timer.setEnabled(False)
        self.pushButton_mt_proc_stop_timer.setEnabled(True)
        self.pushButton_mt_proc_rem_timer.setEnabled(False)
        self.thread_dict[current_task.id].start()

    def timer_task_thread(self, current_task: Task) -> None:
        """
        Цикл, увеличивающий таймер задачи на секунду каждую секунду.
        Обновляет отображение таймера, если задача выбрана.
        """
        while self.flag_time_task[current_task.id]:
            time.sleep(1)
            current_task.timer += timedelta(seconds=1)

            if current_task == self.comboBox_mt_proc_all.currentData():
                self.label_mt_proc_timer.setText(str(current_task.timer.replace(microsecond=0).time()))

    def stop_task_timer(self) -> None:
        """
        Останавливает таймер задачи.
        """
        current_task = self.comboBox_mt_proc_all.currentData()

        self.pushButton_mt_proc_start_timer.setEnabled(True)
        self.pushButton_mt_proc_stop_timer.setEnabled(False)
        self.pushButton_mt_proc_rem_timer.setEnabled(True)
        self.flag_time_task[current_task.id] = False

        self.thread_dict[current_task.id].join()
        current_task.stop_timer()

    def remove_task_timer(self) -> None:
        """
        Обнуляет таймер работы над задачей.
        """
        current_task = self.comboBox_mt_proc_all.currentData()
        current_task.remove_timer()
        self.label_mt_proc_timer.setText('00:00:00')

# __________________ Note_______________________________

    def download_note(self) -> None:
        """
        Загружает заметки из базы данных, создает элементы NoteTask и
        отображает прикреплённую заметку, если она есть.
        """
        self.functions_for_note = (self.save_note, self.del_note, self.attache_note, self.change_note)

        all_notes = No.download_notes()
        self.notes = {}

        index = 0
        for note in all_notes:
            index += 1
            self.notes[index] = NoteTask(self.toolBox_not, index, self.functions_for_note, text=note[1],
                                         note=No(id_note=note[0], text=note[1]))
            if note[2]:
                self.dockWidget_notice.setVisible(True)
                self.label_atached_note.setText(f"{self.notes[index].note.text}")

            self.notes[index].pushButton_del_not.setEnabled(True)
            self.notes[index].pushButton_attach_not.setEnabled(True)
            self.notes[index].pushButton_change_not.setEnabled(True)
            self.notes[index].pushButton_save_not.setEnabled(False)

        self.notes[index + 1] = NoteTask(self.toolBox_not, index + 1, self.functions_for_note)

    def save_note(self, text: str) -> None:
        """
        Сохраняет заметку в базу данных и добавляет ее в интерфейс.
        """
        page_number = max(self.notes)
        note = save_note_to_db(text)

        self.notes[page_number].note = note
        self.notes[page_number + 1] = NoteTask(self.toolBox_not, page_number + 1, self.functions_for_note)

        self.notes[page_number].pushButton_del_not.setEnabled(True)
        self.notes[page_number].pushButton_attach_not.setEnabled(True)
        self.notes[page_number].pushButton_change_not.setEnabled(True)
        self.notes[page_number].pushButton_save_not.setEnabled(False)

    def del_note(self, page_number: int) -> None:
        """
        Удаляет заметку.
        """
        self.notes[page_number].note.delete_note()
        self.toolBox_not.removeItem(self.toolBox_not.currentIndex())
        self.notes.pop(page_number)

    def attache_note(self, page_number: int) -> None:
        """
        Прикрепляет заметку справа.
        """
        self.dockWidget_notice.setVisible(True)
        self.label_atached_note.setText(f"{self.notes[page_number].note.text}")
        self.notes[page_number].note.attach_note()

    def change_note(self, page_number: int, text: str) -> None:
        """
        Изменяет заметку.
        """
        self.notes[page_number].note.edit_note(text=text)
