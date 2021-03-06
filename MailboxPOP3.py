#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import poplib
import re
import datetime
import email, email.parser
from email.header import decode_header
import quopri
import threading
from time import sleep

from Dialog_Loading import *
from PyQt4.QtGui import QMessageBox
from functools import partial

Parser = email.parser.BytesParser()

class MailboxPOP3:

    def __init__ (self, profile):
        self.config = profile['config']['receiver']
        self.storageDir = None
        self.mails = []
        self.local_mails = []
        self.connector = None
        self.dialog = None
        self.synced = False
        self.dialog = Dialog_Loading(self)
        self.dialog.show()
        thr = threading.Thread(target=partial(self.create_connection, profile, self.dialog))
        thr.start()
        while True:
            thr.join(0.1)
            if thr.is_alive():
                QtGui.QApplication.processEvents()
                self.dialog.repaint()
                self.dialog.update()
            else:
                self.dialog.hide()
                break
        self.get_local_mails()

    def read_local_mail (self, filename):
        data = bytes()
        with open(filename, "rb") as stream:
            chunk = stream.read(4096)
            while chunk:
                data += chunk
                chunk = stream.read(4096)
        return data

    def get_local_mails (self):
        files = [os.path.join(self.storageDir, name) for name in os.listdir(self.storageDir)]
        mailno = -1
        for path in files:
            data = self.read_local_mail(path)
            self.local_mails.append({'id': mailno, 'content': data, 'path': path})
            mailno -= 1

    def create_connection (self, profile, dialog):
        pop3 = poplib.POP3_SSL if self.config['ssl'] else poplib.POP3
        safe_name = re.sub(r"[^A-Za-z0-9-]", "-", profile['name'])
        self.storageDir = os.path.join(
            'storage',
            '%i-%s' % (profile['id'], safe_name))
        try:
            os.mkdir(self.storageDir)
        except FileExistsError:
            pass
        try:
            self.connector = pop3(self.config['host'], self.config['port'])
        except Exception:
            pass
        else:
            print("Logging in ...")
            dialog.message.setText("Logging in ...")
            self.connector.user(self.config['username'])
            self.connector.pass_(self.config['password'])

    def reconnect (self):
        print("Resyncing ...")
        if self.connector:
            self.connector.quit()
        pop3 = poplib.POP3_SSL if self.config['ssl'] else poplib.POP3
        try:
            self.connector = pop3(self.config['host'], self.config['port'])
        except Exception:
            pass
        else:
            self.connector.user(self.config['username'])
            self.connector.pass_(self.config['password'])

    def walk_and_decode (self, header, content_type):
        content = ''
        for part in header.walk():
            charset = part.get_content_charset()
            if part.get_content_type() == content_type:
                part_str = part.get_payload(decode=True)
                content += part_str.decode(charset)
        return content

    def decode (self, content):
        header = Parser.parsebytes(content)
        content = ''
        try:
            content = self.walk_and_decode(header, 'text/html')
            if not content:
                bootstrap = '<html><head><style>body{background-color:#ffffff;}</style></head><body>%s</body></html>'
                content = self.walk_and_decode(header, 'text/plain')
                content = bootstrap % content.replace('\n', '<br />')
        except Exception:
            return 'Cannot decode message.'
        else:
            return content

    def fdecode (self, content):
        try:
            tmp = decode_header(content)
            return tmp[0][0].decode(tmp[0][1])
        except Exception:
            return content

    def get (self, mailno):
        content = None
        for mail in self.local_mails:
            if mail['id'] == mailno:
                header = Parser.parsebytes(mail['content'])
                return self.fdecode(header['From']), self.fdecode(header['Subject']), self.fdecode(header['Date']), self.decode(mail['content'])
        for mail in self.mails:
            if mail['id'] == mailno:
                header = Parser.parsebytes(mail['content'])
                return self.fdecode(header['From']), self.fdecode(header['Subject']), self.fdecode(header['Date']), self.decode(mail['content'])
        return 'Mail is empty.'

    def sync (self):
        self.dialog = Dialog_Loading(self)
        self.dialog.show()
        thr = threading.Thread(target=partial(self.do_sync, self.dialog))
        thr.start()
        while True:
            thr.join(0.1)
            if thr.is_alive():
                QtGui.QApplication.processEvents()
                self.dialog.repaint()
                self.dialog.update()
            else:
                self.dialog.hide()
                break

    def delete (self, mailno):
        if mailno < 0:
            for mail in self.local_mails:
                if mail['id'] == mailno:
                    os.unlink(mail['path'])
                    self.local_mails.remove(mail)
        else:
            self.connector.dele(mailno)

    def do_sync (self, dialog):
        if self.synced:
            self.reconnect()
        mail_list = self.connector.list()
        dialog.message.setText("Retrieving messages ...")
        print(mail_list[0].decode('utf-8'))
        self.mails = []
        for mail_info in mail_list[1]:
            mailno = int(mail_info.decode('utf-8').split(' ')[0])
            mail = self.connector.retr(mailno)
            content = b'\n'.join(mail[1])
            header = Parser.parsebytes(content)
            filename = datetime.datetime.now().isoformat()
            subject = header['Subject'] if isinstance(header['Subject'], str) else '<No subject>'
            filename += re.sub(r"[^A-Za-z0-9-]", "-", subject)
            filename = filename[:92]
            filename += '.xml'
            path = os.path.join(self.storageDir, filename)
            with open(path, 'wb') as stream:
                stream.write(content)
            self.mails.append({'id': mailno, 'content': content})
        self.synced = True

    def list (self):
        res = []
        for mail in self.local_mails:
            header = Parser.parsebytes(mail['content'])
            res.append({'id': mail['id'], 'header': header})
        for mail in self.mails:
            header = Parser.parsebytes(mail['content'])
            res.append({'id': mail['id'], 'header': header})
        return res

    def logout (self):
        if self.connector:
            print("Closing connection.")
            try:
                self.connector.quit()
            except Exception:
                pass
            self.connector = None
