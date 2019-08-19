import sys
import serial
import operator
import serial.tools.list_ports
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox,QHeaderView,QAbstractItemView
from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtGui import QIcon,QColor,QStandardItemModel,QStandardItem,QBrush,QColor

from profile.xobj import XObject
from common import common

class pyqt5_serial(object):
    def __init__(self):
        self.ui_obj = XObject.get_object("ui_obj")
        self.main_window_obj = XObject.get_object("main_window_obj")

        self.main_window_obj.setWindowTitle("HT_RF_PRODUCTION_TEST_TOOLS-v0.0.1 by WeiZhenhua")
        self.main_window_obj.setWindowIcon(QIcon('./image/ico.png'))
        self.ser = serial.Serial()
        self.port_check()

        self.send_buf = []

        self.timing_num = 1000
        self.ui_obj.timing_le.setText(str(self.timing_num))
        self.test_times = 3
        self.ui_obj.test_times_le.setText(str(self.test_times))

        #设置数据层次结构，4行4列
        self.model=QStandardItemModel(3,3)
        #设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(['接收','发送','测试结果'])
        for row in range(5):
            for column in range(3):
                if column ==2:
                    item=QStandardItem('通过')
                    item.setTextAlignment(Qt.AlignCenter)
                    # item.setForeground(QBrush(QColor(255, 0, 0)))# 红色
                    item.setForeground(QBrush(QColor(0, 255, 0)))# 绿色
                else:
                    item=QStandardItem('%d'%(row))
                    item.setTextAlignment(Qt.AlignCenter)
                    
                #设置每个位置的文本值
                self.model.setItem(row,column,item)
        self.ui_obj.testcase_tv.setModel(self.model)
        # 横向填满表格
        self.ui_obj.testcase_tv.horizontalHeader().setStretchLastSection(True)
        self.ui_obj.testcase_tv.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui_obj.testcase_tv.setSelectionMode(QAbstractItemView.NoSelection) #不可选中
        self.ui_obj.testcase_tv.setEditTriggers(QAbstractItemView.NoEditTriggers) #不可编辑
        # self.ui_obj.testcase_tv.setShowGrid(False) #网格线条不可见
        self.init()
        # self.model.removeRow(3)删除

    def init(self):
        # 串口检测按钮
        self.ui_obj.s1__box_1.clicked.connect(self.port_check)

        # 串口信息显示
        self.ui_obj.s1__box_2.currentTextChanged.connect(self.port_imf)

        # 打开串口按钮
        self.ui_obj.open_button.clicked.connect(self.port_open)

        # 关闭串口按钮
        self.ui_obj.close_button.clicked.connect(self.port_close)

         # 开始测试
        self.ui_obj.start_test_bt.clicked.connect(self.start_test)

        # 停止测试
        self.ui_obj.stop_test_bt.clicked.connect(self.stop_test)

        # 单次测试
        self.ui_obj.one_test_bt.clicked.connect(self.one_test)

        # 清空
        self.ui_obj.clear_bt.clicked.connect(self.clear_result)

        # 定时发送数据
        self.timer_send = QTimer()
        self.timer_send.timeout.connect(self.data_send_timer)
        # self.ui_obj.timer_send_cb.stateChanged.connect(self.data_send_timer)

        # 定时器接收数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.data_receive)

        # 初始化table view


    # 保存日志
    def save_log(self):
        pass
        # try:
        #     if self.ui_obj.save_log_cb.checkState():
        #         self.file_path =  QtWidgets.QFileDialog.getSaveFileName(self.main_window_obj,"save file","" ,"Txt files(*.log)")
        #         self.ui_obj.timestamp_cb.setEnabled(False)
        #         if self.file_path[0] != '':
        #             self.save_log_fd = open(self.file_path[0], "w")
        #         else:
        #             self.ui_obj.timestamp_cb.setEnabled(True)
        #             self.ui_obj.save_log_cb.setCheckState(0)

        #     else:
        #         self.save_log_fd.close()
        #         self.save_log_fd = None
        #         self.ui_obj.timestamp_cb.setEnabled(True)
        # except:
        #     self.save_log_fd = None
        #     self.ui_obj.save_log_cb.setCheckState(0)
        #     self.ui_obj.timestamp_cb.setEnabled(True)
        #     QMessageBox.critical(self.main_window_obj, "Open Error", "Can not open this files, please check!")
        #     return None

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
            self.ui_obj.formGroupBox1.setTitle("串口状态(打开)")

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
        
        self.ui_obj.formGroupBox1.setTitle("串口状态(关闭)")

        self.timing_num = 1000
        self.ui_obj.timing_le.setText(str(self.timing_num))
        self.test_times = 3
        self.ui_obj.test_times_le.setText(str(self.test_times))

    # 开始测试
    def start_test(self):
        pass
        # if self.ser.isOpen():
        #     self.timing_num = int(self.ui_obj.timing_le.text())
        #     self.test_times = int(self.ui_obj.test_times_le.text())

        #     self.timer_send.start(self.timing_num)

        #     self.send_num = 0
        #     self.ui_obj.send_num_le.setText(str(self.send_num))
        #     self.recv_num = 0
        #     self.ui_obj.recv_num_le.setText(str(self.recv_num))
        #     self.ui_obj.timing_le.setEnabled(False)
        #     self.ui_obj.send_num_le.setEnabled(False)
        #     self.ui_obj.recv_num_le.setEnabled(False)
        #     self.ui_obj.s3__send_text.setEnabled(False)
        #     self.ui_obj.compose_tx.setEnabled(False)

        #     self.ui_obj.compose_bt.setEnabled(False)
        #     self.ui_obj.s3__clear_button.setEnabled(False)
        #     self.ui_obj.s3__send_button.setEnabled(False)
        #     self.ui_obj.start_test_bt.setEnabled(False)
        #     self.ui_obj.s3__clear_button_3.setEnabled(False)
        # else:
        #     QMessageBox.critical(self.main_window_obj, 'Warning', 'Please check port is opend!')

    # 停止测试
    def stop_test(self):
        pass
        # self.ui_obj.timing_le.setEnabled(True)
        # self.ui_obj.send_num_le.setEnabled(True)
        # self.ui_obj.recv_num_le.setEnabled(True)
        # self.ui_obj.s3__send_text.setEnabled(True)
        # self.ui_obj.compose_tx.setEnabled(True)

        # self.ui_obj.compose_bt.setEnabled(True)
        # self.ui_obj.s3__clear_button.setEnabled(True)
        # self.ui_obj.s3__send_button.setEnabled(True)
        # self.ui_obj.start_test_bt.setEnabled(True)
        # self.ui_obj.s3__clear_button_3.setEnabled(True)

        # self.timer_send.stop()

    def one_test(self):
        pass

    def clear_result(self):
        pass

    # 发送数据
    def data_send(self, input_s, hex_send_flag):
        pass
        # if self.ser.isOpen():
        #     if input_s != "":
        #         # 非空字符串
        #         if hex_send_flag:
        #             # hex发送
        #             input_s = input_s.strip()
        #             send_list = []
        #             while input_s != '':
        #                 try:
        #                     num = int(input_s[0:2], 16)
        #                 except ValueError:
        #                     QMessageBox.critical(self.main_window_obj, 'wrong data', 'Please enter hexadecimal, separated by spaces!')
        #                     return None
        #                 input_s = input_s[2:].strip()
        #                 send_list.append(num)
        #             input_s = bytes(send_list)
        #         else:
        #             # ascii发送
        #             input_s = (input_s + '\r\n').encode('utf-8')

        #         num = self.ser.write(input_s)
        #         self.data_num_sended += num
        #         self.ui_obj.send_len_el.setText(str(self.data_num_sended))
        #         self.send_num = self.send_num+1
        #         self.ui_obj.send_num_le.setText(str(self.send_num))
        # else:
        #     QMessageBox.critical(self.main_window_obj, 'Warning', 'Please check port is opend!')

    #选择发送区1发送
    def data_area_1_send(self):
        pass
        # input_s = self.ui_obj.s3__send_text.toPlainText()
        # hex_send_flag = self.ui_obj.hex_send.isChecked()
        # self.data_send(input_s, hex_send_flag)

    # 接收数据
    def data_receive(self):
        pass
        # recv_buf = []
        # try:
        #     num = self.ser.inWaiting()
        # except:
        #     self.port_close()
        #     return None
        # if num > 2:
        #     data = self.ser.read(num)
        #     num = len(data)
        #     out_srt = ''

        #     #添加时间戳
        #     if self.ui_obj.timestamp_cb.checkState():
        #         out_srt = common.get_datetime()
        #         out_srt = "[" + out_srt + "] "
        #     # hex显示
        #     if self.ui_obj.hex_receive.checkState():
        #         out_s = ''
        #         for i in range(0, len(data)):
        #             out_s = out_s + '{:02X}'.format(data[i]) + ' '
        #             recv_buf.append(int(data[i]))
        #         out_s = out_srt + out_s + "\r\n"
        #         self.ui_obj.s2__receive_text.insertPlainText(out_s)
        #     else:
        #         # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
        #         out_s = out_srt + data.decode('iso-8859-1')
        #         self.ui_obj.s2__receive_text.insertPlainText(out_s)

        #     if self.save_log_fd is not None:
        #         self.save_log_fd.write(out_s)

        #     # if operator.eq(recv_buf[:1],self.send_buf[:1]) == True:
        #     if 0xEF in recv_buf:
        #         self.recv_num = self.recv_num + 1
        #         self.ui_obj.recv_num_le.setText(str(self.recv_num))

        #     # 统计接收字符的数量
        #     self.data_num_received += num
        #     self.ui_obj.recv_len_el.setText(str(self.data_num_received))

        #     # 获取到text光标
        #     textCursor = self.ui_obj.s2__receive_text.textCursor()
        #     # 滚动到底部
        #     textCursor.movePosition(textCursor.End)
        #     # 设置光标到text中去
        #     self.ui_obj.s2__receive_text.setTextCursor(textCursor)
        # else:
        #     pass

    # 定时发送数据
    def data_send_timer(self):

        if self.test_times > 0:
            self.test_times = self.test_times-1
            self.data_area_1_send()
        else:
            self.stop_test()


    #组帧
    def compose_func(self):
        pass
        # try:
        #     send_str = ''
        #     self.send_buf = [0xee,]
        #     send_list = [0x68, 0x00, 0x00, 0x40, 0x04, 0xF4, 0xEE, 0x04, 0x02, 0xE8, 0x00, 0x00, 0x00,]
        #     dB_dict = {"dB01":1,"dB02":2,"dB05":5,"dB08":8,"dB11":11,"dB14":14,"dB17":17,"dB20":20}
            
        #     compose_tx_str = self.ui_obj.compose_tx.toPlainText()
        #     compose_tx_str = compose_tx_str.strip()
        #     while compose_tx_str != '':
        #         try:
        #             num = int(compose_tx_str[0:2], 16)
        #         except ValueError:
        #             QMessageBox.critical(self.main_window_obj, 'wrong data', 'Please enter hexadecimal, separated by spaces!')
        #             return None
        #         compose_tx_str = compose_tx_str[2:].strip()
        #         self.send_buf.append(num)

        #     send_list[10] = int(self.ui_obj.channel_num_Box.currentText()) #信道号0-64
        #     send_list[11] = dB_dict[self.ui_obj.dB_Box.currentText()] # 发射功率
        #     send_list[12] = len(self.send_buf) # 数据长度 

        #     send_list.extend(self.send_buf)
        #     send_list.append(common.uchar_checksum(send_list[2:]))
        #     send_list.append(0x16)
        #     send_list[1] = len(send_list) #GD17帧长度

        #     for data in send_list:
        #         send_str = send_str + '{:#04X}'.format(data)[2:4] + " "

        #     self.ui_obj.s3__send_text.clear()
        #     self.ui_obj.s3__send_text.setText(send_str)

        # except Exception as e:
        #     print ()
        #     QMessageBox.critical(self.main_window_obj, "Data Err", "Data Err!")