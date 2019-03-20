import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow,QMessageBox
from driver.pyserial_demo import pyqt5_serial
from driver.tcp_udp_demo import pyqt5_tcp_udp
from profile.xobj import XObject
from pyuic.ui_gadget import Ui_Gadget
from common.common import StopThreading


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window_obj = QtWidgets.QWidget()

    ui_obj = Ui_Gadget()
    ui_obj.setupUi(main_window_obj)

    classes = globals()
    XObject.set_classes(classes)

    XObject.set_object("ui_obj", ui_obj)
    XObject.set_object("main_window_obj", main_window_obj)

    # add driver init
    stop_thread = StopThreading()
    serial_obj = pyqt5_serial()
    #tcp_udp_obj = pyqt5_tcp_udp(stop_thread)


    main_window_obj.show()
    sys.exit(app.exec_())