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

from utils import upload_category, upload_priority


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.resize(933, 548)
        self.setWindowTitle('ТаскТрекер')

        self.calendarWidget = QCalendarWidget(Widget)
        self.add_calendar()

        # Основная штука, где лежат страницы
        self.stackedWidget = QStackedWidget(Widget)
        self.stackedWidget.setGeometry(QRect(10, 10, 671, 521))
        self.stackedWidget.setFrameShape(QFrame.Shape.Box)
        self.stackedWidget.setFrameShadow(QFrame.Shadow.Sunken)

        self.page = QWidget()
        self.page_new_task()
        self.stackedWidget.addWidget(self.page)

        self.page_2 = QWidget()
        self.page_my_tasks()
        self.stackedWidget.addWidget(self.page_2)

        self.page_5 = QWidget()
        self.page_notices()
        self.stackedWidget.addWidget(self.page_5)

        self.attached_notice(Widget)
        self.main_timer(Widget)

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
        self.groupBox_new_task = QGroupBox(self.page)
        self.groupBox_new_task.setGeometry(QRect(10, 10, 531, 451))
        self.groupBox_new_task.setTitle('Новая задача')

        self.gridLayoutWidget = QWidget(self.groupBox_new_task)
        self.gridLayoutWidget.setGeometry(QRect(10, 20, 511, 361))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 10, 0, 0)

        # Название
        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setText('Название:')
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.lineEdit_nt_name = QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_nt_name, 0, 1, 1, 1)

        # Описание
        self.verticalLayout_3 = QVBoxLayout()

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setText('Описание:')
        self.verticalLayout_3.addWidget(self.label_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(self.verticalSpacer)
        self.gridLayout.addLayout(self.verticalLayout_3, 3, 0, 1, 1)

        self.textEdit_nt_description = QTextEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.textEdit_nt_description, 3, 1, 1, 1)


        self.pushButton_nt_my_task = QPushButton(self.page)
        self.pushButton_nt_my_task.setGeometry(QRect(550, 20, 101, 31))
        self.pushButton_nt_my_task.setText('Мои задачи')

        def buttons():

            self.pushButton_nt_create_task = QPushButton(self.groupBox_new_task)
            self.pushButton_nt_create_task.setGeometry(QRect(370, 400, 151, 31))
            self.pushButton_nt_create_task.setText('Создать задачу')





            self.pushButton_nt_not = QPushButton(self.page)
            self.pushButton_nt_not.setGeometry(QRect(550, 60, 101, 31))
            self.pushButton_nt_not.setText('Заметки')
            self.pushButton_nt_not.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        def adding_deadline():
            self.horizontalLayout_50 = QHBoxLayout()

            self.dateTimeEdit_nt = QDateTimeEdit(self.gridLayoutWidget)
            self.dateTimeEdit_nt.setEnabled(False)
            self.dateTimeEdit_nt.setMinimumSize(QSize(150, 0))
            self.horizontalLayout_50.addWidget(self.dateTimeEdit_nt)

            self.horizontalSpacer_34 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            self.horizontalLayout_50.addItem(self.horizontalSpacer_34)
            self.gridLayout.addLayout(self.horizontalLayout_50, 4, 1, 1, 1)

            self.checkBox_nt_add_time = QCheckBox(self.gridLayoutWidget)
            self.checkBox_nt_add_time.setMinimumSize(QSize(137, 0))
            self.checkBox_nt_add_time.setText('Добавить срок')
            self.horizontalLayout_50.addWidget(self.checkBox_nt_add_time)

        def adding_replay():
            self.horizontalLayout_53 = QHBoxLayout()

            self.label_nt_repeat = QLabel(self.gridLayoutWidget)
            self.label_nt_repeat.setEnabled(False)
            self.label_nt_repeat.setMinimumSize(QSize(150, 0))
            self.label_nt_repeat.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
            self.horizontalLayout_53.addWidget(self.label_nt_repeat)

            self.horizontalSpacer_37 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            self.horizontalLayout_53.addItem(self.horizontalSpacer_37)

            self.checkBox_nt_repeat = QCheckBox(self.gridLayoutWidget)
            self.checkBox_nt_repeat.setMinimumSize(QSize(137, 0))
            self.checkBox_nt_repeat.setText('Повторяемая задача')
            self.horizontalLayout_53.addWidget(self.checkBox_nt_repeat)

            self.gridLayout.addLayout(self.horizontalLayout_53, 5, 1, 1, 1)

        def category():
            self.label = QLabel(self.gridLayoutWidget)
            self.label.setText('Категория:')
            self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

            self.horizontalLayout = QHBoxLayout()
            self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

            self.comboBox_nt_category = QComboBox(self.gridLayoutWidget)
            self.comboBox_nt_category.setEnabled(True)
            upload_category(self.comboBox_nt_category)
            self.horizontalLayout.addWidget(self.comboBox_nt_category)

            self.horizontalSpacer = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
            self.horizontalLayout.addItem(self.horizontalSpacer)
            self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

            self.pushButton_nt_new_cat = QPushButton(self.gridLayoutWidget)
            self.pushButton_nt_new_cat.setMaximumSize(QSize(110, 16777215))
            self.pushButton_nt_new_cat.setText('Новая категория')
            self.horizontalLayout.addWidget(self.pushButton_nt_new_cat)

        def priority():
            self.label_3 = QLabel(self.gridLayoutWidget)
            self.label_3.setText('Приоритет:')
            self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

            self.comboBox_nt_prior = QComboBox(self.gridLayoutWidget)
            upload_priority(self.comboBox_nt_prior)
            self.gridLayout.addWidget(self.comboBox_nt_prior, 1, 1, 1, 1)


        buttons()
        adding_deadline()
        adding_replay()
        category()
        priority()

    def page_my_tasks(self):
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.groupBox_mt = QGroupBox(self.page_2)
        self.groupBox_mt.setGeometry(QRect(10, 10, 531, 501))
        self.groupBox_mt.setTitle('Мои задачи:')

        self.tabWidget = QTabWidget(self.groupBox_mt)
        self.tabWidget.setGeometry(QRect(10, 20, 501, 471))
        self.tabWidget.setMinimumSize(QSize(125, 0))

        self.tab = QWidget()
        self.tab_2 = QWidget()
        self.tab_3 = QWidget()

        def planned_tab():
            self.tabWidget.addTab(self.tab, "")

            self.horizontalLayoutWidget_6 = QWidget(self.tab)
            self.horizontalLayoutWidget_6.setGeometry(QRect(10, 350, 471, 91))

            self.verticalLayoutWidget_4 = QWidget(self.tab)
            self.verticalLayoutWidget_4.setGeometry(QRect(10, 10, 471, 341))

            self.verticalLayout_6 = QVBoxLayout(self.verticalLayoutWidget_4)
            self.verticalLayout_6.setSpacing(6)
            self.verticalLayout_6.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
            self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)

            self.comboBox_mt_plan_all = QComboBox(self.verticalLayoutWidget_4)
            self.verticalLayout_6.addWidget(self.comboBox_mt_plan_all)

            self.frame_mt_plan = QFrame(self.verticalLayoutWidget_4)
            self.frame_mt_plan.setEnabled(False)
            self.frame_mt_plan.setFrameShape(QFrame.Shape.Box)
            self.frame_mt_plan.setFrameShadow(QFrame.Shadow.Raised)
            self.frame_mt_plan.setLineWidth(1)

            self.gridLayoutWidget_3 = QWidget(self.frame_mt_plan)
            self.verticalLayout_6.addWidget(self.frame_mt_plan)

            self.gridLayoutWidget_3.setGeometry(QRect(10, 10, 441, 298))
            self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
            self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout_7 = QVBoxLayout()

            # Название
            self.label_13 = QLabel(self.gridLayoutWidget_3)
            self.label_13.setText('Название:')
            self.gridLayout_3.addWidget(self.label_13, 0, 0, 1, 1)

            self.lineEdit__mt_plan_name = QLineEdit(self.gridLayoutWidget_3)
            self.lineEdit__mt_plan_name.setEnabled(False)
            self.gridLayout_3.addWidget(self.lineEdit__mt_plan_name, 0, 1, 1, 1)

            def lower_bar():
                self.horizontalLayout_15 = QHBoxLayout(self.horizontalLayoutWidget_6)
                self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
                self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

                self.horizontalLayout_15.addItem(self.horizontalSpacer_5)

                self.verticalLayout_9 = QVBoxLayout()

                self.pushButton_mt_plan_change_task = QPushButton(self.horizontalLayoutWidget_6)
                self.pushButton_mt_plan_change_task.setMinimumSize(QSize(125, 0))
                self.pushButton_mt_plan_change_task.setText('Изменить задачу')
                self.verticalLayout_9.addWidget(self.pushButton_mt_plan_change_task)

                self.pushButton_mt_plan_start = QPushButton(self.horizontalLayoutWidget_6)
                self.pushButton_mt_plan_start.setMinimumSize(QSize(125, 0))
                self.pushButton_mt_plan_start.setText('Начать выполнение')
                self.verticalLayout_9.addWidget(self.pushButton_mt_plan_start)

                self.pushButton_mt_plan_del = QPushButton(self.horizontalLayoutWidget_6)
                self.pushButton_mt_plan_del.setText('Удалить задачу')
                self.verticalLayout_9.addWidget(self.pushButton_mt_plan_del)

                self.horizontalLayout_15.addLayout(self.verticalLayout_9)

            def adding_deadline():
                self.horizontalLayout_27 = QHBoxLayout()
                self.dateTimeEdit_mt_plan = QDateTimeEdit(self.gridLayoutWidget_3)
                self.dateTimeEdit_mt_plan.setEnabled(False)
                self.dateTimeEdit_mt_plan.setMinimumSize(QSize(150, 0))

                self.horizontalLayout_27.addWidget(self.dateTimeEdit_mt_plan)

                self.horizontalSpacer_15 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

                self.horizontalLayout_27.addItem(self.horizontalSpacer_15)

                self.checkBox_mt_plan_add_timer = QCheckBox(self.gridLayoutWidget_3)
                self.checkBox_mt_plan_add_timer.setEnabled(False)
                self.checkBox_mt_plan_add_timer.setMinimumSize(QSize(137, 0))
                self.checkBox_mt_plan_add_timer.setText('Добавить срок')

                self.horizontalLayout_27.addWidget(self.checkBox_mt_plan_add_timer)

                self.gridLayout_3.addLayout(self.horizontalLayout_27, 4, 1, 1, 1)

            def adding_replay():
                self.horizontalLayout_26 = QHBoxLayout()
                self.label_mt_plan_repeat = QLabel(self.gridLayoutWidget_3)
                self.label_mt_plan_repeat.setEnabled(False)
                self.label_mt_plan_repeat.setMinimumSize(QSize(150, 0))
                self.label_mt_plan_repeat.setText("TextLabel")

                self.horizontalLayout_26.addWidget(self.label_mt_plan_repeat)

                self.horizontalSpacer_14 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

                self.horizontalLayout_26.addItem(self.horizontalSpacer_14)

                self.checkBox_mt_plan_add_repet = QCheckBox(self.gridLayoutWidget_3)
                self.checkBox_mt_plan_add_repet.setEnabled(False)
                self.checkBox_mt_plan_add_repet.setMinimumSize(QSize(137, 0))
                self.checkBox_mt_plan_add_repet.setText('Повторяемая задача')

                self.horizontalLayout_26.addWidget(self.checkBox_mt_plan_add_repet)

                self.gridLayout_3.addLayout(self.horizontalLayout_26, 5, 1, 1, 1)

            def category():
                self.label_14 = QLabel(self.gridLayoutWidget_3)
                self.label_14.setText('Категория:')
                self.gridLayout_3.addWidget(self.label_14, 2, 0, 1, 1)

                self.horizontalLayout_11 = QHBoxLayout()
                self.horizontalLayout_11.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
                self.comboBox_mt_plan_cat = QComboBox(self.gridLayoutWidget_3)
                upload_category(self.comboBox_mt_plan_cat)
                self.comboBox_mt_plan_cat.setEnabled(False)

                self.horizontalLayout_11.addWidget(self.comboBox_mt_plan_cat)

                self.horizontalSpacer_4 = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

                self.horizontalLayout_11.addItem(self.horizontalSpacer_4)

                self.pushButton_mt_plan_new_cat = QPushButton(self.gridLayoutWidget_3)
                self.pushButton_mt_plan_new_cat.setEnabled(False)
                sizePolicy.setHeightForWidth(self.pushButton_mt_plan_new_cat.sizePolicy().hasHeightForWidth())
                self.pushButton_mt_plan_new_cat.setSizePolicy(sizePolicy)
                self.pushButton_mt_plan_new_cat.setMaximumSize(QSize(100, 16777215))
                self.pushButton_mt_plan_new_cat.setText('Новая категория')

                self.horizontalLayout_11.addWidget(self.pushButton_mt_plan_new_cat)

                self.gridLayout_3.addLayout(self.horizontalLayout_11, 2, 1, 1, 1)

            def priority():
                self.label_17 = QLabel(self.gridLayoutWidget_3)
                self.label_17.setText('Приоритет:')
                self.gridLayout_3.addWidget(self.label_17, 1, 0, 1, 1)

                self.comboBox_mt_plan_prior = QComboBox(self.gridLayoutWidget_3)
                self.comboBox_mt_plan_prior.setEnabled(False)

                self.gridLayout_3.addWidget(self.comboBox_mt_plan_prior, 1, 1, 1, 1)

            def description():
                self.label_15 = QLabel(self.gridLayoutWidget_3)
                self.label_15.setText('Описание:')
                self.verticalLayout_7.addWidget(self.label_15)

                self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                self.verticalLayout_7.addItem(self.verticalSpacer_3)
                self.gridLayout_3.addLayout(self.verticalLayout_7, 3, 0, 1, 1)

                self.textEdit_mt_plan_description = QTextEdit(self.gridLayoutWidget_3)
                self.textEdit_mt_plan_description.setEnabled(False)
                self.gridLayout_3.addWidget(self.textEdit_mt_plan_description, 3, 1, 1, 1)

            description()
            lower_bar()
            adding_deadline()
            adding_replay()
            category()
            priority()

        def progress_tab():
            self.verticalLayoutWidget = QWidget(self.tab_2)
            self.verticalLayoutWidget.setGeometry(QRect(10, 10, 471, 341))

            self.verticalLayout_mt_proc = QVBoxLayout(self.verticalLayoutWidget)
            self.verticalLayout_mt_proc.setSpacing(6)
            self.verticalLayout_mt_proc.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
            self.verticalLayout_mt_proc.setContentsMargins(0, 0, 0, 0)

            self.comboBox_mt_proc_all = QComboBox(self.verticalLayoutWidget)
            self.verticalLayout_mt_proc.addWidget(self.comboBox_mt_proc_all)

            self.frame_mt_proc = QFrame(self.verticalLayoutWidget)
            self.frame_mt_proc.setEnabled(False)
            self.frame_mt_proc.setFrameShape(QFrame.Shape.Box)
            self.frame_mt_proc.setFrameShadow(QFrame.Shadow.Raised)
            self.frame_mt_proc.setLineWidth(1)

            self.gridLayoutWidget_2 = QWidget(self.frame_mt_proc)
            self.gridLayoutWidget_2.setGeometry(QRect(10, 10, 441, 298))
            self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
            self.gridLayout_2.setContentsMargins(0, 0, 0, 0)

            # Название
            self.label_6 = QLabel(self.gridLayoutWidget_2)
            self.label_6.setText('Название:')
            self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

            self.lineEdit_mt_proc_name = QLineEdit(self.gridLayoutWidget_2)
            self.lineEdit_mt_proc_name.setEnabled(False)
            self.gridLayout_2.addWidget(self.lineEdit_mt_proc_name, 0, 1, 1, 1)

            self.verticalLayout_mt_proc.addWidget(self.frame_mt_proc)

            self.tabWidget.addTab(self.tab_2, "")

            def lower_bar():
                self.horizontalLayoutWidget_4 = QWidget(self.tab_2)
                self.horizontalLayoutWidget_4.setGeometry(QRect(10, 350, 471, 91))

                self.horizontalLayout_9 = QHBoxLayout(self.horizontalLayoutWidget_4)
                self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)

                self.groupBox_mt_proc_timer = QGroupBox(self.horizontalLayoutWidget_4)
                self.groupBox_mt_proc_timer.setMinimumSize(QSize(260, 0))
                self.groupBox_mt_proc_timer.setTitle('Таймер работы над задачей')
                self.verticalLayoutWidget_2 = QWidget(self.groupBox_mt_proc_timer)

                self.verticalLayoutWidget_2.setGeometry(QRect(10, 20, 241, 71))
                self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
                self.verticalLayout_2.setSpacing(2)
                self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
                self.horizontalLayout_10 = QHBoxLayout()

                self.pushButton_mt_proc_start_timer = QPushButton(self.verticalLayoutWidget_2)
                self.pushButton_mt_proc_start_timer.setText('Запустить')
                self.horizontalLayout_10.addWidget(self.pushButton_mt_proc_start_timer)

                self.pushButton_mt_proc_stop_timer = QPushButton(self.verticalLayoutWidget_2)
                self.pushButton_mt_proc_stop_timer.setText('Остановить')
                self.horizontalLayout_10.addWidget(self.pushButton_mt_proc_stop_timer)

                self.pushButton_mt_proc_rem_timer = QPushButton(self.verticalLayoutWidget_2)
                self.pushButton_mt_proc_rem_timer.setText('Обновить')
                self.horizontalLayout_10.addWidget(self.pushButton_mt_proc_rem_timer)

                self.verticalLayout_2.addLayout(self.horizontalLayout_10)

                self.horizontalLayout_8 = QHBoxLayout()
                self.label_12 = QLabel(self.verticalLayoutWidget_2)
                self.label_12.setText('Время:')
                self.horizontalLayout_8.addWidget(self.label_12)

                self.label_mt_proc_timer = QLabel(self.verticalLayoutWidget_2)
                self.label_mt_proc_timer.setText("TextLabel")

                self.horizontalLayout_8.addWidget(self.label_mt_proc_timer)
                self.verticalLayout_2.addLayout(self.horizontalLayout_8)

                self.horizontalLayout_9.addWidget(self.groupBox_mt_proc_timer)

                self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
                self.horizontalLayout_9.addItem(self.horizontalSpacer_3)

                # кнопки
                self.verticalLayout_5 = QVBoxLayout()
                self.pushButton_mt_proc_change_task = QPushButton(self.horizontalLayoutWidget_4)
                self.pushButton_mt_proc_change_task.setMinimumSize(QSize(125, 0))
                self.pushButton_mt_proc_change_task.setText('Изменить задачу')
                self.verticalLayout_5.addWidget(self.pushButton_mt_proc_change_task)

                self.pushButton_mt_proc_finish = QPushButton(self.horizontalLayoutWidget_4)
                self.pushButton_mt_proc_finish.setMinimumSize(QSize(125, 0))
                self.pushButton_mt_proc_finish.setText('Завершить задачу')
                self.verticalLayout_5.addWidget(self.pushButton_mt_proc_finish)

                self.pushButton_mt_proc_del_task = QPushButton(self.horizontalLayoutWidget_4)
                self.pushButton_mt_proc_del_task.setText('Удалить задачу')
                self.verticalLayout_5.addWidget(self.pushButton_mt_proc_del_task)

                self.horizontalLayout_9.addLayout(self.verticalLayout_5)

            def adding_deadline():
                self.horizontalLayout_25 = QHBoxLayout()

                self.dateTimeEdit_mt_proc = QDateTimeEdit(self.gridLayoutWidget_2)
                self.dateTimeEdit_mt_proc.setEnabled(False)
                self.dateTimeEdit_mt_proc.setMinimumSize(QSize(150, 0))
                self.horizontalLayout_25.addWidget(self.dateTimeEdit_mt_proc)

                self.horizontalSpacer_13 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
                self.horizontalLayout_25.addItem(self.horizontalSpacer_13)

                self.checkBox_mt_proc_add_time = QCheckBox(self.gridLayoutWidget_2)
                self.checkBox_mt_proc_add_time.setEnabled(False)
                self.checkBox_mt_proc_add_time.setMinimumSize(QSize(137, 0))
                self.checkBox_mt_proc_add_time.setText('Добавить срок')
                self.horizontalLayout_25.addWidget(self.checkBox_mt_proc_add_time)

                self.gridLayout_2.addLayout(self.horizontalLayout_25, 4, 1, 1, 1)

            def adding_replay():
                self.horizontalLayout_23 = QHBoxLayout()
                self.label_mt_proc_repeat = QLabel(self.gridLayoutWidget_2)
                self.label_mt_proc_repeat.setEnabled(False)
                self.label_mt_proc_repeat.setMinimumSize(QSize(150, 0))
                self.label_mt_proc_repeat.setText("TextLabel")
                self.horizontalLayout_23.addWidget(self.label_mt_proc_repeat)

                self.horizontalSpacer_12 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
                self.horizontalLayout_23.addItem(self.horizontalSpacer_12)

                self.checkBox_mt_proc_add_repeat = QCheckBox(self.gridLayoutWidget_2)
                self.checkBox_mt_proc_add_repeat.setEnabled(False)
                self.checkBox_mt_proc_add_repeat.setMinimumSize(QSize(137, 0))
                self.checkBox_mt_proc_add_repeat.setText('Повторяемая задача')
                self.horizontalLayout_23.addWidget(self.checkBox_mt_proc_add_repeat)

                self.gridLayout_2.addLayout(self.horizontalLayout_23, 5, 1, 1, 1)

            def category():
                self.label_10 = QLabel(self.gridLayoutWidget_2)
                self.label_10.setText('Категория:')
                self.gridLayout_2.addWidget(self.label_10, 2, 0, 1, 1)

                self.horizontalLayout_5 = QHBoxLayout()
                self.horizontalLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

                self.comboBox_mt_proc_cat = QComboBox(self.gridLayoutWidget_2)
                self.comboBox_mt_proc_cat.setEnabled(False)
                upload_category(self.comboBox_mt_proc_cat)
                self.horizontalLayout_5.addWidget(self.comboBox_mt_proc_cat)

                self.horizontalSpacer_2 = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
                self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

                self.pushButton_mt_proc_new_cat = QPushButton(self.gridLayoutWidget_2)
                self.pushButton_mt_proc_new_cat.setEnabled(False)
                self.pushButton_mt_proc_new_cat.setMaximumSize(QSize(100, 16777215))
                self.pushButton_mt_proc_new_cat.setText('Новая категория')

                self.horizontalLayout_5.addWidget(self.pushButton_mt_proc_new_cat)
                self.gridLayout_2.addLayout(self.horizontalLayout_5, 2, 1, 1, 1)

            def priority():
                self.horizontalLayout_7 = QHBoxLayout()
                self.comboBox_mt_proc_prior = QComboBox(self.gridLayoutWidget_2)
                self.comboBox_mt_proc_prior.setEnabled(False)
                self.gridLayout_2.addWidget(self.comboBox_mt_proc_prior, 1, 1, 1, 1)

                self.label_7 = QLabel(self.gridLayoutWidget_2)
                self.label_7.setText('Приоритет:')
                self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)

            def description():
                self.verticalLayout_4 = QVBoxLayout()
                self.label_5 = QLabel(self.gridLayoutWidget_2)
                self.label_5.setText('Описание:')
                self.verticalLayout_4.addWidget(self.label_5)

                self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                self.verticalLayout_4.addItem(self.verticalSpacer_2)
                self.gridLayout_2.addLayout(self.verticalLayout_4, 3, 0, 1, 1)

                self.textEdit_mt_proc_description = QTextEdit(self.gridLayoutWidget_2)
                self.textEdit_mt_proc_description.setEnabled(False)
                self.gridLayout_2.addWidget(self.textEdit_mt_proc_description, 3, 1, 1, 1)

            description()
            lower_bar()
            adding_deadline()
            adding_replay()
            category()
            priority()

        def done_tab():
            self.verticalLayoutWidget_6 = QWidget(self.tab_3)
            self.verticalLayoutWidget_6.setGeometry(QRect(10, 10, 471, 341))
            self.verticalLayout_10 = QVBoxLayout(self.verticalLayoutWidget_6)
            self.verticalLayout_10.setSpacing(6)
            self.verticalLayout_10.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
            self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)

            self.comboBox_mt_done_all = QComboBox(self.verticalLayoutWidget_6)
            self.verticalLayout_10.addWidget(self.comboBox_mt_done_all)

            self.frame_mt_done = QFrame(self.verticalLayoutWidget_6)
            self.frame_mt_done.setEnabled(False)
            self.frame_mt_done.setFrameShape(QFrame.Shape.Box)
            self.frame_mt_done.setFrameShadow(QFrame.Shadow.Raised)
            self.frame_mt_done.setLineWidth(1)

            self.gridLayoutWidget_4 = QWidget(self.frame_mt_done)
            self.gridLayoutWidget_4.setGeometry(QRect(10, 10, 441, 311))
            self.gridLayout_4 = QGridLayout(self.gridLayoutWidget_4)
            self.gridLayout_4.setContentsMargins(0, 0, 0, 0)

            self.horizontalLayout_19 = QHBoxLayout()
            self.dateTimeEdit_mt_done = QDateTimeEdit(self.gridLayoutWidget_4)
            self.dateTimeEdit_mt_done.setEnabled(False)
            self.dateTimeEdit_mt_done.setMinimumSize(QSize(150, 0))

            # Название
            self.label_20 = QLabel(self.gridLayoutWidget_4)
            self.label_20.setText('Название:')
            self.gridLayout_4.addWidget(self.label_20, 0, 0, 1, 1)

            self.lineEdit_mt_done_name = QLineEdit(self.gridLayoutWidget_4)
            self.lineEdit_mt_done_name.setEnabled(False)
            self.gridLayout_4.addWidget(self.lineEdit_mt_done_name, 0, 1, 1, 1)

            self.horizontalLayout_17 = QHBoxLayout()
            self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            self.horizontalLayout_17.addItem(self.horizontalSpacer_8)

            self.label_task_fire = QLabel(self.gridLayoutWidget_4)
            self.label_task_fire.setText('Задача просрочена! ')

            self.horizontalLayout_17.addWidget(self.label_task_fire)

            self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            self.horizontalLayout_17.addItem(self.horizontalSpacer_9)
            self.gridLayout_4.addLayout(self.horizontalLayout_17, 6, 1, 1, 1)

            self.verticalLayout_10.addWidget(self.frame_mt_done)

            self.horizontalLayoutWidget_7 = QWidget(self.tab_3)
            self.horizontalLayoutWidget_7.setGeometry(QRect(10, 370, 471, 71))

            self.tabWidget.addTab(self.tab_3, "")

            def description():
                self.verticalLayout_11 = QVBoxLayout()
                self.label_22 = QLabel(self.gridLayoutWidget_4)
                self.label_22.setText('Описание:')
                self.verticalLayout_11.addWidget(self.label_22)

                self.verticalSpacer_4 = QSpacerItem(10, 110, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

                self.verticalLayout_11.addItem(self.verticalSpacer_4)
                self.gridLayout_4.addLayout(self.verticalLayout_11, 3, 0, 1, 1)

                self.textEdit_mt_done_description = QTextEdit(self.gridLayoutWidget_4)
                self.textEdit_mt_done_description.setEnabled(False)
                self.textEdit_mt_done_description.setMaximumSize(QSize(373, 125))

                self.gridLayout_4.addWidget(self.textEdit_mt_done_description, 3, 1, 1, 1)

            def lower_bar():
                self.horizontalLayout_22 = QHBoxLayout(self.horizontalLayoutWidget_7)
                self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)

                self.groupBox_5 = QGroupBox(self.horizontalLayoutWidget_7)
                self.groupBox_5.setMinimumSize(QSize(260, 0))
                self.groupBox_5.setTitle('Таймер работы над задачей ')
                self.verticalLayoutWidget_7 = QWidget(self.groupBox_5)

                self.verticalLayoutWidget_7.setGeometry(QRect(10, 20, 241, 41))
                self.verticalLayout_12 = QVBoxLayout(self.verticalLayoutWidget_7)
                self.verticalLayout_12.setSpacing(2)
                self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)

                self.horizontalLayout_24 = QHBoxLayout()

                self.label_25 = QLabel(self.verticalLayoutWidget_7)
                self.label_25.setText('Время: ')
                self.horizontalLayout_24.addWidget(self.label_25)

                self.label_mt_done_timer = QLabel(self.verticalLayoutWidget_7)
                self.label_mt_done_timer.setText("TextLabel")

                self.horizontalLayout_24.addWidget(self.label_mt_done_timer)

                self.verticalLayout_12.addLayout(self.horizontalLayout_24)

                self.horizontalLayout_22.addWidget(self.groupBox_5)

                self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
                self.horizontalLayout_22.addItem(self.horizontalSpacer_7)

                # кнопки
                self.verticalLayout_13 = QVBoxLayout()

                self.pushButton_mt_done_recover_task = QPushButton(self.horizontalLayoutWidget_7)
                self.pushButton_mt_done_recover_task.setMinimumSize(QSize(125, 0))
                self.pushButton_mt_done_recover_task.setText('Восстановить задачу')
                self.verticalLayout_13.addWidget(self.pushButton_mt_done_recover_task)

                self.pushButton_mt_done_del_task = QPushButton(self.horizontalLayoutWidget_7)
                self.pushButton_mt_done_del_task.setText('Удалить задачу ')
                self.verticalLayout_13.addWidget(self.pushButton_mt_done_del_task)

                self.horizontalLayout_22.addLayout(self.verticalLayout_13)

            def adding_deadline():
                self.horizontalLayout_19.addWidget(self.dateTimeEdit_mt_done)

                self.horizontalSpacer_10 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
                self.horizontalLayout_19.addItem(self.horizontalSpacer_10)

                self.checkBox_mt_done_add_timer = QCheckBox(self.gridLayoutWidget_4)
                self.checkBox_mt_done_add_timer.setEnabled(False)
                self.checkBox_mt_done_add_timer.setMinimumSize(QSize(137, 0))
                self.checkBox_mt_done_add_timer.setText('Добавить срок')
                self.horizontalLayout_19.addWidget(self.checkBox_mt_done_add_timer)

                self.gridLayout_4.addLayout(self.horizontalLayout_19, 4, 1, 1, 1)

            def adding_replay():
                self.horizontalLayout_20 = QHBoxLayout()
                self.label_mt_done_repeat = QLabel(self.gridLayoutWidget_4)
                self.label_mt_done_repeat.setEnabled(False)
                self.label_mt_done_repeat.setMinimumSize(QSize(150, 0))
                self.label_mt_done_repeat.setText("TextLabel")
                self.horizontalLayout_20.addWidget(self.label_mt_done_repeat)

                self.horizontalSpacer_11 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
                self.horizontalLayout_20.addItem(self.horizontalSpacer_11)

                self.checkBox_mt_done_add_repeat = QCheckBox(self.gridLayoutWidget_4)
                self.checkBox_mt_done_add_repeat.setEnabled(False)
                self.checkBox_mt_done_add_repeat.setMinimumSize(QSize(137, 0))
                self.checkBox_mt_done_add_repeat.setText('Повторяемая задача')
                self.horizontalLayout_20.addWidget(self.checkBox_mt_done_add_repeat)

                self.gridLayout_4.addLayout(self.horizontalLayout_20, 5, 1, 1, 1)

            def category():
                self.label_21 = QLabel(self.gridLayoutWidget_4)
                self.label_21.setText('Категория:')
                self.gridLayout_4.addWidget(self.label_21, 2, 0, 1, 1)

                self.horizontalLayout_18 = QHBoxLayout()
                self.horizontalLayout_18.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

                self.comboBox_mt_done_cat = QComboBox(self.gridLayoutWidget_4)
                self.comboBox_mt_done_cat.setEnabled(False)
                upload_category(self.comboBox_mt_done_cat)
                self.horizontalLayout_18.addWidget(self.comboBox_mt_done_cat)

                self.horizontalSpacer_6 = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
                self.horizontalLayout_18.addItem(self.horizontalSpacer_6)

                self.pushButton_mt_done_new_cat = QPushButton(self.gridLayoutWidget_4)
                self.pushButton_mt_done_new_cat.setEnabled(False)
                self.pushButton_mt_done_new_cat.setMaximumSize(QSize(100, 16777215))
                self.pushButton_mt_done_new_cat.setText('Новая категория')

                self.horizontalLayout_18.addWidget(self.pushButton_mt_done_new_cat)
                self.gridLayout_4.addLayout(self.horizontalLayout_18, 2, 1, 1, 1)

            def priority():
                self.label_24 = QLabel(self.gridLayoutWidget_4)
                self.label_24.setText('Приоритет:')
                self.gridLayout_4.addWidget(self.label_24, 1, 0, 1, 1)

                self.comboBox_mt_done_prior = QComboBox(self.gridLayoutWidget_4)
                self.comboBox_mt_done_prior.setEnabled(False)

                self.gridLayout_4.addWidget(self.comboBox_mt_done_prior, 1, 1, 1, 1)

            description()
            lower_bar()
            adding_deadline()
            adding_replay()
            category()
            priority()

        def right_bar():
            self.pushButton_mt_crete_task = QPushButton(self.page_2)
            self.pushButton_mt_crete_task.setGeometry(QRect(550, 20, 101, 31))
            self.pushButton_mt_crete_task.setText('Создать задачу')
            self.pushButton_mt_crete_task.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

            self.pushButton_mt_not = QPushButton(self.page_2)
            self.pushButton_mt_not.setGeometry(QRect(550, 60, 101, 31))
            self.pushButton_mt_not.setText('Заметки')
            self.pushButton_mt_not.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

            self.progressBar = QProgressBar(self.page_2)
            self.progressBar.setGeometry(QRect(550, 470, 111, 23))
            self.progressBar.setValue(24)
            self.label_63 = QLabel(self.page_2)
            self.label_63.setGeometry(QRect(550, 430, 91, 31))
            self.label_63.setWordWrap(False)
            self.label_63.setMargin(0)
            self.label_63.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
            self.label_63.setText('Процеcс\nвыполнения:')

        planned_tab()
        progress_tab()
        done_tab()
        right_bar()

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), 'Запланированно')
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), 'В процессе')
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), 'Выполнено')

    def page_notices(self):
        self.groupBox_notices = QGroupBox(self.page_5)
        self.groupBox_notices.setGeometry(QRect(10, 10, 531, 471))
        self.groupBox_notices.setTitle('Заметки')

        self.toolBox_not = QToolBox(self.groupBox_notices)
        self.toolBox_not.setGeometry(QRect(10, 20, 501, 441))

        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.page_6.setGeometry(QRect(0, 0, 501, 411))
        self.toolBox_not.setItemText(self.toolBox_not.indexOf(self.page_6), "Page 1")

        self.verticalLayoutWidget_5 = QWidget(self.page_6)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(0, 0, 501, 161))
        self.verticalLayout_14 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.textBrowser = QTextBrowser(self.verticalLayoutWidget_5)

        self.verticalLayout_14.addWidget(self.textBrowser)

        self.horizontalLayout_2 = QHBoxLayout()
        self.pushButton_attach_not = QPushButton(self.verticalLayoutWidget_5)
        self.pushButton_attach_not.setText('Заметки')

        self.horizontalLayout_2.addWidget(self.pushButton_attach_not)

        self.pushButton_del_not = QPushButton(self.verticalLayoutWidget_5)
        self.pushButton_del_not.setText('Удалить ')

        self.horizontalLayout_2.addWidget(self.pushButton_del_not)

        self.pushButton_save_not = QPushButton(self.verticalLayoutWidget_5)
        self.pushButton_save_not.setText('Сохранить ')

        self.horizontalLayout_2.addWidget(self.pushButton_save_not)

        self.verticalLayout_14.addLayout(self.horizontalLayout_2)

        self.pushButton_cret_tsk_not = QPushButton(self.page_5)
        self.pushButton_cret_tsk_not.setGeometry(QRect(550, 20, 101, 31))
        self.pushButton_cret_tsk_not.setText('Создать задачу')
        self.pushButton_cret_tsk_not.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        self.pushButton_my_task_not = QPushButton(self.page_5)
        self.pushButton_my_task_not.setGeometry(QRect(550, 60, 101, 31))
        self.pushButton_my_task_not.setText('Мои задачи')
        self.pushButton_my_task_not.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

    def attached_notice(self, Widget):
        self.dockWidget_notice = QDockWidget(Widget)
        self.dockWidget_notice.setGeometry(QRect(700, 10, 211, 121))
        self.dockWidgetContents = QWidget()

        self.label_atached_note = QLabel(self.dockWidgetContents)
        self.label_atached_note.setGeometry(QRect(10, 10, 191, 71))
        self.label_atached_note.setText("TextLabel")
        self.dockWidget_notice.setWidget(self.dockWidgetContents)

    def main_timer(self, Widget):
        self.groupBox_main_timer = QGroupBox(Widget)
        self.groupBox_main_timer.setGeometry(QRect(700, 180, 211, 181))
        self.groupBox_main_timer.setTitle('Время работы')

        self.formLayoutWidget = QWidget(self.groupBox_main_timer)
        self.formLayoutWidget.setGeometry(QRect(10, 20, 191, 51))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.formLayoutWidget)
        self.label_8.setText('Прошло: ')

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_8)

        self.label_59 = QLabel(self.formLayoutWidget)
        self.label_59.setFrameShape(QFrame.Shape.NoFrame)
        self.label_59.setFrameShadow(QFrame.Shadow.Plain)
        self.label_59.setText('Осталось:')

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_59)

        self.label_main_timer_passed = QLabel(self.formLayoutWidget)
        self.label_main_timer_passed.setText("TextLabel")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_main_timer_passed)

        self.label_main_timer_last = QLabel(self.formLayoutWidget)
        self.label_main_timer_last.setText('TextLabel')

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.label_main_timer_last)

        self.verticalLayoutWidget_3 = QWidget(self.groupBox_main_timer)
        self.verticalLayoutWidget_3.setGeometry(QRect(40, 80, 160, 86))
        self.verticalLayout_8 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.pushButton_19 = QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_19.setText('Установить таймер')

        self.verticalLayout_8.addWidget(self.pushButton_19)

        self.pushButton_20 = QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_20.setText('Отключить таймер ')

        self.verticalLayout_8.addWidget(self.pushButton_20)

        self.pushButton_21 = QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_21.setText('Посмотреть историю ')
        self.verticalLayout_8.addWidget(self.pushButton_21)




