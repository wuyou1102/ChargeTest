# -*- encoding:UTF-8 -*-
import wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import matplotlib.pyplot as plt
import numpy
from libs import Utility

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class BaseMplPanel(wx.Panel):
    def __init__(self, parent, name, unit):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.title = name + unit
        self.name = name
        self.unit = unit
        self.data = None
        MplSizer = wx.BoxSizer(wx.VERTICAL)
        # 配置项『
        self.dpi = 100
        self.facecolor = '#FEF9E7'
        self.data_limit_length = 120
        self.min_tc = None
        self.max_tc = None
        # 配置项』
        self.x_limit_range = numpy.arange(self.data_limit_length)
        self.blank_array = numpy.array([])
        self.Figure = Figure((1.6, 0.9), self.dpi)
        self.Axes = self.Figure.add_axes([0.05, 0.02, 0.93, 0.96])
        self.FigureCanvas = FigureCanvasWxAgg(self, -1, self.Figure)
        MplSizer.Add(self.FigureCanvas, 1, wx.EXPAND | wx.ALL, 0)
        MainSizer.Add(MplSizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 1)
        self.SetSizer(MainSizer)
        self.Update()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.refresh, self.timer)

    def start(self, interval, data):
        self.data = data
        self.timer.Start(interval * 1000)

    def stop(self):
        self.timer.Stop()

    def __init_setting_sizer(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        y_set_sizer = self.__init_ybound_set_sizer()
        button_sizer = self.__init_button_sizer()
        sizer.Add(y_set_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        return sizer

    def __init_button_sizer(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_button = wx.Button(self, wx.ID_ANY, u"保存当前截图", wx.DefaultPosition, (80, -1), 0)
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
        sizer.Add(save_button, 0, wx.EXPAND | wx.ALL, 2)
        return sizer

    def init_ybound_set_sizer(self, parent):
        y_set_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(parent, wx.ID_ANY, u"%s范围: " % self.name, wx.DefaultPosition, wx.DefaultSize,
                              style=wx.TEXT_ALIGNMENT_CENTER)
        to = wx.StaticText(parent, wx.ID_ANY, u"～", wx.DefaultPosition, wx.DefaultSize,
                           style=wx.TEXT_ALIGNMENT_CENTER)
        unit_title = wx.StaticText(parent, wx.ID_ANY, self.unit, wx.DefaultPosition, wx.DefaultSize,
                                   style=wx.TEXT_ALIGNMENT_CENTER)
        self.min_tc = wx.TextCtrl(parent, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, (50, -1),
                                  wx.TE_RIGHT | wx.TE_PROCESS_ENTER)
        self.max_tc = wx.TextCtrl(parent, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, (50, -1),
                                  wx.TE_RIGHT | wx.TE_PROCESS_ENTER)

        self.max_tc.Bind(wx.EVT_TEXT_ENTER, self.update_ybound)
        self.min_tc.Bind(wx.EVT_TEXT_ENTER, self.update_ybound)
        y_set_sizer.Add(title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)
        y_set_sizer.Add(self.min_tc, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)
        y_set_sizer.Add(to, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)
        y_set_sizer.Add(self.max_tc, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)
        y_set_sizer.Add(unit_title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)
        return y_set_sizer

    def update_ybound(self, event):
        try:
            y_max = int(self.max_tc.GetValue())
            y_min = int(self.min_tc.GetValue())
            if y_max < y_min:
                y_min, y_max = y_max, y_min
            self.set_ybound(lower=y_min, upper=y_max)
            Utility.AlertMsg(u"设置成功")
        except ValueError:
            Utility.AlertError(u"输入异常: \"%s\" or \"%s\"" % (self.min_tc.GetValue(), self.max_tc.GetValue()))

    # def on_save(self, event):
    #     dlg = wx.FileDialog(
    #         self,
    #         message="Save plot as...",
    #         defaultDir=os.getcwd(),
    #         defaultFile="%s-%s.png" % (self.get_title(), Utility.get_timestamp()),
    #         wildcard="PNG (*.png)|*.png",
    #         style=wx.FD_SAVE)
    #
    #     if dlg.ShowModal() == wx.ID_OK:
    #         path = dlg.GetPath()
    #         self.FigureCanvas.print_figure(path, dpi=self.dpi)

    def get_title(self):
        return self.title

    def close_timer(self):
        self.timer.Stop()

    def refresh(self, event):
        raise NotImplementedError('MPL must have refresh function')

    def get_object(self):
        return self.obj

    def update(self):
        self.FigureCanvas.draw()

    def set_ybound(self, lower, upper):
        self.Axes.set_ybound(lower=lower, upper=upper)
        self.min_tc.SetValue(str(lower))
        self.max_tc.SetValue(str(upper))

    def init_axes(self, x_lower=0, x_upper=120):
        self.Axes.set_facecolor(self.facecolor)
        self.Axes.set_xbound(lower=x_lower, upper=x_upper)
        self.Axes.yaxis.grid(True)
        self.Axes.xaxis.grid(True)
        self.Axes.xaxis.set_visible(False)
        self.Axes.tick_params(labelsize=9, direction='in', grid_alpha=0.3)  # 设置坐标系文字大小
        # self.Axes.set_title(self.title, size=12)
        self.update()

    def refresh_line(self, line, data):
        if len(data) < self.data_limit_length:
            line.set_xdata(numpy.arange(len(data)))
            line.set_ydata(numpy.array(data))
        else:
            line.set_xdata(self.x_limit_range)
            line.set_ydata(numpy.array(data[-self.data_limit_length:]))
        self.update()


class AmpereMpl(BaseMplPanel):
    def __init__(self, parent):
        BaseMplPanel.__init__(self, parent, name=u"电流", unit=u"(mA)")
        self.__init_plot()
        self.init_axes()

    def refresh(self, event):
        self.refresh_line(self.line, self.data.get_ampere())

    def __init_plot(self):
        self.line, = self.Axes.plot(numpy.array([]), numpy.array([]), color="blue", linewidth=1, label=u'电流(mA)',
                                    linestyle='-')
        self.Axes.legend()


class VoltageMpl(BaseMplPanel):
    def __init__(self, parent):
        BaseMplPanel.__init__(self, parent, name=u"电压", unit=u"(mV)")
        self.__init_plot()
        self.init_axes()

    def refresh(self, event):
        self.refresh_line(self.line, self.data.get_voltage())

    def __init_plot(self):
        self.line, = self.Axes.plot(numpy.array([]), numpy.array([]), color="green", linewidth=1, label=u'电压(mV)',
                                    linestyle='-')
        self.Axes.legend()
