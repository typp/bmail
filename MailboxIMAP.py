# -*- coding: utf-8 -*-

import imaplib
import email.parser
import threading
from time import sleep

from Dialog_Loading import *
from PyQt5.QtWidgets import QMessageBox
from functools import partial

Parser = email.parser.BytesParser()

class MailboxIMAP:

    def __init__ (self, profile):
        self.config = profile['config']['receiver']
        self.connector = None
        self.dialog = Dialog_Loading(self)
        self.dialog.show()
        thr = threading.Thread(target=partial(self.create_connection, profile, self.dialog))
        thr.start()
        while True:
            thr.join(0.1)
            if thr.is_alive():
                QtWidgets.QApplication.processEvents()
                self.dialog.repaint()
                self.dialog.update()
            else:
                self.dialog.hide()
                break

    def logout (self):
        if self.connector:
            print('Closing connection.')
            self.connector.logout()

    def create_connection (self, profile, dialog):
        imap = imaplib.IMAP4_SSL if self.config['ssl'] else imaplib.IMAP4
        try:
            self.connector = imap(self.config['host'], self.config['port'])
        except:
            pass
        else:
            print("Logging in ...")
            dialog.message.setText("Logging in ...")
            self.connector.login(self.config['username'], self.config['password'])

    def walk_and_decode (self, header, content_type):
        content = ''
        for part in header.walk():
            charset = part.get_content_charset()
            if part.get_content_type() == content_type:
                part_str = part.get_payload(decode=True)
                content += part_str.decode(charset)
        return content

    def fdecode (self, content):
        return content

    def decode (self, content):
        header = Parser.parsebytes(content)
        content = ''
        try:
            content = self.walk_and_decode(header, 'text/html')
            if not content:
                content = self.walk_and_decode(header, 'text/plain')
        except:
            return 'Cannot decode message'
        else:
            return content

    def get (self, mailno):
        rv, data = self.connector.fetch(str(mailno), '(RFC822)')
        if rv != 'OK': return None
        header = Parser.parsebytes(data[0][1])
        return header['From'], header['Subject'], header['Date'], self.decode(data[0][1])

    def sync (self):
        pass

    def list (self):
        mails = []
        rv, data = self.connector.select('INBOX')
        if rv != 'OK': return []
        rv, data = self.connector.search(None, "ALL")
        if rv != 'OK': return []
        for mailno in map(int, data[0].split()):
            rv, data = self.connector.fetch(str(mailno), '(RFC822)')
            if rv != 'OK': continue
            header = Parser.parsebytes(data[0][1])
            mails.append({'id': mailno, 'header': header})
        return mails

    def delete (self, mailno):
        rv, data = self.connector.store(str(mailno), '+FLAGS', r'(\Deleted)')
        if rv != 'OK': return False
        rv, data = self.connector.expunge()
        if rv != 'OK': return False
        return True
