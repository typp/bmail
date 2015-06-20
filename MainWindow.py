# -*- coding: utf-8 -*-

import sys
import os
import re
import yaml

from functools import partial

# try:
#     from PySide import QtCore
#     from PySide import QtWidgets
# except:
#     from PyQt5.QtCore import pyqtSlot as Slot
#     from PyQt5 import QtCore
#     from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5 import QtGui

from Dialog_NewProfile import *
from Dialog_NewMail import *

from MailboxPOP3 import *

class MainWindow (QMainWindow):
    def __init__ (self):
        QMainWindow.__init__(self)
        dirname = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname, "mainwindow.ui"), self)
        self.profiles = []
        self.action_New.triggered.connect(self.newProfileDialog)
        self.newMailButton.clicked.connect(self.newMailDialog)
        self.profileDir = 'profile'
        self.currentProfile = None
        self.currentProfileAction = None
        self.updateAllProfiles()

    def updateAllProfiles (self):
        files = [os.path.join(self.profileDir, path)
                for path
                in os.listdir(self.profileDir)
                if os.path.isfile(os.path.join(self.profileDir, path))]
        for path in files:
            profile = None
            with open(path, 'r') as stream:
                profile = yaml.load(stream)
            if profile:
                self.appendProfile(profile, os.path.basename(path))

    def newProfileDialog (self):
        dialog = Dialog_NewProfile(self)
        dialog.exec()

    def newMailDialog (self):
        dialog = Dialog_NewMail(self)
        dialog.exec()

    def appendProfile (self, name, entry_value):
        self.action_No_profile_known.setVisible(False)
        action = QtWidgets.QAction(self)
        action.setText(profile['name'])
        action.setObjectName('action_' + filename)
        action.triggered.connect(partial(self.selectProfile, action, profile))
        self.profiles.append(profile)
        self.menuProfile.addAction(action)
        return action

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
        if config['protocol'] == "POP3":
            self.currentProfile = MailboxPOP3(config)
        profile_id = self.getProfileID()
        filename = self.getProfileFile(profile_id, name)
        profile = {
            'id': profile_id,
            'name': name,
            'config': config
        }
        with open(filename, 'w') as stream:
            stream.write(yaml.dump(profile))
        action = self.appendProfile(profile, filename)
        self.selectProfile(action, profile)

    def selectProfile (self, action, profile):
        if not self.currentProfile or profile['id'] != self.currentProfile['id']:
            if profile['config']['protocol'] == "POP3":
                self.mailbox = MailboxPOP3(profile)
            else:
                return
            print('couille')
            self.mailbox.sync()
            while self.mailList.count() > 0:
                self.mailList.takeItem(0)
            for message in self.mailbox.list():
                item = QListWidgetItem(message['header']['subject'])
                self.mailList.addItem(item)
                self.mailList.itemClicked.connect(partial(self.showMail, message['id']))
            if self.currentProfileAction:
                font = QtGui.QFont()
                font.setBold(False)
                self.currentProfileAction.setFont(False)
            self.currentProfileAction = action
            font = QtGui.QFont()
            font.setBold(True)
            self.currentProfileAction.setFont(font)
            self.currentProfile = profile

    def showMail (self, item, mailno):
        print('bite')
