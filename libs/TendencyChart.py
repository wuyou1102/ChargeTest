# -*- encoding:UTF-8 -*-
__author__ = 'wuyou'
from pylab import plt
from numpy import linspace
import xlrd
import sys

excel_path = sys.argv[0]

line_width = 0.6
line_style = '-'
line_color_volt = 'g'
line_color_amp = 'r'
figure_height = 10
figure_width = 10


def draw_png(excel_path):
    v, a = get_data(excel_path)
    png_path = excel_path.replace('.xls', '.png')
    return draw_proc_rank_data(volt=v, amp=a, save_path=png_path)


def draw_proc_rank_data(volt, amp, save_path='tmp.png'):
    times = len(volt) if len(volt) > len(amp) else len(amp)
    figure_width = 65536 / 50 if times > 65536 else times / 50

    plt.figure(figsize=(figure_width, figure_height), clear=True)
    subfig = plt.subplot(111)
    plt.xlim(0, times)
    plt.ylim(-0.1, 4.5)
    plt.xticks(linspace(0, times, 200 if times > 200 else times))  # 设置很坐标格式，小于200的数据
    plt.yticks(linspace(-0.1, 4.5, 47))

    line, = subfig.plot(volt, label="Voltage", linewidth=line_width,
                        color=line_color_volt)
    line, = subfig.plot(amp, label="Ampera", linewidth=line_width,
                        color=line_color_amp)

    box = subfig.get_position()
    subfig.set_position([box.x0, box.y0, box.width, box.height])
    subfig.legend(loc=0, fontsize=8)  # , bbox_to_anchor=(1, 0.5)
    plt.xlabel('Number of times')
    plt.ylabel('Voltage & Ampera')
    plt.title('Charge Test', fontsize=20, loc='left')
    plt.grid(True)
    plt.savefig(save_path)
    plt.clf()
    plt.close()


def get_data(excel):
    workboox = xlrd.open_workbook(excel)
    sheet = workboox.sheet_by_index(0)
    v_list = sheet.col_values(1, 1)
    a_list = sheet.col_values(2, 1)
    return v_list, a_list,


draw_png('C:\Users\dell\Desktop\\a.xls')
