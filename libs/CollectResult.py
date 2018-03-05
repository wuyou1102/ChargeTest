# -*- encoding:UTF-8 -*-
__author__ = 'c_youwu'
import threading
from ExcelStyle import ExcelStyle
from xlwt import Workbook
from libs import ConsolePrint


class CollectResult(object):
    def __init__(self, save_path):
        self.lock = threading.Lock()
        self.normal_style1 = ExcelStyle.cell_style(horizontal='c', font_size=13)
        self.save_path = save_path
        self.excel = Workbook()
        self.__init_summary_sheet()


    def __init_summary_sheet(self):
        self.sheet = self.excel.add_sheet('Summary', True)
        self.write_row_data(n='#', v=u'电压(V)', a=u'电流(A)', t=u'时间')

    def write_row_data(self, **kwargs):
        if self.lock.acquire():
            try:
                row_num = len(self.sheet.rows)  # 得到最后一行的
                n = kwargs.get('n')
                v = kwargs.get('v')
                a = kwargs.get('a')
                t = kwargs.get('t')
                self.sheet.write(row_num, 0, n, style=self.normal_style1)
                self.sheet.write(row_num, 1, v, style=self.normal_style1)
                self.sheet.write(row_num, 2, a, style=self.normal_style1)
                self.sheet.write(row_num, 3, t, style=self.normal_style1)

                self.excel.save(self.save_path)
            except IOError:
                ConsolePrint.error("请关闭打开的Excel文件，这样数据才可以写入文件。")
                # self.excel.save(self.save_path)
            finally:
                self.lock.release()


if __name__ == '__main__':
    import os

    cr = CollectResult('C:\Git\AppStress\log')


    def find_xml(path, files=[]):
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                find_xml(path=file_path, files=files)
            elif file.endswith('.xml'):
                files.append(file_path)
        return files


    cases = find_xml('C:\Git\AppStress\\repository\cases')
    result1 = ['Pass', 'Fail']
    logpath = ['', 'C:\Git\AppStress\\repository\cases']
    import random

    for case in cases:
        cr.write_row_data(device='ddddd', case=case, result=random.choice(result1), log=random.choice(logpath))
