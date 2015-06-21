# -*- coding: utf-8 -*-

import sys
import os

from PyQt5.QtWidgets import QMessageBox
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
        self.autoPortSelection = True

        self.input_sender_checkbox_Authentificate.stateChanged.connect(self.toggleSenderAuthentification)
        self.input_sender_checkbox_ReuseReceiverCreds.stateChanged.connect(self.toggleSenderReuseReceiverCreds)
        self.input_sender_checkbox_SSL.stateChanged.connect(self.toggleSenderSSLTLS)
        self.input_sender_checkbox_TLS.stateChanged.connect(self.toggleSenderTLSSSL)
        self.input_sender_checkbox_SSL.stateChanged.connect(self.toggleSenderPort)
        self.input_sender_checkbox_TLS.stateChanged.connect(self.toggleSenderPort)
        self.input_receiver_radio_POP3.toggled.connect(self.toggleReceiverPort)
        self.input_receiver_radio_IMAP.toggled.connect(self.toggleReceiverPort)
        self.input_receiver_checkbox_SSL.stateChanged.connect(self.toggleReceiverPort)
        self.input_receiver_Port.valueChanged.connect(self.toggleAutoPortSelection)
        self.input_sender_Port.valueChanged.connect(self.toggleAutoPortSelection)

    def toggleAutoPortSelection (self, value):
        self.autoPortSelection = False

    def toggleSenderPort (self, state):
        if not self.autoPortSelection: return
        if self.input_sender_checkbox_SSL.isChecked():
            self.input_sender_Port.setValue(465)
        elif self.input_sender_checkbox_TLS.isChecked():
            self.input_sender_Port.setValue(587)
        else:
            self.input_sender_Port.setValue(25)
        self.autoPortSelection = True

    def toggleReceiverPort (self, state):
        if not self.autoPortSelection: return
        if self.input_receiver_radio_POP3.isChecked():
            if self.input_receiver_checkbox_SSL.isChecked():
                self.input_receiver_Port.setValue(995)
            else:
                self.input_receiver_Port.setValue(110)
        elif self.input_receiver_radio_IMAP.isChecked():
            if self.input_receiver_checkbox_SSL.isChecked():
                self.input_receiver_Port.setValue(993)
            else:
                self.input_receiver_Port.setValue(143)
        self.autoPortSelection = True

    def toggleSenderSSLTLS (self, state):
        if state and self.input_sender_checkbox_TLS.isChecked():
            self.input_sender_checkbox_TLS.setChecked(False)

    def toggleSenderTLSSSL (self, state):
        if state and self.input_sender_checkbox_SSL.isChecked():
            self.input_sender_checkbox_SSL.setChecked(False)

    def toggleSenderAuthentification (self, state):
        self.input_sender_checkbox_ReuseReceiverCreds.setEnabled(state)
        self.toggleSenderReuseReceiverCreds(not state)

    def toggleSenderReuseReceiverCreds (self, state):
        self.input_sender_Username.setEnabled(not state)
        self.input_sender_Password.setEnabled(not state)
        self.input_sender_checkbox_RememberPass.setEnabled(not state)

    def accept (self):
        if not self.input_ProfileName.text().strip():
            QMessageBox(QMessageBox.Critical, "Error", "You have to specify a profile name.").exec_()
            return

        self.close()

        sender_reuse_creds = self.input_sender_checkbox_ReuseReceiverCreds.isChecked()
        receiver_method = "POP3" if self.input_receiver_radio_POP3.isChecked() else "IMAP"
        self.parent.registerProfile(self.input_ProfileName.text().strip(), {
            'sender': {
                'host': self.input_sender_Host.text().strip(),
                'port': self.input_sender_Port.value(),
                'protocol': 'SMTP',
                'auth': self.input_sender_checkbox_Authentificate.isChecked(),
                'username': self.input_sender_Username.text().strip() if not sender_reuse_creds else self.input_receiver_Username.text().strip(),
                'password': self.input_sender_Password.text() if not sender_reuse_creds else self.input_receiver_Password.text(),
                'passRemember': self.input_sender_checkbox_RememberPass.isChecked() if not sender_reuse_creds else self.input_receiver_checkbox_RememberPass.isChecked(),
                'ssl': self.input_sender_radio_SSL.isChecked(),
                'tls': self.input_sender_radio_TLS.isChecked()
            },
            'receiver': {
                'host': self.input_receiver_Host.text().strip(),
                'port': self.input_receiver_Port.value(),
                'protocol': receiver_method,
                'username': self.input_receiver_Username.text().strip(),
                'password': self.input_receiver_Password.text(),
                'passRemember': self.input_receiver_checkbox_RememberPass.isChecked(),
                'ssl': self.input_receiver_checkbox_SSL.isChecked()
            },
            'email': self.input_EmailAddress.text().strip(),
            'realName': self.input_RealName.text().strip() if self.input_RealName.text().strip() else ''
        })
