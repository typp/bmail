# -*- coding: utf-8 -*-

import sys
import os
import re
import yaml

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
from Dialog_NewMail import *

class MainWindow (QMainWindow):
    def __init__ (self):
        QtWidgets.QMainWindow.__init__(self)
        dirname = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname, "mainwindow.ui"), self)
        self.action_profiles = []
        self.action_New.triggered.connect(self.newProfileDialog)
        self.newMailButton.clicked.connect(self.newMailDialog)
        self.profileDir = 'profile'

    def newProfileDialog (self):
        dialog = Dialog_NewProfile(self)
        dialog.exec()

    def newMailDialog (self):
        dialog = Dialog_NewMail(self)
        dialog.exec()

    def appendProfile (self, name, entry_value):
        self.action_No_profile_known.setVisible(False)
        action = QtWidgets.QAction(self)
        action.setText(name)
        action.setObjectName(entry_value)
        self.action_profiles.append(QtWidgets.QAction(self))
        self.menuProfile.addAction(action)

    def getProfileID (self):
        files = os.listdir(self.profileDir)
        profile_id = 1
        used_ids = []
        for name in files:
            try:
                used_ids.append(int(name.split('-')[0]))
            except:
                pass
        print(used_ids)
        while profile_id in used_ids:
            profile_id += 1
        return profile_id

    def getProfileFile (self, profile_id, name):
        safe_name = re.sub(r"[^A-Za-z0-9-]", "-", name)
        return os.path.join(
            self.profileDir,
            "%03d-%s.yaml" % (profile_id, safe_name))

    def registerProfile (self, name, config):
        """
        config.host: string
        config.post: integer
        config.protocol: "POP3" | "IMAP"
        config.username: string
        config.password: string
        config.passRemember: boolean
        config.ssl: boolean
        """
        profile_id = self.getProfileID()
        filename = self.getProfileFile(profile_id, name)
        with open(filename, 'w') as stream:
            stream.write(yaml.dump({
                'id': profile_id,
                'name': name,
                'config': config
            }))
        self.appendProfile(name, filename)


