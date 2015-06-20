#!/usr/bin/env python3

import imaplib
import email

class MailboxIMAP:
    connector = None

    def __init__(self, config):
        self.config = config
        imap = imaplib.IMAP4_SSL if config['ssl'] else poplib.IMAP4
        self.connector = imap(config['host'], config['port'])
        self.connector.login(config['username'], config['password'])

    def __del__(self):
        if self.connector:
            self.connector.logout()

    def list(self, _max = 10):
        mails = []

        rv, data = self.connector.select('INBOX')
        if rv != 'OK': return []
        rv, data = self.connector.search(None, "ALL")
        if rv != 'OK': return []

        for _id in map(int, data[0].split()):
            header = self.get(_id)
            if not header: continue
            mails.append({'id': _id, 'header': header})
        return mails

    def get(self, _id):
        rv, data = self.connector.fetch(str(_id), '(RFC822)')
        if rv != 'OK': return None
        return email.message_from_string(data[0][1].decode('utf-8'))

    def delete(self, _id):
        rv, data = self.connector.store(str(_id), '+FLAGS', r'(\Deleted)')
        if rv != 'OK': return False
        rv, data = self.connector.expunge()
        if rv != 'OK': return False
        return True
