# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication

from UIfunc import Controller

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Controller()
    window.show()
    window.init_DB_user()
    sys.exit(app.exec_())