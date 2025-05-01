from PySide6.QtWidgets import QApplication, QWidget, QDialog, QMainWindow
from PySide6.QtCore import QCoreApplication, QRect, QSize, Qt
from PySide6.QtGui import QCursor, QFont
from PySide6.QtWidgets import (QCalendarWidget, QCheckBox, QComboBox,
    QDateTimeEdit, QDockWidget, QFormLayout, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QTabWidget,
    QTextBrowser, QTextEdit, QToolBox, QVBoxLayout,
    QWidget)


class Base(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.style = None
        with open("forms/style.css", "r") as f:
            self.style = f.read()

        self.setStyleSheet(self.style)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Название
        self.label_2 = QLabel('Название:', self)
        self.layout.addWidget(self.label_2, 0, 0, 1, 1)

        self.line_edit_name = QLineEdit(self)
        self.layout.addWidget(self.line_edit_name, 0, 1, 1, 1)

        # Описание
        self.verticalLayout_3 = QVBoxLayout()

        self.label_4 = QLabel('Описание:', self)
        self.verticalLayout_3.addWidget(self.label_4)

        self.verticalSpacer = QSpacerItem(20, 105)
        self.verticalLayout_3.addItem(self.verticalSpacer)
        self.layout.addLayout(self.verticalLayout_3, 3, 0, 1, 1)

        self.text_edit_description = QTextEdit(self)
        self.text_edit_description.setMaximumSize(QSize(499, 110))
        self.layout.addWidget(self.text_edit_description, 3, 1, 1, 1)

        self.adding_deadline()
        self.adding_replay()
        self.category()
        self.priority()
        self.overdue_task()

    def category(self):
        self.label = QLabel('Категория:', self)
        self.layout.addWidget(self.label, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.combo_box_category = QComboBox(self)
        self.combo_box_category.setEnabled(True)
        self.horizontalLayout.addWidget(self.combo_box_category)

        self.horizontalSpacer = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.layout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.push_button_new_cat = QPushButton('Новая категория', self)
        self.push_button_new_cat.setMaximumSize(QSize(120, 16777215))
        self.horizontalLayout.addWidget(self.push_button_new_cat)

    def priority(self):
        self.label_3 = QLabel('Приоритет:', self)
        self.layout.addWidget(self.label_3, 1, 0, 1, 1)

        self.combo_box_prior = QComboBox(self)
        self.layout.addWidget(self.combo_box_prior, 1, 1, 1, 1)

    def adding_deadline(self):
        self.horizontalLayout_50 = QHBoxLayout()

        self.datetime_edit = QDateTimeEdit(self)
        self.datetime_edit.setVisible(False)
        self.datetime_edit.setMinimumSize(QSize(150, 0))
        self.horizontalLayout_50.addWidget(self.datetime_edit)

        self.horizontalSpacer_34 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_50.addItem(self.horizontalSpacer_34)
        self.layout.addLayout(self.horizontalLayout_50, 4, 1, 1, 1)

        self.check_box_add_time = QCheckBox('Добавить срок', self)
        self.check_box_add_time.setMinimumSize(QSize(137, 25))
        self.horizontalLayout_50.addWidget(self.check_box_add_time)

    def adding_replay(self):
        self.horizontalLayout_53 = QHBoxLayout()

        self.label_repeat = QLabel("TextLabel", self)
        self.label_repeat.setEnabled(False)
        self.label_repeat.setMinimumSize(QSize(150, 0))
        self.horizontalLayout_53.addWidget(self.label_repeat)

        self.horizontalSpacer_37 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_53.addItem(self.horizontalSpacer_37)

        self.check_box_repeat = QCheckBox('Повторяемая задача', self)
        self.check_box_repeat.setMinimumSize(QSize(137, 0))
        self.horizontalLayout_53.addWidget(self.check_box_repeat)

        self.layout.addLayout(self.horizontalLayout_53, 5, 1, 1, 1)

    def overdue_task(self):
        self.task_fire_widget = QWidget(self)
        self.horizontalLayout_17 = QHBoxLayout(self.task_fire_widget)
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_17.addItem(self.horizontalSpacer_8)

        self.label_task_fire = QLabel('Задача просрочена!', self)
        self.horizontalLayout_17.addWidget(self.label_task_fire)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_17.addItem(self.horizontalSpacer_9)
        self.layout.addWidget(self.task_fire_widget, 6, 1, 1, 1)

        self.task_fire_widget.setVisible(False)



class Note(QWidget):
    def __init__(self, toolBox_not, page_number, parent=None):
        super().__init__(parent)
        self.style = None
        with open("forms/style.css", "r") as f:
            self.style = f.read()

        self.page = QWidget(self)
        self.page.setStyleSheet(self.style)

        toolBox_not.addItem(self.page, f'Заметка № {page_number}')

        self.verticalLayoutWidget = QWidget(self.page)
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 501, 161))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.text_edit_note = QTextEdit(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.text_edit_note)

        self.horizontalLayout = QHBoxLayout()
        self.pushButton_attach_not = QPushButton('Закрепить', self.verticalLayoutWidget)
        self.pushButton_attach_not.setEnabled(False)
        self.horizontalLayout.addWidget(self.pushButton_attach_not)

        self.pushButton_change_not = QPushButton('Изменить', self.verticalLayoutWidget)
        self.pushButton_change_not.setEnabled(False)
        self.horizontalLayout.addWidget(self.pushButton_change_not)

        self.pushButton_del_not = QPushButton('Удалить', self.verticalLayoutWidget)
        self.pushButton_del_not.setEnabled(False)
        self.horizontalLayout.addWidget(self.pushButton_del_not)

        self.pushButton_save_not = QPushButton('Сохранить', self.verticalLayoutWidget)
        self.horizontalLayout.addWidget(self.pushButton_save_not)
        self.verticalLayout.addLayout(self.horizontalLayout)


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):

        self.style = None
        with open("forms/style.css", "r") as f:
            self.style = f.read()

        self.resize(933, 548)
        self.setWindowTitle('ТаскТрекер')
        self.setStyleSheet(self.style)

        self.calendarWidget = QCalendarWidget(self)
        self.add_calendar()

        # Основная штука, где лежат страницы
        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setGeometry(QRect(10, 10, 671, 521))
        self.stackedWidget.setFrameShape(QFrame.Shape.Box)
        self.stackedWidget.setFrameShadow(QFrame.Shadow.Sunken)

        self.page = QWidget()
        self.page_new_task()
        self.stackedWidget.addWidget(self.page)

        self.page_2 = QWidget()
        self.page_my_tasks()
        self.stackedWidget.addWidget(self.page_2)

        self.page_3 = QWidget()
        self.page_notices()
        self.stackedWidget.addWidget(self.page_3)

        self.attached_note(self)
        self.main_timer(self)

    def add_calendar(self):
        self.calendarWidget.setEnabled(True)
        self.calendarWidget.setGeometry(QRect(700, 370, 211, 161))
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(9)
        font.setBold(False)
        self.calendarWidget.setFont(font)
        self.calendarWidget.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.calendarWidget.setMouseTracking(False)
        self.calendarWidget.setTabletTracking(False)
        self.calendarWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.calendarWidget.setAcceptDrops(False)
        self.calendarWidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.calendarWidget.setAutoFillBackground(True)
        self.calendarWidget.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.calendarWidget.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)
        self.calendarWidget.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.ShortDayNames)
        self.calendarWidget.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.calendarWidget.setDateEditAcceptDelay(1500)


    def page_new_task(self):
        self.groupBox_new_task = QGroupBox('Новая задача', self.page)
        self.groupBox_new_task.setGeometry(QRect(10, 10, 531, 451))

        self.grid_layout_new_task = Base(self.groupBox_new_task)
        self.grid_layout_new_task.setGeometry(QRect(10, 20, 511, 361))

        self.pushButton_nt_create_task = QPushButton('Создать задачу', self.groupBox_new_task)
        self.pushButton_nt_create_task.setGeometry(QRect(370, 400, 151, 31))

        self.pushButton_nt_my_task = QPushButton('Мои задачи', self.page)
        self.pushButton_nt_my_task.setGeometry(QRect(550, 20, 101, 31))

        self.pushButton_nt_not = QPushButton('Заметки', self.page)
        self.pushButton_nt_not.setGeometry(QRect(550, 60, 101, 31))


    def page_my_tasks(self):
        self.groupBox_mt = QGroupBox('Мои задачи:', self.page_2)
        self.groupBox_mt.setGeometry(QRect(10, 10, 531, 501))

        self.tabWidget = QTabWidget(self.groupBox_mt)
        self.tabWidget.setGeometry(QRect(10, 20, 501, 471))

        self.tab = QWidget()
        self.tab_2 = QWidget()
        self.tab_3 = QWidget()

        self.page_planned_tab()
        self.page_progress_tab()
        self.page_done_tab()
        self.right_bar()

    def page_planned_tab(self):
        self.tabWidget.addTab(self.tab, "Запланированно")

        self.horizontalLayoutWidget_6 = QWidget(self.tab)
        self.horizontalLayoutWidget_6.setGeometry(QRect(10, 350, 471, 91))

        self.verticalLayoutWidget_4 = QWidget(self.tab)
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 10, 471, 341))

        self.verticalLayout_6 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)

        self.comboBox_mt_plan_all = QComboBox(self.verticalLayoutWidget_4)
        self.verticalLayout_6.addWidget(self.comboBox_mt_plan_all)

        self.frame_mt_plan = QFrame(self.verticalLayoutWidget_4)
        self.frame_mt_plan.setEnabled(False)
        self.frame_mt_plan.setFrameShape(QFrame.Shape.Box)
        self.frame_mt_plan.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_mt_plan.setLineWidth(1)

        self.grid_layout_plan = Base(self.frame_mt_plan)
        self.verticalLayout_6.addWidget(self.frame_mt_plan)

        self.grid_layout_plan.setGeometry(QRect(10, 10, 441, 298))
        self.verticalLayout_7 = QVBoxLayout()

        # lower_bar
        self.horizontalLayout_15 = QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_15.setContentsMargins(0, 5, 0, 5)
        self.horizontalSpacer_5 = QSpacerItem(120, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_5)

        self.verticalLayout_9 = QVBoxLayout()

        self.pushButton_mt_plan_change_task = QPushButton('Изменить задачу', self.horizontalLayoutWidget_6)
        self.pushButton_mt_plan_change_task.setFixedSize(QSize(140, 24))
        self.pushButton_mt_plan_change_task.setEnabled(False)
        self.verticalLayout_9.addWidget(self.pushButton_mt_plan_change_task)

        self.pushButton_mt_plan_start = QPushButton('Начать выполнение', self.horizontalLayoutWidget_6)
        self.pushButton_mt_plan_start.setFixedSize(QSize(140, 24))
        self.pushButton_mt_plan_start.setEnabled(False)
        self.verticalLayout_9.addWidget(self.pushButton_mt_plan_start)

        self.pushButton_mt_plan_del = QPushButton('Удалить задачу', self.horizontalLayoutWidget_6)
        self.pushButton_mt_plan_del.setFixedSize(QSize(140, 24))
        self.pushButton_mt_plan_del.setEnabled(False)
        self.verticalLayout_9.addWidget(self.pushButton_mt_plan_del)

        self.horizontalLayout_15.addLayout(self.verticalLayout_9)

    def page_progress_tab(self):
        self.tabWidget.addTab(self.tab_2, "В процессе")
        self.verticalLayoutWidget = QWidget(self.tab_2)
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 471, 341))

        self.verticalLayout_mt_proc = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_mt_proc.setContentsMargins(0, 0, 0, 0)

        self.comboBox_mt_proc_all = QComboBox(self.verticalLayoutWidget)
        self.verticalLayout_mt_proc.addWidget(self.comboBox_mt_proc_all)

        self.frame_mt_proc = QFrame(self.verticalLayoutWidget)
        self.frame_mt_proc.setEnabled(False)
        self.frame_mt_proc.setFrameShape(QFrame.Shape.Box)
        self.frame_mt_proc.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_mt_proc.setLineWidth(1)

        self.grid_layout_proc = Base(self.frame_mt_proc)
        self.grid_layout_proc.setGeometry(QRect(10, 10, 441, 298))

        self.verticalLayout_mt_proc.addWidget(self.frame_mt_proc)

        #lower_bar
        self.horizontalLayoutWidget_4 = QWidget(self.tab_2)
        self.horizontalLayoutWidget_4.setGeometry(QRect(10, 350, 471, 91))

        self.horizontalLayout_9 = QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_9.setContentsMargins(0, 5, 0, 5)

        self.groupBox_mt_proc_timer = QGroupBox('Таймер работы над задачей', self.horizontalLayoutWidget_4)
        self.groupBox_mt_proc_timer.setMinimumSize(QSize(285, 0))
        self.groupBox_mt_proc_timer.setEnabled(False)
        self.verticalLayoutWidget_2 = QWidget(self.groupBox_mt_proc_timer)

        self.verticalLayoutWidget_2.setGeometry(QRect(10, 20, 266, 71))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(0, 3, 0, -2)
        self.horizontalLayout_10 = QHBoxLayout()

        self.pushButton_mt_proc_start_timer = QPushButton('Запустить', self.verticalLayoutWidget_2)
        self.horizontalLayout_10.addWidget(self.pushButton_mt_proc_start_timer)

        self.pushButton_mt_proc_stop_timer = QPushButton('Остановить', self.verticalLayoutWidget_2)
        self.horizontalLayout_10.addWidget(self.pushButton_mt_proc_stop_timer)

        self.pushButton_mt_proc_rem_timer = QPushButton('Обновить', self.verticalLayoutWidget_2)
        self.horizontalLayout_10.addWidget(self.pushButton_mt_proc_rem_timer)

        self.verticalLayout_2.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_8 = QHBoxLayout()
        self.label_12 = QLabel('Время:', self.verticalLayoutWidget_2)
        self.label_12.setMaximumSize(QSize(50, 15))
        self.horizontalLayout_8.addWidget(self.label_12)

        self.label_mt_proc_timer = QLabel("00:00:00", self.verticalLayoutWidget_2)
        self.horizontalLayout_8.addWidget(self.label_mt_proc_timer)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9.addWidget(self.groupBox_mt_proc_timer)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_9.addItem(self.horizontalSpacer_3)

        # кнопки
        self.verticalLayout_5 = QVBoxLayout()
        self.pushButton_mt_proc_change_task = QPushButton('Изменить задачу', self.horizontalLayoutWidget_4)
        self.pushButton_mt_proc_change_task.setEnabled(False)
        self.pushButton_mt_proc_change_task.setMinimumSize(QSize(130, 0))
        self.verticalLayout_5.addWidget(self.pushButton_mt_proc_change_task)

        self.pushButton_mt_proc_finish = QPushButton('Завершить задачу', self.horizontalLayoutWidget_4)
        self.pushButton_mt_proc_finish.setEnabled(False)
        self.verticalLayout_5.addWidget(self.pushButton_mt_proc_finish)

        self.pushButton_mt_proc_del_task = QPushButton('Удалить задачу', self.horizontalLayoutWidget_4)
        self.pushButton_mt_proc_del_task.setEnabled(False)
        self.verticalLayout_5.addWidget(self.pushButton_mt_proc_del_task)

        self.horizontalLayout_9.addLayout(self.verticalLayout_5)

    def page_done_tab(self):
        self.tabWidget.addTab(self.tab_3, "Выполнено")

        self.verticalLayoutWidget_6 = QWidget(self.tab_3)
        self.verticalLayoutWidget_6.setGeometry(QRect(10, 10, 471, 341))
        self.verticalLayout_10 = QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)

        self.comboBox_mt_done_all = QComboBox(self.verticalLayoutWidget_6)
        self.verticalLayout_10.addWidget(self.comboBox_mt_done_all)

        self.frame_mt_done = QFrame(self.verticalLayoutWidget_6)
        self.frame_mt_done.setEnabled(False)
        self.frame_mt_done.setFrameShape(QFrame.Shape.Box)
        self.frame_mt_done.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_mt_done.setLineWidth(1)

        self.grid_layout_done = Base(self.frame_mt_done)
        self.grid_layout_done.setGeometry(QRect(10, 10, 441, 298))

        self.verticalLayout_10.addWidget(self.frame_mt_done)

        # lower_bar
        self.horizontalLayoutWidget_7 = QWidget(self.tab_3)
        self.horizontalLayoutWidget_7.setGeometry(QRect(10, 350, 471, 91))
        self.horizontalLayout_22 = QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout_22.setContentsMargins(0, 5, 0, 5)

        self.groupBox_5 = QGroupBox('Таймер работы над задачей', self.horizontalLayoutWidget_7)
        self.groupBox_5.setFixedSize(285, 81)
        self.verticalLayoutWidget_7 = QWidget(self.groupBox_5)

        self.horizontalLayout_24 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_24.setContentsMargins(0, 0, 0, 0)

        self.label_25 = QLabel('Время:', self.verticalLayoutWidget_7)
        self.label_25.setMaximumSize(QSize(40, 15))
        self.horizontalLayout_24.addWidget(self.label_25)

        self.label_mt_done_timer = QLabel("00:00:00", self.verticalLayoutWidget_7)
        self.horizontalLayout_24.addWidget(self.label_mt_done_timer)

        self.horizontalLayout_22.addWidget(self.groupBox_5)

        self.horizontalSpacer_7 = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_22.addItem(self.horizontalSpacer_7)

        # кнопки
        self.verticalLayout_13 = QVBoxLayout()

        self.pushButton_mt_done_recover_task = QPushButton('Восстановить задачу', self.horizontalLayoutWidget_7)
        self.pushButton_mt_done_recover_task.setEnabled(False)
        self.pushButton_mt_done_recover_task.setMinimumSize(QSize(130, 0))
        self.verticalLayout_13.addWidget(self.pushButton_mt_done_recover_task)

        self.pushButton_mt_done_del_task = QPushButton('Удалить задачу', self.horizontalLayoutWidget_7)
        self.pushButton_mt_done_del_task.setEnabled(False)
        self.verticalLayout_13.addWidget(self.pushButton_mt_done_del_task)
        self.horizontalLayout_22.addLayout(self.verticalLayout_13)


    def right_bar(self):
        self.pushButton_mt_crete_task = QPushButton('Новая задача', self.page_2)
        self.pushButton_mt_crete_task.setGeometry(QRect(550, 20, 101, 31))

        self.pushButton_mt_not = QPushButton('Заметки', self.page_2)
        self.pushButton_mt_not.setGeometry(QRect(550, 60, 101, 31))

        self.progressBar = QProgressBar(self.page_2)
        self.progressBar.setGeometry(QRect(550, 470, 111, 23))
        self.progressBar.setValue(0)
        self.label_63 = QLabel('Процеcс\nвыполнения:', self.page_2)
        self.label_63.setGeometry(QRect(550, 430, 91, 31))


    def page_notices(self):
        self.groupBox_notices = QGroupBox('Заметки', self.page_3)
        self.groupBox_notices.setGeometry(QRect(10, 10, 531, 471))

        self.toolBox_not = QToolBox(self.groupBox_notices)

        self.toolBox_not.setGeometry(QRect(10, 20, 501, 441))

        self.pushButton_cret_tsk_not = QPushButton('Новая задача', self.page_3)
        self.pushButton_cret_tsk_not.setGeometry(QRect(550, 20, 101, 31))

        self.pushButton_my_task_not = QPushButton('Мои задачи', self.page_3)
        self.pushButton_my_task_not.setGeometry(QRect(550, 60, 101, 31))

    def attached_note(self, Widget):
        self.dockWidget_notice = QDockWidget(Widget, features=QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.dockWidget_notice.setGeometry(QRect(700, 10, 211, 121))
        self.dockWidget_notice.setVisible(False)
        self.dockWidget_notice.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.dockWidgetContents = QWidget()

        self.label_atached_note = QLabel("TextLabel", self.dockWidgetContents)
        self.label_atached_note.setGeometry(QRect(0, 0, 211, 71))
        self.label_atached_note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dockWidget_notice.setWidget(self.dockWidgetContents)

        self.label_atached_note.setProperty("class", "note")
        self.label_atached_note.setStyleSheet(self.style)


    def main_timer(self, Widget):
        self.groupBox_main_timer = QGroupBox('Время работы', Widget)
        self.groupBox_main_timer.setGeometry(QRect(700, 180, 211, 181))

        self.formLayoutWidget = QWidget(self.groupBox_main_timer)
        self.formLayoutWidget.setGeometry(QRect(10, 20, 191, 51))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)

        self.label_8 = QLabel('Прошло:', self.formLayoutWidget)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_8)

        self.label_59 = QLabel('Осталось:', self.formLayoutWidget)
        self.label_59.setFrameShape(QFrame.Shape.NoFrame)
        self.label_59.setFrameShadow(QFrame.Shadow.Plain)
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_59)

        self.label_main_timer_passed = QLabel("", self.formLayoutWidget)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_main_timer_passed)

        self.label_main_timer_last = QLabel('', self.formLayoutWidget)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.label_main_timer_last)

        self.verticalLayoutWidget_3 = QWidget(self.groupBox_main_timer)
        self.verticalLayoutWidget_3.setGeometry(QRect(40, 80, 160, 86))
        self.verticalLayout_8 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)

        self.pushButton_set_timer = QPushButton('Установить таймер', self.verticalLayoutWidget_3)
        self.verticalLayout_8.addWidget(self.pushButton_set_timer)

        self.pushButton_20 = QPushButton('Отключить таймер', self.verticalLayoutWidget_3)
        self.verticalLayout_8.addWidget(self.pushButton_20)

        self.pushButton_21 = QPushButton('Посмотреть историю', self.verticalLayoutWidget_3)
        self.verticalLayout_8.addWidget(self.pushButton_21)

