# -*- coding: utf-8 -*-

import sys
import os

from PyQt4.QtGui import QDialog
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtGui
from PyQt4 import uic

class Dialog_About (QDialog):
    def __init__ (self, parent):
        QDialog.__init__(self)
        self.parent = parent
        dirname = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname, "dialog_about.ui"), self)
        self.scene = QtGui.QGraphicsScene()
        self.view = QtGui.QGraphicsView(self.scene)
        self.item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap("about.png"))
        self.scene.addItem(self.item);
        self.horizontalLayout.addWidget(self.view)
        self.view.show()
