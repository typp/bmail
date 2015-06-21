# -*- coding: utf-8 -*-

import sys
import os

from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic

class Dialog_About (QDialog):
    def __init__ (self, parent):
        QDialog.__init__(self)
        self.parent = parent
        dirname = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname, "dialog_about.ui"), self)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.item = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap("about.png"))
        self.scene.addItem(self.item);
        self.horizontalLayout.addWidget(self.view)
        self.view.show()
