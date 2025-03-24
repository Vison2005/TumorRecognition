#main.py
import sys
from PyQt5.QtWidgets import QApplication
from interface import MainWindow
flag = 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
