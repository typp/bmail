#! /usr/bin/env python3

import sys
import getpass
import poplib

class MailboxPOP3:

        def __init__ (self, host, port=110):
                print("Connecting...")
                self.connector = poplib.POP3_SSL(host, port)
                username = input("Username: ")
                self.connector.user(username)
                self.connector.pass_(getpass.getpass())

        def list (self):
                print("LIST...")
                mails = self.connector.list()
                print(mails)
                print(self.connector.retr(1))

if __name__ == '__main__':
        M = MailboxPOP3(sys.argv[1], int(sys.argv[2]))
        M.list()
