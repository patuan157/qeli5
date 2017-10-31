import wx
import events
from CustomFrame import CustomFrame

if __name__ == '__main__':
    app = wx.App()
    CustomFrame(None).Show()
    app.MainLoop()
