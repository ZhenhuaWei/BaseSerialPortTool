import sys
import time
import socket
import threading
from PyQt5 import QtWidgets,QtCore,QtGui
from pyuic.ui_gadget import Ui_Gadget
from profile.xobj import XObject
from common import common

class pyqt5_tcp_udp(QtWidgets.QDialog):
    # 自定义一个信号
    signal_write_msg = QtCore.pyqtSignal(str)

    def __init__(self, st):
        super(pyqt5_tcp_udp,self).__init__()

        self.ui_obj = XObject.get_object("ui_obj")
        self.main_window_obj = XObject.get_object("main_window_obj")

        self.st = st
        self.tcp_socket = None
        self.udp_socket = None
        self.sever_th = None
        self.client_th = None
        self.client_socket_list = list()
        self.another = None
        self.link = False
        self.address = None

        self.click_get_ip()
        self.init()

    def init(self):
        # 信号统一由write_msg处理
        self.signal_write_msg.connect(self.write_msg)

        self.ui_obj.pushButton_get_ip.clicked.connect(self.click_get_ip)

        self.ui_obj.pushButton_link.clicked.connect(self.click_link)

        self.ui_obj.pushButton_unlink.clicked.connect(self.click_unlink)

        self.ui_obj.p_clear_send_area.clicked.connect(self.click_clear_send_area)

        self.ui_obj.p_clear_recv_area.clicked.connect(self.click_clear_recv_area)

        self.ui_obj.pushButton_send.clicked.connect(self.click_send)

        self.ui_obj.comboBox_type.currentIndexChanged.connect(self.combobox_change)

        self.ui_obj.lb_3.hide()
        self.ui_obj.lineEdit_destination_ip.hide()    
        self.ui_obj.pushButton_unlink.setEnabled(False)

    def click_clear_recv_area(self):
        self.ui_obj.textBrowser_recv.clear()

    def click_clear_send_area(self):
        self.ui_obj.textEdit_send.setText("")

    def combobox_change(self):
        _translate = QtCore.QCoreApplication.translate
        if self.link is True:
            self.close_all()

        if self.ui_obj.comboBox_type.currentIndex() == 0 or self.ui_obj.comboBox_type.currentIndex() == 2:
            self.ui_obj.lb_3.hide()
            self.ui_obj.lineEdit_destination_ip.hide()
            self.ui_obj.lb_2.setText(_translate("Gadget", "Port:"))
        if self.ui_obj.comboBox_type.currentIndex() == 1 or self.ui_obj.comboBox_type.currentIndex() == 3:
            self.ui_obj.lb_3.show()
            self.ui_obj.lineEdit_destination_ip.show()
            self.ui_obj.lb_2.setText(_translate("Gadget", "Destination port:"))


    def write_msg(self, msg):
        self.ui_obj.textBrowser_recv.insertPlainText(msg)
        self.ui_obj.textBrowser_recv.moveCursor(QtGui.QTextCursor.End)

    def click_get_ip(self):
        self.ui_obj.lineEdit_local_ip.clear()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            my_addr = s.getsockname()[0]
            self.ui_obj.lineEdit_local_ip.setText(str(my_addr))
        except Exception as ret:
            # 若无法连接网络，会调用以下方法
            try:
                my_addr = socket.gethostbyname(socket.gethostname())
                self.ui_obj.lineEdit_local_ip.setText(str(my_addr))
            except Exception as ret_e:
                self.signal_write_msg.emit("Can not get ip, please connect network!\n")
        finally:
            s.close()

    def click_link(self):
        ret = False
        if self.ui_obj.comboBox_type.currentIndex() == 0:
            ret = self.tcp_server_start()
        if self.ui_obj.comboBox_type.currentIndex() == 1:
            ret = self.tcp_client_start()
        if self.ui_obj.comboBox_type.currentIndex() == 2:
            ret = self.udp_server_start()
        if self.ui_obj.comboBox_type.currentIndex() == 3:
            ret = self.udp_client_start()
        if ret:
            self.link = True
            self.ui_obj.pushButton_unlink.setEnabled(True)
            self.ui_obj.pushButton_link.setEnabled(False)

    def udp_client_start(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.address = (str(self.ui_obj.lineEdit_destination_ip.text()), int(self.ui_obj.lineEdit_port.text()))
        except Exception as ret:
            msg = 'Please check destination ip and Port!\n'
            self.signal_write_msg.emit(msg)
            return False
        else:
            msg = 'UDP Client already start!\n'
            self.signal_write_msg.emit(msg)
            return True

    def udp_server_start(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.port = int(self.ui_obj.lineEdit_port.text())
            address = ('', self.port)
            self.udp_socket.bind(address)
        except Exception as ret:
            msg = 'Please check Port!\n'
            self.signal_write_msg.emit(msg)
            return False
        else:
            self.sever_th = threading.Thread(target=self.udp_server_concurrency)
            self.sever_th.start()
            msg = 'UDP Server are listening Port:{}\n'.format(self.port)
            self.signal_write_msg.emit(msg)
            return True

    def udp_server_concurrency(self):
        while True:
            recv_msg, recv_addr = self.udp_socket.recvfrom(1024)
            msg = recv_msg.decode('utf-8')

            #添加时间戳
            if self.ui_obj.checkBox_timestamp.checkState():
                out_srt = common.get_datetime()
                msg = "[" + out_srt + "]" + msg

            msg = 'From ip:{} Port:{}:\n{}\n'.format(recv_addr[0], recv_addr[1], msg)
            self.signal_write_msg.emit(msg)

    def tcp_client_concurrency(self):
        while True:
            recv_msg = self.tcp_socket.recv(1024)
            if recv_msg:
                msg = recv_msg.decode('utf-8')

                #添加时间戳
                if self.ui_obj.checkBox_timestamp.checkState():
                    out_srt = common.get_datetime()
                    msg = "[" + out_srt + "]" + msg

                msg = 'From ip:{} Port:{}:\n{}\n'.format(self.address[0], self.address[1], msg)
                self.signal_write_msg.emit(msg)
            else:
                self.tcp_socket.close()
                self.reset()
                msg = 'Disconnect from Server!\n'
                self.signal_write_msg.emit(msg)
                break

    def tcp_client_start(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.address = (str(self.ui_obj.lineEdit_destination_ip.text()), int(self.ui_obj.lineEdit_port.text()))
        except Exception as ret:
            msg = 'Please check destination ip and destination port!\n'
            self.signal_write_msg.emit(msg)
            return False
        else:
            try:
                msg = 'Connecting destination Server\n'
                self.signal_write_msg.emit(msg)
                self.tcp_socket.connect(self.address)
            except Exception as ret:
                msg = 'Can not connect destination Server!\n'
                self.signal_write_msg.emit(msg)
                return False
            else:
                self.client_th = threading.Thread(target=self.tcp_client_concurrency)
                self.client_th.start()
                msg = 'TCP Client already connected ip:%s Port:%s\n' % self.address
                self.signal_write_msg.emit(msg)
                return True

    def tcp_server_start(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.setblocking(False)
        try:
            port = int(self.ui_obj.lineEdit_port.text())
            self.tcp_socket.bind(('', port))
        except Exception as ret:
            msg = 'Please check Port!\n'
            self.signal_write_msg.emit(msg)
            return False
        else:
            self.tcp_socket.listen()
            self.sever_th = threading.Thread(target=self.tcp_server_concurrency)
            self.sever_th.start()
            msg = 'TCP Server are listening Port:%s\n' % str(port)
            self.signal_write_msg.emit(msg)
            return True

    def tcp_server_concurrency(self):
        while True:
            try:
                client_socket, client_address = self.tcp_socket.accept()
            except Exception as ret:
                time.sleep(0.001)
            else:
                client_socket.setblocking(False)
                self.client_socket_list.append((client_socket, client_address))
                msg = 'TCP Server connect to ip:%s Port:%s\n' % client_address
                self.signal_write_msg.emit(msg)
            for client, address in self.client_socket_list:
                try:
                    recv_msg = client.recv(1024)
                except Exception as ret:
                    pass
                else:
                    if recv_msg:
                        msg = recv_msg.decode('utf-8')
                        #添加时间戳
                        if self.ui_obj.checkBox_timestamp.checkState():
                            out_srt = common.get_datetime()
                            msg = "[" + out_srt + "]" + msg
                            
                        msg = 'From ip:{} Port:{}:\n{}\n'.format(address[0], address[1], msg)
                        self.signal_write_msg.emit(msg)
                    else:
                        client.close()
                        self.client_socket_list.remove((client, address))


    def click_unlink(self):
        self.close_all()
        self.link = False
        self.ui_obj.pushButton_unlink.setEnabled(False)
        self.ui_obj.pushButton_link.setEnabled(True)

    def close_all(self):
        if self.ui_obj.comboBox_type.currentIndex() == 0:
            try:
                for client, address in self.client_socket_list:
                    client.close()
                self.tcp_socket.close()
                if self.link is True:
                    msg = 'Already disconnect!\n'
                    self.signal_write_msg.emit(msg)

                self.st.stop_thread(self.sever_th)
            except Exception as ret:
                pass
        if self.ui_obj.comboBox_type.currentIndex() == 1:
            try:
                self.tcp_socket.close()
                if self.link is True:
                    msg = 'Already disconnect!\n'
                    self.signal_write_msg.emit(msg)

                self.st.stop_thread(self.client_th)
            except Exception as ret:
                pass
        if self.ui_obj.comboBox_type.currentIndex() == 2:
            try:
                self.udp_socket.close()
                if self.link is True:
                    msg = 'Already disconnect!\n'
                    self.signal_write_msg.emit(msg)

                self.st.stop_thread(self.sever_th)
            except Exception as ret:
                pass
        if self.ui_obj.comboBox_type.currentIndex() == 3:
            try:
                self.udp_socket.close()
                if self.link is True:
                    msg = 'Already disconnect!\n'
                    self.signal_write_msg.emit(msg)

                self.st.stop_thread(self.client_th)
            except Exception as ret:
                pass
        self.reset()

    def reset(self):
        self.link = False
        self.client_socket_list = list()
        self.ui_obj.pushButton_unlink.setEnabled(False)
        self.ui_obj.pushButton_link.setEnabled(True)

    def click_send(self):
        if self.link is False:
            msg = 'Please check and connect to Server!\n'
            self.signal_write_msg.emit(msg)
        else:
            try:
                send_msg = (str(self.ui_obj.textEdit_send.toPlainText())).encode('utf-8')

                if self.ui_obj.comboBox_type.currentIndex() == 0:
                    for client, address in self.client_socket_list:
                        client.send(send_msg)
                    msg = 'TCP Server already send\n'
                    self.signal_write_msg.emit(msg)
                if self.ui_obj.comboBox_type.currentIndex() == 1:
                    self.tcp_socket.send(send_msg)
                    msg = 'TCP Client already send\n'
                    self.signal_write_msg.emit(msg)
                if self.ui_obj.comboBox_type.currentIndex() == 2:
                    msg = 'UDP Server can not send, Please change to UDP Client!\n'
                    self.signal_write_msg.emit(msg)
                if self.ui_obj.comboBox_type.currentIndex() == 3:
                    self.udp_socket.sendto(send_msg, self.address)
                    msg = 'UDP Client already send\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                msg = 'Send fail!\n'
                self.signal_write_msg.emit(msg)
