import sys
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

from profile.xobj import XObject
from common import common

class pyqt5_serial(object):
    def __init__(self):
        self.ui_obj = XObject.get_object("ui_obj")
        self.main_window_obj = XObject.get_object("main_window_obj")

        self.main_window_obj.setWindowTitle("HT_RF_TRSP_Tools-v0.0.3")
        self.main_window_obj.setWindowIcon(QIcon('./image/ico.png'))
        self.ser = serial.Serial()
        self.port_check()
        self.save_log_flag = 0
        self.save_log_fd = None

        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.ui_obj.recv_len_el.setText(str(self.data_num_received))
        self.data_num_sended = 0
        self.ui_obj.send_len_el.setText(str(self.data_num_sended))

        # 11-99变量
        self.small_value = 11
        self.big_value = 11

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

        # 保存日志
        self.ui_obj.save_log_cb.clicked.connect(self.save_log)

        # 定时器接收数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.data_receive)

        # 清除组帧透传窗口
        self.ui_obj.s3__clear_button_3.clicked.connect(self.compose_data_clear)

        # 清除接收窗口
        self.ui_obj.s2__clear_button.clicked.connect(self.receive_data_clear)

        # 隐藏端口设置
        self.ui_obj.setting_hide_cb.clicked.connect(self.setting_hide)

        # 发送按钮
        self.ui_obj.send_bt.clicked.connect(self.send_func)

        # 组信标帧按钮
        self.ui_obj.beacon_compose_bt.clicked.connect(self.compose_trsp_beacon)

        # 组信标帧按钮
        self.ui_obj.test_beacon_send_bt.clicked.connect(self.test_beacon_send)

    def setting_hide(self):
        if self.ui_obj.setting_hide_cb.isChecked():
            self.ui_obj.formGroupBox1.hide()
        else:
            self.ui_obj.formGroupBox1.show()

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
            self.ui_obj.s1__box_1.setEnabled(False)
            self.ui_obj.s1__box_2.setEnabled(False)
            self.ui_obj.s1__box_3.setEnabled(False)
            self.ui_obj.s1__box_4.setEnabled(False)
            self.ui_obj.s1__box_5.setEnabled(False)
            self.ui_obj.s1__box_6.setEnabled(False)
            self.ui_obj.close_button.setEnabled(True)
            self.ui_obj.formGroupBox1.setTitle("Port State(Opened)")
            self.ui_obj.port_state.setText("(" + self.ser.port + " opened" + ")")


    # 关闭串口
    def port_close(self):
        self.timer.stop()
        #self.timer_send.stop()
        try:
            self.ser.close()
        except:
            pass
        self.ui_obj.open_button.setEnabled(True)
        self.ui_obj.close_button.setEnabled(False)
        #self.ui_obj.lineEdit_3.setEnabled(True)
        self.ui_obj.s1__box_1.setEnabled(True)
        self.ui_obj.s1__box_2.setEnabled(True)
        self.ui_obj.s1__box_3.setEnabled(True)
        self.ui_obj.s1__box_4.setEnabled(True)
        self.ui_obj.s1__box_5.setEnabled(True)
        self.ui_obj.s1__box_6.setEnabled(True)
        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.ui_obj.recv_len_el.setText(str(self.data_num_received))
        self.data_num_sended = 0
        self.ui_obj.send_len_el.setText(str(self.data_num_sended))
        self.ui_obj.formGroupBox1.setTitle("Port State(Closed)")
        self.ui_obj.port_state.setText("Port Closed")

    # 发送数据
    def data_send(self, input_s, hex_send_flag):
        if self.ser.isOpen():
            if input_s != "":
                # 非空字符串
                if hex_send_flag:
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
                self.ui_obj.send_len_el.setText(str(self.data_num_sended))
        else:
            QMessageBox.critical(self.main_window_obj, "Send Err", "please open Port!")

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
            self.ui_obj.recv_len_el.setText(str(self.data_num_received))

            # 获取到text光标
            textCursor = self.ui_obj.s2__receive_text.textCursor()
            # 滚动到底部
            textCursor.movePosition(textCursor.End)
            # 设置光标到text中去
            self.ui_obj.s2__receive_text.setTextCursor(textCursor)
        else:
            pass

    # 透传区域发送
    def send_func(self):
        input_s = self.compose_func(self.get_trsp_data)
        if input_s is None:
            return
        hex_send_flag = self.ui_obj.hex_send.isChecked()
        self.data_send(input_s, hex_send_flag)

    def test_beacon_send(self):
        input_s = self.compose_func(self.get_beacon_trsp_data)
        if input_s is None:
            return
        hex_send_flag = self.ui_obj.hex_send.isChecked()
        self.data_send(input_s, hex_send_flag)

    # 清除透传数据区
    def compose_data_clear(self):
        self.ui_obj.compose_tx.setText("")

    # 清除接收区
    def receive_data_clear(self):
        self.ui_obj.s2__receive_text.setText("")
        self.data_num_received = 0
        self.ui_obj.recv_len_el.setText(str(self.data_num_received))
        self.data_num_sended = 0
        self.ui_obj.send_len_el.setText(str(self.data_num_sended))

    # 组信标帧
    def compose_trsp_beacon(self, test_flag):
        send_str = ""
        beacon_list = [0x40, 0xcd, 0x01, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, \
            0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x29, 0x12, 0x00, \
            0x60, 0x09, 0x00, 0x09, 0x00, 0x00, 0x7e, 0x03, 0x00]

        #panid
        beacon_list[26] = int(self.ui_obj.beacon_panid_le.text(), 10)>>8
        beacon_list[25] = int(self.ui_obj.beacon_panid_le.text(), 10)&0xff

        # 信标标识
        beacon_list[21] = int(self.ui_obj.beacon_sn_le.text(), 10)

        # 网络规模
        beacon_list[23] = int(self.ui_obj.net_volume_le.text(), 10)>>8
        beacon_list[22] = int(self.ui_obj.net_volume_le.text(), 10)&0xff

        # 场强门限
        beacon_list[24] = int(self.ui_obj.rssi_thr_le.text(), 10)

        # 中心节点地址
        cco_addr_str = self.ui_obj.cco_addr_le.text()
        strlen = len(cco_addr_str)
        if strlen<12:
            cco_addr_str = "0"*(12-strlen)+cco_addr_str
        beacon_list[32] = int(cco_addr_str[0:2], 16)
        beacon_list[31] = int(cco_addr_str[2:4], 16)
        beacon_list[30] = int(cco_addr_str[4:6], 16)
        beacon_list[29] = int(cco_addr_str[6:8], 16)
        beacon_list[28] = int(cco_addr_str[8:10], 16)
        beacon_list[27] = int(cco_addr_str[10:12], 16)

        # Mac 层目的地址
        macdestaddr_str = self.ui_obj.macdestaddr_le.text()
        strlen = len(macdestaddr_str)
        if strlen<12:
            macdestaddr_str = "0"*(12-strlen)+macdestaddr_str
        beacon_list[10] = int(macdestaddr_str[0:2], 16)
        beacon_list[9] = int(macdestaddr_str[2:4], 16)
        beacon_list[8] = int(macdestaddr_str[4:6], 16)
        beacon_list[7] = int(macdestaddr_str[6:8], 16)
        beacon_list[6] = int(macdestaddr_str[8:10], 16)
        beacon_list[5] = int(macdestaddr_str[10:12], 16)

        if (test_flag == 0):
            # Mac 层源地址
            macsrcaddr_str = self.ui_obj.macsrcaddr_le.text()
            strlen = len(macsrcaddr_str)
            if strlen<12:
                macsrcaddr_str = "0"*(12-strlen)+macsrcaddr_str
            beacon_list[16] = int(macsrcaddr_str[0:2], 16)
            beacon_list[15] = int(macsrcaddr_str[2:4], 16)
            beacon_list[14] = int(macsrcaddr_str[4:6], 16)
            beacon_list[13] = int(macsrcaddr_str[6:8], 16)
            beacon_list[12] = int(macsrcaddr_str[8:10], 16)
            beacon_list[11] = int(macsrcaddr_str[10:12], 16)

            for data in beacon_list:
                send_str = send_str + '{:#04X}'.format(data)[2:4] + " "

            self.ui_obj.compose_tx.clear()
            self.ui_obj.compose_tx.setText(send_str)
        else:# 测试 模拟信标应答
            self.ui_obj.compose_tx.clear()

            self.small_value = self.small_value+1
            if self.small_value == 100:
                self.small_value = 11
                self.big_value = self.big_value + 1
                if self.big_value == 100:
                    self.big_value = 11

            addr_str = "00009900"
            addr_str = addr_str + str(self.big_value)
            addr_str = addr_str + str(self.small_value)
            self.ui_obj.macsrcaddr_le.setText(addr_str)

            macsrcaddr_str = self.ui_obj.macsrcaddr_le.text()
            strlen = len(macsrcaddr_str)
            if strlen<12:
                macsrcaddr_str = "0"*(12-strlen)+macsrcaddr_str
            beacon_list[16] = int(macsrcaddr_str[0:2], 16)
            beacon_list[15] = int(macsrcaddr_str[2:4], 16)
            beacon_list[14] = int(macsrcaddr_str[4:6], 16)
            beacon_list[13] = int(macsrcaddr_str[6:8], 16)
            beacon_list[12] = int(macsrcaddr_str[8:10], 16)
            beacon_list[11] = int(macsrcaddr_str[10:12], 16)

            for data in beacon_list:
                send_str = send_str + '{:#04X}'.format(data)[2:4] + " "

        return send_str

    # 获取透传帧
    def get_trsp_data(self):
        return self.ui_obj.compose_tx.toPlainText()

    # 组信标测试帧
    def get_beacon_trsp_data(self):
        return self.compose_trsp_beacon(1)

    #组发送帧 = 固定头尾 + 透传数据
    def compose_func(self, compose_obj):
        try:
            send_str = ''
            send_list = [0x53,0x4D,0,0]
            trsp_list = []
            channel_num_str = self.ui_obj.channel_num_le.text()
            compose_tx_str = compose_obj()

            if int(channel_num_str) >= 0 and int(channel_num_str) <=64:
                send_list[2] = int(channel_num_str)
                compose_tx_str = compose_tx_str.strip()
                while compose_tx_str != '':
                    try:
                        num = int(compose_tx_str[0:2], 16)
                    except ValueError:
                        QMessageBox.critical(self.main_window_obj, 'wrong data', 'Please enter hexadecimal, separated by spaces!')
                        return None
                    compose_tx_str = compose_tx_str[2:].strip()
                    trsp_list.append(num)
                send_list[3] = len(trsp_list)

                send_list.extend(trsp_list)
                send_list.append(common.uchar_checksum(send_list))

                for data in send_list:
                    send_str = send_str + '{:#04X}'.format(data)[2:4] + " "

                return send_str

            else:
                QMessageBox.critical(self.main_window_obj, "Channel Num Err", "Channel Num range 0~64")
                return None
        except Exception as e:
            QMessageBox.critical(self.main_window_obj, "Channel Num Err", "Channel Num range 0~64")
            return None