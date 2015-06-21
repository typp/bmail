# -*- coding: utf-8 -*-

import sys
import os
import threading
from functools import partial

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

import ckeditor

from Dialog_Loading import *

class Dialog_NewMail (QDialog):
    def __init__ (self, parent, to='', subject='', content=''):
        QDialog.__init__(self)
        dirname = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname, "dialog_newmail.ui"), self)
        self.parent = parent

        self.editor = ckeditor.WebView(self)
        self.layout.layout().addWidget(self.editor, 0, Qt.AlignCenter)
        self.editor.addEditor(os.path.join(dirname, "js/ckeditor/ckeditor.js"), editor='editor1')

        self.input_To.setText(to)
        self.input_Subject.setText(subject)
        self.editor.setEditorHtml(content)

    def accept (self):
        if not self.input_To.text().strip():
            QMessageBox(QMessageBox.Critical, "Error", "You have to specify a recipient.").exec_()
            return

        to = self.input_To.text().strip()
        subject = self.input_Subject.text().strip()
        content = self.editor.getEditorHtml().strip()

        dialog = Dialog_Loading(self)
        dialog.message.setText("Sending e-mail ...")
        dialog.show()
        thr = threading.Thread(target=partial(self.parent.sendbox.send, to, subject, content))
        thr.start()
        while True:
            thr.join(0.1)
            if thr.is_alive():
                QtWidgets.QApplication.processEvents()
                dialog.repaint()
                dialog.update()
            else:
                dialog.hide()
                break
        self.close()
