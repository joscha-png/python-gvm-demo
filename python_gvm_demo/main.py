import time

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtWidgets import QWidget, QMainWindow, QMessageBox
from PyQt5.Qt import QStandardItemModel
from gvm.connections import SSHConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import ObjectTransform

from gvm.errors import GvmServerError


class Ui_MainForm(QWidget):
    def __init__(self):
        super().__init__()

    def handle_start_button_clicked(self):
        button = self.sender()

        index = self.table.indexAt(button.pos())
        if index.isValid():
            # print(index.row(),index.column())

            task = self.tasks[index.row()]
            try:
                response = self.gmp.start_task(task.uuid)
            except GvmServerError:
                QMessageBox.about(QMainWindow(), "Error", "Can't start this task.")
            # print(response)

            # self.load_tasks_ui()

    def handle_stop_button_clicked(self):
        button = self.sender()

        index = self.table.indexAt(button.pos())
        if index.isValid():
            task = self.tasks[index.row()]
            try:
                response = self.gmp.stop_task(task.uuid)
            except GvmServerError:
                QMessageBox.about(QMainWindow(), "Error", "Can't stop this task.")

    def handle_tasks_button_clicked(self):
        self.timer.stop()
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_tasks_ui)
        self.timer.start(5000)

        self.load_tasks_ui()

    def handle_reports_button_clicked(self):
        self.timer.stop()
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_reports_ui)
        self.timer.start(50000)

        self.load_reports_ui()

    def load_tasks_ui(self):
        print("Tasks load")

        response = self.gmp.get_tasks(filter="rows=-1")
        self.tasks = response.tasks

        _translate = QtCore.QCoreApplication.translate
        self.caption_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.caption_label.setFont(font)
        self.caption_label.setStyleSheet("color: white")
        self.caption_label.setAlignment(QtCore.Qt.AlignCenter)
        self.caption_label.setObjectName("caption_label")
        self.caption_label.setText(
            _translate("MainForm", "Aufgaben: " + str(len(self.tasks)))
        )

        # Before adding the new one delete the old
        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().deleteLater()

        self.verticalLayout.addWidget(self.caption_label)

        self.table = QtWidgets.QTableWidget()

        # Get the data

        self.table.setColumnCount(8)
        self.table.setRowCount(len(response.tasks))

        for index in range(len(response.tasks)):
            item0 = QTableWidgetItem(self.tasks[index].name)
            item1 = QTableWidgetItem(self.tasks[index].status)

            if self.tasks[index].target.uuid == "":
                item1 = QTableWidgetItem("Container")

            if self.tasks[index].status == "Running":
                item1 = QTableWidgetItem(str(self.tasks[index].progress) + "%")
            elif self.tasks[index].status == "Done":
                item1 = QTableWidgetItem("Fertig")
            elif self.tasks[index].status == "Requested":
                item1 = QTableWidgetItem("Angefragt")

            item2 = QTableWidgetItem(str(self.tasks[index].report_count.current))

            report = ""
            severity = ""
            if self.tasks[index].last_report is not None:
                if self.tasks[index].last_report.timestamp is not None:
                    report = self.tasks[index].last_report.timestamp.strftime(
                        "%a, %d. %B %Y %H:%M %Z"
                    )
                else:
                    report = ""
                severity = str(self.tasks[index].last_report.severity.full)
                if severity == "-99.0":
                    severity = "N/A"
            else:
                report = ""
                severity = ""

            item3 = QTableWidgetItem(report)
            item4 = QTableWidgetItem(severity)

            trend = ""
            if self.tasks[index].trend is not None:
                if self.tasks[index].trend == "same":
                    trend = "➙"
                elif self.tasks[index].trend == "more":
                    trend = "➚"
                elif self.tasks[index].trend == "less":
                    trend = "➘"
                elif self.tasks[index].trend == "down":
                    trend = "↓"
                elif self.tasks[index].trend == "up":
                    trend = "↑"
                else:
                    trend = self.tasks[index].trend

            item5 = QTableWidgetItem(trend)

            # Change alignment
            item0.setTextAlignment(Qt.AlignCenter)
            item1.setTextAlignment(Qt.AlignCenter)
            item2.setTextAlignment(Qt.AlignCenter)
            item3.setTextAlignment(Qt.AlignCenter)
            item4.setTextAlignment(Qt.AlignCenter)
            item5.setTextAlignment(Qt.AlignCenter)

            item0.setForeground(QColor(Qt.white))
            item1.setForeground(QColor(Qt.white))
            item2.setForeground(QColor(Qt.white))
            item3.setForeground(QColor(Qt.white))
            item4.setForeground(QColor(Qt.white))
            item5.setForeground(QColor(Qt.white))

            if index % 2 == 1:
                item0.setBackground(QColor(qRgb(70, 70, 70)))
                item1.setBackground(QColor(qRgb(70, 70, 70)))
                item2.setBackground(QColor(qRgb(70, 70, 70)))
                item3.setBackground(QColor(qRgb(70, 70, 70)))
                item4.setBackground(QColor(qRgb(70, 70, 70)))
                item5.setBackground(QColor(qRgb(70, 70, 70)))
            else:
                item0.setBackground(QColor(qRgb(50, 50, 50)))
                item1.setBackground(QColor(qRgb(50, 50, 50)))
                item2.setBackground(QColor(qRgb(50, 50, 50)))
                item3.setBackground(QColor(qRgb(50, 50, 50)))
                item4.setBackground(QColor(qRgb(50, 50, 50)))
                item5.setBackground(QColor(qRgb(50, 50, 50)))

            self.table.setItem(index, 0, item0)
            self.table.setItem(index, 1, item1)
            self.table.setItem(index, 2, item2)
            self.table.setItem(index, 3, item3)
            self.table.setItem(index, 4, item4)
            self.table.setItem(index, 5, item5)

            button = QtWidgets.QPushButton("►")
            button.setStyleSheet("color: white")
            button.clicked.connect(self.handle_start_button_clicked)
            self.table.setCellWidget(index, 6, button)

            button = QtWidgets.QPushButton("▌▌")
            button.setStyleSheet("color: white")
            button.clicked.connect(self.handle_stop_button_clicked)
            self.table.setCellWidget(index, 7, button)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)
        header.setStyleSheet("background-color: rgb(7,121,193); color: white")
        self.table.setHorizontalHeaderLabels(
            [
                "Name",
                "Status",
                "Berichte",
                "Letzter Bericht",
                "Schweregrad",
                "Trend",
                "Start Task",
                "Stop Task",
            ]
        )

        self.verticalLayout.addWidget(self.table)

    def load_reports_ui(self):
        print("reports work in progress")

        # Get the data
        response = self.gmp.get_reports()  # filter="rows=-1"
        self.reports = response.reports

        _translate = QtCore.QCoreApplication.translate
        self.caption_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.caption_label.setFont(font)
        self.caption_label.setStyleSheet("color: white")
        self.caption_label.setAlignment(QtCore.Qt.AlignCenter)
        self.caption_label.setObjectName("caption_label")
        self.caption_label.setText(
            _translate("MainForm", "Berichte: " + str(len(self.reports)))
        )

        # Before adding the new one delete the old
        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().deleteLater()

        self.verticalLayout.addWidget(self.caption_label)

        self.table = QtWidgets.QTableWidget()

        self.table.setColumnCount(9)
        self.table.setRowCount(len(response.reports))

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)
        header.setStyleSheet("background-color: rgb(7,121,193); color: white")

        header_item_high = QtWidgets.QTableWidgetItem("Hoch")
        header_item_high.setBackground(QtGui.QColor(200, 56, 20))

        header_item_medium = QtWidgets.QTableWidgetItem("Mittel")
        header_item_medium.setBackground(QtGui.QColor(240, 165, 25))

        header_item_low = QtWidgets.QTableWidgetItem("Niedrig")
        header_item_low.setBackground(QtGui.QColor(79, 145, 199))

        header_item_log = QtWidgets.QTableWidgetItem("Log")
        header_item_log.setBackground(QtGui.QColor(0, 0, 0))

        header_item_false_positiv = QtWidgets.QTableWidgetItem("Falsch-Positiv")
        header_item_false_positiv.setBackground(QtGui.QColor(0, 0, 0))

        self.table.setHorizontalHeaderItem(4, header_item_high)
        self.table.setHorizontalHeaderItem(5, header_item_medium)
        self.table.setHorizontalHeaderItem(6, header_item_low)
        self.table.setHorizontalHeaderItem(7, header_item_log)
        self.table.setHorizontalHeaderItem(8, header_item_false_positiv)

        self.table.setHorizontalHeaderLabels(
            [
                "Datum",
                "Status",
                "Aufgabe",
                "Schweregrad",
                "Hoch",
                "Mittel",
                "Niedrig",
                "Log",
                "Falsch-Positiv",
            ]
        )

        # Hier kommt die Logik rein
        for index in reversed(range(len(response.reports))):
            # items erstellen
            item0 = QTableWidgetItem()
            if self.reports[index].timestamp is not None:
                date = self.reports[index].timestamp.strftime("%a, %d. %B %Y %H:%M %Z")
                item0 = QTableWidgetItem(date)

            item1 = QTableWidgetItem(self.reports[index].task.status)
            if self.reports[index].task.target.uuid == "":
                item1 = QTableWidgetItem("Container")

            item2 = QTableWidgetItem(self.reports[index].task.name)

            severity = str(self.reports[index].severity.full)
            if severity == "-99.0":
                severity = "N/A"

            item3 = QTableWidgetItem(severity)

            """
            severity mapping:
                hole    -> hoch
                warning -> mittel
                info    -> niedrig
                log     -> log
            """
            item4 = QTableWidgetItem(str(self.reports[index].result_count.hole.full))
            item5 = QTableWidgetItem(str(self.reports[index].result_count.warning.full))
            item6 = QTableWidgetItem(str(self.reports[index].result_count.info.full))
            item7 = QTableWidgetItem(str(self.reports[index].result_count.log.full))
            item8 = None
            if self.reports[index].result_count.false_positiv.full is None:
                item8 = QTableWidgetItem("0")
            else:
                item8 = QTableWidgetItem(
                    str(self.reports[index].result_count.false_positive.full)
                )

            # Items anpassen
            item0.setTextAlignment(Qt.AlignCenter)
            item1.setTextAlignment(Qt.AlignCenter)
            item2.setTextAlignment(Qt.AlignCenter)
            item3.setTextAlignment(Qt.AlignCenter)
            item4.setTextAlignment(Qt.AlignCenter)
            item5.setTextAlignment(Qt.AlignCenter)
            item6.setTextAlignment(Qt.AlignCenter)
            item7.setTextAlignment(Qt.AlignCenter)
            item8.setTextAlignment(Qt.AlignCenter)

            item0.setForeground(QColor(Qt.white))
            item1.setForeground(QColor(Qt.white))
            item2.setForeground(QColor(Qt.white))
            item3.setForeground(QColor(Qt.white))
            item4.setForeground(QColor(Qt.white))
            item5.setForeground(QColor(Qt.white))
            item6.setForeground(QColor(Qt.white))
            item7.setForeground(QColor(Qt.white))
            item8.setForeground(QColor(Qt.white))

            if index % 2 == 1:
                item0.setBackground(QColor(qRgb(70, 70, 70)))
                item1.setBackground(QColor(qRgb(70, 70, 70)))
                item2.setBackground(QColor(qRgb(70, 70, 70)))
                item3.setBackground(QColor(qRgb(70, 70, 70)))
                item4.setBackground(QColor(qRgb(70, 70, 70)))
                item5.setBackground(QColor(qRgb(70, 70, 70)))
                item6.setBackground(QColor(qRgb(70, 70, 70)))
                item7.setBackground(QColor(qRgb(70, 70, 70)))
                item8.setBackground(QColor(qRgb(70, 70, 70)))
            else:
                item0.setBackground(QColor(qRgb(50, 50, 50)))
                item1.setBackground(QColor(qRgb(50, 50, 50)))
                item2.setBackground(QColor(qRgb(50, 50, 50)))
                item3.setBackground(QColor(qRgb(50, 50, 50)))
                item4.setBackground(QColor(qRgb(50, 50, 50)))
                item5.setBackground(QColor(qRgb(50, 50, 50)))
                item6.setBackground(QColor(qRgb(50, 50, 50)))
                item7.setBackground(QColor(qRgb(50, 50, 50)))
                item8.setBackground(QColor(qRgb(50, 50, 50)))

            # items in tabelle einsetzen
            self.table.setItem(index, 0, item0)
            self.table.setItem(index, 1, item1)
            self.table.setItem(index, 2, item2)
            self.table.setItem(index, 3, item3)
            self.table.setItem(index, 4, item4)
            self.table.setItem(index, 5, item5)
            self.table.setItem(index, 6, item6)
            self.table.setItem(index, 7, item7)
            self.table.setItem(index, 8, item8)

        self.verticalLayout.addWidget(self.table)

    def load_results_ui(self):
        print("results work in progress")

    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(1224, 598)
        MainForm.setStyleSheet("background-color: rgb(32, 32, 32)")
        self.window = MainForm

        self.centralwidget = QtWidgets.QWidget(MainForm)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalFrame = QtWidgets.QFrame(self.centralwidget)
        self.verticalFrame.setStyleSheet("background-color: black;")
        self.verticalFrame.setObjectName("verticalFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalFrame)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.logo_label = QtWidgets.QLabel(self.verticalFrame)
        self.logo_label.setMaximumSize(QtCore.QSize(200, 200))
        self.logo_label.setText("")
        self.logo_label.setPixmap(QtGui.QPixmap("Logos/Logo.png"))
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_label.setObjectName("logo_label")
        self.verticalLayout_3.addWidget(self.logo_label)
        self.tasks_button = QtWidgets.QPushButton(self.verticalFrame)

        self.tasks_button.clicked.connect(lambda: self.handle_tasks_button_clicked())

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tasks_button.sizePolicy().hasHeightForWidth())
        self.tasks_button.setSizePolicy(sizePolicy)
        self.tasks_button.setMinimumSize(QtCore.QSize(200, 30))
        self.tasks_button.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.tasks_button.setFont(font)
        self.tasks_button.setStyleSheet(
            "color: rgb(102, 196, 48) ;\n"
            "border-width: 2px;\n"
            "background-color: rgb(32, 32, 32);\n"
            "border-color: rgb(255, 255, 255);"
        )
        self.tasks_button.setObjectName("tasks_button")
        self.verticalLayout_3.addWidget(self.tasks_button)
        self.results_button = QtWidgets.QPushButton(self.verticalFrame)

        self.results_button.clicked.connect(lambda: self.load_results_ui())

        self.results_button.setMinimumSize(QtCore.QSize(200, 30))
        self.results_button.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.results_button.setFont(font)
        self.results_button.setStyleSheet(
            "color: rgb(102, 196, 48) ;\n"
            "border-width: 2px;\n"
            "background-color: rgb(32, 32, 32);\n"
            "border-color: rgb(255, 255, 255);"
        )
        self.results_button.setObjectName("results_button")
        self.verticalLayout_3.addWidget(self.results_button)
        self.reports_button = QtWidgets.QPushButton(self.verticalFrame)

        self.reports_button.clicked.connect(
            lambda: self.handle_reports_button_clicked()
        )

        self.reports_button.setMinimumSize(QtCore.QSize(200, 30))
        self.reports_button.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.reports_button.setFont(font)
        self.reports_button.setStyleSheet(
            "color: rgb(102, 196, 48) ;\n"
            "border-width: 2px;\n"
            "background-color: rgb(32, 32, 32);\n"
            "border-color: rgb(255, 255, 255);"
        )
        self.reports_button.setObjectName("reports_button")
        self.verticalLayout_3.addWidget(
            self.reports_button, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        )

        self.verticalLayout_2.addWidget(self.verticalFrame)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout.addLayout(self.verticalLayout)
        MainForm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainForm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 22))
        self.menubar.setObjectName("menubar")
        MainForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainForm)
        self.statusbar.setObjectName("statusbar")
        MainForm.setStatusBar(self.statusbar)

        self.retranslateUi(MainForm)
        self.window.setWindowTitle("Main")
        QtCore.QMetaObject.connectSlotsByName(MainForm)
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_tasks_ui)
        self.timer.start(5000)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "MainWindow"))
        self.tasks_button.setText(_translate("MainForm", "Aufgaben"))
        self.results_button.setText(_translate("MainForm", "Ergebnisse"))
        self.reports_button.setText(_translate("MainForm", "Berichte"))

    @staticmethod
    def load_startup_ui(gmp, main_window):
        if gmp:
            ui = Ui_MainForm()
            ui.gmp = gmp
            ui.setupUi(main_window)

            main_window.show()
            ui.load_tasks_ui()

            main_window.show()
