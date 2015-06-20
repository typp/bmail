#! /usr/bin/env python3

import sys
import getpass
import poplib

class MailboxPOP3:

        def __init__ (self, config):
                self.config = config
                print("Connecting...", end="", flush=True)
                pop3 = poplib.POP3_SSL if config['ssl'] else poplib.POP3
                self.connector = pop3(config['host'], config['port'])
                self.connector.user(config['username'])
                self.connector.pass_(config['password'])

        def list (self):
                print("LIST...")
                mails = self.connector.list()
                print(mails)
                print(self.connector.retr(1))

if __name__ == '__main__':
        M = MailboxPOP3(sys.argv[1], int(sys.argv[2]))
        M.list()
