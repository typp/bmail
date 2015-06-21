# -*- coding: utf-8 -*-

import sys
import os
import _thread
from time import sleep

from PyQt4.QtGui import QDialog
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic

class Dialog_Loading (QDialog):
    def __init__ (self, parent, callback=None):
        QDialog.__init__(self)
        dirname = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname, "dialog_loading.ui"), self)
        self.parent = parent
        if callback:
            self.show()
            _thread.start_new_thread(callback, (self,))
