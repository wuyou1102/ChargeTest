# -*- encoding:UTF-8 -*-
__author__ = 'wuyou'
from libs.SCPI import SerialInstrument
from time import sleep, time
from libs.CollectResult import CollectResult
from libs.TimeFormat import TimeFormat
from os.path import join
import threading
from libs import ConsolePrint
from os.path import exists
from os import makedirs
from pyvisa.errors import VI_ERROR_SYSTEM_ERROR

disable = None
enable = None


class Execution(threading.Thread):
    def __init__(self, port, save_path="D:\\ChargeTest", sleep_time=10, calibration=0):
        threading.Thread.__init__(self)
        if disable is not None:
            disable()
        ConsolePrint.debug('WUYOU:START')
        ConsolePrint.debug('Port:\"%s\"' % port)
        ConsolePrint.debug('Save:\"%s\"' % save_path)
        ConsolePrint.debug('Sleep:\"%s\" (S)' % sleep_time)
        ConsolePrint.debug('Calibration:\"%s\" (V)' % calibration)
        ConsolePrint.info("测试开始，执行初始化中。")
        self.__port = port
        self.__save_path = save_path
        if not exists(self.__save_path):
            makedirs(self.__save_path)
        self.__stop_flag = False
        self.__count = 0
        self.__excel = CollectResult(save_path=join(save_path, '%s.xls' % TimeFormat.timestamp()))
        self.__serial = SerialInstrument(port)
        self.__sleep_time = sleep_time
        self.__cal_voltage = calibration

    def run(self):
        self.__serial._send_command('MEASUrement:IMMed:TYPe MEAN')
        try:
            while True:
                if self.__stop_flag:
                    break
                self.__count += 1
                a = self.get_ampere()
                v = self.get_voltage()
                if a is None or v is None:
                    ConsolePrint.error("出现了意外情况，异常终止。")
                    break
                if a is False or v is False:
                    ConsolePrint.error("与示波器通信失败，等待重试。")
                    sleep(0.1)
                    continue
                ConsolePrint.info("电流={a} (A）, 电压={v} （V）".format(a=a, v=v))
                self.__excel.write_row_data(n=self.__count, v=v, a=a,
                                            t=TimeFormat.test_timestamp())
                ConsolePrint.info("等待{time}秒".format(time=self.__sleep_time))
                sleep(self.__sleep_time)
        except Exception:
            ConsolePrint.traceback()
        finally:
            ConsolePrint.info("测试结束。")
            if enable is not None:
                enable()

    def get_ampere(self):
        try:
            self.__serial._send_command('MEASUrement:IMMed:SOUrce CH4')
            sleep(0.1)
            result, a = self.__serial._send_command('MEASUrement:IMMed:VALue?')
            if a.endswith('E-3'):
                a = float(a[:-3]) / 1000
            else:
                a = float(a)
            return a
        except ValueError:
            ConsolePrint.traceback()
            ConsolePrint.error(result)
            ConsolePrint.error(a)
            return None
        except VI_ERROR_SYSTEM_ERROR:
            ConsolePrint.traceback()
            return False

    def get_voltage(self):
        try:
            self.__serial._send_command('MEASUrement:IMMed:SOUrce CH1')
            sleep(0.1)
            result, v = self.__serial._send_command('MEASUrement:IMMed:VALue?')
            if v.endswith('E-3'):
                v = float(v[:-3]) / 1000
            else:
                v = float(v)
            return v + self.__cal_voltage
        except ValueError:
            ConsolePrint.traceback()
            ConsolePrint.error(result)
            ConsolePrint.error(v)
            return None
        except VI_ERROR_SYSTEM_ERROR:
            ConsolePrint.traceback()
            return False

    def stop(self):
        self.__stop_flag = True
