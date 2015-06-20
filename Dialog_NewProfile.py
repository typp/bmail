# -*- coding: utf-8 -*-

import sys
import os

from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import uic

class Dialog_NewProfile(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        dirname = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname, "dialog_newprofile.ui"), self)
