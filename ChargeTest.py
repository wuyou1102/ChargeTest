# -*- encoding:UTF-8 -*-
__author__ = 'wuyou'
import sys
import wx
from libs import UserInterface

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    app = wx.App()
    f = UserInterface()
    f.Show()
    app.MainLoop()
