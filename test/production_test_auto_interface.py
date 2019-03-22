#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
python_src_path = os.__file__

import sys
base_disk = python_src_path[0].upper()
sys.path.append(base_disk + r':\Python27')
sys.path.append(base_disk + r":\Python27\Lib")
sys.path.append(base_disk + r':\Python27\Lib\DLLs')
sys.path.append(base_disk + r":\Python27\Lib\site-packages")

import binascii
from ctypes import *
import collections
import fileinput
# import glob
import logging
import math
import Queue
import re
import serial
import struct
import time
import threading
# import traceback


DictFilterGpio = {
        0: "23",  # STA: 23
        1: "28",  # IIC: 28
        2: "2"    # CCO: 2
    }

DictTestCase = collections.OrderedDict()
DictTestCase["efuse_lock_flag"] = 0
DictTestCase["write_vendor_id_flag"] = 1
DictTestCase["read_fw_ver_flag"] = 2
DictTestCase["read_chip_id_flag"] = 3
DictTestCase["read_ori_mac_address_flag"] = 4
DictTestCase["burned_mac_address_flag"] = 5
DictTestCase["noise_floor_detection_flag"] = 6
DictTestCase["tx_rx_loopback_flag"] = 7
DictTestCase["flatness_flag"] = 8
DictTestCase["sen_csr_flag"] = 9
DictTestCase["led_control_flag"] = 10

'''
struct data type menu
    char: c
    signed char: b
    unsigned char: B
    _Bool: ?
    short: h
    unsigned short: H
    int: i
    unsigned int: I
    long: l
    unsigned long: L
    long long: q
    unsigned long long: Q
    float: f
    double: d
'''

DictStructTxRxLoopback = collections.OrderedDict()
DictStructTxRxLoopback["w_character"] = 'B'
DictStructTxRxLoopback["q_character"] = 'B'
DictStructTxRxLoopback["accurate_indication"] = 'B'
DictStructTxRxLoopback["tx_gain"] = 'B'
DictStructTxRxLoopback["tx_adc_power"] = 'B'
DictStructTxRxLoopback["tx_dc"] = 'b'
DictStructTxRxLoopback["tx_ppm"] = 'h'
DictStructTxRxLoopback["tx_snr"] = 'b'
DictStructTxRxLoopback["rx_phase"] = 'B'
DictStructTxRxLoopback["rx_gain"] = 'B'
DictStructTxRxLoopback["rx_adc_power"] = 'B'
DictStructTxRxLoopback["rx_dc"] = 'b'
DictStructTxRxLoopback["rx_ppm"] = 'b'
DictStructTxRxLoopback["rx_snr"] = 'b'
DictStructTxRxLoopback["dut_real_ppm"] = 'h'

DictStructChipInfo = collections.OrderedDict()
DictStructChipInfo["mac_addr_1"] = 'B'
DictStructChipInfo["mac_addr_2"] = 'B'
DictStructChipInfo["mac_addr_3"] = 'B'
DictStructChipInfo["version_info"] = 'H'

DictStructChipInfoVersionInfo = collections.OrderedDict()  # little endian
DictStructChipInfoVersionInfo["not_used_4bits"] = 4  # top digit
DictStructChipInfoVersionInfo["ver_wafer"] = 4
DictStructChipInfoVersionInfo["ver_reserved"] = 4
DictStructChipInfoVersionInfo["ver_pkg_bumping"] = 2
DictStructChipInfoVersionInfo["ver_pkg_lic"] = 1
DictStructChipInfoVersionInfo["ver_pkg_flash"] = 1  # bottom digit

config_file = r"config_production_test_interface.txt"
global_vendor_id, global_device_type, global_phase_str, global_dynamic_filter_en = '', 0, '', 0


def avaliable_serial_ports_list():
    return_list = []
    ports = ("COM%s" % (i + 1) for i in range(256))

    # platform_info = sys.platform
    # if platform_info.startswith("win"):
    #     ports = ("COM%s" % (i + 1) for i in range(256))
    # elif platform_info.startswith("linux") or platform_info.startswith("cygwin"):
    #     ports = glob.glob("/dev/tty[A-Za-z]*")
    # elif platform_info.startswith("darwin"):
    #     ports = glob.glob("/dev/tty.*")
    # else:
    #     raise EnvironmentError(r"Unsupported platform")

    for each_port in ports:
        try:
            obj_ser = serial.Serial(each_port)
            obj_ser.close()
            return_list.append(each_port)
        except Exception:
            pass

    if return_list:
        return ("1,%s" % ('@'.join(return_list)).replace("COM", ""))
    else:
        return ("0,No serial port available")


def generate_config_file():
    global config_file

    config_info = '''
    #########################################################################
    #                                                                       #
    #                       Production Test Config                          #
    #                                                                       #
    #########################################################################
    
    device_type = 0  # 0: STA / 1: IIC / 2: CCO
    dynamic_filter_en = 0  # 0: fixed filter / 1: dynamic filter
    vendor_id = PH
    phase = A  # Phase A(L/G), Phase B(L/N), Phase C(N/G)
    burned_mac_address = 11:22:33:44:55:88
    nf_detection_times = 5
    flatness_threshold = 50
    hpf_thd_700k = 15
    hpf_thd_2m = 40
    csr_thd = 90
    gold_ppm = -3  # golden real ppm : keep integer and remove fraction part!
    phy_power_att = 0  # unit: dB, for communication sensitivity test
    filter_gpio_num = 23  # STA: 23 / IIC: 28 / CCO: 2

    # ------------ Function Enable Flag ------------
    # 1: Enable, 0: Disable

    read_fw_ver_flag = 1
    read_chip_id_flag = 1
    read_ori_mac_address_flag = 1
    burned_mac_address_flag = 1
    noise_floor_detection_flag = 1
    tx_rx_loopback_flag = 1
    flatness_flag = 1
    sen_csr_flag = 1
    led_control_flag = 1
    '''

    try:
        if not os.path.exists(config_file):
            with open(config_file, 'w') as wf:
                wf.write(config_info)

        return ("1,Config file rewrite successfully")
    except Exception, e_info:
        return ("0,Config file rewrite failed(Error Info: %s)" % str(e_info))


def config_file_parameters_set(str_vendor_id, int_device_type, str_phase_str, int_dynamic_filter_en):
    global config_file
    global global_vendor_id
    global global_device_type
    global global_phase_str
    global global_dynamic_filter_en

    global_vendor_id, global_device_type = str_vendor_id, int_device_type
    global_phase_str, global_dynamic_filter_en = str_phase_str, int_dynamic_filter_en

    if re.match(r"[A-Za-z]{2}", str_vendor_id):
        pass
    else:
        return ("0,Vendor ID(%s) format should be 2 bytes" % str_vendor_id)

    try:
        file_data = ''
        dev_type_str = "device_type"
        dy_filter_str = "dynamic_filter_en"
        vid_str = "vendor_id"
        p_str = "phase"
        f_gpio_str = "filter_gpio_num"
        compile_dev_type_str = re.compile(r"\s*" + dev_type_str + r"\s+=\s+(.*)")
        compile_dy_filter_str = re.compile(r"\s*" + dy_filter_str + r"\s+=\s+(.*)")
        compile_vid_str = re.compile(r"\s*" + vid_str + r"\s+=\s+(.*)")
        compile_p_str = re.compile(r"\s*" + p_str + r"\s+=\s+(.*)")
        compile_f_gpio_str = re.compile(r"\s*" + f_gpio_str + r"\s+=(.*)")

        if not os.path.exists(config_file):
            generate_config_file()

        with open(config_file, "r") as rf:
            for each_line in rf:
                m_dev_type_str = compile_dev_type_str.match(each_line)
                m_dy_filter_str = compile_dy_filter_str.match(each_line)
                m_vid_str = compile_vid_str.match(each_line)
                m_p_str = compile_p_str.match(each_line)
                m_f_gpio_str = compile_f_gpio_str.match(each_line)

                if m_dev_type_str:
                    file_data += each_line.replace(m_dev_type_str.group(0), dev_type_str + " = " +
                                                   str(int_device_type) +
                                                   r"  # 0: STA / 1: IIC / 2: CCO")

                elif m_dy_filter_str:
                    file_data += each_line.replace(m_dy_filter_str.group(0), dy_filter_str + " = " +
                                                   str(int_dynamic_filter_en) +
                                                   r"  # 0: fixed filter / 1: dynamic filter")

                elif m_vid_str:
                    file_data += each_line.replace(m_vid_str.group(0), vid_str + " = " + str_vendor_id)

                elif m_p_str:
                    file_data += each_line.replace(m_p_str.group(0), p_str + " = " + str_phase_str +
                                                   r"  # Phase A(L/G), Phase B(L/N), Phase C(N/G)")

                elif m_f_gpio_str:
                    file_data += each_line.replace(m_f_gpio_str.group(0), f_gpio_str + " = " +
                                                   DictFilterGpio[int_device_type] +
                                                   r"  # STA: 23 / IIC: 28 / CCO: 2")

                else:
                    file_data += each_line

        with open(config_file, "w") as wf:
            wf.write(file_data)

        return ("1,Parameters set completes and config file write in successfully")

    except Exception, e_info:
        return ("0,Error info: %s" % str(e_info))


def config_file_parameters_get():
    global config_file
    global global_vendor_id
    global global_device_type
    global global_phase_str
    global global_dynamic_filter_en

    return_list = []
    m_info_comp = re.compile(r"(\w+)\s*=\s*(.+)")
    m_annotation_comp = re.compile(r"(.*?)#(.*)")

    if not os.path.exists(config_file):
        generate_config_file()

    for eachline in fileinput.FileInput(config_file):
        m_info = m_info_comp.match(eachline)
        if m_info:
            m_key = (m_info.group(1)).strip()
            m_annotation = m_annotation_comp.search(m_info.group(2))
            if m_annotation:
                m_value = (m_annotation.group(1)).strip()
            else:
                m_value = (m_info.group(2)).strip()

            if m_key == "device_type":
                global_device_type = int(m_value)

            elif m_key == "dynamic_filter_en":
                global_dynamic_filter_en = int(m_value)

            elif m_key == "vendor_id":
                global_vendor_id = m_value

            elif m_key == "phase":
                global_phase_str = m_value
                global_phase_str = global_phase_str.replace(" ", '')
                global_phase_str = global_phase_str.replace(",", "#")

            else:
                pass

    return_list.append(global_vendor_id)
    return_list.append(str(global_device_type))
    return_list.append(global_phase_str)
    return_list.append(str(global_dynamic_filter_en))

    return ("1,%s" % '@'.join(return_list))


def test_case_set(test_case_info_str):
    global config_file

    file_data = ''
    test_case_name_list = DictTestCase.keys()
    test_case_value_list = DictTestCase.values()

    test_case_info_str = (test_case_info_str.replace(" ", "")).strip()
    test_case_info_list = test_case_info_str.split("@")

    reset_list, test_case_name_set_list, test_case_value_set_list = [], [], []
    for each_case_info in test_case_info_list:
        each_case_index_str, each_case_en_str = each_case_info.split("#")
        test_case_name_set_list.append(int(each_case_index_str))
        test_case_value_set_list.append(int(each_case_en_str))

    if not os.path.exists(config_file):
        generate_config_file()

    if test_case_value_list == test_case_name_set_list:  # match all test cases
        m_test_case_compile = re.compile(r"\s*(\w+_flag)\s*=\s*\d+")
        with open(config_file, "r") as rf:
            for each_line in rf:
                m_test_case = m_test_case_compile.match(each_line)

                if m_test_case:
                    m_test_case_name = m_test_case.group(1)
                    if m_test_case_name in test_case_name_list:
                        test_case_index = test_case_name_list.index(m_test_case_name)
                        file_data += each_line.replace(m_test_case.group(0),
                                                       m_test_case_name + r" = " +
                                                       str(test_case_value_set_list[test_case_index]))

                else:
                    file_data += each_line

        with open(config_file, "w") as wf:
            wf.write(file_data)

        return ("1,Test cases flag rewrite in config file completes")

    else:
        return ("0,Test cases flag rewrite in config file failed")


def test_case_get():
    global config_file

    return_list = []
    m_info_comp = re.compile(r"(\w+)\s*=\s*(.+)")
    m_annotation_comp = re.compile(r"(.*?)#(.*)")

    return_list.append("%d#%s" % (DictTestCase["efuse_lock_flag"], "1"))

    for eachline in fileinput.FileInput(config_file):
        m_info = m_info_comp.match(eachline)
        if m_info:
            m_key = (m_info.group(1)).strip()
            if not m_key.find(r"_flag") >= 0:
                continue

            m_annotation = m_annotation_comp.search(m_info.group(2))
            if m_annotation:
                m_value = (m_annotation.group(1)).strip()
            else:
                m_value = (m_info.group(2)).strip()

            return_list.append("%d#%s" % (DictTestCase[m_key], m_value))

    return ("1,%s" % '@'.join(return_list))


def try_except(func):
    def handle_problems(obj_instance, *args, **kwargs):
        try:
            res = func(obj_instance, *args, **kwargs)
            return res
        except Exception:
            exc_type, exc_instance, exc_traceback = sys.exc_info()
            # formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
            # exc_info = ("\n%s\n%s:\n%s" % (formatted_traceback, exc_type.__name__, exc_instance))
            return ("0,%s" % exc_instance)
        finally:
            pass

    return handle_problems


def timeout_set(time_interval):
    def wrapper(func):
        def time_out(obj_instance):
            obj_instance.time_out_queue.put(1)
            # print ("Timeout Error: function not responded in %d seconds, exit automatically!" % time_interval)

        def deco(obj_instance, *args, **kwargs):
            timer = threading.Timer(time_interval, time_out, args=(obj_instance, ))
            timer.start()
            res = func(obj_instance, *args, **kwargs)
            timer.cancel()
            obj_instance.time_out_queue.queue.clear()
            return res

        return deco
    return wrapper


class Production_test:

    DictPhase = {
        "A": "01",  # Phase A
        "B": "02",  # Phase B
        "C": "03"  # Phase C
    }

    DictChipInfo = {
        "00011": "K48V1A",
        "00001": "K68V1A",
        "00101": "K68V1B(bumping)",
        "10011": "K48V2A",
        "10001": "K68V2A",
        "10201": "K68V2B(no bumping)",
        "10101": "K68(unknown)"
    }

    init_str = "entry_sbl_cli"
    base_str = "bootm fw_mode=1"
    config_file = r"config_production_test_interface.txt"

    cur_work_dir = os.getcwd()
    log_base_folder = cur_work_dir + "\\" + "Production_test_log"
    if not os.path.exists(log_base_folder):
        os.makedirs(log_base_folder)

    def __init__(self, serial_port_num):

        self.dump_data_str = ''
        self.tmi_num = 4
        self.cur_gain_cnt, self.dynamic_filter_en = 0, 0
        self.burned_mac_address_flag, self.led_control_flag, self.sen_csr_flag = 0, 0, 0
        self.read_fw_ver_flag, self.read_chip_id_flag, self.read_ori_mac_address_flag = 0, 0, 0
        self.noise_floor_detection_flag, self.tx_rx_loopback_flag, self.flatness_flag = 0, 0, 0
        self.log_folder, self.device_type, self.phase_str = None, None, None
        self.first_cur_gain, self.label_str, self.f_handler, self.c_handler = None, None, None, None
        self.serial_port_num, self.ser_handler, self.logger, self.time_stamp = None, None, None, None
        self.flatness_threshold, self.hpf_thd_700k, self.hpf_thd_2m, self.csr_thd = None, None, None, None
        self.vendor_id, self.global_phase_str, self.phase_list, self.burned_mac_address = None, None, [], None
        self.gold_ppm, self.phy_power_att, self.filter_gpio_num, self.nf_detection_times = None, None, None, None

        self.serial_port_num = serial_port_num

        self.time_out_queue = Queue.Queue(maxsize=10)
        self.data_trans_queue = Queue.Queue(maxsize=10)

        self.time_stamp = time.strftime("%Y-%m-%d %X")
        self.time_stamp = self.time_stamp.replace(" ", "-")
        self.time_stamp = self.time_stamp.replace(":", "-")

    @try_except
    def serial_port_open(self):
        self.config_parameters_load()
        self.ser_handler = serial.Serial(port='com' + str(self.serial_port_num), baudrate=115200, timeout=0.1)

        return ("1,Serial port COM%d opened successfully" % self.serial_port_num)

    @try_except
    def serial_port_close(self):
        if self.ser_handler.isOpen():
            self.ser_handler.close()

        return ("1,Serial port COM%d closed" % self.serial_port_num)

    @try_except
    def pt_logger_open(self, label_str):
        self.label_str = label_str

        self.log_folder = Production_test.log_base_folder + "\\" + self.label_str
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

        log_name = self.label_str + "_" + self.time_stamp
        self.logger = logging.getLogger(str(self.serial_port_num))
        self.logger.setLevel(logging.DEBUG)  # logging level: debug < info < warning < error < critical
        logfile = self.log_folder + "\\" + log_name + ".log"
        self.f_handler = logging.FileHandler(logfile, mode='a')
        self.f_handler.setLevel(logging.DEBUG)  # file level
        self.c_handler = logging.StreamHandler()
        self.c_handler.setLevel(logging.INFO)  # console level: DEBUG\INFO
        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
        self.f_handler.setFormatter(formatter)
        self.c_handler.setFormatter(formatter)
        self.logger.addHandler(self.f_handler)
        self.logger.addHandler(self.c_handler)

        return ("1,Logger %s created successfully" % self.logger.name)

    @try_except
    def pt_logger_close(self):
        self.f_handler.close()
        self.c_handler.close()
        self.logger.removeHandler(self.f_handler)
        self.logger.removeHandler(self.c_handler)

        return ("1,Logger %s removed successfully" % self.logger.name)

    @try_except
    def config_parameters_load(self):
        m_info_comp = re.compile(r"\s*(\w+)\s*=\s*(.+)")
        m_annotation_comp = re.compile(r"(.*?)#(.*)")

        for eachline in fileinput.FileInput(Production_test.config_file):
            m_info = m_info_comp.match(eachline)
            if m_info:
                m_key = (m_info.group(1)).strip()
                m_annotation = m_annotation_comp.search(m_info.group(2))
                if m_annotation:
                    m_value = (m_annotation.group(1)).strip()
                else:
                    m_value = (m_info.group(2)).strip()

                if m_key == "device_type":
                    self.device_type = int(m_value)

                elif m_key == "dynamic_filter_en":
                    self.dynamic_filter_en = int(m_value)

                elif m_key == "vendor_id":
                    self.vendor_id = m_value

                elif m_key == "phase":
                    self.phase_str = m_value
                    tmp_list = (self.phase_str.strip()).split(",")
                    for each_p in tmp_list:
                        self.phase_list.append(each_p.strip())

                elif m_key == "burned_mac_address":
                    self.burned_mac_address = m_value

                elif m_key == "nf_detection_times":
                    self.nf_detection_times = int(m_value)

                elif m_key == "flatness_threshold":
                    self.flatness_threshold = int(m_value)

                elif m_key == "hpf_thd_700k":
                    self.hpf_thd_700k = int(m_value)

                elif m_key == "hpf_thd_2m":
                    self.hpf_thd_2m = int(m_value)

                elif m_key == "csr_thd":
                    self.csr_thd = int(m_value)

                elif m_key == "gold_ppm":
                    # keep integer and remove fraction part
                    self.gold_ppm = int(float(m_value))

                elif m_key == "phy_power_att":
                    self.phy_power_att = int(m_value)

                elif m_key == "filter_gpio_num":
                    self.filter_gpio_num = int(m_value)

                elif m_key == "read_fw_ver_flag":
                    self.read_fw_ver_flag = int(m_value)
                elif m_key == "read_chip_id_flag":
                    self.read_chip_id_flag = int(m_value)
                elif m_key == "read_ori_mac_address_flag":
                    self.read_ori_mac_address_flag = int(m_value)
                elif m_key == "burned_mac_address_flag":
                    self.burned_mac_address_flag = int(m_value)
                elif m_key == "noise_floor_detection_flag":
                    self.noise_floor_detection_flag = int(m_value)
                elif m_key == "tx_rx_loopback_flag":
                    self.tx_rx_loopback_flag = int(m_value)
                elif m_key == "flatness_flag":
                    self.flatness_flag = int(m_value)
                elif m_key == "sen_csr_flag":
                    self.sen_csr_flag = int(m_value)
                elif m_key == "led_control_flag":
                    self.led_control_flag = int(m_value)

                else:
                    pass

    @staticmethod
    def cmd_id_get(data_str):
        m_cmd_id = re.search(r"2323(\w{24})(\w{8})(\w{8})(\w{8})(\w{4})((\w{2})+)4040", data_str)
        if m_cmd_id:
            str_cmd_id = m_cmd_id.group(5)  # eg. 0200
        else:
            str_cmd_id = None

        return str_cmd_id

    @try_except
    @timeout_set(3)
    def cmd_send(self, cmd_str):
        cmd_id_str = self.cmd_id_get(cmd_str)
        self.ser_handler.write(binascii.a2b_hex(cmd_str))
        cs_info = ''

        m_tt_comp = re.compile(r"2323[0]{24}\w{8}01[0]{6}[0-9a-fA-F]{8}" + cmd_id_str + r"(\w{2})+?4040")

        while 1:
            cs_info += self.ser_handler.read(1)
            bytes2read = self.ser_handler.inWaiting()
            tmp = self.ser_handler.read(bytes2read)
            cs_info += tmp

            m_tt = m_tt_comp.search(cs_info.encode("hex"))
            if m_tt:
                self.logger.debug("cmd_send receive return info: %s" % m_tt.group(0))
                raw_data_str = m_tt.group(0).decode("hex")
                self.data_trans_queue.put(raw_data_str[32:-2])
                return 0

            if not self.time_out_queue.empty():
                return -1

    @staticmethod
    def command_line_build(cli_data_field_str):
        str_head = r"2323" + r"00" * 12
        str_moduleid = r"03000000"
        str_messageid = r"04000000"
        str_tail = r"4040"

        len_total_data = len(cli_data_field_str) / 2  # length unit: byte
        totallen_str = struct.pack('<I', len_total_data).encode("hex")
        command_line = str_head + str_moduleid + str_messageid + totallen_str + cli_data_field_str + str_tail

        return command_line

    @staticmethod
    def structure_info_parse_bits(obj_struct_dict, raw_data_str, lb_endian):
        return_list = []
        dict_bytes_type = {
            1: 'B',
            2: 'H',
            4: 'I'
        }
        structure_parameters = obj_struct_dict.keys()
        structure_bits_form = obj_struct_dict.values()
        total_bits = sum(structure_bits_form)
        bytes_cnt = total_bits / 8
        parse_format = struct.Struct(lb_endian + dict_bytes_type[bytes_cnt])

        parse_value = (parse_format.unpack(raw_data_str))[0]
        total_bits_info = (bin(parse_value)[2:]).zfill(total_bits)

        temp_sum = 0
        for each_index in range(len(structure_bits_form)):
            each_parameter = structure_parameters[each_index]
            each_bits_len = structure_bits_form[each_index]
            each_slice = slice(temp_sum, temp_sum + each_bits_len)
            return_list.append((each_parameter, total_bits_info[each_slice]))
            temp_sum += each_bits_len

        return return_list

    @staticmethod
    def structure_info_parse_bytes(obj_struct_dict, raw_data_str, lb_endian):
        structure_parameters = obj_struct_dict.keys()
        structure_data_form = ''.join(obj_struct_dict.values())
        parse_format = struct.Struct(lb_endian + structure_data_form)

        parse_results_list = list(parse_format.unpack(raw_data_str))
        return_list = zip(structure_parameters, parse_results_list)

        return return_list

    @try_except
    def power_down_up(self):
        str_power_down = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 04 00 00 00 00 00 00 00 00 00 00 00 40 40"
        str_power_up = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 40 40"
        command_str_power_down = str_power_down.replace(" ", "")
        command_str_power_up = str_power_up.replace(" ", "")

        self.ser_handler.write(binascii.a2b_hex(command_str_power_down))
        time.sleep(0.1)
        self.ser_handler.write(binascii.a2b_hex(command_str_power_up))
        time.sleep(0.1)

    @try_except
    def rst_low_high(self):
        str_rst_low = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 04 00 00 00 04 00 00 00 00 00 00 00 40 40"
        str_rst_high = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 04 00 00 00 03 00 00 00 00 00 00 00 40 40"
        command_str_rst_low = str_rst_low.replace(" ", "")
        command_str_rst_high = str_rst_high.replace(" ", "")

        self.ser_handler.write(binascii.a2b_hex(command_str_rst_low))
        time.sleep(0.1)
        self.ser_handler.write(binascii.a2b_hex(command_str_rst_high))
        time.sleep(0.1)

    @try_except
    @timeout_set(5)
    def enter_test_mode(self):
        s_info = ''
        enter_str = Production_test.base_str + "\n"

        m_sbl_comp = re.compile(r"kunlun v1.0 >")
        m_init_done_comp = re.compile(r"2323[0]{24}\w{8}01[0]{6}0c[0]{6}2c0006000600[0]{12}4040")

        while 1:
            self.ser_handler.write(Production_test.init_str)
            s_info += self.ser_handler.read(1)
            bytes2read = self.ser_handler.inWaiting()
            tmp = self.ser_handler.read(bytes2read)
            s_info += tmp

            m_sbl = m_sbl_comp.search(s_info)
            m_init_done = m_init_done_comp.search(s_info.encode("hex"))

            if m_sbl:
                self.ser_handler.write("\n")
                self.ser_handler.write(enter_str)
                s_info = s_info.replace(m_sbl.group(0), "")

            if m_init_done:
                logger_info = r"1,Test Mode Entered and Initial completes"
                return logger_info

            if not self.time_out_queue.empty():
                logger_info = r"0,TimeOut Error Test Mode Enter failed"
                return logger_info

    @try_except
    @timeout_set(2)
    def efuse_prog_bit_lock(self):
        str_efuse_lock = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                         r"03 00 00 00 2d 00 00 00 06 00 00 00 2d 00 00 00 00 00 40 40"
        command_str_efuse_lock = str_efuse_lock.replace(" ", "")
        cmd_id_str = self.cmd_id_get(command_str_efuse_lock)
        self.ser_handler.write(binascii.a2b_hex(command_str_efuse_lock))
        return_str, cs_info = '', ''

        m_tt_comp = re.compile(r"2323[0]{24}\w{8}01[0]{6}\w{8}" + cmd_id_str + r"01000100(\w{2})4040")

        while 1:
            cs_info += self.ser_handler.read(1)
            bytes2read = self.ser_handler.inWaiting()
            tmp = self.ser_handler.read(bytes2read)
            cs_info += tmp

            m_tt = m_tt_comp.search(cs_info.encode("hex"))
            if m_tt:
                return_str = m_tt.group(1)
                if "00" == return_str:
                    logger_info = (r"1,Efuse Program Done Bit already 1 Check Completes")
                elif "01" == return_str:
                    logger_info = (r"1,Efuse Program Done Bit original 0 Write Bit 1 Lock Completes")
                else:
                    logger_info = ("0,Return Value Error: %s" % return_str)
                self.logger.debug(logger_info)
                return logger_info

            if not self.time_out_queue.empty():
                logger_info = r"0,Efuse lock Timeout"
                return logger_info

    @try_except
    @timeout_set(2)
    def vendor_id_set(self):
        ascii_vid_str = binascii.b2a_hex(self.vendor_id)
        if 4 == len(ascii_vid_str):
            tmp_vid_str = ''
            for each_l in ascii_vid_str:
                tmp_vid_str += each_l
                if 2 == len(tmp_vid_str):
                    tmp_vid_str += " "
        else:
            return (r"0,Vendor ID Length Should be 2 bytes")

        str_vendor_id_set = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                            r"03 00 00 00 31 00 00 00 08 00 00 00 " \
                            r"31 00 02 00 02 00 " + tmp_vid_str + r" 40 40"
        command_str_vendor_id_set = str_vendor_id_set.replace(" ", "")
        cmd_id_str = self.cmd_id_get(command_str_vendor_id_set)
        self.ser_handler.write(binascii.a2b_hex(command_str_vendor_id_set))
        return_str, cs_info = '', ''

        m_tt_comp = re.compile(r"2323[0]{24}\w{8}01[0]{6}\w{8}" + cmd_id_str + r"01000100(\w{2})4040")

        while 1:
            cs_info += self.ser_handler.read(1)
            bytes2read = self.ser_handler.inWaiting()
            tmp = self.ser_handler.read(bytes2read)
            cs_info += tmp

            m_tt = m_tt_comp.search(cs_info.encode("hex"))
            if m_tt:
                return_str = m_tt.group(1)
                if "01" == return_str:
                    logger_info = r"1,Vendor ID set completes"
                    self.logger.debug(logger_info)
                    return (r"1,")
                else:
                    logger_info = r"0,Vendor ID set failed(Load OEM Error)"
                    self.logger.debug(logger_info)
                    return logger_info

            if not self.time_out_queue.empty():
                logger_info = r"0,Vendor ID Set Timeout"
                self.logger.debug(logger_info)
                return logger_info

    @try_except
    @timeout_set(2)
    def read_chip_info(self):
        int_ver_wafer, int_ver_reserved = 0, 0
        int_ver_pkg_bumping, int_ver_pkg_lic, int_ver_pkg_flash = 0, 0, 0
        str_ver_wafer, str_ver_reserved = '', ''
        str_ver_pkg_bumping, str_ver_pkg_lic, str_ver_pkg_flash = '', '', ''
        str_read_chip_id = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                           r"03 00 00 00 25 00 00 00 06 00 00 00 25 00 00 00 00 00 40 40"
        command_str_read_chip_id = str_read_chip_id.replace(" ", "")
        cmd_id_str = self.cmd_id_get(command_str_read_chip_id)
        self.ser_handler.write(binascii.a2b_hex(command_str_read_chip_id))
        return_list, cs_info = [], ''

        m_tt_comp = re.compile(r"2323[0]{24}\w{8}01[0]{6}\w{8}" + cmd_id_str + r"05000500((\w{2})+?)4040")

        while 1:
            cs_info += self.ser_handler.read(1)
            bytes2read = self.ser_handler.inWaiting()
            tmp = self.ser_handler.read(bytes2read)
            cs_info += tmp

            m_tt = m_tt_comp.search(cs_info.encode("hex"))
            if m_tt:
                chip_info_str = m_tt.group(1)
                # raw_data_str = chip_info_str.decode("hex")
                chip_version_info_str = chip_info_str[6:]
                raw_data_str_chip_version_info = chip_version_info_str.decode("hex")
                list_chip_version_info = self.structure_info_parse_bits(DictStructChipInfoVersionInfo,
                                                                        raw_data_str_chip_version_info,
                                                                        '<')

                for each_info in list_chip_version_info:
                    each_info_name = each_info[0]
                    each_info_str = each_info[1]
                    each_info_bin_str = "0b" + each_info_str

                    if "ver_wafer" == each_info_name:
                        str_ver_wafer = each_info_str
                        int_ver_wafer = int(each_info_bin_str, 2)
                    elif "ver_reserved" == each_info_name:
                        str_ver_reserved = each_info_str
                        int_ver_reserved = int(each_info_bin_str, 2)
                    elif "ver_pkg_bumping" == each_info_name:
                        str_ver_pkg_bumping = each_info_str
                        int_ver_pkg_bumping = int(each_info_bin_str, 2)
                    elif "ver_pkg_lic" == each_info_name:
                        str_ver_pkg_lic = each_info_str
                        int_ver_pkg_lic = int(each_info_bin_str, 2)
                    elif "ver_pkg_flash" == each_info_name:
                        str_ver_pkg_flash = each_info_str
                        int_ver_pkg_flash = int(each_info_bin_str, 2)
                    else:
                        pass

                chip_info_dict_str = (str(int_ver_wafer) + str(int_ver_reserved) + str(int_ver_pkg_bumping) +
                                      str(int_ver_pkg_lic) + str(int_ver_pkg_flash))

                cid_str = m_tt.group(1)[0:6]
                chip_id_str_new, letter_index = '', 0
                for each_letter in cid_str:
                    chip_id_str_new += each_letter
                    letter_index += 1
                    if letter_index == 2:
                        chip_id_str_new += "-"
                        letter_index = 0

                if chip_info_dict_str in Production_test.DictChipInfo.keys():
                    str_chip_type = Production_test.DictChipInfo[chip_info_dict_str]
                    return_list.append(("chip type", str_chip_type))
                    return_list.append(("chip id", chip_id_str_new[0:-1]))
                    return_list.append(("ver_wafer", "0b" + str_ver_wafer))
                    return_list.append(("ver_reserved", "0b" + str_ver_reserved))
                    return_list.append(("ver_pkg_bumping", "0b" + str_ver_pkg_bumping))
                    return_list.append(("ver_pkg_lic", "0b" + str_ver_pkg_lic))
                    return_list.append(("ver_pkg_flash", "0b" + str_ver_pkg_flash))

                    for each_logger_info in return_list:
                        self.logger.debug(each_logger_info)

                    return ("1,Chip type: %s" % str_chip_type)
                else:
                    self.logger.debug("Chip Info String: %s and Chip Info ID: %s" % (chip_info_str, chip_info_dict_str))
                    logger_info = ("0,Chip Info %s Mismatched" % chip_info_dict_str)
                    self.logger.debug(logger_info)
                    return logger_info

            if not self.time_out_queue.empty():
                logger_info = r"0,Chip ID Read Timeout"
                self.logger.debug(logger_info)
                return logger_info

    @try_except
    @timeout_set(2)
    def read_fw_ver(self):
        str_read_chip_id = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                           r"03 00 00 00 26 00 00 00 06 00 00 00 26 00 00 00 00 00 40 40"
        command_str_read_chip_id = str_read_chip_id.replace(" ", "")
        cmd_id_str = self.cmd_id_get(command_str_read_chip_id)
        self.ser_handler.write(binascii.a2b_hex(command_str_read_chip_id))
        return_str, cs_info = '', ''

        m_tt_comp = re.compile(r"2323[0]{24}\w{8}01[0]{6}\w{8}" + cmd_id_str + r"\w{4}\w{4}((\w{2})+?)4040")

        while 1:
            cs_info += self.ser_handler.read(1)
            bytes2read = self.ser_handler.inWaiting()
            tmp = self.ser_handler.read(bytes2read)
            cs_info += tmp

            m_tt = m_tt_comp.search(cs_info.encode("hex"))
            if m_tt:
                fw_ver_str = m_tt.group(1)
                logger_info = ("1,%s" % fw_ver_str.decode("hex"))
                self.logger.debug(logger_info)
                return logger_info

            if not self.time_out_queue.empty():
                logger_info = r"0,FW Version Read Timeout"
                self.logger.debug(logger_info)
                return logger_info

    @staticmethod
    def mac_addr_format_adjust(input_mac_addr):
        reformat_tuple = []
        obj_mac_addr_str = input_mac_addr.replace(" ", "")
        m_mac_addr_compile = re.compile(r"(\d+):(\d+):(\d+):(\d+):(\d+):(\d+)")
        m_mac_addr = m_mac_addr_compile.match(obj_mac_addr_str)

        if m_mac_addr:
            m_groups = m_mac_addr.groups()
            for each_group_str in m_groups:
                if 2 < len(each_group_str):
                    return -1
                elif 1 == len(each_group_str):
                    reformat_tuple.append('{0:0>2}'.format(each_group_str))
                elif 2 == len(each_group_str):
                    reformat_tuple.append(each_group_str)
                else:
                    pass
            if 6 == len(reformat_tuple):
                reformat_mac_addr = ':'.join(reformat_tuple)
                return reformat_mac_addr
            else:
                return -1
        else:
            return -1

    @try_except
    @timeout_set(2)
    def mac_addr_burn(self, burned_mac_address):
        self.burned_mac_address = burned_mac_address

        str_mac_addr = self.mac_addr_format_adjust(burned_mac_address)
        if -1 == str_mac_addr:
            return (r"0,Mac Adderss Format Error, please check...")

        str_burn_mac_addr_base = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                                 r"03 00 00 00 27 00 00 00 0c 00 00 00 27 00 06 00 06 00 "
        burn_mac_addr_command_str = (str_burn_mac_addr_base + str_mac_addr.replace(":", " ") + r" 40 40").replace(" ",
                                                                                                                  "")
        cmd_id_str = self.cmd_id_get(burn_mac_addr_command_str)
        self.ser_handler.write(binascii.a2b_hex(burn_mac_addr_command_str))
        cs_info = ''

        m_tt_comp = re.compile(r"2323[0]{24}\w{8}01[0]{6}\w{8}" + cmd_id_str + r"\w{4}\w{4}((\w{2})+?)4040")

        while 1:
            cs_info += self.ser_handler.read(1)
            bytes2read = self.ser_handler.inWaiting()
            tmp = self.ser_handler.read(bytes2read)
            cs_info += tmp

            m_tt = m_tt_comp.search(cs_info.encode("hex"))
            if m_tt:
                logger_info = ("1,%s" % str_mac_addr)
                self.logger.debug(logger_info)
                return logger_info

            if not self.time_out_queue.empty():
                logger_info = r"0,Mac Adderss Burned Timeout"
                self.logger.debug(logger_info)
                return logger_info

    @try_except
    @timeout_set(2)
    def mac_addr_read(self):
        str_read_mac_addr = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                            r"03 00 00 00 2b 00 00 00 06 00 00 00 2b 00 00 00 00 00 40 40"
        command_str_read_mac_addr = str_read_mac_addr.replace(" ", "")
        cmd_id_str = self.cmd_id_get(command_str_read_mac_addr)
        self.ser_handler.write(binascii.a2b_hex(command_str_read_mac_addr))
        return_str, cs_info, letter_index = '', '', 0

        m_tt_comp = re.compile(r"2323[0]{24}\w{8}01[0]{6}\w{8}" + cmd_id_str + r"\w{4}\w{4}((\w{2})+?)4040")

        while 1:
            cs_info += self.ser_handler.read(1)
            bytes2read = self.ser_handler.inWaiting()
            tmp = self.ser_handler.read(bytes2read)
            cs_info += tmp

            m_tt = m_tt_comp.search(cs_info.encode("hex"))
            if m_tt:
                return_mac_addr_str = m_tt.group(1)
                for each_l in return_mac_addr_str:
                    letter_index += 1
                    return_str += each_l
                    if letter_index == 2:
                        return_str += ":"
                        letter_index = 0

                logger_info = ("1,%s" % return_str[0:-1])
                self.logger.debug(logger_info)
                return logger_info

            if not self.time_out_queue.empty():
                logger_info = r"0,Mac Adderss Read Timeout"
                self.logger.debug(logger_info)
                return logger_info

    @try_except
    def pt_calc_noise_floor(self):
        nf_list = []

        for test_time in range(self.nf_detection_times):
            value_nf = self.calc_noise_floor()
            time.sleep(0.1)
            if 0 < value_nf:
                nf_list.append(value_nf)
            elif -1 == value_nf:
                logger_info = r"0,Noise Floor Calculate TimeOut"
                self.logger.debug(logger_info)
                return logger_info
            else:
                logger_info = r"0,Noise Floor Calculate Error"
                self.logger.debug(logger_info)
                return logger_info

        min_value_nf = min(nf_list)
        logger_info = ("1,Value Of Noise Floor is %d" % min_value_nf)
        self.logger.debug(logger_info)
        return logger_info

    @try_except
    @timeout_set(2)
    def calc_noise_floor(self):
        str_scan_nf = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                      r"03 00 00 00 0a 00 00 00 08 00 00 00 0a 00 02 00 02 00 08 00 40 40"
        command_str_scan_nf = str_scan_nf.replace(" ", "")
        cmd_id_str = self.cmd_id_get(command_str_scan_nf)
        self.ser_handler.write(binascii.a2b_hex(command_str_scan_nf))
        cs_info = ''

        m_tt_comp = re.compile(r"2323[0]{24}\w{8}01[0]{6}\w{8}" + cmd_id_str + r"\w{4}\w{4}((\w{2})+?)4040")

        while 1:
            cs_info += self.ser_handler.read(1)
            bytes2read = self.ser_handler.inWaiting()
            tmp = self.ser_handler.read(bytes2read)
            cs_info += tmp

            m_tt = m_tt_comp.search(cs_info.encode("hex"))
            if m_tt:
                str_nf_value = m_tt.group(1)
                dec_nf_value = int("0x" + str_nf_value, 16)
                return dec_nf_value

            if not self.time_out_queue.empty():
                return -1

    @try_except
    def pt_txrx_loopback(self):
        result_cnt, results_list = 0, []

        for each_phase in self.phase_list:
            each_phase_str = Production_test.DictPhase[each_phase]
            self.logger.debug("-* " * 20)
            self.logger.debug("Channel %s TXRX Loopback Test" % each_phase)
            self.logger.debug("-* " * 20)

            return_result = self.txrx_loopback_process(each_phase_str)

            if "1" == return_result[0]:
                results_list.append("Phase %s pass" % each_phase)
                result_cnt += 1
            else:
                results_list.append("Phase %s fail" % each_phase)

        if result_cnt == len(results_list):
            return ("1,%s" % '@'.join(results_list))
        else:
            return ("0,%s" % '@'.join(results_list))

    @try_except
    def txrx_loopback_process(self, p_str):
        return_value, dut_real_ppm = 0, 0
        return_dict, tx_info_list, list_error_info = {}, [], []

        # golden ppm(int16_t) format: parameter
        little_endian_g_ppm = struct.pack("<h", self.gold_ppm).encode("hex")
        temp_str, temp_index = '', 0
        for each_l in little_endian_g_ppm:
            temp_index += 1
            if 2 == temp_index:
                temp_str += each_l + " "
                temp_index = 0
            else:
                temp_str += each_l
        rf_little_endian_g_ppm = temp_str.strip()

        # dtest tx psg sof 2 a/b/c 0 : data field info
        str_cli_data_field = r"04 00 0b 00 0b 00 " + p_str + " 10 01 00 02 00 00 00 10 " + rf_little_endian_g_ppm
        str_cli_data_field = str_cli_data_field.replace(" ", '')
        command_str = self.command_line_build(str_cli_data_field)
        self.logger.debug("Command Line str: %s" % command_str)

        self.cmd_send(command_str)

        try:
            rd_info = self.data_trans_queue.get(timeout=4)
        except Exception, e_info:
            return ("0,Error: Receving Data Time out, error info: %s" % str(e_info))

        tx_info_list = self.structure_info_parse_bytes(DictStructTxRxLoopback, rd_info, '<')

        if ('accurate_indication', 255) in tx_info_list or ('accurate_indication', 4) in tx_info_list:
            self.logger.debug("TXRX loopback SUCCESSFUL!!")
            tx_rssi, rx_rssi, tx_ppm, rx_dc, rx_ppm, rx_snr = 0, 0, 0, 0, 0, 0
            tx_power_gain, tx_power_rmi, rx_power_gain, rx_power_rmi, = 0, 0, 0, 0

            for each_info in tx_info_list:
                if each_info[0] == "tx_gain":
                    tx_power_gain = each_info[1] - 24
                    self.logger.debug("tx_gain : %d" % tx_power_gain)
                    return_dict["tx_gain"] = tx_power_gain

                elif each_info[0] == "tx_adc_power":
                    tx_power_rmi = each_info[1]
                    self.logger.debug("tx_adc_power : %d" % tx_power_rmi)
                    return_dict["tx_adc_power"] = tx_power_rmi

                    tx_rssi = tx_power_rmi - tx_power_gain
                    self.logger.debug("tx_rssi : %s" % tx_rssi)
                    return_dict["tx_rssi"] = tx_rssi

                elif each_info[0] == "tx_dc":
                    tx_dc = each_info[1]
                    self.logger.debug("tx_dc : %d" % tx_dc)
                    return_dict["tx_dc"] = tx_dc

                elif each_info[0] == "tx_ppm":
                    tx_ppm = each_info[1]
                    self.logger.debug("tx_ppm : %d" % tx_ppm)
                    return_dict["tx_ppm"] = tx_ppm

                elif each_info[0] == "dut_real_ppm":
                    dut_real_ppm = each_info[1]
                    if dut_real_ppm > 0:
                        ppm_info = r"Faster than reference frequency!"
                    elif dut_real_ppm < 0:
                        ppm_info = r"Slower than reference frequency!"
                    else:
                        ppm_info = r"Match reference frequency!"

                    self.logger.debug("Dut_real_ppm: %d (%s)" % (dut_real_ppm, ppm_info))
                    return_dict["Dut_real_ppm"] = dut_real_ppm

                elif each_info[0] == "rx_dc":
                    rx_dc = each_info[1]
                    self.logger.debug("rx_dc : %d" % rx_dc)
                    return_dict["rx_dc"] = rx_dc

                elif each_info[0] == "rx_ppm":
                    pass
                    # rx_ppm = each_info[1]
                    # logger_printer.info("rx_ppm : %d" % rx_ppm)

                elif each_info[0] == "rx_snr":
                    rx_snr = each_info[1]
                    self.logger.debug("rx_snr : %d" % rx_snr)
                    return_dict["rx_snr"] = rx_snr

                elif each_info[0] == "rx_gain":
                    rx_power_gain = each_info[1] - 24
                    self.logger.debug("rx_gain : %d" % rx_power_gain)
                    return_dict["rx_gain"] = rx_power_gain

                elif each_info[0] == "rx_adc_power":
                    rx_power_rmi = each_info[1]
                    self.logger.debug("rx_adc_power : %d" % rx_power_rmi)
                    return_dict["rx_adc_power"] = rx_power_rmi

                    rx_rssi = rx_power_rmi - rx_power_gain
                    self.logger.debug("rx_rssi : %s" % rx_rssi)
                    return_dict["rx_rssi"] = rx_rssi

                elif each_info[0] == "accurate_indication":
                    accurate_indication = each_info[1]
                    self.logger.debug("accurate_indication : %s" % accurate_indication)
                    return_dict["accurate_indication"] = accurate_indication

                elif each_info[0] == "w_character":
                    w_character = each_info[1]
                    self.logger.debug("w_character : %c" % w_character)
                    return_dict["w_character"] = w_character

                elif each_info[0] == "q_character":
                    q_character = each_info[1]
                    self.logger.debug("q_character : %c" % q_character)
                    return_dict["q_character"] = q_character

                else:
                    tmp_printer_str = each_info[0] + r" : " + str(each_info[1])
                    self.logger.debug(tmp_printer_str)

            if (tx_rssi < 50):
                return_value = -1
                list_error_info.append("tx_rssi(%d) is less than 50!" % tx_rssi)

            if (dut_real_ppm > 15):
                return_value = -1
                list_error_info.append("DUT_real_ppm(%d) is larger than 15!" % dut_real_ppm)

            elif (dut_real_ppm < -15):
                return_value = -1
                list_error_info.append("DUT_real_ppm(%d) is less than -15!" % dut_real_ppm)

            if (rx_dc > 50):
                return_value = -1
                list_error_info.append("rx_dc(%d) is larger than 50!" % rx_dc)

            if (rx_snr < 10):
                return_value = -1
                list_error_info.append("rx_snr(%d) is less than 10!" % rx_snr)

        else:
            self.logger.debug("TXRX loopback FAIL!")
            self.logger.debug("Response as below: ")
            for each_tx_info in tx_info_list[0:3]:
                self.logger.debug(each_tx_info)
            if ('accurate_indication', 0) in tx_info_list:
                list_error_info.append(r"real ppm value over range!")
            elif ('accurate_indication', 1) in tx_info_list:
                list_error_info.append(r"golden unit is not online!")
            elif ('accurate_indication', 2) in tx_info_list:
                list_error_info.append(r"snr check failed!")
            elif ('accurate_indication', 3) in tx_info_list:
                list_error_info.append(r"ppm calibration burned failed!")
            else:
                list_error_info.append(r"accurate indication mismatched!")
            return_value = -1

        if -1 == return_value:
            self.logger.debug("TEST Result =================> FAIL!!!!")
            error_info = " ".join(list_error_info)
            for each_error_info in list_error_info:
                self.logger.debug(each_error_info)
            return ("0,%s" % error_info)
        else:
            self.logger.debug("TEST Result =================> PASS!!!!")
            return ("1,%s" % str(return_dict))

    @try_except
    def pt_flatness_test(self):
        result_cnt, results_list, return_list = 0, [], []

        for each_phase in self.phase_list:
            each_phase_str = Production_test.DictPhase[each_phase]
            self.logger.debug("-* " * 20)
            self.logger.debug("Channel %s Flatness Detection Test" % each_phase)
            self.logger.debug("-* " * 20)

            for gpio_value in range(2):  # 0 or 1
                if self.dynamic_filter_en:
                    self.phase_filter_gpio_control(gpio_value)
                flatness_test_info = "Phase_%s_GPIO_%d_Flatness_Data" % (each_phase, gpio_value)
                return_flatness_test = self.flatness_test(each_phase_str, flatness_test_info)

                if isinstance(return_flatness_test, list):
                    var_value_of_csi_dump = return_flatness_test[1]
                    # differentiate band 32-120: 700K and 2M spectrogram
                    filter_threshold = return_flatness_test[0]
                    self.logger.debug("filter difference value: %d" % filter_threshold)
                    if self.hpf_thd_700k >= filter_threshold:
                        filter_type_value = 700
                    elif self.hpf_thd_2m >= filter_threshold:
                        filter_type_value = 2000
                    else:
                        filter_type_value = 0
                    self.logger.debug("Filter Type is %dK" % filter_type_value)
                    self.logger.debug("Value of Flatness is %f" % var_value_of_csi_dump)
                    if var_value_of_csi_dump < self.flatness_threshold:
                        self.logger.debug("Flatness is good!")
                        results_list.append("1,GPIO_%d Phase_%s Passed" % (gpio_value, each_phase))
                    else:
                        self.logger.debug("Flatness is bad!")
                        results_list.append("0,GPIO_%d Phase_%s Failed" % (gpio_value, each_phase))

                elif -1 == return_flatness_test:
                    self.logger.debug("Test <flatness_detection_phase_%s> Failed..." % each_phase)
                    results_list.append("0,GPIO_%d Phase_%s TimeOut" % (gpio_value, each_phase))

                else:
                    pass

                time.sleep(1)
                if not self.dynamic_filter_en:
                    break

        for each_result_info in results_list:
            if "1" == each_result_info[0]:
                result_cnt += 1
            else:
                pass
            return_list.append(each_result_info[2:])

        if result_cnt == len(results_list) and result_cnt > 0:
            return ("1,%s" % '@'.join(return_list))
        else:
            return ("0,%s" % '@'.join(return_list))

    @try_except
    def phase_filter_gpio_control(self, switch_flag):
        # GPIO STA: 23 / IIC: 28 / CCO: 2
        str_hex_fgpio = struct.pack("<B", self.filter_gpio_num).encode("hex")
        str_filter_gpio_on = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                             r"03 00 00 00 21 00 00 00 08 00 00 00 21 00 02 00 02 00 " + str_hex_fgpio + r" 01 40 40"
        str_filter_gpio_off = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                              r"03 00 00 00 21 00 00 00 08 00 00 00 21 00 02 00 02 00 " + str_hex_fgpio + r" 00 40 40"

        command_str_filter_gpio_on = str_filter_gpio_on.replace(" ", "")
        command_str_filter_gpio_off = str_filter_gpio_off.replace(" ", "")

        if switch_flag:
            self.logger.debug("Filter GPIO_%d Pulled Up..." % self.filter_gpio_num)
            self.ser_handler.write(binascii.a2b_hex(command_str_filter_gpio_on))
        else:
            self.logger.debug("Filter GPIO_%d Pulled Down..." % self.filter_gpio_num)
            self.ser_handler.write(binascii.a2b_hex(command_str_filter_gpio_off))
        time.sleep(1)

    @try_except
    def csi_dump_data_collect(self, pdata_msg):
        if 3 == len(pdata_msg):
            csi_batch_info_len, fmt_csi_batch_info = 3, "3B"
        else:
            csi_batch_info_len, fmt_csi_batch_info = 8, "4H"
        csi_batch_info_str = pdata_msg[-csi_batch_info_len:]
        csi_dump_data_str = pdata_msg[0:-csi_batch_info_len]
        fs_csi_batch_info = struct.Struct('<' + fmt_csi_batch_info)
        csi_batch_info = (fs_csi_batch_info.unpack(csi_batch_info_str))
        start_tone_num = csi_batch_info[0]
        end_tone_num = csi_batch_info[1]
        gain_entry_num = csi_batch_info[2]
        # packet_info = csi_batch_info[3]
        self.cur_gain_cnt += 1

        if 1 == self.cur_gain_cnt:
            self.first_cur_gain = gain_entry_num

        if start_tone_num == end_tone_num == 0:
            self.dump_data_str += csi_dump_data_str

        elif 87 == start_tone_num and 81 == end_tone_num and 1 == gain_entry_num:
            return -1

        else:
            self.dump_data_str += pdata_msg
            return_str = self.dump_data_str
            self.dump_data_str = ''
            return return_str

    @staticmethod
    def calc_variance(obj_data_list):
        sum_data = sum(obj_data_list)
        average_value = float(sum_data) / len(obj_data_list)

        temp_sum = 0
        for each_value in obj_data_list:
            temp_sum += (each_value - average_value) ** 2
        variance_value = float(temp_sum) / len(obj_data_list)

        return variance_value

    @try_except
    def generate_plot_file(self, obj_x_axis_data_list, obj_y_axis_data_list, obj_file_name):
        len_x_data, len_y_data = len(obj_x_axis_data_list), len(obj_y_axis_data_list)
        if len_x_data == len_y_data:
            plot_data_folder = self.log_folder + "\\" + "flatness_data_" + self.time_stamp
            if not os.path.exists(plot_data_folder):
                os.makedirs(plot_data_folder)

            plot_file = plot_data_folder + "\\" + obj_file_name + r".txt"
            with open(plot_file, 'w') as wf:
                for each_index in range(len_x_data):
                    wf.write("%s %s\n" %
                             (str(obj_x_axis_data_list[each_index]),
                              str(obj_y_axis_data_list[each_index])))

            return 0
        else:
            return -1

    @try_except
    @timeout_set(5)
    def flatness_test(self, p_str, flatness_test_info_str):
        str_tx_psg_sof_3_a = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                             r"03 00 00 00 04 00 00 00 0f 00 00 00 04 00 09 00 09 00 " + \
                             p_str + r" 10 01 00 03 00 00 00 10 40 40"
        command_str_tx_psg_sof_3_a = str_tx_psg_sof_3_a.replace(" ", "")
        cmd_id_str = self.cmd_id_get(command_str_tx_psg_sof_3_a)
        self.ser_handler.write(binascii.a2b_hex(command_str_tx_psg_sof_3_a))
        return_list, cs_info = [], ''

        m_tt_comp = re.compile(r"2323[0]{24}\w{8}01[0]{6}\w{8}" + cmd_id_str + r"\w{4}\w{4}((\w{2})+?)4040")

        while 1:
            cs_info += self.ser_handler.read(1)
            bytes2read = self.ser_handler.inWaiting()
            tmp = self.ser_handler.read(bytes2read)
            cs_info += tmp

            m_tt = m_tt_comp.search(cs_info.encode("hex"))
            if m_tt:
                qinfo = m_tt.group(0)
                sinfo = qinfo.decode("hex")
                total_data = sinfo[2:-2]
                head_fmt = '6B6B2H2I'  # 24
                len_head_fmt = struct.calcsize(head_fmt)
                data_head = total_data[0:len_head_fmt]
                ss = struct.Struct(head_fmt)
                undata_head = ss.unpack(data_head)
                # (addr_1, addr_2, addr_3, addr_4, addr_5, addr_6, addr_1, addr_2, addr_3, addr_4, addr_5, addr_6,
                #  module_id, crc_2bytes, message_id, length)

                r_module_id = undata_head[-4]
                r_msg_id = undata_head[-2]
                if (r_module_id == 3 and r_msg_id == 1):
                    r_msg_len = undata_head[-1]
                    data_msg = total_data[-r_msg_len:]

                    base_msg = data_msg[0:6]
                    b_fmt = struct.Struct('<HHH')
                    r_base_msg = b_fmt.unpack(base_msg)
                    rid = r_base_msg[0]
                    tlen = r_base_msg[1]
                    dlen = r_base_msg[2]

                    if (rid == 0x04 and tlen == dlen):
                        try:
                            pure_data_msg = data_msg[6:]
                            csi_data_collect_return_str = self.csi_dump_data_collect(pure_data_msg)
                            if -1 == csi_data_collect_return_str:
                                self.logger.debug(r"Collecting CSI Dump Data Error, please check...")
                                return -1

                            elif not csi_data_collect_return_str:
                                self.logger.debug("Collecting CSI Dump Data, please wait...")
                                cs_info = cs_info.replace(m_tt.group(0).decode("hex"), "")
                                continue

                            else:
                                self.logger.debug("Collecting CSI Dump Data Completes...")
                                csi_dump_data_str_len = len(csi_data_collect_return_str)
                                fmt_scan_csi = str(csi_dump_data_str_len / 2) + 'H'
                                fs_scan_csi = struct.Struct('<' + fmt_scan_csi)
                                undata_msg = fs_scan_csi.unpack(csi_data_collect_return_str)
                                csi_dump_info_i, csi_dump_info_q, csi_dump_info_amp_avg, i_index = 0, 0, 0, 0
                                csi_dump_amp_avg_info_list = []
                                while 1:
                                    csi_dump_info_i = c_int16(undata_msg[i_index]).value  # signed number
                                    i_index += 1
                                    csi_dump_info_q = c_int16(undata_msg[i_index]).value  # signed number
                                    i_index += 1
                                    if csi_dump_info_i == csi_dump_info_q == 0:
                                        csi_dump_info_amp_avg = 0
                                    else:
                                        csi_dump_info_amp_avg = 10 * math.log10(csi_dump_info_i ** 2 +
                                                                                csi_dump_info_q ** 2)

                                    csi_dump_amp_avg_info_list.append(csi_dump_info_amp_avg)
                                    if i_index == len(undata_msg) - 4:
                                        csi_dump_amp_avg_info_list.append(undata_msg[-4])  # start tone
                                        csi_dump_amp_avg_info_list.append(undata_msg[-3])  # end tone
                                        csi_dump_amp_avg_info_list.append(self.first_cur_gain)  # gain value
                                        csi_dump_amp_avg_info_list.append(c_int16(undata_msg[-1]).value)  # packet info
                                        return_list.append(c_int16(undata_msg[-1]).value)
                                        break

                            start_pos = csi_dump_amp_avg_info_list[-4]
                            end_pos = csi_dump_amp_avg_info_list[-3]
                            x_axis_list = range(start_pos, end_pos + 1)
                            y_axis_list = csi_dump_amp_avg_info_list[0: -4]

                            return_value = self.generate_plot_file(x_axis_list,
                                                                   y_axis_list,
                                                                   flatness_test_info_str)
                            if -1 == return_value:
                                self.logger.debug("Generate plot data file failed, please check raw data!")
                                return -1

                            var_dump_value = self.calc_variance(y_axis_list)

                            return_list.append(var_dump_value)
                            self.logger.debug("Matplot complete, please check the diagram!")
                            return return_list

                        except Exception, e_info:
                            self.logger.debug("Error in flatness detection %s skip this test!" % str(e_info))
                            return -1

            if not self.time_out_queue.empty():
                return -1

    @try_except
    def pt_sen_csr_detection(self):
        csr_retry_cnt = 3
        result_cnt, results_list, return_list = 0, [], []

        for each_phase in self.phase_list:
            each_phase_str = Production_test.DictPhase[each_phase]
            self.logger.debug("-* " * 20)
            self.logger.debug("Channel %s Sensitivity and Communication Success Rate Detection Test" % each_phase)
            self.logger.debug("-* " * 20)

            for retry_i in range(csr_retry_cnt):
                self.logger.debug("CSR Test %d time, Down %d dB Power: TMI 4" % (retry_i + 1, self.phy_power_att))
                time.sleep(1)
                value_of_sen_csr = self.sen_csr_detection(each_phase_str)
                if -1 == value_of_sen_csr:
                    results_info = ("0,Phase_%s csr TimeOut..." % each_phase)
                    results_list.append(results_info)
                    break
                elif self.csr_thd > value_of_sen_csr:
                    if csr_retry_cnt == retry_i + 1:
                        results_info = ("0,Phase_%s csr failed: %d%% less than %d%%" %
                                        (each_phase, value_of_sen_csr, self.csr_thd))
                        results_list.append(results_info)
                    else:
                        self.logger.debug("0,sensitivity_csr_phase_%s: %d%% less than %d%%" %
                                          (each_phase, value_of_sen_csr, self.csr_thd))
                        continue
                else:
                    results_info = ("1,Phase_%s csr %d%% Passed" %
                                    (each_phase, value_of_sen_csr))
                    results_list.append(results_info)
                    break

        for each_result_info in results_list:
            if "1" == each_result_info[0]:
                result_cnt += 1
            else:
                pass
            return_list.append(each_result_info[2:])

        if result_cnt == len(results_list):
            return ("1,%s" % '@'.join(return_list))
        else:
            return ("0,%s" % '@'.join(return_list))

    @try_except
    @timeout_set(4)
    def sen_csr_detection(self, p_str):
        hex_tmi = (struct.pack('<B', self.tmi_num)).encode("hex")
        hex_pwr_att = (struct.pack('<B', self.phy_power_att)).encode("hex")
        str_sen_csr = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                      r"03 00 00 00 04 00 00 00 10 00 00 00 04 00 0a 00 0a 00 " + \
                      p_str + r" 10 01 00 04 00 00 00 " + hex_tmi + " " + hex_pwr_att + r" 40 40"
        command_str_sen_csr = str_sen_csr.replace(" ", "")
        cmd_id_str = self.cmd_id_get(command_str_sen_csr)
        self.ser_handler.write(binascii.a2b_hex(command_str_sen_csr))
        return_value, cs_info = 0, ''

        m_tt_comp = re.compile(r"2323[0]{24}\w{8}01[0]{6}\w{8}" + cmd_id_str + r"01000100(\w{2})4040")

        while 1:
            cs_info += self.ser_handler.read(1)
            bytes2read = self.ser_handler.inWaiting()
            tmp = self.ser_handler.read(bytes2read)
            cs_info += tmp

            m_tt = m_tt_comp.search(cs_info.encode("hex"))
            if m_tt:
                hex_str = r"0x" + m_tt.group(1)
                return_value = int(hex_str, 16)
                return return_value

            if not self.time_out_queue.empty():
                return -1

    @try_except
    def led_control(self):
        str_tx_led_up = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                        r"03 00 00 00 21 00 00 00 08 00 00 00 21 00 02 00 02 00 20 01 40 40"
        str_tx_led_off = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                         r"03 00 00 00 21 00 00 00 08 00 00 00 21 00 02 00 02 00 20 00 40 40"
        str_rx_led_up = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                        r"03 00 00 00 21 00 00 00 08 00 00 00 21 00 02 00 02 00 21 01 40 40"
        str_rx_led_off = r"23 23 00 00 00 00 00 00 00 00 00 00 00 00 " \
                         r"03 00 00 00 21 00 00 00 08 00 00 00 21 00 02 00 02 00 21 00 40 40"
        command_str_tx_led_up = str_tx_led_up.replace(" ", "")
        command_str_tx_led_off = str_tx_led_off.replace(" ", "")
        command_str_rx_led_up = str_rx_led_up.replace(" ", "")
        command_str_rx_led_off = str_rx_led_off.replace(" ", "")

        self.logger.debug("Tx LED(GPIO32) Pulled Up/Down...")
        time.sleep(0.1)
        self.ser_handler.write(binascii.a2b_hex(command_str_tx_led_up))
        time.sleep(0.1)
        self.ser_handler.write(binascii.a2b_hex(command_str_tx_led_off))

        time.sleep(0.1)
        self.logger.debug("Rx LED(GPIO33) Pulled Up/Down...")
        self.ser_handler.write(binascii.a2b_hex(command_str_rx_led_up))
        time.sleep(0.1)
        self.ser_handler.write(binascii.a2b_hex(command_str_rx_led_off))

        return ("1,LED control successfully")


if __name__ == '__main__':
    pass
