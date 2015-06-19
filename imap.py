#!/usr/bin/env python3

import imaplib
import re

class IMAPClient(object):
    connection = None
    list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

    def __init__(self, hostname):
        self.connection = imaplib.IMAP4_SSL(hostname)

    def login(self, username, password):
        self.connection.login(username, password)

    def logout(self):
        self.connection.logout()

    def list(self, **kwargs):
        def parse_list(line):
            flags, delimiter, mailbox_name = self.list_response_pattern.match(line).groups()
            mailbox_name = mailbox_name.strip('"')
            return (flags, delimiter, mailbox_name)
        typ, mlist = self.connection.list(**kwargs)
        if typ == 'OK': return [parse_list(line)[2] for line in mlist]
        return None

imap = IMAPClient("imap.gmail.com")
imap.login("zadkiel.aharonian@gmail.com", "****")
print(imap.list())
