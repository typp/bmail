# -*- coding: utf-8 -*-

import sys
import os
import re
import yaml
import webbrowser

from functools import partial

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtWebKitWidgets import QWebPage

from Dialog_NewProfile import *
from Dialog_NewMail import *
from Dialog_About import *

from MailboxPOP3 import *
from MailboxIMAP import *
from SendboxSMTP import *

class MainWindow (QMainWindow):
    def __init__ (self):
        QMainWindow.__init__(self)
        dirname = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(dirname, "mainwindow.ui"), self)
        self.profiles = []
        self.action_New.triggered.connect(self.newProfileDialog)
        self.action_Exit.triggered.connect(self.close)
        self.action_About.triggered.connect(self.aboutDialog)
        self.newMailButton.clicked.connect(self.newMailDialog)
        self.answerButton.clicked.connect(self.answerMail)
        self.syncButton.clicked.connect(self.syncMailbox)
        self.deleteButton.clicked.connect(self.deleteMail)
        self.webView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.webView.linkClicked.connect(self.openLinkInBrowser)
        self.profileDir = 'profile'
        self.currentProfile = None
        self.currentProfileAction = None
        self.mailbox = None
        self.sendbox = None
        self.currentMailNo = None
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

    def aboutDialog (self):
        dialog = Dialog_About(self)
        dialog.exec()

    def newMailDialog (self, **kwargs):
        if self.sendbox:
            dialog = Dialog_NewMail(self, **kwargs)
            dialog.exec()
        else:
            QMessageBox(QMessageBox.Critical, "Error", "You have update the Sender configuration to be able to send mails.").exec_()

    def appendProfile (self, profile, filename):
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
        config.receiver.host: string
        config.receiver.port: integer
        config.receiver.protocol: "POP3" | "IMAP"
        config.receiver.username: string
        config.receiver.password: string
        config.receiver.passRemember: boolean
        config.receiver.ssl: boolean

        config.sender.host: string
        config.sender.port: integer
        config.sender.protocol: "SMTP"
        config.sender.auth: boolean
        config.sender.username: string
        config.sender.password: string
        config.sender.passRemember: boolean
        config.sender.ssl: boolean
        config.sender.tls: boolean

        config.email: string
        """

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

    def connectToServers (self, profile):
        recv = profile['config']['receiver']['protocol']
        send = profile['config']['sender']['protocol']
        if recv == "POP3":
            self.mailbox = MailboxPOP3(profile)
        elif recv == "IMAP":
            self.mailbox = MailboxIMAP(profile)
        if send == "SMTP":
            self.sendbox = SendboxSMTP(profile)

    def selectProfile (self, action, profile):
        if not self.currentProfile or profile['id'] != self.currentProfile['id']:
            self.logout()
            try:
                self.connectToServers(profile)
                self.mailbox.sync()
                self.refreshMailList()
            except Exception:
                QMessageBox(QMessageBox.Critical, "Error", "Failure while trying to join the servers.").exec_()
            if self.currentProfileAction:
                font = QtGui.QFont()
                font.setBold(False)
                self.currentProfileAction.setFont(font)
            self.currentProfileAction = action
            font = QtGui.QFont()
            font.setBold(True)
            self.currentProfileAction.setFont(font)
            self.currentProfile = profile

    def showMail (self, item):
        mailno = item.data(Qt.UserRole)
        from_, subject, date, content = self.mailbox.get(mailno)
        self.mail_From.setText(from_)

        self.mail_Subject.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # cutting the subject to force word wrapping
        for i in range(int(len(subject) / 100)):
            subject = subject[:i*100] + ' ' + subject[i*100:]

        self.mail_Subject.setText(subject)
        self.mail_Date.setText(date)
        self.webView.setHtml(content)
        self.currentMailNo = mailno

    def refreshMailList (self):
        while self.mailList.count() > 0:
            self.mailList.takeItem(0)
        for message in reversed(self.mailbox.list()):
            subject = self.mailbox.fdecode(message['header']['Subject'])
            subject = subject if isinstance(subject, str) else '<No subject>'
            item = QListWidgetItem(subject)
            item.setData(Qt.UserRole, message['id']);
            self.mailList.addItem(item)
        self.mailList.itemClicked.connect(self.showMail)

    def syncMailbox (self):
        try:
            self.mailbox.sync()
            self.refreshMailList()
        except Exception:
            QMessageBox(QMessageBox.Critical, "Error", "Failure while trying to join the servers.").exec_()

    def openLinkInBrowser(self, url):
        webbrowser.open(url.toString())

    def deleteMail (self):
        if self.currentMailNo != None: # currentMailNo can be 0
            self.mailbox.delete(self.currentMailNo)

            if self.mailList.currentRow() + 1 <= self.mailList.count():
                next_row = self.mailList.currentRow()
            elif self.mailList.currentRow() - 1 <= self.mailList.count():
                next_row = self.mailList.currentRow() - 1
            else:
                next_row = 0

            self.mailList.takeItem(self.mailList.currentRow())
            self.mailList.setCurrentRow(next_row)
            self.showMail(self.mailList.currentItem())
        else:
            QMessageBox(QMessageBox.Critical, "Error", "You have to select an email before.").exec_()

    def answerMail (self):
        if self.currentMailNo != None:
            _from, subject, date, content = self.mailbox.get(self.currentMailNo)
            dialog = self.newMailDialog(to=_from, subject='RE: ' + subject)
        else:
            QMessageBox(QMessageBox.Critical, "Error", "You have to select an email before.").exec_()

    def logout (self):
        if self.mailbox:
            self.mailbox.logout()
            self.mailbox = None
        if self.sendbox:
            self.sendbox.logout()
            self.sendbox = None

    def closeEvent (self, event):
        if self.mailbox:
            self.logout()
            event.accept()
