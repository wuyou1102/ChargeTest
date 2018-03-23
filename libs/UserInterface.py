# -*- encoding:UTF-8 -*-
import sys
import wx
from time import sleep
from libs.SCPI import get_serial_source
from libs import Execution

from libs import ConsolePrint

reload(sys)
sys.setdefaultencoding('utf-8')


class RedirectText(object):
    def __init__(self, wx_text_ctrl):
        self.out = wx_text_ctrl

    def write(self, string):
        wx.CallAfter(self.out.WriteText, string)


class UserInterface(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title="Charge&Discharge V1.5", size=(480, 400))
        self.Center()
        self.panel = wx.Panel(self, -1)
        self.execution_thread = None
        main_box = wx.BoxSizer(wx.VERTICAL)  # 整个界面，水平布局

        message_box = wx.BoxSizer(wx.VERTICAL)
        self.TC_message = wx.TextCtrl(self.panel, -1, '',
                                      style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        self.TC_message.SetInsertionPointEnd()
        self.TC_message.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False))
        redir = RedirectText(self.TC_message)
        sys.stdout = redir
        message_box.Add(self.TC_message, 1, wx.EXPAND)
        serial_box = wx.BoxSizer(wx.HORIZONTAL)
        serial_title = wx.StaticText(self.panel, -1, label='Port:')
        self.serial_choice = wx.Choice(self.panel, -1, choices=get_serial_source())

        calibration_title = wx.StaticText(self.panel, -1, label='电压校准 (mV):')
        self.calibration_SC = wx.SpinCtrl(self.panel, id=-1, size=(80, -1), style=wx.SP_ARROW_KEYS | wx.SP_BORDER,
                                          min=-1000, max=1000,
                                          initial=0)

        serial_box.Add(serial_title, 0, wx.TOP, 3)
        serial_box.Add(self.serial_choice, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        serial_box.Add(calibration_title, 0, wx.TOP | wx.LEFT, 3)
        serial_box.Add(self.calibration_SC, 0, wx.LEFT, 5)
        option_box = wx.BoxSizer(wx.HORIZONTAL)
        interval_title = wx.StaticText(self.panel, -1, label='间隔:')
        self.interval_slider = wx.Slider(self.panel, -1, minValue=1, maxValue=300, style=wx.SL_LABELS)
        self.interval_slider.SetValue(10)
        option_box.Add(interval_title, 0, wx.ALIGN_CENTER_VERTICAL)
        option_box.Add(self.interval_slider, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM, 5)
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        start_button = wx.Button(self.panel, -1, 'Start', size=(50, 50))
        self.Bind(wx.EVT_BUTTON, self.on_start, start_button)
        stop_button = wx.Button(self.panel, -1, 'Stop', size=(50, 50))
        self.Bind(wx.EVT_BUTTON, self.on_stop, stop_button)
        convert_button = wx.Button(self.panel, -1, 'Convert', size=(55, 50))
        self.Bind(wx.EVT_BUTTON, self.on_convert, convert_button)
        button_box.Add(start_button, 0)
        button_box.Add(stop_button, 0)
        button_box.Add(convert_button, 0)
        option_box.Add(button_box, 0, wx.EXPAND | wx.LEFT | wx.BOTTOM, 5)

        main_box.Add(serial_box, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 5)
        main_box.Add(option_box, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 5)
        main_box.Add(message_box, 1, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT | wx.BOTTOM, 5)
        self.panel.SetSizer(main_box)
        self.__control_sharing()

    def __control_sharing(self):
        def msg_output(msg):
            sleep(0.01)
            wx.CallAfter(self.TC_message.AppendText, msg)

        def disable():
            self.calibration_SC.Disable()
            self.serial_choice.Disable()
            self.interval_slider.Disable()

        def enable():
            self.calibration_SC.Enable()
            self.serial_choice.Enable()
            self.interval_slider.Enable()

        ConsolePrint.msg_output = msg_output
        Execution.disable = disable
        Execution.enable = enable

    def on_start(self, event):
        if self.execution_thread is None or not self.execution_thread.isAlive():
            port = self.get_select_port()
            s_t = self.get_sleep_time()
            c_v = self.get_calibration_voltage()
            self.execution_thread = Execution.Execution(port=port, sleep_time=s_t, calibration=c_v)
            self.execution_thread.setDaemon(True)
            self.execution_thread.start()
        else:
            ConsolePrint.warm("已经有一个正在执行的测试。")

    def on_stop(self, event):
        if self.execution_thread is None:
            ConsolePrint.warm("没有发现需要停止的测试。")
            return False
        if self.execution_thread.isAlive():
            ConsolePrint.warm("正在停止测试，请耐心等待。")
            self.execution_thread.stop()
        else:
            ConsolePrint.warm("没有发现需要停止的测试。")

    def get_select_port(self):
        return self.serial_choice.GetStringSelection()

    def get_sleep_time(self):
        return self.interval_slider.GetValue()

    def get_calibration_voltage(self):
        return self.calibration_SC.GetValue() / 1000.0

    def on_convert(self, event):
        dlg = wx.FileDialog(self,
                            message="Select excel",
                            wildcard="Excel (*.xls)|*.xls|All files (*.*)|*.*",
                            defaultDir="D:\\ChargeTest",
                            style=wx.FD_OPEN
                            )
        if dlg.ShowModal() == wx.ID_OK:
            excel_path = dlg.GetPaths()[0]
            print excel_path
        dlg.Destroy()


if __name__ == '__main__':
    app = wx.App()
    f = UserInterface()
    f.Show()
    app.MainLoop()
