# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/ui_gadget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Gadget(object):
    def setupUi(self, Gadget):
        Gadget.setObjectName("Gadget")
        Gadget.resize(850, 550)
        Gadget.setMinimumSize(QtCore.QSize(850, 550))
        Gadget.setMaximumSize(QtCore.QSize(850, 550))
        self.gridLayout_23 = QtWidgets.QGridLayout(Gadget)
        self.gridLayout_23.setObjectName("gridLayout_23")
        self.stackedWidget = QtWidgets.QStackedWidget(Gadget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.stackedWidget.setFont(font)
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidgetPage1 = QtWidgets.QWidget()
        self.stackedWidgetPage1.setObjectName("stackedWidgetPage1")
        self.gridLayout_22 = QtWidgets.QGridLayout(self.stackedWidgetPage1)
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.recv_len_label = QtWidgets.QLabel(self.stackedWidgetPage1)
        self.recv_len_label.setMinimumSize(QtCore.QSize(75, 20))
        self.recv_len_label.setMaximumSize(QtCore.QSize(75, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.recv_len_label.setFont(font)
        self.recv_len_label.setObjectName("recv_len_label")
        self.gridLayout_8.addWidget(self.recv_len_label, 0, 3, 1, 1)
        self.send_len_label = QtWidgets.QLabel(self.stackedWidgetPage1)
        self.send_len_label.setMinimumSize(QtCore.QSize(75, 20))
        self.send_len_label.setMaximumSize(QtCore.QSize(75, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.send_len_label.setFont(font)
        self.send_len_label.setObjectName("send_len_label")
        self.gridLayout_8.addWidget(self.send_len_label, 0, 5, 1, 1)
        self.setting_hide_cb = QtWidgets.QCheckBox(self.stackedWidgetPage1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.setting_hide_cb.setFont(font)
        self.setting_hide_cb.setObjectName("setting_hide_cb")
        self.gridLayout_8.addWidget(self.setting_hide_cb, 0, 0, 1, 1)
        self.send_len_el = QtWidgets.QLineEdit(self.stackedWidgetPage1)
        self.send_len_el.setMinimumSize(QtCore.QSize(60, 20))
        self.send_len_el.setMaximumSize(QtCore.QSize(60, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.send_len_el.setFont(font)
        self.send_len_el.setObjectName("send_len_el")
        self.gridLayout_8.addWidget(self.send_len_el, 0, 6, 1, 1)
        self.recv_len_el = QtWidgets.QLineEdit(self.stackedWidgetPage1)
        self.recv_len_el.setMinimumSize(QtCore.QSize(60, 20))
        self.recv_len_el.setMaximumSize(QtCore.QSize(60, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.recv_len_el.setFont(font)
        self.recv_len_el.setObjectName("recv_len_el")
        self.gridLayout_8.addWidget(self.recv_len_el, 0, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem, 0, 2, 1, 1)
        self.port_state = QtWidgets.QLabel(self.stackedWidgetPage1)
        self.port_state.setMinimumSize(QtCore.QSize(100, 20))
        self.port_state.setMaximumSize(QtCore.QSize(100, 20))
        self.port_state.setText("")
        self.port_state.setObjectName("port_state")
        self.gridLayout_8.addWidget(self.port_state, 0, 1, 1, 1)
        self.gridLayout_22.addLayout(self.gridLayout_8, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.formGroupBox1 = QtWidgets.QGroupBox(self.stackedWidgetPage1)
        self.formGroupBox1.setMinimumSize(QtCore.QSize(250, 200))
        self.formGroupBox1.setMaximumSize(QtCore.QSize(250, 200))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.formGroupBox1.setFont(font)
        self.formGroupBox1.setObjectName("formGroupBox1")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.formGroupBox1)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.s1__lb_1 = QtWidgets.QLabel(self.formGroupBox1)
        self.s1__lb_1.setMinimumSize(QtCore.QSize(100, 20))
        self.s1__lb_1.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.s1__lb_1.setFont(font)
        self.s1__lb_1.setObjectName("s1__lb_1")
        self.gridLayout_6.addWidget(self.s1__lb_1, 0, 0, 1, 1)
        self.s1__box_1 = QtWidgets.QPushButton(self.formGroupBox1)
        self.s1__box_1.setMinimumSize(QtCore.QSize(120, 20))
        self.s1__box_1.setMaximumSize(QtCore.QSize(120, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.s1__box_1.setFont(font)
        self.s1__box_1.setAutoRepeatInterval(100)
        self.s1__box_1.setDefault(True)
        self.s1__box_1.setObjectName("s1__box_1")
        self.gridLayout_6.addWidget(self.s1__box_1, 0, 1, 1, 1)
        self.s1__lb_2 = QtWidgets.QLabel(self.formGroupBox1)
        self.s1__lb_2.setMinimumSize(QtCore.QSize(100, 20))
        self.s1__lb_2.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.s1__lb_2.setFont(font)
        self.s1__lb_2.setObjectName("s1__lb_2")
        self.gridLayout_6.addWidget(self.s1__lb_2, 1, 0, 1, 1)
        self.s1__box_2 = QtWidgets.QComboBox(self.formGroupBox1)
        self.s1__box_2.setMinimumSize(QtCore.QSize(120, 20))
        self.s1__box_2.setMaximumSize(QtCore.QSize(120, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.s1__box_2.setFont(font)
        self.s1__box_2.setObjectName("s1__box_2")
        self.gridLayout_6.addWidget(self.s1__box_2, 1, 1, 1, 1)
        self.s1__lb_3 = QtWidgets.QLabel(self.formGroupBox1)
        self.s1__lb_3.setMinimumSize(QtCore.QSize(100, 20))
        self.s1__lb_3.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.s1__lb_3.setFont(font)
        self.s1__lb_3.setObjectName("s1__lb_3")
        self.gridLayout_6.addWidget(self.s1__lb_3, 3, 0, 1, 1)
        self.s1__box_3 = QtWidgets.QComboBox(self.formGroupBox1)
        self.s1__box_3.setMinimumSize(QtCore.QSize(100, 20))
        self.s1__box_3.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.s1__box_3.setFont(font)
        self.s1__box_3.setObjectName("s1__box_3")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.gridLayout_6.addWidget(self.s1__box_3, 3, 1, 1, 1)
        self.s1__lb_4 = QtWidgets.QLabel(self.formGroupBox1)
        self.s1__lb_4.setMinimumSize(QtCore.QSize(100, 20))
        self.s1__lb_4.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.s1__lb_4.setFont(font)
        self.s1__lb_4.setObjectName("s1__lb_4")
        self.gridLayout_6.addWidget(self.s1__lb_4, 4, 0, 1, 1)
        self.s1__box_4 = QtWidgets.QComboBox(self.formGroupBox1)
        self.s1__box_4.setMinimumSize(QtCore.QSize(100, 20))
        self.s1__box_4.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.s1__box_4.setFont(font)
        self.s1__box_4.setObjectName("s1__box_4")
        self.s1__box_4.addItem("")
        self.s1__box_4.addItem("")
        self.s1__box_4.addItem("")
        self.s1__box_4.addItem("")
        self.gridLayout_6.addWidget(self.s1__box_4, 4, 1, 1, 1)
        self.s1__lb_5 = QtWidgets.QLabel(self.formGroupBox1)
        self.s1__lb_5.setMinimumSize(QtCore.QSize(100, 20))
        self.s1__lb_5.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.s1__lb_5.setFont(font)
        self.s1__lb_5.setObjectName("s1__lb_5")
        self.gridLayout_6.addWidget(self.s1__lb_5, 5, 0, 1, 1)
        self.s1__box_5 = QtWidgets.QComboBox(self.formGroupBox1)
        self.s1__box_5.setMinimumSize(QtCore.QSize(100, 20))
        self.s1__box_5.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.s1__box_5.setFont(font)
        self.s1__box_5.setObjectName("s1__box_5")
        self.s1__box_5.addItem("")
        self.s1__box_5.addItem("")
        self.s1__box_5.addItem("")
        self.s1__box_5.addItem("")
        self.s1__box_5.addItem("")
        self.gridLayout_6.addWidget(self.s1__box_5, 5, 1, 1, 1)
        self.s1__lb_6 = QtWidgets.QLabel(self.formGroupBox1)
        self.s1__lb_6.setMinimumSize(QtCore.QSize(100, 20))
        self.s1__lb_6.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.s1__lb_6.setFont(font)
        self.s1__lb_6.setObjectName("s1__lb_6")
        self.gridLayout_6.addWidget(self.s1__lb_6, 6, 0, 1, 1)
        self.s1__box_6 = QtWidgets.QComboBox(self.formGroupBox1)
        self.s1__box_6.setMinimumSize(QtCore.QSize(100, 20))
        self.s1__box_6.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.s1__box_6.setFont(font)
        self.s1__box_6.setObjectName("s1__box_6")
        self.s1__box_6.addItem("")
        self.s1__box_6.addItem("")
        self.gridLayout_6.addWidget(self.s1__box_6, 6, 1, 1, 1)
        self.open_button = QtWidgets.QPushButton(self.formGroupBox1)
        self.open_button.setMinimumSize(QtCore.QSize(100, 20))
        self.open_button.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.open_button.setFont(font)
        self.open_button.setObjectName("open_button")
        self.gridLayout_6.addWidget(self.open_button, 7, 0, 1, 1)
        self.close_button = QtWidgets.QPushButton(self.formGroupBox1)
        self.close_button.setMinimumSize(QtCore.QSize(100, 20))
        self.close_button.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.close_button.setFont(font)
        self.close_button.setObjectName("close_button")
        self.gridLayout_6.addWidget(self.close_button, 7, 1, 1, 1)
        self.state_label = QtWidgets.QLabel(self.formGroupBox1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.state_label.setFont(font)
        self.state_label.setText("")
        self.state_label.setTextFormat(QtCore.Qt.AutoText)
        self.state_label.setScaledContents(True)
        self.state_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.state_label.setObjectName("state_label")
        self.gridLayout_6.addWidget(self.state_label, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.formGroupBox1, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.gridLayout_22.addLayout(self.gridLayout, 0, 1, 2, 1)
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.verticalGroupBox = QtWidgets.QGroupBox(self.stackedWidgetPage1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalGroupBox.sizePolicy().hasHeightForWidth())
        self.verticalGroupBox.setSizePolicy(sizePolicy)
        self.verticalGroupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.verticalGroupBox.setFont(font)
        self.verticalGroupBox.setObjectName("verticalGroupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.verticalGroupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.s2__receive_text = QtWidgets.QTextEdit(self.verticalGroupBox)
        self.s2__receive_text.setEnabled(True)
        self.s2__receive_text.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.s2__receive_text.setFont(font)
        self.s2__receive_text.setObjectName("s2__receive_text")
        self.gridLayout_4.addWidget(self.s2__receive_text, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(self.verticalGroupBox, 0, 1, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.hex_receive = QtWidgets.QCheckBox(self.stackedWidgetPage1)
        self.hex_receive.setMinimumSize(QtCore.QSize(100, 20))
        self.hex_receive.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.hex_receive.setFont(font)
        self.hex_receive.setChecked(True)
        self.hex_receive.setObjectName("hex_receive")
        self.gridLayout_5.addWidget(self.hex_receive, 2, 0, 1, 1)
        self.s2__clear_button = QtWidgets.QPushButton(self.stackedWidgetPage1)
        self.s2__clear_button.setMinimumSize(QtCore.QSize(100, 20))
        self.s2__clear_button.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.s2__clear_button.setFont(font)
        self.s2__clear_button.setObjectName("s2__clear_button")
        self.gridLayout_5.addWidget(self.s2__clear_button, 3, 0, 1, 1)
        self.save_log_cb = QtWidgets.QCheckBox(self.stackedWidgetPage1)
        self.save_log_cb.setMinimumSize(QtCore.QSize(100, 20))
        self.save_log_cb.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.save_log_cb.setFont(font)
        self.save_log_cb.setObjectName("save_log_cb")
        self.gridLayout_5.addWidget(self.save_log_cb, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem2, 4, 0, 1, 1)
        self.timestamp_cb = QtWidgets.QCheckBox(self.stackedWidgetPage1)
        self.timestamp_cb.setMinimumSize(QtCore.QSize(100, 20))
        self.timestamp_cb.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.timestamp_cb.setFont(font)
        self.timestamp_cb.setObjectName("timestamp_cb")
        self.gridLayout_5.addWidget(self.timestamp_cb, 0, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.gridLayout_22.addLayout(self.gridLayout_9, 1, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.channel_num_lb = QtWidgets.QLabel(self.stackedWidgetPage1)
        self.channel_num_lb.setMinimumSize(QtCore.QSize(100, 20))
        self.channel_num_lb.setMaximumSize(QtCore.QSize(100, 20))
        self.channel_num_lb.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.channel_num_lb.setObjectName("channel_num_lb")
        self.gridLayout_2.addWidget(self.channel_num_lb, 0, 0, 1, 1)
        self.channel_num_le = QtWidgets.QLineEdit(self.stackedWidgetPage1)
        self.channel_num_le.setMinimumSize(QtCore.QSize(60, 25))
        self.channel_num_le.setMaximumSize(QtCore.QSize(60, 25))
        self.channel_num_le.setObjectName("channel_num_le")
        self.gridLayout_2.addWidget(self.channel_num_le, 0, 1, 1, 1)
        self.hex_send = QtWidgets.QCheckBox(self.stackedWidgetPage1)
        self.hex_send.setChecked(True)
        self.hex_send.setObjectName("hex_send")
        self.gridLayout_2.addWidget(self.hex_send, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 0, 3, 1, 1)
        self.gridLayout_22.addLayout(self.gridLayout_2, 2, 0, 1, 1)
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.compose_tx = QtWidgets.QTextEdit(self.stackedWidgetPage1)
        self.compose_tx.setMinimumSize(QtCore.QSize(0, 70))
        self.compose_tx.setMaximumSize(QtCore.QSize(16777215, 70))
        self.compose_tx.setObjectName("compose_tx")
        self.gridLayout_10.addWidget(self.compose_tx, 0, 1, 1, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.send_bt = QtWidgets.QPushButton(self.stackedWidgetPage1)
        self.send_bt.setMinimumSize(QtCore.QSize(100, 40))
        self.send_bt.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.send_bt.setFont(font)
        self.send_bt.setObjectName("send_bt")
        self.gridLayout_7.addWidget(self.send_bt, 1, 0, 1, 1)
        self.s3__clear_button_3 = QtWidgets.QPushButton(self.stackedWidgetPage1)
        self.s3__clear_button_3.setMinimumSize(QtCore.QSize(100, 20))
        self.s3__clear_button_3.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.s3__clear_button_3.setFont(font)
        self.s3__clear_button_3.setObjectName("s3__clear_button_3")
        self.gridLayout_7.addWidget(self.s3__clear_button_3, 0, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        self.gridLayout_22.addLayout(self.gridLayout_10, 3, 0, 1, 1)
        self.stackedWidget.addWidget(self.stackedWidgetPage1)
        self.gridLayout_23.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(Gadget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_21 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setEnabled(True)
        self.label.setMinimumSize(QtCore.QSize(80, 20))
        self.label.setMaximumSize(QtCore.QSize(80, 20))
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.macdestaddr_le = QtWidgets.QLineEdit(self.tab)
        self.macdestaddr_le.setMinimumSize(QtCore.QSize(140, 20))
        self.macdestaddr_le.setMaximumSize(QtCore.QSize(140, 20))
        self.macdestaddr_le.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.macdestaddr_le.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.macdestaddr_le.setObjectName("macdestaddr_le")
        self.gridLayout_3.addWidget(self.macdestaddr_le, 0, 1, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setMinimumSize(QtCore.QSize(80, 20))
        self.label_2.setMaximumSize(QtCore.QSize(80, 20))
        self.label_2.setObjectName("label_2")
        self.gridLayout_11.addWidget(self.label_2, 0, 0, 1, 1)
        self.macsrcaddr_le = QtWidgets.QLineEdit(self.tab)
        self.macsrcaddr_le.setMinimumSize(QtCore.QSize(140, 20))
        self.macsrcaddr_le.setMaximumSize(QtCore.QSize(140, 20))
        self.macsrcaddr_le.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.macsrcaddr_le.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.macsrcaddr_le.setObjectName("macsrcaddr_le")
        self.gridLayout_11.addWidget(self.macsrcaddr_le, 0, 1, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_11, 1, 0, 1, 1)
        self.gridLayout_15 = QtWidgets.QGridLayout()
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.beacon_compose_bt = QtWidgets.QPushButton(self.tab)
        self.beacon_compose_bt.setMinimumSize(QtCore.QSize(80, 20))
        self.beacon_compose_bt.setMaximumSize(QtCore.QSize(80, 20))
        self.beacon_compose_bt.setObjectName("beacon_compose_bt")
        self.gridLayout_15.addWidget(self.beacon_compose_bt, 0, 0, 1, 1)
        self.test_beacon_send_bt = QtWidgets.QPushButton(self.tab)
        self.test_beacon_send_bt.setObjectName("test_beacon_send_bt")
        self.gridLayout_15.addWidget(self.test_beacon_send_bt, 0, 1, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_15, 2, 0, 1, 1)
        self.gridLayout_21.addLayout(self.gridLayout_16, 0, 0, 1, 1)
        self.gridLayout_19 = QtWidgets.QGridLayout()
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setMinimumSize(QtCore.QSize(60, 20))
        self.label_3.setMaximumSize(QtCore.QSize(60, 20))
        self.label_3.setObjectName("label_3")
        self.gridLayout_12.addWidget(self.label_3, 0, 0, 1, 1)
        self.beacon_sn_le = QtWidgets.QLineEdit(self.tab)
        self.beacon_sn_le.setMinimumSize(QtCore.QSize(60, 20))
        self.beacon_sn_le.setMaximumSize(QtCore.QSize(60, 20))
        self.beacon_sn_le.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.beacon_sn_le.setObjectName("beacon_sn_le")
        self.gridLayout_12.addWidget(self.beacon_sn_le, 0, 1, 1, 1)
        self.gridLayout_19.addLayout(self.gridLayout_12, 0, 0, 1, 1)
        self.gridLayout_13 = QtWidgets.QGridLayout()
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setMinimumSize(QtCore.QSize(60, 20))
        self.label_4.setMaximumSize(QtCore.QSize(60, 20))
        self.label_4.setObjectName("label_4")
        self.gridLayout_13.addWidget(self.label_4, 0, 0, 1, 1)
        self.net_volume_le = QtWidgets.QLineEdit(self.tab)
        self.net_volume_le.setMinimumSize(QtCore.QSize(60, 20))
        self.net_volume_le.setMaximumSize(QtCore.QSize(60, 20))
        self.net_volume_le.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.net_volume_le.setObjectName("net_volume_le")
        self.gridLayout_13.addWidget(self.net_volume_le, 0, 1, 1, 1)
        self.gridLayout_19.addLayout(self.gridLayout_13, 1, 0, 1, 1)
        self.gridLayout_14 = QtWidgets.QGridLayout()
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setMinimumSize(QtCore.QSize(60, 20))
        self.label_5.setMaximumSize(QtCore.QSize(60, 20))
        self.label_5.setObjectName("label_5")
        self.gridLayout_14.addWidget(self.label_5, 0, 0, 1, 1)
        self.rssi_thr_le = QtWidgets.QLineEdit(self.tab)
        self.rssi_thr_le.setMinimumSize(QtCore.QSize(60, 20))
        self.rssi_thr_le.setMaximumSize(QtCore.QSize(60, 20))
        self.rssi_thr_le.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.rssi_thr_le.setObjectName("rssi_thr_le")
        self.gridLayout_14.addWidget(self.rssi_thr_le, 0, 1, 1, 1)
        self.gridLayout_19.addLayout(self.gridLayout_14, 2, 0, 1, 1)
        self.gridLayout_21.addLayout(self.gridLayout_19, 0, 1, 1, 1)
        self.gridLayout_20 = QtWidgets.QGridLayout()
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.gridLayout_17 = QtWidgets.QGridLayout()
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setMinimumSize(QtCore.QSize(100, 20))
        self.label_6.setMaximumSize(QtCore.QSize(100, 20))
        self.label_6.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_17.addWidget(self.label_6, 0, 0, 1, 1)
        self.beacon_panid_le = QtWidgets.QLineEdit(self.tab)
        self.beacon_panid_le.setMinimumSize(QtCore.QSize(60, 20))
        self.beacon_panid_le.setMaximumSize(QtCore.QSize(60, 20))
        self.beacon_panid_le.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.beacon_panid_le.setObjectName("beacon_panid_le")
        self.gridLayout_17.addWidget(self.beacon_panid_le, 0, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_17.addItem(spacerItem4, 0, 2, 1, 1)
        self.gridLayout_20.addLayout(self.gridLayout_17, 0, 0, 1, 1)
        self.gridLayout_18 = QtWidgets.QGridLayout()
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setMinimumSize(QtCore.QSize(100, 20))
        self.label_7.setMaximumSize(QtCore.QSize(100, 20))
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_18.addWidget(self.label_7, 0, 0, 1, 1)
        self.cco_addr_le = QtWidgets.QLineEdit(self.tab)
        self.cco_addr_le.setMinimumSize(QtCore.QSize(140, 20))
        self.cco_addr_le.setMaximumSize(QtCore.QSize(140, 20))
        self.cco_addr_le.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cco_addr_le.setObjectName("cco_addr_le")
        self.gridLayout_18.addWidget(self.cco_addr_le, 0, 1, 1, 1)
        self.gridLayout_20.addLayout(self.gridLayout_18, 1, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_20.addItem(spacerItem5, 2, 0, 1, 1)
        self.gridLayout_21.addLayout(self.gridLayout_20, 0, 2, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(84, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_21.addItem(spacerItem6, 0, 3, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(84, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_21.addItem(spacerItem7, 0, 4, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_23.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.retranslateUi(Gadget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Gadget)

    def retranslateUi(self, Gadget):
        _translate = QtCore.QCoreApplication.translate
        Gadget.setWindowTitle(_translate("Gadget", "Form"))
        self.recv_len_label.setText(_translate("Gadget", "Recv Length:"))
        self.send_len_label.setText(_translate("Gadget", "Send Length:"))
        self.setting_hide_cb.setText(_translate("Gadget", "Hide Check"))
        self.formGroupBox1.setTitle(_translate("Gadget", "Port Setting"))
        self.s1__lb_1.setText(_translate("Gadget", "Detection:"))
        self.s1__box_1.setText(_translate("Gadget", "Detection Port"))
        self.s1__lb_2.setText(_translate("Gadget", "Select:"))
        self.s1__lb_3.setText(_translate("Gadget", "Boud Rate:"))
        self.s1__box_3.setItemText(0, _translate("Gadget", "115200"))
        self.s1__box_3.setItemText(1, _translate("Gadget", "2400"))
        self.s1__box_3.setItemText(2, _translate("Gadget", "4800"))
        self.s1__box_3.setItemText(3, _translate("Gadget", "9600"))
        self.s1__box_3.setItemText(4, _translate("Gadget", "14400"))
        self.s1__box_3.setItemText(5, _translate("Gadget", "19200"))
        self.s1__box_3.setItemText(6, _translate("Gadget", "38400"))
        self.s1__box_3.setItemText(7, _translate("Gadget", "57600"))
        self.s1__box_3.setItemText(8, _translate("Gadget", "76800"))
        self.s1__box_3.setItemText(9, _translate("Gadget", "12800"))
        self.s1__box_3.setItemText(10, _translate("Gadget", "230400"))
        self.s1__box_3.setItemText(11, _translate("Gadget", "460800"))
        self.s1__box_3.setItemText(12, _translate("Gadget", "3000000"))
        self.s1__lb_4.setText(_translate("Gadget", "Data Bit:"))
        self.s1__box_4.setItemText(0, _translate("Gadget", "8"))
        self.s1__box_4.setItemText(1, _translate("Gadget", "7"))
        self.s1__box_4.setItemText(2, _translate("Gadget", "6"))
        self.s1__box_4.setItemText(3, _translate("Gadget", "5"))
        self.s1__lb_5.setText(_translate("Gadget", "Check Bit:"))
        self.s1__box_5.setItemText(0, _translate("Gadget", "O"))
        self.s1__box_5.setItemText(1, _translate("Gadget", "E"))
        self.s1__box_5.setItemText(2, _translate("Gadget", "N"))
        self.s1__box_5.setItemText(3, _translate("Gadget", "M"))
        self.s1__box_5.setItemText(4, _translate("Gadget", "S"))
        self.s1__lb_6.setText(_translate("Gadget", "Stop Bit:"))
        self.s1__box_6.setItemText(0, _translate("Gadget", "1"))
        self.s1__box_6.setItemText(1, _translate("Gadget", "2"))
        self.open_button.setText(_translate("Gadget", "Open"))
        self.close_button.setText(_translate("Gadget", "Close"))
        self.verticalGroupBox.setTitle(_translate("Gadget", "Receiving Area:"))
        self.hex_receive.setText(_translate("Gadget", "Hex Recv"))
        self.s2__clear_button.setText(_translate("Gadget", "Clear"))
        self.save_log_cb.setText(_translate("Gadget", "Save Log"))
        self.timestamp_cb.setText(_translate("Gadget", "Timestamp"))
        self.channel_num_lb.setText(_translate("Gadget", "Channel :"))
        self.channel_num_le.setToolTip(_translate("Gadget", "<html><head/><body><p>0-64</p></body></html>"))
        self.channel_num_le.setText(_translate("Gadget", "0"))
        self.hex_send.setText(_translate("Gadget", "HexSend"))
        self.compose_tx.setHtml(_translate("Gadget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">00 00 00</p></body></html>"))
        self.send_bt.setText(_translate("Gadget", "Send"))
        self.s3__clear_button_3.setText(_translate("Gadget", "Clear"))
        self.label.setText(_translate("Gadget", "MAC目标地址："))
        self.macdestaddr_le.setToolTip(_translate("Gadget", "<html><head/><body><p>BCD码地址</p></body></html>"))
        self.macdestaddr_le.setText(_translate("Gadget", "FFFFFFFFFFFF"))
        self.label_2.setText(_translate("Gadget", "MAC 源地址："))
        self.macsrcaddr_le.setToolTip(_translate("Gadget", "<html><head/><body><p>BCD码地址</p></body></html>"))
        self.macsrcaddr_le.setText(_translate("Gadget", "778899"))
        self.beacon_compose_bt.setText(_translate("Gadget", "组帧"))
        self.test_beacon_send_bt.setToolTip(_translate("Gadget", "<html><head/><body><p>模拟信标应答：</p><p>MAC层源地址从000099000001依次递增</p></body></html>"))
        self.test_beacon_send_bt.setText(_translate("Gadget", "模拟信标应答"))
        self.label_3.setText(_translate("Gadget", "信标标识："))
        self.beacon_sn_le.setToolTip(_translate("Gadget", "<html><head/><body><p>十进制</p></body></html>"))
        self.beacon_sn_le.setText(_translate("Gadget", "1"))
        self.label_4.setText(_translate("Gadget", "网络规模："))
        self.net_volume_le.setToolTip(_translate("Gadget", "<html><head/><body><p>十进制</p></body></html>"))
        self.net_volume_le.setText(_translate("Gadget", "20"))
        self.label_5.setText(_translate("Gadget", "场强门限："))
        self.rssi_thr_le.setToolTip(_translate("Gadget", "<html><head/><body><p>十进制</p></body></html>"))
        self.rssi_thr_le.setText(_translate("Gadget", "96"))
        self.label_6.setText(_translate("Gadget", "载荷PanID："))
        self.beacon_panid_le.setToolTip(_translate("Gadget", "<html><head/><body><p>十进制1-65535</p></body></html>"))
        self.beacon_panid_le.setText(_translate("Gadget", "5555"))
        self.label_7.setText(_translate("Gadget", "中心节点地址："))
        self.cco_addr_le.setToolTip(_translate("Gadget", "<html><head/><body><p>BCD码地址</p></body></html>"))
        self.cco_addr_le.setText(_translate("Gadget", "778899"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Gadget", "信标帧"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Gadget", "网络维护请求"))

