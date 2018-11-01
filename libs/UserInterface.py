# -*- encoding:UTF-8 -*-
import sys
import wx
import MplPanel
from libs.SCPI import get_serial_source
from libs.SCPI import SerialInstrument
from libs import Utility
import pyvisa
from libs.ChargeData import ChargeData

reload(sys)
sys.setdefaultencoding('utf-8')


class RedirectText(object):
    def __init__(self, wx_text_ctrl):
        self.out = wx_text_ctrl

    def write(self, string):
        wx.CallAfter(self.out.WriteText, string)


class UserInterface(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title="充放电自动化测试 Ver.2.0", size=(800, 800))
        self.Center()
        self.panel = UserInterfacePanel(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.panel.close()
        event.Skip()


class UserInterfacePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        port_sizer = self.__init_port_sizer()
        spin_sizer = self.__init_spin_sizer()
        self.ampe = MplPanel.AmpereMpl(self)
        self.volt = MplPanel.VoltageMpl(self)
        setting_sizer = self.__init_mpl_setting_sizer()
        self.instrumentation = None
        self.data = None
        main_sizer.Add(port_sizer, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        main_sizer.Add(spin_sizer, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        main_sizer.Add(setting_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(wx.StaticLine(self, style=wx.HORIZONTAL), 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.volt, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        main_sizer.Add(self.ampe, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        main_sizer.Add(wx.StaticLine(self, style=wx.HORIZONTAL), 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_sizer)
        self.Layout()

    def __init_port_sizer(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(self, wx.ID_ANY, label=u'仪器端口:', style=wx.TEXT_ALIGNMENT_CENTER)
        self.port_choice = wx.Choice(self, wx.ID_ANY, choices=get_serial_source())
        refresh = wx.Button(self, wx.ID_ANY, u"刷新", size=(50, -1))
        connect = wx.Button(self, wx.ID_ANY, u"连接", size=(50, -1))
        refresh.Bind(wx.EVT_BUTTON, self.on_refresh)
        connect.Bind(wx.EVT_BUTTON, self.on_connect)
        sizer.Add(title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        sizer.Add(self.port_choice, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        sizer.Add(connect, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        sizer.Add(refresh, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        return sizer

    def __init_mpl_setting_sizer(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        v_setting_sizer = self.volt.init_ybound_set_sizer(self)
        a_setting_sizer = self.ampe.init_ybound_set_sizer(self)

        self.ampe.set_ybound(0, 2000)
        self.volt.set_ybound(3500, 4500)
        sizer.Add(v_setting_sizer, 0, wx.ALL, 0)
        sizer.Add(wx.StaticLine(self, style=wx.LI_VERTICAL), 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(a_setting_sizer, 0, wx.ALL, 0)
        return sizer

    def on_refresh(self, event):
        choices = get_serial_source()
        self.port_choice.Items = choices

    def on_connect(self, event):
        obj = event.GetEventObject()
        state = obj.GetLabel()
        if state == u"连接":
            port = self.port_choice.GetStringSelection()
            if not port:
                return False
            try:
                self.instrumentation = SerialInstrument(port)
                self.port_choice.Disable()
                obj.SetLabel(u"断开")
            except pyvisa.errors.VisaIOError:
                Utility.AlertError(u"连接失败")
        else:
            if self.instrumentation:
                self.instrumentation.disconnect()
                self.instrumentation = None
            self.port_choice.Enable()
            obj.SetLabel(u"连接")

    def __init_spin_ctrl(self, name, min_value, max_value, initial_value, unit):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(self, wx.ID_ANY, label=name, style=wx.TEXT_ALIGNMENT_CENTER)
        spin_ctrl = wx.SpinCtrl(self, wx.ID_ANY, size=(70, -1), style=wx.SP_ARROW_KEYS | wx.SP_BORDER, min=min_value,
                                max=max_value,
                                initial=initial_value)
        unit = wx.StaticText(self, wx.ID_ANY, label=u"(%s)" % unit, style=wx.TEXT_ALIGNMENT_CENTER)
        sizer.Add(title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        sizer.Add(spin_ctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        sizer.Add(unit, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        return sizer, spin_ctrl

    def __init_spin_sizer(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        interval_sizer, self.interval_spin = self.__init_spin_ctrl(name=u"取样间隔:", min_value=1, max_value=300,
                                                                   initial_value=1, unit=u"秒")
        v_calibration_sizer, self.v_calibration_spin = self.__init_spin_ctrl(name=u"电压校准", min_value=-1000,
                                                                             max_value=1000,
                                                                             initial_value=0, unit=u"mV")
        a_calibration_sizer, self.a_calibration_spin = self.__init_spin_ctrl(name=u"电流校准", min_value=-1000,
                                                                             max_value=1000,
                                                                             initial_value=0, unit=u"mA")
        sizer.Add(v_calibration_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        sizer.Add(wx.StaticLine(self, style=wx.LI_VERTICAL), 0, wx.EXPAND | wx.ALL, 7)
        sizer.Add(a_calibration_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        sizer.Add(wx.StaticLine(self, style=wx.LI_VERTICAL), 0, wx.EXPAND | wx.ALL, 7)
        sizer.Add(interval_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        self.start_button = wx.Button(self, wx.ID_ANY, u"开始", size=(50, -1))
        self.stop_button = wx.Button(self, wx.ID_ANY, u"停止", size=(50, -1))
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start)
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop)
        sizer.Add(self.start_button, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 1)
        sizer.Add(self.stop_button, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 1)
        return sizer

    def on_start(self, event):
        if self.instrumentation:
            interval = self.interval_spin.GetValue()
            v_cali = self.v_calibration_spin.GetValue()
            a_cali = self.a_calibration_spin.GetValue()
            self.data = ChargeData(interval=interval, instr=self.instrumentation, v_cali=v_cali, a_cali=a_cali)
            self.ampe.start(interval=interval, data=self.data)
            self.volt.start(interval=interval, data=self.data)
            self.EnableCtrl(enable=False)
        else:
            Utility.AlertError(u"请先连接设备")

    def on_stop(self, event):
        try:
            self.data.stop()
            self.ampe.stop()
            self.volt.stop()
            Utility.AlertMsg(u"已停止")
            self.EnableCtrl(enable=True)
        except AttributeError:
            pass

    def EnableCtrl(self, enable=True):
        disable = not enable
        self.start_button.Enable(enable)
        self.stop_button.Enable(disable)
        self.v_calibration_spin.Enable(enable)
        self.a_calibration_spin.Enable(enable)
        self.interval_spin.Enable(enable)

    def close(self):
        if self.instrumentation:
            self.instrumentation.disconnect()
