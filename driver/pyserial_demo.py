import sys
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer

from profile.xobj import XObject
from common import common

class pyqt5_serial(object):
    def __init__(self):
        self.ui_obj = XObject.get_object("ui_obj")
        self.main_window_obj = XObject.get_object("main_window_obj")

        self.main_window_obj.setWindowTitle("Gadget by ZhenhuaWei")
        self.ser = serial.Serial()
        self.port_check()
        self.save_log_flag = 0
        self.save_log_fd = None

        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.ui_obj.lineEdit.setText(str(self.data_num_received))
        self.data_num_sended = 0
        self.ui_obj.lineEdit_2.setText(str(self.data_num_sended))

        self.init()

    def init(self):
        # 串口检测按钮
        self.ui_obj.s1__box_1.clicked.connect(self.port_check)

        # 串口信息显示
        self.ui_obj.s1__box_2.currentTextChanged.connect(self.port_imf)

        # 打开串口按钮
        self.ui_obj.open_button.clicked.connect(self.port_open)

        # 关闭串口按钮
        self.ui_obj.close_button.clicked.connect(self.port_close)

        # 发送数据按钮
        self.ui_obj.s3__send_button.clicked.connect(self.data_send)

        # 保存日志
        self.ui_obj.save_log_cb.clicked.connect(self.save_log)

        # 定时发送数据
        self.timer_send = QTimer()
        self.timer_send.timeout.connect(self.data_send)
        self.ui_obj.timer_send_cb.stateChanged.connect(self.data_send_timer)

        # 定时器接收数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.data_receive)

        # 清除发送窗口
        self.ui_obj.s3__clear_button.clicked.connect(self.send_data_clear)

        # 清除接收窗口
        self.ui_obj.s2__clear_button.clicked.connect(self.receive_data_clear)

    # 保存日志
    def save_log(self):
        try:
            if self.ui_obj.save_log_cb.checkState():
                self.file_path =  QtWidgets.QFileDialog.getSaveFileName(self.main_window_obj,"save file","" ,"Txt files(*.log)")
                self.ui_obj.timestamp_cb.setEnabled(False)
                if self.file_path[0] != '':
                    self.save_log_fd = open(self.file_path[0], "w")
                else:
                    self.ui_obj.timestamp_cb.setEnabled(True)
                    self.ui_obj.save_log_cb.setCheckState(0)

            else:
                self.save_log_fd.close()
                self.save_log_fd = None
                self.ui_obj.timestamp_cb.setEnabled(True)
        except:
            self.save_log_fd = None
            self.ui_obj.save_log_cb.setCheckState(0)
            self.ui_obj.timestamp_cb.setEnabled(True)
            QMessageBox.critical(self.main_window_obj, "Open Error", "Can not open this files, please check!")
            return None

    # 串口检测
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.ui_obj.s1__box_2.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.ui_obj.s1__box_2.addItem(port[0])
        if len(self.Com_Dict) == 0:
            self.ui_obj.state_label.setText("No Serial Port")

    # 串口信息
    def port_imf(self):
        # 显示选定的串口的详细信息
        imf_s = self.ui_obj.s1__box_2.currentText()
        if imf_s != "":
            self.ui_obj.state_label.setText(self.Com_Dict[self.ui_obj.s1__box_2.currentText()])

    # 打开串口
    def port_open(self):
        try:
            self.ser.port = self.ui_obj.s1__box_2.currentText()
            self.ser.baudrate = int(self.ui_obj.s1__box_3.currentText())
            self.ser.bytesize = int(self.ui_obj.s1__box_4.currentText())
            self.ser.stopbits = int(self.ui_obj.s1__box_6.currentText())
            self.ser.parity = self.ui_obj.s1__box_5.currentText()
            self.ser.open()
        except:
            QMessageBox.critical(self.main_window_obj, "Port Error", "Can not open this port, please check!")
            return None

        # 打开串口接收定时器，周期为2ms
        self.timer.start(2)

        if self.ser.isOpen():
            #清空缓存区
            self.ser.reset_output_buffer()
            self.ui_obj.open_button.setEnabled(False)
            self.ui_obj.close_button.setEnabled(True)
            self.ui_obj.formGroupBox1.setTitle("Port State(Opened)")

    # 关闭串口
    def port_close(self):
        self.timer.stop()
        self.timer_send.stop()
        try:
            self.ser.close()
        except:
            pass
        self.ui_obj.open_button.setEnabled(True)
        self.ui_obj.close_button.setEnabled(False)
        self.ui_obj.lineEdit_3.setEnabled(True)
        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.ui_obj.lineEdit.setText(str(self.data_num_received))
        self.data_num_sended = 0
        self.ui_obj.lineEdit_2.setText(str(self.data_num_sended))
        self.ui_obj.formGroupBox1.setTitle("Port State(Closed)")

    # 发送数据
    def data_send(self):
        if self.ser.isOpen():
            input_s = self.ui_obj.s3__send_text.toPlainText()
            if input_s != "":
                # 非空字符串
                if self.ui_obj.hex_send.isChecked():
                    # hex发送
                    input_s = input_s.strip()
                    send_list = []
                    while input_s != '':
                        try:
                            num = int(input_s[0:2], 16)
                        except ValueError:
                            QMessageBox.critical(self.main_window_obj, 'wrong data', 'Please enter hexadecimal, separated by spaces!')
                            return None
                        input_s = input_s[2:].strip()
                        send_list.append(num)
                    input_s = bytes(send_list)
                else:
                    # ascii发送
                    input_s = (input_s + '\r\n').encode('utf-8')

                num = self.ser.write(input_s)
                self.data_num_sended += num
                self.ui_obj.lineEdit_2.setText(str(self.data_num_sended))
        else:
            pass

    # 接收数据
    def data_receive(self):
        try:
            num = self.ser.inWaiting()
        except:
            self.port_close()
            return None
        if num > 5:
            data = self.ser.read(num)
            num = len(data)
            out_srt = ''

            #添加时间戳
            if self.ui_obj.timestamp_cb.checkState():
                out_srt = common.get_datetime()
                out_srt = "[" + out_srt + "] "
            # hex显示
            if self.ui_obj.hex_receive.checkState():
                out_s = ''
                for i in range(0, len(data)):
                    out_s = out_s + '{:02X}'.format(data[i]) + ' '
                out_s = out_srt + out_s + "\r\n"
                self.ui_obj.s2__receive_text.insertPlainText(out_s)
            else:
                # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
                out_s = out_srt + data.decode('iso-8859-1')
                self.ui_obj.s2__receive_text.insertPlainText(out_s)

            if self.save_log_fd is not None:
                self.save_log_fd.write(out_s)

            # 统计接收字符的数量
            self.data_num_received += num
            self.ui_obj.lineEdit.setText(str(self.data_num_received))

            # 获取到text光标
            textCursor = self.ui_obj.s2__receive_text.textCursor()
            # 滚动到底部
            textCursor.movePosition(textCursor.End)
            # 设置光标到text中去
            self.ui_obj.s2__receive_text.setTextCursor(textCursor)
        else:
            pass

    # 定时发送数据
    def data_send_timer(self):
        if self.ui_obj.timer_send_cb.isChecked():
            self.timer_send.start(int(self.ui_obj.lineEdit_3.text()))
            self.ui_obj.lineEdit_3.setEnabled(False)
        else:
            self.timer_send.stop()
            self.ui_obj.lineEdit_3.setEnabled(True)

    # 清除显示
    def send_data_clear(self):
        self.ui_obj.s3__send_text.setText("")

    def receive_data_clear(self):
        self.ui_obj.s2__receive_text.setText("")



