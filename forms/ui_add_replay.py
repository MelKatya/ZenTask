from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QGroupBox, QHeaderView, QLabel,
    QSizePolicy, QTreeWidget, QTreeWidgetItem, QWidget)


class UiDialog(object):
    def setup_ui(self, Dialog):
        Dialog.setWindowTitle('Повтор')
        Dialog.resize(389, 301)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(30, 260, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setTitle('Добавить повтор')
        self.groupBox.setGeometry(QRect(10, 10, 361, 241))

        self.treeWidget_3 = QTreeWidget(self.groupBox)

        __qtreewidgetitem = QTreeWidgetItem(self.treeWidget_3)
        for i in range(31):
            QTreeWidgetItem(__qtreewidgetitem)


        __qtreewidgetitem1 = QTreeWidgetItem(self.treeWidget_3)
        for i in range(7):
            QTreeWidgetItem(__qtreewidgetitem1)

        ___week = self.treeWidget_3.topLevelItem(1)
        ___week.setText(0, 'Неделя')
        for i, day in zip(range(7), ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс')):
            ___qt = ___week.child(i)
            ___qt.setText(0, day)
        # ___qtreewidgetitem34 = ___week.child(0)
        # ___qtreewidgetitem34.setText(0, 'Пн')
        # ___qtreewidgetitem35 = ___week.child(1)
        # ___qtreewidgetitem35.setText(0, 'Вт')

        # # Добавляем 3 корневых элемента
        # root1 = QTreeWidgetItem(self.treeWidget_3, ["Корень 1"])
        # root2 = QTreeWidgetItem(self.treeWidget_3, ["Корень 2"])
        # root3 = QTreeWidgetItem(self.treeWidget_3, ["Неделя"])  # Третий корневой элемент (нужный вам)
        #
        # # Добавляем root3 в self.treeWidget_3 (это уже сделано выше, но можно явно)
        # self.treeWidget_3.addTopLevelItem(root3)
        #
        # # Добавляем 7 дочерних элементов к root3 (дни недели)
        # for day in ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"):
        #     child = QTreeWidgetItem(root3, [day])  # Создаем дочерний элемент

        __qtreewidgetitem2 = QTreeWidgetItem(self.treeWidget_3)
        for i in range(24):
            QTreeWidgetItem(__qtreewidgetitem2)


        self.treeWidget_3.setGeometry(QRect(10, 30, 141, 201))
        self.treeWidget_3.setAlternatingRowColors(True)
        self.treeWidget_3.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.treeWidget_3.setAnimated(True)
        self.treeWidget_3.setAllColumnsShowFocus(True)
        self.treeWidget_3.setHeaderHidden(True)
        ## клики
        self.treeWidget_3.itemClicked.connect(self.the_button_was_clicked)

        self.label = QLabel(self.groupBox)
        self.label.setText("Задача будет повторяться:")
        self.label.setGeometry(QRect(160, 30, 151, 31))
        self.label_2 = QLabel(self.groupBox)

        self.label_2.setGeometry(QRect(160, 50, 191, 41))
        # self.label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_2.setText('ggg')

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def the_button_was_clicked(self):
        print('ckck')

    def retranslateUi(self, Dialog):
        ___qtreewidgetitem = self.treeWidget_3.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"1", None));

        __sortingEnabled = self.treeWidget_3.isSortingEnabled()
        self.treeWidget_3.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget_3.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Dialog", u"\u041c\u0435\u0441\u044f\u0446", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Dialog", u"1", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("Dialog", u"2", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem1.child(2)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("Dialog", u"3", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem1.child(3)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("Dialog", u"4", None));
        ___qtreewidgetitem6 = ___qtreewidgetitem1.child(4)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("Dialog", u"5", None));
        ___qtreewidgetitem7 = ___qtreewidgetitem1.child(5)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("Dialog", u"6", None));
        ___qtreewidgetitem8 = ___qtreewidgetitem1.child(6)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("Dialog", u"7", None));
        ___qtreewidgetitem9 = ___qtreewidgetitem1.child(7)
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("Dialog", u"8", None));
        ___qtreewidgetitem10 = ___qtreewidgetitem1.child(8)
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("Dialog", u"9", None));
        ___qtreewidgetitem11 = ___qtreewidgetitem1.child(9)
        ___qtreewidgetitem11.setText(0, QCoreApplication.translate("Dialog", u"10", None));
        ___qtreewidgetitem12 = ___qtreewidgetitem1.child(10)
        ___qtreewidgetitem12.setText(0, QCoreApplication.translate("Dialog", u"11", None));
        ___qtreewidgetitem13 = ___qtreewidgetitem1.child(11)
        ___qtreewidgetitem13.setText(0, QCoreApplication.translate("Dialog", u"12", None));
        ___qtreewidgetitem14 = ___qtreewidgetitem1.child(12)
        ___qtreewidgetitem14.setText(0, QCoreApplication.translate("Dialog", u"13", None));
        ___qtreewidgetitem15 = ___qtreewidgetitem1.child(13)
        ___qtreewidgetitem15.setText(0, QCoreApplication.translate("Dialog", u"14", None));
        ___qtreewidgetitem16 = ___qtreewidgetitem1.child(14)
        ___qtreewidgetitem16.setText(0, QCoreApplication.translate("Dialog", u"15", None));
        ___qtreewidgetitem17 = ___qtreewidgetitem1.child(15)
        ___qtreewidgetitem17.setText(0, QCoreApplication.translate("Dialog", u"16", None));
        ___qtreewidgetitem18 = ___qtreewidgetitem1.child(16)
        ___qtreewidgetitem18.setText(0, QCoreApplication.translate("Dialog", u"17", None));
        ___qtreewidgetitem19 = ___qtreewidgetitem1.child(17)
        ___qtreewidgetitem19.setText(0, QCoreApplication.translate("Dialog", u"18", None));
        ___qtreewidgetitem20 = ___qtreewidgetitem1.child(18)
        ___qtreewidgetitem20.setText(0, QCoreApplication.translate("Dialog", u"19", None));
        ___qtreewidgetitem21 = ___qtreewidgetitem1.child(19)
        ___qtreewidgetitem21.setText(0, QCoreApplication.translate("Dialog", u"20", None));
        ___qtreewidgetitem22 = ___qtreewidgetitem1.child(20)
        ___qtreewidgetitem22.setText(0, QCoreApplication.translate("Dialog", u"21", None));
        ___qtreewidgetitem23 = ___qtreewidgetitem1.child(21)
        ___qtreewidgetitem23.setText(0, QCoreApplication.translate("Dialog", u"22", None));
        ___qtreewidgetitem24 = ___qtreewidgetitem1.child(22)
        ___qtreewidgetitem24.setText(0, QCoreApplication.translate("Dialog", u"23", None));
        ___qtreewidgetitem25 = ___qtreewidgetitem1.child(23)
        ___qtreewidgetitem25.setText(0, QCoreApplication.translate("Dialog", u"24", None));
        ___qtreewidgetitem26 = ___qtreewidgetitem1.child(24)
        ___qtreewidgetitem26.setText(0, QCoreApplication.translate("Dialog", u"25", None));
        ___qtreewidgetitem27 = ___qtreewidgetitem1.child(25)
        ___qtreewidgetitem27.setText(0, QCoreApplication.translate("Dialog", u"26", None));
        ___qtreewidgetitem28 = ___qtreewidgetitem1.child(26)
        ___qtreewidgetitem28.setText(0, QCoreApplication.translate("Dialog", u"27", None));
        ___qtreewidgetitem29 = ___qtreewidgetitem1.child(27)
        ___qtreewidgetitem29.setText(0, QCoreApplication.translate("Dialog", u"28", None));
        ___qtreewidgetitem30 = ___qtreewidgetitem1.child(28)
        ___qtreewidgetitem30.setText(0, QCoreApplication.translate("Dialog", u"29", None));
        ___qtreewidgetitem31 = ___qtreewidgetitem1.child(29)
        ___qtreewidgetitem31.setText(0, QCoreApplication.translate("Dialog", u"30", None));
        ___qtreewidgetitem32 = ___qtreewidgetitem1.child(30)
        ___qtreewidgetitem32.setText(0, QCoreApplication.translate("Dialog", u"31", None))


        ___qtreewidgetitem41 = self.treeWidget_3.topLevelItem(2)
        ___qtreewidgetitem41.setText(0, QCoreApplication.translate("Dialog", u"\u0414\u0435\u043d\u044c", None))
        ___qtreewidgetitem42 = ___qtreewidgetitem41.child(0)
        ___qtreewidgetitem42.setText(0, QCoreApplication.translate("Dialog", u"00:00", None))
        ___qtreewidgetitem43 = ___qtreewidgetitem41.child(1)
        ___qtreewidgetitem43.setText(0, QCoreApplication.translate("Dialog", u"01:00", None))
        ___qtreewidgetitem44 = ___qtreewidgetitem41.child(2)
        ___qtreewidgetitem44.setText(0, QCoreApplication.translate("Dialog", u"02:00", None));
        ___qtreewidgetitem45 = ___qtreewidgetitem41.child(3)
        ___qtreewidgetitem45.setText(0, QCoreApplication.translate("Dialog", u"03:00", None));
        ___qtreewidgetitem46 = ___qtreewidgetitem41.child(4)
        ___qtreewidgetitem46.setText(0, QCoreApplication.translate("Dialog", u"04:00", None));
        ___qtreewidgetitem47 = ___qtreewidgetitem41.child(5)
        ___qtreewidgetitem47.setText(0, QCoreApplication.translate("Dialog", u"05:00", None));
        ___qtreewidgetitem48 = ___qtreewidgetitem41.child(6)
        ___qtreewidgetitem48.setText(0, QCoreApplication.translate("Dialog", u"06:00", None));
        ___qtreewidgetitem49 = ___qtreewidgetitem41.child(7)
        ___qtreewidgetitem49.setText(0, QCoreApplication.translate("Dialog", u"07:00", None));
        ___qtreewidgetitem50 = ___qtreewidgetitem41.child(8)
        ___qtreewidgetitem50.setText(0, QCoreApplication.translate("Dialog", u"08:00", None));
        ___qtreewidgetitem51 = ___qtreewidgetitem41.child(9)
        ___qtreewidgetitem51.setText(0, QCoreApplication.translate("Dialog", u"09:00", None));
        ___qtreewidgetitem52 = ___qtreewidgetitem41.child(10)
        ___qtreewidgetitem52.setText(0, QCoreApplication.translate("Dialog", u"10:00", None));
        ___qtreewidgetitem53 = ___qtreewidgetitem41.child(11)
        ___qtreewidgetitem53.setText(0, QCoreApplication.translate("Dialog", u"11:00", None));
        ___qtreewidgetitem54 = ___qtreewidgetitem41.child(12)
        ___qtreewidgetitem54.setText(0, QCoreApplication.translate("Dialog", u"12:00", None));
        ___qtreewidgetitem55 = ___qtreewidgetitem41.child(13)
        ___qtreewidgetitem55.setText(0, QCoreApplication.translate("Dialog", u"13:00", None));
        ___qtreewidgetitem56 = ___qtreewidgetitem41.child(14)
        ___qtreewidgetitem56.setText(0, QCoreApplication.translate("Dialog", u"14:00", None));
        ___qtreewidgetitem57 = ___qtreewidgetitem41.child(15)
        ___qtreewidgetitem57.setText(0, QCoreApplication.translate("Dialog", u"15:00", None));
        ___qtreewidgetitem58 = ___qtreewidgetitem41.child(16)
        ___qtreewidgetitem58.setText(0, QCoreApplication.translate("Dialog", u"16:00", None));
        ___qtreewidgetitem59 = ___qtreewidgetitem41.child(17)
        ___qtreewidgetitem59.setText(0, QCoreApplication.translate("Dialog", u"17:00", None));
        ___qtreewidgetitem60 = ___qtreewidgetitem41.child(18)
        ___qtreewidgetitem60.setText(0, QCoreApplication.translate("Dialog", u"18:00", None));
        ___qtreewidgetitem61 = ___qtreewidgetitem41.child(19)
        ___qtreewidgetitem61.setText(0, QCoreApplication.translate("Dialog", u"19:00", None));
        ___qtreewidgetitem62 = ___qtreewidgetitem41.child(20)
        ___qtreewidgetitem62.setText(0, QCoreApplication.translate("Dialog", u"20:00", None));
        ___qtreewidgetitem63 = ___qtreewidgetitem41.child(21)
        ___qtreewidgetitem63.setText(0, QCoreApplication.translate("Dialog", u"21:00", None));
        ___qtreewidgetitem64 = ___qtreewidgetitem41.child(22)
        ___qtreewidgetitem64.setText(0, QCoreApplication.translate("Dialog", u"22:00", None));
        ___qtreewidgetitem65 = ___qtreewidgetitem41.child(23)
        ___qtreewidgetitem65.setText(0, QCoreApplication.translate("Dialog", u"23:00", None));
        self.treeWidget_3.setSortingEnabled(__sortingEnabled)

