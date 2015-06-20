#! /usr/bin/env python3

import sys
import getpass
import poplib
from email.parser import Parser as EmailParser
import re
import datetime

from Dialog_Loading import *

class MailboxPOP3:

    def __init__ (self, profile):
        self.config = profile['config']
        dialog = Dialog_Loading(self)
        dialog.show()
        pop3 = poplib.POP3_SSL if self.config['ssl'] else poplib.POP3
        self.mails = []
        safe_name = re.sub(r"[^A-Za-z0-9-]", "-", profile['name'])
        self.storageDir = os.path.join(
                'storage',
                '%i-%s' % (profile['id'], safe_name))
        try:
            os.mkdir(self.storageDir)
        except FileExistsError:
            pass
        self.connector = None
        try:
            self.connector = pop3(self.config['host'], self.config['port'])
        except:
            alert = QMessageBox(QMessageBox.Critical, "Error",
                "Could not connect to %s." % self.config["host"])
        else:
            print("Logging in ...")
            dialog.message.setText("Logging in ...")
            self.connector.user(self.config['username'])
            self.connector.pass_(self.config['password'])
            dialog.hide()

    def sync (self):
        maillist = self.connector.list()
        for mailcap in maillist[1]:
            mailno = int(mailcap.decode('utf-8').split(' ')[0])
            mail = self.connector.retr(mailno)
            content = '\n'.join(x.decode('utf-8') for x in mail[1])
            header = EmailParser().parsestr(content)
            filename = datetime.datetime.now().isoformat()
            filename += re.sub(r"[^A-Za-z0-9-]", "-", header['Subject'])
            filename += '.dat'
            path = os.path.join(self.storageDir, filename)
            with open(path, 'w') as stream:
                stream.write(content)
            self.mails.append({'id': mailno, 'content': mail[1]})
        print('fesse')

    def list (self):
        res = []
        for mail in self.mails:
            header = EmailParser().parsestr(''.join(x.decode('utf-8') for x in mail['content']))
            res.append({'id': mail['id'], 'header': header})
        return res

