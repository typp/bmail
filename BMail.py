#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import signal

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import QApplication
except ImportError:
    print("%s: Please install correctly PyQt4" % (sys.argv[0]))
    sys.exit(1)

from MainWindow import *

if __name__ == '__main__':
    try:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as inst:
        print("BMail: Critical error: %s" % (inst,))
