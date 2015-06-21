# -*- coding: utf-8 -*-

import sys
import os

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

import ckeditor

class Dialog_NewMail (QDialog):
    def __init__ (self, parent):
        QDialog.__init__(self)
        dirname = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname, "dialog_newmail.ui"), self)
        self.parent = parent

        self.editor = ckeditor.WebView(self)
        self.layout.layout().addWidget(self.editor, 0, Qt.AlignCenter)
        self.editor.addEditor(os.path.join(dirname, "js/ckeditor/ckeditor.js"), editor='editor1')

        self.buttonBox.accepted.connect(self.OK)

    def OK (self):
        to = self.input_To.text()
        subject = self.input_Subject.text()
        content = self.editor.getEditorHtml()
        self.parent.sendbox.send(to, subject, content)
