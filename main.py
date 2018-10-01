import sys
from PyQt5 import QtWidgets
from driver.pyserial_demo import Pyqt5_Serial

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = Pyqt5_Serial()
    myshow.show()
    
    sys.exit(app.exec_())