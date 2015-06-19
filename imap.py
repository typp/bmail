#!/usr/bin/env python3

##########
import yaml
config = None
with open('config.yaml', 'r') as stream:
    config = yaml.load(stream)
##########

print (config["MonCompte"]["username"])

import imaplib
import re


class IMAPClient(object):
    connection = None
    list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

    def __init__(self, hostname, ssl=True):
        if ssl: self.connection = imaplib.IMAP4_SSL(hostname)
        else: self.connection = imaplib.IMAP4(hostname)

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
        if typ == 'OK': return [parse_list(line.decode("utf-8"))[2] for line in mlist]
        return None

imap = IMAPClient(config["MonCompte"]["hostname"], ssl=config["MonCompte"]["ssl"])
imap.login(config["MonCompte"]["username"], config["MonCompte"]["password"])
print(imap.list())
