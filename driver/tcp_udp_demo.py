import sys
import socket
from PyQt5 import QtWidgets
from pyuic.ui_gadget import Ui_Gadget


class pyqt5_tcp_udp(QtWidgets.QWidget, Ui_Gadget):
    def __init__(self):
        super(pyqt5_tcp_udp, self).__init__()
        self.setupUi(self)
        self.client_socket_list = list()
        self.another = None
        self.link = False

        # 打开软件时默认获取本机ip
        self.click_get_ip()

    def click_get_ip(self):
        """
        pushbutton_get_ip控件点击触发的槽
        :return: None
        """
        # 获取本机ip
        self.lineEdit_local_ip.clear()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            my_addr = s.getsockname()[0]
            self.lineEdit_local_ip.setText(str(my_addr))
        except Exception as ret:
            # 若无法连接互联网使用，会调用以下方法
            try:
                my_addr = socket.gethostbyname(socket.gethostname())
                self.lineEdit_local_ip.setText(str(my_addr))
            except Exception as ret_e:
                self.signal_write_msg.emit("Can not get ip，please connect network！\n")
        finally:
            s.close()