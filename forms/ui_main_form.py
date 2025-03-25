# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QCheckBox, QComboBox,
    QDateTimeEdit, QDockWidget, QFormLayout, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QTabWidget,
    QTextBrowser, QTextEdit, QToolBox, QVBoxLayout,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(933, 548)
        self.calendarWidget = QCalendarWidget(Widget)
        self.calendarWidget.setObjectName(u"calendarWidget")
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
        self.stackedWidget = QStackedWidget(Widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(10, 10, 671, 521))
        self.stackedWidget.setFrameShape(QFrame.Shape.Box)
        self.stackedWidget.setFrameShadow(QFrame.Shadow.Sunken)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.groupBox_new_task = QGroupBox(self.page)
        self.groupBox_new_task.setObjectName(u"groupBox_new_task")
        self.groupBox_new_task.setGeometry(QRect(10, 10, 531, 451))
        self.gridLayoutWidget = QWidget(self.groupBox_new_task)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 20, 511, 361))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.gridLayout.addLayout(self.verticalLayout_3, 3, 0, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.comboBox_nt_prior = QComboBox(self.gridLayoutWidget)
        self.comboBox_nt_prior.setObjectName(u"comboBox_nt_prior")

        self.gridLayout.addWidget(self.comboBox_nt_prior, 1, 1, 1, 1)

        self.textEdit_nt_description = QTextEdit(self.gridLayoutWidget)
        self.textEdit_nt_description.setObjectName(u"textEdit_nt_description")

        self.gridLayout.addWidget(self.textEdit_nt_description, 3, 1, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.horizontalLayout_50 = QHBoxLayout()
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.dateTimeEdit_nt = QDateTimeEdit(self.gridLayoutWidget)
        self.dateTimeEdit_nt.setObjectName(u"dateTimeEdit_nt")
        self.dateTimeEdit_nt.setEnabled(False)
        self.dateTimeEdit_nt.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_50.addWidget(self.dateTimeEdit_nt)

        self.horizontalSpacer_34 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_50.addItem(self.horizontalSpacer_34)

        self.checkBox_nt_add_time = QCheckBox(self.gridLayoutWidget)
        self.checkBox_nt_add_time.setObjectName(u"checkBox_nt_add_time")
        self.checkBox_nt_add_time.setEnabled(False)
        self.checkBox_nt_add_time.setMinimumSize(QSize(137, 0))

        self.horizontalLayout_50.addWidget(self.checkBox_nt_add_time)


        self.gridLayout.addLayout(self.horizontalLayout_50, 4, 1, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.horizontalLayout_53 = QHBoxLayout()
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.label_nt_repeat = QLabel(self.gridLayoutWidget)
        self.label_nt_repeat.setObjectName(u"label_nt_repeat")
        self.label_nt_repeat.setEnabled(False)
        self.label_nt_repeat.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_53.addWidget(self.label_nt_repeat)

        self.horizontalSpacer_37 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_53.addItem(self.horizontalSpacer_37)

        self.checkBox_nt_repeat = QCheckBox(self.gridLayoutWidget)
        self.checkBox_nt_repeat.setObjectName(u"checkBox_nt_repeat")
        self.checkBox_nt_repeat.setEnabled(False)
        self.checkBox_nt_repeat.setMinimumSize(QSize(137, 0))

        self.horizontalLayout_53.addWidget(self.checkBox_nt_repeat)


        self.gridLayout.addLayout(self.horizontalLayout_53, 5, 1, 1, 1)

        self.lineEdit_nt_name = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_nt_name.setObjectName(u"lineEdit_nt_name")

        self.gridLayout.addWidget(self.lineEdit_nt_name, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.comboBox_nt_category = QComboBox(self.gridLayoutWidget)
        self.comboBox_nt_category.setObjectName(u"comboBox_nt_category")
        self.comboBox_nt_category.setEnabled(True)

        self.horizontalLayout.addWidget(self.comboBox_nt_category)

        self.horizontalSpacer = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_nt_new_cat = QPushButton(self.gridLayoutWidget)
        self.pushButton_nt_new_cat.setObjectName(u"pushButton_nt_new_cat")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_nt_new_cat.sizePolicy().hasHeightForWidth())
        self.pushButton_nt_new_cat.setSizePolicy(sizePolicy)
        self.pushButton_nt_new_cat.setMaximumSize(QSize(110, 16777215))

        self.horizontalLayout.addWidget(self.pushButton_nt_new_cat)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.pushButton_nt_create_task = QPushButton(self.groupBox_new_task)
        self.pushButton_nt_create_task.setObjectName(u"pushButton_nt_create_task")
        self.pushButton_nt_create_task.setGeometry(QRect(370, 400, 151, 31))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_nt_create_task.sizePolicy().hasHeightForWidth())
        self.pushButton_nt_create_task.setSizePolicy(sizePolicy1)
        self.pushButton_nt_my_task = QPushButton(self.page)
        self.pushButton_nt_my_task.setObjectName(u"pushButton_nt_my_task")
        self.pushButton_nt_my_task.setGeometry(QRect(550, 20, 101, 31))
        self.pushButton_nt_not = QPushButton(self.page)
        self.pushButton_nt_not.setObjectName(u"pushButton_nt_not")
        self.pushButton_nt_not.setGeometry(QRect(550, 60, 101, 31))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.groupBox_mt = QGroupBox(self.page_2)
        self.groupBox_mt.setObjectName(u"groupBox_mt")
        self.groupBox_mt.setGeometry(QRect(10, 10, 531, 501))
        self.tabWidget = QTabWidget(self.groupBox_mt)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 20, 501, 471))
        self.tabWidget.setMinimumSize(QSize(125, 0))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayoutWidget_4 = QWidget(self.tab)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 10, 471, 341))
        self.verticalLayout_6 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.comboBox_mt_plan_all = QComboBox(self.verticalLayoutWidget_4)
        self.comboBox_mt_plan_all.setObjectName(u"comboBox_mt_plan_all")

        self.verticalLayout_6.addWidget(self.comboBox_mt_plan_all)

        self.frame_mt_plan = QFrame(self.verticalLayoutWidget_4)
        self.frame_mt_plan.setObjectName(u"frame_mt_plan")
        self.frame_mt_plan.setEnabled(False)
        self.frame_mt_plan.setFrameShape(QFrame.Shape.Box)
        self.frame_mt_plan.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_mt_plan.setLineWidth(1)
        self.gridLayoutWidget_3 = QWidget(self.frame_mt_plan)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 10, 441, 298))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_15 = QLabel(self.gridLayoutWidget_3)
        self.label_15.setObjectName(u"label_15")

        self.verticalLayout_7.addWidget(self.label_15)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_3)


        self.gridLayout_3.addLayout(self.verticalLayout_7, 3, 0, 1, 1)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_mt_plan_repeat = QLabel(self.gridLayoutWidget_3)
        self.label_mt_plan_repeat.setObjectName(u"label_mt_plan_repeat")
        self.label_mt_plan_repeat.setEnabled(False)
        self.label_mt_plan_repeat.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_26.addWidget(self.label_mt_plan_repeat)

        self.horizontalSpacer_14 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_14)

        self.checkBox_mt_plan_add_repet = QCheckBox(self.gridLayoutWidget_3)
        self.checkBox_mt_plan_add_repet.setObjectName(u"checkBox_mt_plan_add_repet")
        self.checkBox_mt_plan_add_repet.setEnabled(False)
        self.checkBox_mt_plan_add_repet.setMinimumSize(QSize(137, 0))

        self.horizontalLayout_26.addWidget(self.checkBox_mt_plan_add_repet)


        self.gridLayout_3.addLayout(self.horizontalLayout_26, 5, 1, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.comboBox_mt_plan_cat = QComboBox(self.gridLayoutWidget_3)
        self.comboBox_mt_plan_cat.setObjectName(u"comboBox_mt_plan_cat")
        self.comboBox_mt_plan_cat.setEnabled(False)

        self.horizontalLayout_11.addWidget(self.comboBox_mt_plan_cat)

        self.horizontalSpacer_4 = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_4)

        self.pushButton_mt_plan_new_cat = QPushButton(self.gridLayoutWidget_3)
        self.pushButton_mt_plan_new_cat.setObjectName(u"pushButton_mt_plan_new_cat")
        self.pushButton_mt_plan_new_cat.setEnabled(False)
        sizePolicy.setHeightForWidth(self.pushButton_mt_plan_new_cat.sizePolicy().hasHeightForWidth())
        self.pushButton_mt_plan_new_cat.setSizePolicy(sizePolicy)
        self.pushButton_mt_plan_new_cat.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_11.addWidget(self.pushButton_mt_plan_new_cat)


        self.gridLayout_3.addLayout(self.horizontalLayout_11, 2, 1, 1, 1)

        self.label_13 = QLabel(self.gridLayoutWidget_3)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_3.addWidget(self.label_13, 0, 0, 1, 1)

        self.label_17 = QLabel(self.gridLayoutWidget_3)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_3.addWidget(self.label_17, 1, 0, 1, 1)

        self.textEdit_mt_plan_description = QTextEdit(self.gridLayoutWidget_3)
        self.textEdit_mt_plan_description.setObjectName(u"textEdit_mt_plan_description")
        self.textEdit_mt_plan_description.setEnabled(False)

        self.gridLayout_3.addWidget(self.textEdit_mt_plan_description, 3, 1, 1, 1)

        self.lineEdit__mt_plan_name = QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit__mt_plan_name.setObjectName(u"lineEdit__mt_plan_name")
        self.lineEdit__mt_plan_name.setEnabled(False)

        self.gridLayout_3.addWidget(self.lineEdit__mt_plan_name, 0, 1, 1, 1)

        self.label_14 = QLabel(self.gridLayoutWidget_3)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_3.addWidget(self.label_14, 2, 0, 1, 1)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.comboBox_mt_plan_prior = QComboBox(self.gridLayoutWidget_3)
        self.comboBox_mt_plan_prior.setObjectName(u"comboBox_mt_plan_prior")
        self.comboBox_mt_plan_prior.setEnabled(False)

        self.horizontalLayout_14.addWidget(self.comboBox_mt_plan_prior)


        self.gridLayout_3.addLayout(self.horizontalLayout_14, 1, 1, 1, 1)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.dateTimeEdit_mt_plan = QDateTimeEdit(self.gridLayoutWidget_3)
        self.dateTimeEdit_mt_plan.setObjectName(u"dateTimeEdit_mt_plan")
        self.dateTimeEdit_mt_plan.setEnabled(False)
        self.dateTimeEdit_mt_plan.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_27.addWidget(self.dateTimeEdit_mt_plan)

        self.horizontalSpacer_15 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_15)

        self.checkBox_mt_plan_add_timer = QCheckBox(self.gridLayoutWidget_3)
        self.checkBox_mt_plan_add_timer.setObjectName(u"checkBox_mt_plan_add_timer")
        self.checkBox_mt_plan_add_timer.setEnabled(False)
        self.checkBox_mt_plan_add_timer.setMinimumSize(QSize(137, 0))

        self.horizontalLayout_27.addWidget(self.checkBox_mt_plan_add_timer)


        self.gridLayout_3.addLayout(self.horizontalLayout_27, 4, 1, 1, 1)


        self.verticalLayout_6.addWidget(self.frame_mt_plan)

        self.horizontalLayoutWidget_6 = QWidget(self.tab)
        self.horizontalLayoutWidget_6.setObjectName(u"horizontalLayoutWidget_6")
        self.horizontalLayoutWidget_6.setGeometry(QRect(10, 350, 471, 91))
        self.horizontalLayout_15 = QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_5)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.pushButton_mt_plan_change_task = QPushButton(self.horizontalLayoutWidget_6)
        self.pushButton_mt_plan_change_task.setObjectName(u"pushButton_mt_plan_change_task")
        self.pushButton_mt_plan_change_task.setMinimumSize(QSize(125, 0))
        self.pushButton_mt_plan_change_task.setMaximumSize(QSize(120, 16777215))

        self.verticalLayout_9.addWidget(self.pushButton_mt_plan_change_task)

        self.pushButton_mt_plan_start = QPushButton(self.horizontalLayoutWidget_6)
        self.pushButton_mt_plan_start.setObjectName(u"pushButton_mt_plan_start")
        self.pushButton_mt_plan_start.setMinimumSize(QSize(125, 0))
        self.pushButton_mt_plan_start.setMaximumSize(QSize(120, 16777215))

        self.verticalLayout_9.addWidget(self.pushButton_mt_plan_start)

        self.pushButton_mt_plan_del = QPushButton(self.horizontalLayoutWidget_6)
        self.pushButton_mt_plan_del.setObjectName(u"pushButton_mt_plan_del")

        self.verticalLayout_9.addWidget(self.pushButton_mt_plan_del)


        self.horizontalLayout_15.addLayout(self.verticalLayout_9)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayoutWidget = QWidget(self.tab_2)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 471, 341))
        self.verticalLayout_mt_proc = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_mt_proc.setSpacing(6)
        self.verticalLayout_mt_proc.setObjectName(u"verticalLayout_mt_proc")
        self.verticalLayout_mt_proc.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_mt_proc.setContentsMargins(0, 0, 0, 0)
        self.comboBox_mt_proc_all = QComboBox(self.verticalLayoutWidget)
        self.comboBox_mt_proc_all.setObjectName(u"comboBox_mt_proc_all")

        self.verticalLayout_mt_proc.addWidget(self.comboBox_mt_proc_all)

        self.frame_mt_proc = QFrame(self.verticalLayoutWidget)
        self.frame_mt_proc.setObjectName(u"frame_mt_proc")
        self.frame_mt_proc.setEnabled(False)
        self.frame_mt_proc.setFrameShape(QFrame.Shape.Box)
        self.frame_mt_proc.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_mt_proc.setLineWidth(1)
        self.gridLayoutWidget_2 = QWidget(self.frame_mt_proc)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 10, 441, 298))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.gridLayoutWidget_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.label_10 = QLabel(self.gridLayoutWidget_2)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 2, 0, 1, 1)

        self.lineEdit_mt_proc_name = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_mt_proc_name.setObjectName(u"lineEdit_mt_proc_name")
        self.lineEdit_mt_proc_name.setEnabled(False)

        self.gridLayout_2.addWidget(self.lineEdit_mt_proc_name, 0, 1, 1, 1)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_mt_proc_repeat = QLabel(self.gridLayoutWidget_2)
        self.label_mt_proc_repeat.setObjectName(u"label_mt_proc_repeat")
        self.label_mt_proc_repeat.setEnabled(False)
        self.label_mt_proc_repeat.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_23.addWidget(self.label_mt_proc_repeat)

        self.horizontalSpacer_12 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_12)

        self.checkBox_mt_proc_add_repeat = QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_mt_proc_add_repeat.setObjectName(u"checkBox_mt_proc_add_repeat")
        self.checkBox_mt_proc_add_repeat.setEnabled(False)
        self.checkBox_mt_proc_add_repeat.setMinimumSize(QSize(137, 0))

        self.horizontalLayout_23.addWidget(self.checkBox_mt_proc_add_repeat)


        self.gridLayout_2.addLayout(self.horizontalLayout_23, 5, 1, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.comboBox_mt_proc_cat = QComboBox(self.gridLayoutWidget_2)
        self.comboBox_mt_proc_cat.setObjectName(u"comboBox_mt_proc_cat")
        self.comboBox_mt_proc_cat.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.comboBox_mt_proc_cat)

        self.horizontalSpacer_2 = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.pushButton_mt_proc_new_cat = QPushButton(self.gridLayoutWidget_2)
        self.pushButton_mt_proc_new_cat.setObjectName(u"pushButton_mt_proc_new_cat")
        self.pushButton_mt_proc_new_cat.setEnabled(False)
        sizePolicy.setHeightForWidth(self.pushButton_mt_proc_new_cat.sizePolicy().hasHeightForWidth())
        self.pushButton_mt_proc_new_cat.setSizePolicy(sizePolicy)
        self.pushButton_mt_proc_new_cat.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_5.addWidget(self.pushButton_mt_proc_new_cat)


        self.gridLayout_2.addLayout(self.horizontalLayout_5, 2, 1, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_5 = QLabel(self.gridLayoutWidget_2)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_4.addWidget(self.label_5)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.gridLayout_2.addLayout(self.verticalLayout_4, 3, 0, 1, 1)

        self.textEdit_mt_proc_description = QTextEdit(self.gridLayoutWidget_2)
        self.textEdit_mt_proc_description.setObjectName(u"textEdit_mt_proc_description")
        self.textEdit_mt_proc_description.setEnabled(False)

        self.gridLayout_2.addWidget(self.textEdit_mt_proc_description, 3, 1, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.comboBox_mt_proc_prior = QComboBox(self.gridLayoutWidget_2)
        self.comboBox_mt_proc_prior.setObjectName(u"comboBox_mt_proc_prior")
        self.comboBox_mt_proc_prior.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.comboBox_mt_proc_prior)


        self.gridLayout_2.addLayout(self.horizontalLayout_7, 1, 1, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.dateTimeEdit_mt_proc = QDateTimeEdit(self.gridLayoutWidget_2)
        self.dateTimeEdit_mt_proc.setObjectName(u"dateTimeEdit_mt_proc")
        self.dateTimeEdit_mt_proc.setEnabled(False)
        self.dateTimeEdit_mt_proc.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_25.addWidget(self.dateTimeEdit_mt_proc)

        self.horizontalSpacer_13 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_13)

        self.checkBox_mt_proc_add_time = QCheckBox(self.gridLayoutWidget_2)
        self.checkBox_mt_proc_add_time.setObjectName(u"checkBox_mt_proc_add_time")
        self.checkBox_mt_proc_add_time.setEnabled(False)
        self.checkBox_mt_proc_add_time.setMinimumSize(QSize(137, 0))

        self.horizontalLayout_25.addWidget(self.checkBox_mt_proc_add_time)


        self.gridLayout_2.addLayout(self.horizontalLayout_25, 4, 1, 1, 1)


        self.verticalLayout_mt_proc.addWidget(self.frame_mt_proc)

        self.horizontalLayoutWidget_4 = QWidget(self.tab_2)
        self.horizontalLayoutWidget_4.setObjectName(u"horizontalLayoutWidget_4")
        self.horizontalLayoutWidget_4.setGeometry(QRect(10, 350, 471, 91))
        self.horizontalLayout_9 = QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.groupBox_mt_proc__timer = QGroupBox(self.horizontalLayoutWidget_4)
        self.groupBox_mt_proc__timer.setObjectName(u"groupBox_mt_proc__timer")
        self.groupBox_mt_proc__timer.setMinimumSize(QSize(260, 0))
        self.groupBox_mt_proc__timer.setMaximumSize(QSize(260, 16777215))
        self.verticalLayoutWidget_2 = QWidget(self.groupBox_mt_proc__timer)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 20, 241, 71))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.pushButton_mt_proc_start_timer = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_mt_proc_start_timer.setObjectName(u"pushButton_mt_proc_start_timer")
        self.pushButton_mt_proc_start_timer.setMaximumSize(QSize(110, 16777215))

        self.horizontalLayout_10.addWidget(self.pushButton_mt_proc_start_timer)

        self.pushButton_mt_proc_stop_timer = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_mt_proc_stop_timer.setObjectName(u"pushButton_mt_proc_stop_timer")

        self.horizontalLayout_10.addWidget(self.pushButton_mt_proc_stop_timer)

        self.pushButton_mt_proc_rem_timer = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_mt_proc_rem_timer.setObjectName(u"pushButton_mt_proc_rem_timer")

        self.horizontalLayout_10.addWidget(self.pushButton_mt_proc_rem_timer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_12 = QLabel(self.verticalLayoutWidget_2)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_8.addWidget(self.label_12)

        self.label_mt_proc_timer = QLabel(self.verticalLayoutWidget_2)
        self.label_mt_proc_timer.setObjectName(u"label_mt_proc_timer")

        self.horizontalLayout_8.addWidget(self.label_mt_proc_timer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_9.addWidget(self.groupBox_mt_proc__timer)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_3)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.pushButton_mt_proc_change_task = QPushButton(self.horizontalLayoutWidget_4)
        self.pushButton_mt_proc_change_task.setObjectName(u"pushButton_mt_proc_change_task")
        self.pushButton_mt_proc_change_task.setMinimumSize(QSize(125, 0))
        self.pushButton_mt_proc_change_task.setMaximumSize(QSize(110, 16777215))

        self.verticalLayout_5.addWidget(self.pushButton_mt_proc_change_task)

        self.pushButton_mt_proc_finish = QPushButton(self.horizontalLayoutWidget_4)
        self.pushButton_mt_proc_finish.setObjectName(u"pushButton_mt_proc_finish")
        self.pushButton_mt_proc_finish.setMinimumSize(QSize(125, 0))
        self.pushButton_mt_proc_finish.setMaximumSize(QSize(110, 16777215))

        self.verticalLayout_5.addWidget(self.pushButton_mt_proc_finish)

        self.pushButton_mt_proc_del_task = QPushButton(self.horizontalLayoutWidget_4)
        self.pushButton_mt_proc_del_task.setObjectName(u"pushButton_mt_proc_del_task")

        self.verticalLayout_5.addWidget(self.pushButton_mt_proc_del_task)


        self.horizontalLayout_9.addLayout(self.verticalLayout_5)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayoutWidget_6 = QWidget(self.tab_3)
        self.verticalLayoutWidget_6.setObjectName(u"verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(10, 10, 471, 361))
        self.verticalLayout_10 = QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_10.setSpacing(6)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.comboBox_mt_done_all = QComboBox(self.verticalLayoutWidget_6)
        self.comboBox_mt_done_all.setObjectName(u"comboBox_mt_done_all")

        self.verticalLayout_10.addWidget(self.comboBox_mt_done_all)

        self.frame_mt_done = QFrame(self.verticalLayoutWidget_6)
        self.frame_mt_done.setObjectName(u"frame_mt_done")
        self.frame_mt_done.setEnabled(False)
        self.frame_mt_done.setFrameShape(QFrame.Shape.Box)
        self.frame_mt_done.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_mt_done.setLineWidth(1)
        self.gridLayoutWidget_4 = QWidget(self.frame_mt_done)
        self.gridLayoutWidget_4.setObjectName(u"gridLayoutWidget_4")
        self.gridLayoutWidget_4.setGeometry(QRect(10, 10, 441, 311))
        self.gridLayout_4 = QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.comboBox_mt_done_cat = QComboBox(self.gridLayoutWidget_4)
        self.comboBox_mt_done_cat.setObjectName(u"comboBox_mt_done_cat")
        self.comboBox_mt_done_cat.setEnabled(False)

        self.horizontalLayout_18.addWidget(self.comboBox_mt_done_cat)

        self.horizontalSpacer_6 = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_6)

        self.pushButton_mt_done_new_cat = QPushButton(self.gridLayoutWidget_4)
        self.pushButton_mt_done_new_cat.setObjectName(u"pushButton_mt_done_new_cat")
        self.pushButton_mt_done_new_cat.setEnabled(False)
        sizePolicy.setHeightForWidth(self.pushButton_mt_done_new_cat.sizePolicy().hasHeightForWidth())
        self.pushButton_mt_done_new_cat.setSizePolicy(sizePolicy)
        self.pushButton_mt_done_new_cat.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_18.addWidget(self.pushButton_mt_done_new_cat)


        self.gridLayout_4.addLayout(self.horizontalLayout_18, 2, 1, 1, 1)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.dateTimeEdit_mt_done = QDateTimeEdit(self.gridLayoutWidget_4)
        self.dateTimeEdit_mt_done.setObjectName(u"dateTimeEdit_mt_done")
        self.dateTimeEdit_mt_done.setEnabled(False)
        self.dateTimeEdit_mt_done.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_19.addWidget(self.dateTimeEdit_mt_done)

        self.horizontalSpacer_10 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_10)

        self.checkBox_mt_done_add_timer = QCheckBox(self.gridLayoutWidget_4)
        self.checkBox_mt_done_add_timer.setObjectName(u"checkBox_mt_done_add_timer")
        self.checkBox_mt_done_add_timer.setEnabled(False)
        self.checkBox_mt_done_add_timer.setMinimumSize(QSize(137, 0))

        self.horizontalLayout_19.addWidget(self.checkBox_mt_done_add_timer)


        self.gridLayout_4.addLayout(self.horizontalLayout_19, 4, 1, 1, 1)

        self.label_20 = QLabel(self.gridLayoutWidget_4)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_4.addWidget(self.label_20, 0, 0, 1, 1)

        self.label_24 = QLabel(self.gridLayoutWidget_4)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_4.addWidget(self.label_24, 1, 0, 1, 1)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.comboBox_mt_done_prior = QComboBox(self.gridLayoutWidget_4)
        self.comboBox_mt_done_prior.setObjectName(u"comboBox_mt_done_prior")
        self.comboBox_mt_done_prior.setEnabled(False)

        self.horizontalLayout_21.addWidget(self.comboBox_mt_done_prior)


        self.gridLayout_4.addLayout(self.horizontalLayout_21, 1, 1, 1, 1)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_22 = QLabel(self.gridLayoutWidget_4)
        self.label_22.setObjectName(u"label_22")

        self.verticalLayout_11.addWidget(self.label_22)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_4)


        self.gridLayout_4.addLayout(self.verticalLayout_11, 3, 0, 1, 1)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_mt_done_repeat = QLabel(self.gridLayoutWidget_4)
        self.label_mt_done_repeat.setObjectName(u"label_mt_done_repeat")
        self.label_mt_done_repeat.setEnabled(False)
        self.label_mt_done_repeat.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_20.addWidget(self.label_mt_done_repeat)

        self.horizontalSpacer_11 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_11)

        self.checkBox_mt_done_add_repeat = QCheckBox(self.gridLayoutWidget_4)
        self.checkBox_mt_done_add_repeat.setObjectName(u"checkBox_mt_done_add_repeat")
        self.checkBox_mt_done_add_repeat.setEnabled(False)
        self.checkBox_mt_done_add_repeat.setMinimumSize(QSize(137, 0))

        self.horizontalLayout_20.addWidget(self.checkBox_mt_done_add_repeat)


        self.gridLayout_4.addLayout(self.horizontalLayout_20, 5, 1, 1, 1)

        self.lineEdit_mt_done_name = QLineEdit(self.gridLayoutWidget_4)
        self.lineEdit_mt_done_name.setObjectName(u"lineEdit_mt_done_name")
        self.lineEdit_mt_done_name.setEnabled(False)

        self.gridLayout_4.addWidget(self.lineEdit_mt_done_name, 0, 1, 1, 1)

        self.textEdit_mt_done_description = QTextEdit(self.gridLayoutWidget_4)
        self.textEdit_mt_done_description.setObjectName(u"textEdit_mt_done_description")
        self.textEdit_mt_done_description.setEnabled(False)

        self.gridLayout_4.addWidget(self.textEdit_mt_done_description, 3, 1, 1, 1)

        self.label_21 = QLabel(self.gridLayoutWidget_4)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_4.addWidget(self.label_21, 2, 0, 1, 1)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_8)

        self.label_task_fire = QLabel(self.gridLayoutWidget_4)
        self.label_task_fire.setObjectName(u"label_task_fire")

        self.horizontalLayout_17.addWidget(self.label_task_fire)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_9)


        self.gridLayout_4.addLayout(self.horizontalLayout_17, 6, 1, 1, 1)


        self.verticalLayout_10.addWidget(self.frame_mt_done)

        self.horizontalLayoutWidget_7 = QWidget(self.tab_3)
        self.horizontalLayoutWidget_7.setObjectName(u"horizontalLayoutWidget_7")
        self.horizontalLayoutWidget_7.setGeometry(QRect(10, 370, 471, 71))
        self.horizontalLayout_22 = QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.groupBox_5 = QGroupBox(self.horizontalLayoutWidget_7)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMinimumSize(QSize(260, 0))
        self.groupBox_5.setMaximumSize(QSize(260, 16777215))
        self.verticalLayoutWidget_7 = QWidget(self.groupBox_5)
        self.verticalLayoutWidget_7.setObjectName(u"verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(10, 20, 241, 41))
        self.verticalLayout_12 = QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_12.setSpacing(2)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_25 = QLabel(self.verticalLayoutWidget_7)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_24.addWidget(self.label_25)

        self.label_mt_done_timer = QLabel(self.verticalLayoutWidget_7)
        self.label_mt_done_timer.setObjectName(u"label_mt_done_timer")

        self.horizontalLayout_24.addWidget(self.label_mt_done_timer)


        self.verticalLayout_12.addLayout(self.horizontalLayout_24)


        self.horizontalLayout_22.addWidget(self.groupBox_5)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_7)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.pushButton_mt_done_recover_task = QPushButton(self.horizontalLayoutWidget_7)
        self.pushButton_mt_done_recover_task.setObjectName(u"pushButton_mt_done_recover_task")
        self.pushButton_mt_done_recover_task.setMinimumSize(QSize(125, 0))
        self.pushButton_mt_done_recover_task.setMaximumSize(QSize(120, 16777215))

        self.verticalLayout_13.addWidget(self.pushButton_mt_done_recover_task)

        self.pushButton_mt_done_del_task = QPushButton(self.horizontalLayoutWidget_7)
        self.pushButton_mt_done_del_task.setObjectName(u"pushButton_mt_done_del_task")

        self.verticalLayout_13.addWidget(self.pushButton_mt_done_del_task)


        self.horizontalLayout_22.addLayout(self.verticalLayout_13)

        self.tabWidget.addTab(self.tab_3, "")
        self.pushButton_mt_crete_task = QPushButton(self.page_2)
        self.pushButton_mt_crete_task.setObjectName(u"pushButton_mt_crete_task")
        self.pushButton_mt_crete_task.setGeometry(QRect(550, 20, 101, 31))
        self.pushButton_mt_not = QPushButton(self.page_2)
        self.pushButton_mt_not.setObjectName(u"pushButton_mt_not")
        self.pushButton_mt_not.setGeometry(QRect(550, 60, 101, 31))
        self.progressBar = QProgressBar(self.page_2)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(550, 470, 111, 23))
        self.progressBar.setValue(24)
        self.label_63 = QLabel(self.page_2)
        self.label_63.setObjectName(u"label_63")
        self.label_63.setGeometry(QRect(550, 430, 91, 31))
        self.label_63.setWordWrap(False)
        self.label_63.setMargin(0)
        self.label_63.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.stackedWidget.addWidget(self.page_2)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.groupBox_notices = QGroupBox(self.page_5)
        self.groupBox_notices.setObjectName(u"groupBox_notices")
        self.groupBox_notices.setGeometry(QRect(10, 10, 531, 471))
        self.toolBox_not = QToolBox(self.groupBox_notices)
        self.toolBox_not.setObjectName(u"toolBox_not")
        self.toolBox_not.setGeometry(QRect(10, 20, 501, 441))
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.page_6.setGeometry(QRect(0, 0, 501, 411))
        self.verticalLayoutWidget_5 = QWidget(self.page_6)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(0, 0, 501, 161))
        self.verticalLayout_14 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.textBrowser = QTextBrowser(self.verticalLayoutWidget_5)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_14.addWidget(self.textBrowser)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_attach_not = QPushButton(self.verticalLayoutWidget_5)
        self.pushButton_attach_not.setObjectName(u"pushButton_attach_not")

        self.horizontalLayout_2.addWidget(self.pushButton_attach_not)

        self.pushButton_del_not = QPushButton(self.verticalLayoutWidget_5)
        self.pushButton_del_not.setObjectName(u"pushButton_del_not")

        self.horizontalLayout_2.addWidget(self.pushButton_del_not)

        self.pushButton_save_not = QPushButton(self.verticalLayoutWidget_5)
        self.pushButton_save_not.setObjectName(u"pushButton_save_not")

        self.horizontalLayout_2.addWidget(self.pushButton_save_not)


        self.verticalLayout_14.addLayout(self.horizontalLayout_2)

        self.toolBox_not.addItem(self.page_6, u"Page 1")
        self.pushButton_cret_tsk_not = QPushButton(self.page_5)
        self.pushButton_cret_tsk_not.setObjectName(u"pushButton_cret_tsk_not")
        self.pushButton_cret_tsk_not.setGeometry(QRect(550, 20, 101, 31))
        self.pushButton_my_task_not = QPushButton(self.page_5)
        self.pushButton_my_task_not.setObjectName(u"pushButton_my_task_not")
        self.pushButton_my_task_not.setGeometry(QRect(550, 60, 101, 31))
        self.stackedWidget.addWidget(self.page_5)
        self.dockWidget_notice = QDockWidget(Widget)
        self.dockWidget_notice.setObjectName(u"dockWidget_notice")
        self.dockWidget_notice.setGeometry(QRect(700, 10, 211, 121))
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.label_atached_note = QLabel(self.dockWidgetContents)
        self.label_atached_note.setObjectName(u"label_atached_note")
        self.label_atached_note.setGeometry(QRect(10, 10, 191, 71))
        self.dockWidget_notice.setWidget(self.dockWidgetContents)
        self.groupBox_main_timer = QGroupBox(Widget)
        self.groupBox_main_timer.setObjectName(u"groupBox_main_timer")
        self.groupBox_main_timer.setGeometry(QRect(700, 180, 211, 181))
        self.formLayoutWidget = QWidget(self.groupBox_main_timer)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 20, 191, 51))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.formLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_8)

        self.label_59 = QLabel(self.formLayoutWidget)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setFrameShape(QFrame.Shape.NoFrame)
        self.label_59.setFrameShadow(QFrame.Shadow.Plain)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_59)

        self.label_main_timer_passed = QLabel(self.formLayoutWidget)
        self.label_main_timer_passed.setObjectName(u"label_main_timer_passed")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_main_timer_passed)

        self.label_main_timer_last = QLabel(self.formLayoutWidget)
        self.label_main_timer_last.setObjectName(u"label_main_timer_last")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.label_main_timer_last)

        self.verticalLayoutWidget_3 = QWidget(self.groupBox_main_timer)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(40, 80, 160, 86))
        self.verticalLayout_8 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.pushButton_19 = QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_19.setObjectName(u"pushButton_19")

        self.verticalLayout_8.addWidget(self.pushButton_19)

        self.pushButton_20 = QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_20.setObjectName(u"pushButton_20")

        self.verticalLayout_8.addWidget(self.pushButton_20)

        self.pushButton_21 = QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_21.setObjectName(u"pushButton_21")

        self.verticalLayout_8.addWidget(self.pushButton_21)

#if QT_CONFIG(shortcut)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(Widget)

        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(2)
        self.toolBox_not.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.groupBox_new_task.setTitle(QCoreApplication.translate("Widget", u"\u041d\u043e\u0432\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435:", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435:", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442:", None))
        self.checkBox_nt_add_time.setText(QCoreApplication.translate("Widget", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0440\u043e\u043a", None))
        self.label.setText(QCoreApplication.translate("Widget", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f:", None))
        self.label_nt_repeat.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.checkBox_nt_repeat.setText(QCoreApplication.translate("Widget", u"\u041f\u043e\u0432\u0442\u043e\u0440\u044f\u0435\u043c\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430", None))
        self.pushButton_nt_new_cat.setText(QCoreApplication.translate("Widget", u"\u041d\u043e\u0432\u0430\u044f \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f", None))
        self.pushButton_nt_create_task.setText(QCoreApplication.translate("Widget", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443", None))
        self.pushButton_nt_my_task.setText(QCoreApplication.translate("Widget", u"\u041c\u043e\u0438 \u0437\u0430\u0434\u0430\u0447\u0438", None))
        self.pushButton_nt_not.setText(QCoreApplication.translate("Widget", u"\u0417\u0430\u043c\u0435\u0442\u043a\u0438", None))
        self.groupBox_mt.setTitle(QCoreApplication.translate("Widget", u"\u041c\u043e\u0438 \u0437\u0430\u0434\u0430\u0447\u0438:", None))
        self.label_15.setText(QCoreApplication.translate("Widget", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435:", None))
        self.label_mt_plan_repeat.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.checkBox_mt_plan_add_repet.setText(QCoreApplication.translate("Widget", u"\u041f\u043e\u0432\u0442\u043e\u0440\u044f\u0435\u043c\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430", None))
        self.pushButton_mt_plan_new_cat.setText(QCoreApplication.translate("Widget", u"\u041d\u043e\u0432\u0430\u044f \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f", None))
        self.label_13.setText(QCoreApplication.translate("Widget", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435:", None))
        self.label_17.setText(QCoreApplication.translate("Widget", u"\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442:", None))
        self.label_14.setText(QCoreApplication.translate("Widget", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f:", None))
        self.checkBox_mt_plan_add_timer.setText(QCoreApplication.translate("Widget", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0440\u043e\u043a", None))
        self.pushButton_mt_plan_change_task.setText(QCoreApplication.translate("Widget", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443", None))
        self.pushButton_mt_plan_start.setText(QCoreApplication.translate("Widget", u"\u041d\u0430\u0447\u0430\u0442\u044c \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435", None))
        self.pushButton_mt_plan_del.setText(QCoreApplication.translate("Widget", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Widget", u"\u0417\u0430\u043f\u043b\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u043e", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435:", None))
        self.label_10.setText(QCoreApplication.translate("Widget", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f:", None))
        self.label_mt_proc_repeat.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.checkBox_mt_proc_add_repeat.setText(QCoreApplication.translate("Widget", u"\u041f\u043e\u0432\u0442\u043e\u0440\u044f\u0435\u043c\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430", None))
        self.pushButton_mt_proc_new_cat.setText(QCoreApplication.translate("Widget", u"\u041d\u043e\u0432\u0430\u044f \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435:", None))
        self.label_7.setText(QCoreApplication.translate("Widget", u"\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442:", None))
        self.checkBox_mt_proc_add_time.setText(QCoreApplication.translate("Widget", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0440\u043e\u043a", None))
        self.groupBox_mt_proc__timer.setTitle(QCoreApplication.translate("Widget", u"\u0422\u0430\u0439\u043c\u0435\u0440 \u0440\u0430\u0431\u043e\u0442\u044b \u043d\u0430\u0434 \u0437\u0430\u0434\u0430\u0447\u0435\u0439", None))
        self.pushButton_mt_proc_start_timer.setText(QCoreApplication.translate("Widget", u"\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c", None))
        self.pushButton_mt_proc_stop_timer.setText(QCoreApplication.translate("Widget", u"\u041e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c", None))
        self.pushButton_mt_proc_rem_timer.setText(QCoreApplication.translate("Widget", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c", None))
        self.label_12.setText(QCoreApplication.translate("Widget", u"\u0412\u0440\u0435\u043c\u044f:", None))
        self.label_mt_proc_timer.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.pushButton_mt_proc_change_task.setText(QCoreApplication.translate("Widget", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443", None))
        self.pushButton_mt_proc_finish.setText(QCoreApplication.translate("Widget", u"\u0417\u0430\u0432\u0435\u0440\u0448\u0438\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443", None))
        self.pushButton_mt_proc_del_task.setText(QCoreApplication.translate("Widget", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Widget", u"\u0412 \u043f\u0440\u043e\u0446\u0435\u0441\u0441\u0435", None))
        self.pushButton_mt_done_new_cat.setText(QCoreApplication.translate("Widget", u"\u041d\u043e\u0432\u0430\u044f \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f", None))
        self.checkBox_mt_done_add_timer.setText(QCoreApplication.translate("Widget", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0440\u043e\u043a", None))
        self.label_20.setText(QCoreApplication.translate("Widget", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435:", None))
        self.label_24.setText(QCoreApplication.translate("Widget", u"\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442:", None))
        self.label_22.setText(QCoreApplication.translate("Widget", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435:", None))
        self.label_mt_done_repeat.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.checkBox_mt_done_add_repeat.setText(QCoreApplication.translate("Widget", u"\u041f\u043e\u0432\u0442\u043e\u0440\u044f\u0435\u043c\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430", None))
        self.label_21.setText(QCoreApplication.translate("Widget", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f:", None))
        self.label_task_fire.setText(QCoreApplication.translate("Widget", u"\u0417\u0430\u0434\u0430\u0447\u0430 \u043f\u0440\u043e\u0441\u0440\u043e\u0447\u0435\u043d\u0430!", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Widget", u"\u0422\u0430\u0439\u043c\u0435\u0440 \u0440\u0430\u0431\u043e\u0442\u044b \u043d\u0430\u0434 \u0437\u0430\u0434\u0430\u0447\u0435\u0439", None))
        self.label_25.setText(QCoreApplication.translate("Widget", u"\u0412\u0440\u0435\u043c\u044f:", None))
        self.label_mt_done_timer.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.pushButton_mt_done_recover_task.setText(QCoreApplication.translate("Widget", u"\u0412\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443", None))
        self.pushButton_mt_done_del_task.setText(QCoreApplication.translate("Widget", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Widget", u"\u0412\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u043e", None))
        self.pushButton_mt_crete_task.setText(QCoreApplication.translate("Widget", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443", None))
        self.pushButton_mt_not.setText(QCoreApplication.translate("Widget", u"\u0417\u0430\u043c\u0435\u0442\u043a\u0438", None))
        self.label_63.setText(QCoreApplication.translate("Widget", u"\u041f\u0440\u043e\u0446\u0435\u0441<br>\u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f:", None))
        self.groupBox_notices.setTitle(QCoreApplication.translate("Widget", u"\u0417\u0430\u043c\u0435\u0442\u043a\u0438", None))
        self.pushButton_attach_not.setText(QCoreApplication.translate("Widget", u"\u0417\u0430\u043a\u0440\u0435\u043f\u0438\u0442\u044c", None))
        self.pushButton_del_not.setText(QCoreApplication.translate("Widget", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.pushButton_save_not.setText(QCoreApplication.translate("Widget", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.toolBox_not.setItemText(self.toolBox_not.indexOf(self.page_6), QCoreApplication.translate("Widget", u"Page 1", None))
        self.pushButton_cret_tsk_not.setText(QCoreApplication.translate("Widget", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443", None))
        self.pushButton_my_task_not.setText(QCoreApplication.translate("Widget", u"\u041c\u043e\u0438 \u0437\u0430\u0434\u0430\u0447\u0438", None))
        self.label_atached_note.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.groupBox_main_timer.setTitle(QCoreApplication.translate("Widget", u"\u0412\u0440\u0435\u043c\u044f \u0440\u0430\u0431\u043e\u0442\u044b", None))
        self.label_8.setText(QCoreApplication.translate("Widget", u"\u041f\u0440\u043e\u0448\u043b\u043e:", None))
        self.label_59.setText(QCoreApplication.translate("Widget", u"\u041e\u0441\u0442\u0430\u043b\u043e\u0441\u044c:", None))
        self.label_main_timer_passed.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.label_main_timer_last.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.pushButton_19.setText(QCoreApplication.translate("Widget", u"\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u0442\u0430\u0439\u043c\u0435\u0440", None))
        self.pushButton_20.setText(QCoreApplication.translate("Widget", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u0442\u0430\u0439\u043c\u0435\u0440", None))
        self.pushButton_21.setText(QCoreApplication.translate("Widget", u"\u041f\u043e\u0441\u043c\u043e\u0442\u0440\u0435\u0442\u044c \u0438\u0441\u0442\u043e\u0440\u0438\u044e", None))
    # retranslateUi

