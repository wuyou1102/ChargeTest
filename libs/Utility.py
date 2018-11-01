# -*- encoding:UTF-8 -*-
import wx


def AlertError(msg):
    dialog = wx.MessageDialog(None, msg, u"错误", wx.OK | wx.ICON_ERROR)
    dialog.ShowModal()
    dialog.Destroy()


def AlertMsg(msg):
    dialog = wx.MessageDialog(None, msg, u"消息", wx.OK | wx.ICON_INFORMATION)
    dialog.ShowModal()
    dialog.Destroy()

