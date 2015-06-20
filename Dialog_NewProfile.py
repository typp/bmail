# -*- coding: utf-8 -*-

import sys
import os

from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import uic

class Dialog_NewProfile (QDialog):
    def __init__ (self, parent):
        QDialog.__init__(self)
        dirname = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname, "dialog_newprofile.ui"), self)
        self.parent = parent
        self.buttonBox.accepted.connect(self.OK)

    def OK (self):
        method = "POP3" if self.input_radio_POP3.isChecked() else "IMAP"
        self.parent.registerProfile(self.input_ProfileName.text(), {
            'host': self.input_Host.text(),
            'port': self.input_Port.value(),
            'protocol': method,
            'username': self.input_Username.text(),
            'password': self.input_Password.text(),
            'passRemember': self.input_checkbox_RememberPass.isChecked(),
            'ssl': self.input_checkbox_SSL.isChecked()
        })
