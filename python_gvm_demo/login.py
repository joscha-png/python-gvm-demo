from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget, QMainWindow, QMessageBox
from socket import gaierror
from gvm.connections import SSHConnection
from gvm.transforms import ObjectTransform
from gvm.protocols.gmp import Gmp
from gvm.errors import GvmResponseError, GvmError
from paramiko.ssh_exception import NoValidConnectionsError
from main import Ui_MainForm


class LoginEvent(QObject):
    login_event = pyqtSignal(object, object)


class Ui_LoginForm(object):
    def setupUi(self, LoginForm):

        self.signal = LoginEvent()
        self.signal.login_event.connect(Ui_MainForm.load_startup_ui)
        self.window = LoginForm

        LoginForm.setObjectName("LoginForm")
        LoginForm.resize(501, 597)
        LoginForm.setStyleSheet("background-color: rgb(32, 32, 32)")
        self.centralwidget = QtWidgets.QWidget(LoginForm)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_6.setSpacing(10)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.logo_label = QtWidgets.QLabel(self.centralwidget)
        self.logo_label.setMaximumSize(QtCore.QSize(200, 200))
        self.logo_label.setText("")
        self.logo_label.setPixmap(QtGui.QPixmap("Logos/Logo.png"))
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_label.setObjectName("logo_label")
        self.verticalLayout_6.addWidget(
            self.logo_label, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop
        )
        self.loginlabel = QtWidgets.QLabel(self.centralwidget)
        self.loginlabel.setMaximumSize(QtCore.QSize(200, 62))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.loginlabel.setFont(font)
        self.loginlabel.setStyleSheet("color: \n" "rgb(112, 112, 112)")
        self.loginlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.loginlabel.setObjectName("loginlabel")
        self.verticalLayout_6.addWidget(self.loginlabel, 0, QtCore.Qt.AlignHCenter)
        self.info_label = QtWidgets.QLabel(self.centralwidget)
        self.info_label.setMaximumSize(QtCore.QSize(250, 12))
        self.info_label.setStyleSheet("color: white")
        self.info_label.setObjectName("info_label")
        self.verticalLayout_6.addWidget(self.info_label, 0, QtCore.Qt.AlignHCenter)
        self.hostname_input = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.hostname_input.sizePolicy().hasHeightForWidth()
        )
        self.hostname_input.setSizePolicy(sizePolicy)
        self.hostname_input.setStyleSheet(
            "color: rgb(255, 255, 255);\n" "border:  1px solid white"
        )
        self.hostname_input.setAlignment(QtCore.Qt.AlignCenter)
        self.hostname_input.setObjectName("hostname_input")
        self.verticalLayout_6.addWidget(self.hostname_input, 0, QtCore.Qt.AlignHCenter)
        self.username_label = QtWidgets.QLabel(self.centralwidget)
        self.username_label.setMaximumSize(QtCore.QSize(200, 12))
        self.username_label.setStyleSheet("color: white")
        self.username_label.setObjectName("username_label")
        self.verticalLayout_6.addWidget(self.username_label, 0, QtCore.Qt.AlignHCenter)
        self.username_input = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.username_input.sizePolicy().hasHeightForWidth()
        )
        self.username_input.setSizePolicy(sizePolicy)
        self.username_input.setStyleSheet(
            "color: rgb(255, 255, 255);\n" "border:  1px solid white"
        )
        self.username_input.setAlignment(QtCore.Qt.AlignCenter)
        self.username_input.setObjectName("username_input")
        self.verticalLayout_6.addWidget(self.username_input, 0, QtCore.Qt.AlignHCenter)
        self.password_label = QtWidgets.QLabel(self.centralwidget)
        self.password_label.setMaximumSize(QtCore.QSize(200, 12))
        self.password_label.setStyleSheet("color: white")
        self.password_label.setObjectName("password_label")
        self.verticalLayout_6.addWidget(self.password_label, 0, QtCore.Qt.AlignHCenter)
        self.password_input = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.password_input.sizePolicy().hasHeightForWidth()
        )
        self.password_input.setSizePolicy(sizePolicy)
        self.password_input.setStyleSheet(
            "color: rgb(255, 255, 255);\n" "border:  1px solid white;"
        )
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setAlignment(QtCore.Qt.AlignCenter)
        self.password_input.setObjectName("password_input")
        self.verticalLayout_6.addWidget(self.password_input, 0, QtCore.Qt.AlignHCenter)
        self.login_button = QtWidgets.QPushButton(self.centralwidget)
        self.login_button.setMaximumSize(QtCore.QSize(200, 34))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.login_button.setFont(font)
        self.login_button.setStyleSheet(
            "color: rgb(102, 196, 48) ;\n"
            "border-width: 2px;\n"
            "border-color: rgb(255, 255, 255);\n"
            " "
        )
        self.login_button.setObjectName("login_button")

        self.login_button.clicked.connect(self.check_login)

        self.verticalLayout_6.addWidget(self.login_button, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addLayout(self.verticalLayout_6)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout.addLayout(self.verticalLayout)
        LoginForm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LoginForm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 501, 22))
        self.menubar.setObjectName("menubar")
        LoginForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LoginForm)
        self.statusbar.setObjectName("statusbar")
        LoginForm.setStatusBar(self.statusbar)

        self.retranslateUi(LoginForm)
        self.window.setWindowTitle("Login")
        QtCore.QMetaObject.connectSlotsByName(LoginForm)

    def retranslateUi(self, LoginForm):
        _translate = QtCore.QCoreApplication.translate
        LoginForm.setWindowTitle(_translate("LoginForm", "MainWindow"))
        self.loginlabel.setText(_translate("LoginForm", "Login"))
        self.info_label.setText(_translate("LoginForm", "Hostname:"))
        self.hostname_input.setPlaceholderText(_translate("LoginForm", "Hostname"))
        self.username_label.setText(_translate("LoginForm", "Username:"))
        self.username_input.setPlaceholderText(_translate("LoginForm", "Username"))
        self.password_label.setText(_translate("LoginForm", "Password:"))
        self.password_input.setPlaceholderText(_translate("LoginForm", "Password"))
        self.login_button.setText(_translate("LoginForm", "Anmelden"))

    def check_login(self):
        if (
            self.hostname_input.text() == ""
            or self.username_input.text() == ""
            or self.password_input.text() == ""
        ):
            QMessageBox.about(QMainWindow(), "Error", "Please enter a all Information")
        else:
            try:
                connection = SSHConnection(hostname=self.hostname_input.text())

                with Gmp(connection=connection, transform=ObjectTransform()) as gmp:
                    try:
                        response = gmp.authenticate(
                            username=self.username_input.text(),
                            password=self.password_input.text(),
                        )
                        print(response)
                        self.signal.login_event.emit(gmp, self.window)
                    except GvmResponseError:
                        QMessageBox.about(
                            QMainWindow(), "Error", "Wrong username or password."
                        )

            except (gaierror, NoValidConnectionsError, GvmError) as ex:
                QMessageBox.about(QMainWindow(), "Error", str(ex))
