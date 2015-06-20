# -*- coding: utf-8 -*-

import imaplib
import email.parser

from Dialog_Loading import *
from PyQt5.QtWidgets import QMessageBox

Parser = email.parser.BytesParser()

class MailboxIMAP:
    def __init__ (self, profile):
        self.config = profile['config']['receiver']
        self.connector = None
        self.create_connection(profile)

    def __del__ (self):
        if self.connector:
            self.connector.logout()

    def create_connection (self, profile):
        dialog = Dialog_Loading(self)
        dialog.show()

        imap = imaplib.IMAP4_SSL if self.config['ssl'] else imaplib.IMAP4
        try:
            self.connector = imap(self.config['host'], self.config['port'])
        except:
            alert = QMessageBox(QMessageBox.Critical, "Error",
                                "Could not connect to %s." % self.config["host"])
        else:
            print("Logging in ...")
            dialog.message.setText("Logging in ...")
            self.connector.login(self.config['username'], self.config['password'])
            dialog.hide()

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
                content = self.walk_and_decode(header, 'text/plain')
        except:
            return 'Cannot decode message'
        else:
            return content

    def get (self, mailno):
        rv, data = self.connector.fetch(str(mailno), '(RFC822)')
        if rv != 'OK': return None
        return self.decode(data[0][1])

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
