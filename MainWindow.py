# -*- coding: utf-8 -*-

import sys
import os

# try:
#     from PySide import QtCore
#     from PySide import QtWidgets
# except:
#     from PyQt5.QtCore import pyqtSlot as Slot
#     from PyQt5 import QtCore
#     from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import uic

from Dialog_NewProfile import *

class MainWindow(QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        dirname = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname, "mainwindow.ui"), self)
        self.action_New.triggered.connect(self.newProfileDialog)

    def newProfileDialog(self):
        dialog = Dialog_NewProfile()
        dialog.exec()
