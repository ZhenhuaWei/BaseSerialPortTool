import datetime
import threading
import ctypes
import inspect

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