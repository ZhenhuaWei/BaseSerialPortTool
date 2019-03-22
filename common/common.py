import datetime
import threading
import ctypes
import inspect
import random

class StopThreading:
    @staticmethod
    def _async_raise(tid, exc_type):
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exc_type):
            exc_type = type(exc_type)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)



def get_datetime():
    """ get current date time, as accurate as milliseconds
        
        Args: None
            
        Returns:
            str type
            eg: "2018-10-01 00:32:39.993176"
            
    """
    return str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

def uchar_checksum(data, byteorder='little'):
    '''
    char_checksum 按字节计算校验和。每个字节被翻译为无符号整数
    @param data: 字节串 
    @param byteorder: 大/小端
    @return:返回最低1位
    '''
    length = len(data)
    checksum = 0
    for i in range(0, length):
        checksum += int.from_bytes(data[i:i+1], byteorder, signed=False)
        checksum &= 0xFF # 强制截断
         
    return checksum