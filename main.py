import wx
from MainFrame import MainFrame

if __name__ == '__main__':
    app = wx.App()
    MainFrame(None).Show()
    app.MainLoop()
