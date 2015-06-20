# -*- coding: utf-8 -*-

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.fed.append('\n\n')
        elif tag == 'br':
            self.fed.append('\n')
    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.fed.append('\n\n')
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

class SendboxSMTP:
    connector = None

    def __init__(self, profile):
        self.config = profile['config']['sender']
        smtp = smtplib.SMTP_SSL if self.config['ssl'] else smtplib.SMTP
        self.connector = smtp(self.config['host'], self.config['port'])
        if self.config['auth']:
            if self.config['tls']:
                try:
                    self.connector.ehlo()
                    self.connector.starttls()
                    self.connector.ehlo()
                except smtplib.SMTPException:
                    pass
            self.connector.login(self.config['username'], self.config['password'])

    def __del__(self):
        if self.connector:
            try:
                self.connector.quit()
            except:
                pass

    def send(self, to, subject, html):
        mail = MIMEMultipart('alternative')
        mail['Subject'] = subject
        mail['From'] = self.config['email']
        mail['To'] = to

        stripper = MLStripper()
        stripper.feed(html)
        text = stripper.get_data()

        mail.attach(MIMEText(text, 'plain'))
        mail.attach(MIMEText(html, 'html'))

        self.connector.sendmail(mail['From'], mail['To'], mail.as_string())
