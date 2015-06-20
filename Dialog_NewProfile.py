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
        self.input_sender_checkbox_Authentificate.stateChanged.connect(self.toggleSenderAuthentification)
        self.input_sender_checkbox_ReuseReceiverCreds.stateChanged.connect(self.toggleSenderReuseReceiverCreds)

    def toggleSenderAuthentification (self, state):
        self.input_sender_checkbox_ReuseReceiverCreds.setEnabled(state)
        self.toggleSenderReuseReceiverCreds(not state)

    def toggleSenderReuseReceiverCreds (self, state):
        self.input_sender_Username.setEnabled(not state)
        self.input_sender_Password.setEnabled(not state)
        self.input_sender_checkbox_RememberPass.setEnabled(not state)

    def OK (self):
        sender_reuse_creds = self.input_sender_checkbox_ReuseReceiverCreds.isChecked()
        receiver_method = "POP3" if self.input_receiver_radio_POP3.isChecked() else "IMAP"
        self.parent.registerProfile(self.input_ProfileName.text(), {
            'sender': {
                'host': self.input_sender_Host.text(),
                'port': self.input_sender_Port.value(),
                'protocol': 'SMTP',
                'auth': self.input_sender_checkbox_Authentificate.isChecked(),
                'username': self.input_sender_Username.text() if not sender_reuse_creds else self.input_receiver_Username.text(),
                'password': self.input_sender_Password.text() if not sender_reuse_creds else self.input_receiver_Password.text(),
                'passRemember': self.input_sender_checkbox_RememberPass.isChecked() if not sender_reuse_creds else self.input_receiver_checkbox_RememberPass.isChecked(),
                'ssl': self.input_sender_checkbox_SSL.isChecked(),
                'tls': self.input_sender_checkbox_TLS.isChecked()
            },
            'receiver': {
                'host': self.input_receiver_Host.text(),
                'port': self.input_receiver_Port.value(),
                'protocol': receiver_method,
                'username': self.input_receiver_Username.text(),
                'password': self.input_receiver_Password.text(),
                'passRemember': self.input_receiver_checkbox_RememberPass.isChecked(),
                'ssl': self.input_receiver_checkbox_SSL.isChecked()
            },
            'email': self.input_EmailAddress.text()
        })
