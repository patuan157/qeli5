import wx
import events
from MainFrame import MainFrame

class CustomFrame(MainFrame):
    def __init__(self, parent):
        MainFrame.__init__(self, parent)
        self.saveBtn.Bind(wx.EVT_BUTTON, events.onSaveBtnClick)
        self.loadBtn.Bind(wx.EVT_BUTTON, events.onLoadBtnClick)
        self.removeBtn.Bind(wx.EVT_BUTTON, events.onRemoveBtnClick)
        self.submitBtn.Bind(wx.EVT_BUTTON, events.onSubmitBtnClick)
        self.vocalBtn.Bind(wx.EVT_BUTTON, events.onVocalBtnClick)
