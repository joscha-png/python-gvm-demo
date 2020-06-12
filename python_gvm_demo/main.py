from login import Ui_LoginForm
from start import Ui_StartForm
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QMainWindow, QMessageBox) 

from gvm.connections import SSHConnection
from gvm.protocols.gmp import Gmp
from gvm.transform import ObjectTransform





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    StartForm = QtWidgets.QMainWindow()
    ui = Ui_StartForm()
    ui.setupUi(StartForm)
    StartForm.show()
    print("before sleep")
    time.sleep(10)
    print("after sleep")
    sys.exit(app.exec_())

