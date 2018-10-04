import sys
import time
import socket
import threading
from PyQt5 import QtWidgets,QtCore,QtGui
from pyuic.ui_gadget import Ui_Gadget
from profile.xobj import XObject


class pyqt5_tcp_udp(QtWidgets.QDialog):
    # 自定义一个信号
    signal_write_msg = QtCore.pyqtSignal(str)

    def __init__(self):
        super(pyqt5_tcp_udp,self).__init__()

        self.ui_obj = XObject.get_object("ui_obj")
        self.main_window_obj = XObject.get_object("main_window_obj")

        self.tcp_socket = None
        self.sever_th = None
        self.client_th = None
        self.client_socket_list = list()
        self.another = None
        self.link = False

        self.click_get_ip()
        self.init()

    def init(self):
        # 信号统一由write_msg处理
        self.signal_write_msg.connect(self.write_msg)

        self.ui_obj.pushButton_get_ip.clicked.connect(self.click_get_ip)

        self.ui_obj.pushButton_link.clicked.connect(self.click_link)

        self.ui_obj.pushButton_unlink.clicked.connect(self.click_unlink)

        self.ui_obj.pushButton_clear_send_area.clicked.connect(self.click_clear_send_area)

        self.ui_obj.pushButton_clear_recv_area.clicked.connect(self.click_clear_recv_area)

        self.ui_obj.pushButton_send.clicked.connect(self.click_send)

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
                self.signal_write_msg.emit("Can not get ip，please connect network！\n")
        finally:
            s.close()

    def click_link(self):
        if self.ui_obj.comboBox_type.currentIndex() == 0:
            self.tcp_server_start()
        if self.ui_obj.comboBox_type.currentIndex() == 1:
            self.tcp_client_start()
        if self.ui_obj.comboBox_type.currentIndex() == 2:
            pass
            #self.udp_server_start()
        if self.ui_obj.comboBox_type.currentIndex() == 3:
            pass
            #self.udp_client_start()
        self.link = True
        self.ui_obj.pushButton_unlink.setEnabled(True)
        self.ui_obj.pushButton_link.setEnabled(False)

    def tcp_client_start(self):
        pass

    def tcp_server_start(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 取消主动断开连接四次握手后的TIME_WAIT状态
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设定套接字为非阻塞式
        self.tcp_socket.setblocking(False)
        try:
            port = int(self.ui_obj.lineEdit_port.text())
            self.tcp_socket.bind(('', port))
        except Exception as ret:
            msg = 'Please check port!\n'
            self.signal_write_msg.emit(msg)
        else:
            self.tcp_socket.listen()
            self.sever_th = threading.Thread(target=self.tcp_server_concurrency)
            self.sever_th.start()
            msg = 'TCP Server are listening port:%s\n' % str(port)
            self.signal_write_msg.emit(msg)

    def tcp_server_concurrency(self):
        while True:
            try:
                client_socket, client_address = self.tcp_socket.accept()
            except Exception as ret:
                time.sleep(0.001)
            else:
                client_socket.setblocking(False)
                # 将创建的客户端套接字存入列表,client_address为ip和端口的元组
                self.client_socket_list.append((client_socket, client_address))
                msg = 'TCP服务端已连接IP:%s端口:%s\n' % client_address
                self.signal_write_msg.emit(msg)
            # 轮询客户端套接字列表，接收数据
            for client, address in self.client_socket_list:
                try:
                    recv_msg = client.recv(1024)
                except Exception as ret:
                    pass
                else:
                    if recv_msg:
                        msg = recv_msg.decode('utf-8')
                        msg = 'From IP:{}port:{}:\n{}\n'.format(address[0], address[1], msg)
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

                self.st.stop_thread(self.sever_th)
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
                self.st.stop_thread(self.client_th)
            except Exception as ret:
                pass
        if self.ui_obj.comboBox_type.currentIndex() == 3:
            try:
                self.udp_socket.close()
                if self.link is True:
                    msg = 'Already disconnect!\n'
                    self.signal_write_msg.emit(msg)

                self.st.stop_thread(self.sever_th)
                self.st.stop_thread(self.client_th)
            except Exception as ret:
                pass
        self.reset()

    def reset(self):
        self.link = False
        self.client_socket_list = list()
        self.ui_obj.pushButton_unlink.setEnabled(False)
        self.ui_obj.pushButton_link.setEnabled(True)

    def click_clear_send_area(self):
        pass

    def click_clear_recv_area(self):
        pass

    def click_send(self):
        pass
