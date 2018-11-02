# -*- encoding:UTF-8 -*-
from libs import ConsolePrint
from libs import ThreadManager
from pyvisa.errors import VI_ERROR_SYSTEM_ERROR
import time
from libs.TimeFormat import TimeFormat
from libs.CollectResult import CollectResult
import os
import sys

reports_folder = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "charge_reports")
if not os.path.exists(reports_folder):
    os.makedirs(reports_folder)


class ChargeData(object):
    def __init__(self, interval, instr, v_cali=0, a_cali=0):
        self.instr = instr
        self.interval = interval
        self.v_cali = v_cali
        self.a_cali = a_cali
        self.__stop = True
        self.__ampere = list()
        self.__voltage = list()
        self.__count = 0
        self.__excel = CollectResult(save_path=os.path.join(reports_folder, '%s.xls' % TimeFormat.timestamp()))
        ThreadManager.append_work(target=self.refresh, allow_dupl=False)

    def refresh(self):
        while self.__stop:
            self.__count += 1
            a = self.__query_ampere()
            v = self.__query_voltage()
            self.__excel.write_row_data(n=self.__count, v=v, a=a,
                                        t=TimeFormat.test_timestamp())
            self.__ampere.append(a)
            self.__voltage.append(v)
            time.sleep(self.interval - 0.4)

    def stop(self):
        self.__stop = False

    def get_ampere(self):
        return self.__ampere

    def get_voltage(self):
        return self.__voltage

    def __query_ampere(self):
        try:
            # self.instr._send_command('MEASUrement:IMMed:SOUrce CH4')
            # result, a = self.instr._send_command('MEASUrement:IMMed:VALue?')
            # result, a = self.instr._send_command('MEASU:IMMed:SOU CH4:VALue?')
            result, a = self.instr.get_channel_value(4)
            print a
            a = float(a) * 1000
            return int(a + self.a_cali)
        except ValueError:
            ConsolePrint.traceback()
            ConsolePrint.error(result)
            ConsolePrint.error(a)
            return -1
        except VI_ERROR_SYSTEM_ERROR:
            ConsolePrint.traceback()
            return -2

    def __query_voltage(self):
        try:
            # self.instr._send_command('MEASUrement:IMMed:SOUrce CH1')
            # result, v = self.instr._send_command('MEASUrement:IMMed:VALue?')
            result, v = self.instr.get_channel_value(1)
            print v
            v = float(v) * 1000
            return int(v + self.v_cali)
        except ValueError:
            ConsolePrint.traceback()
            ConsolePrint.error(result)
            ConsolePrint.error(v)
            return -1
        except VI_ERROR_SYSTEM_ERROR:
            ConsolePrint.traceback()
            return -2
