# -*- coding: utf-8 -*-

###########################################################################
# Python code generated with wxFormBuilder (version Dec 21 2016)
# http://www.wxformbuilder.org/
##
# PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
# Class MainFrame
###########################################################################


class MainFrame (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"PostgreSQL Query Plan Vocalizer",
                          pos=wx.DefaultPosition, size=wx.Size(1199, 739), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer9 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText2 = wx.StaticText(
            self, wx.ID_ANY, u"Saved Queries", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        self.m_staticText2.SetFont(wx.Font(
            9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Segoe UI"))

        bSizer10.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.saveBox = wx.TreeCtrl(
            self, wx.ID_ANY, wx.DefaultPosition, wx.Size(245, 620), wx.TR_DEFAULT_STYLE)
        bSizer10.Add(self.saveBox, 0, wx.ALL, 5)

        bSizer14 = wx.BoxSizer(wx.HORIZONTAL)

        self.saveBtn = wx.Button(
            self, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.Size(75, -1), 0)
        bSizer14.Add(self.saveBtn, 0, wx.ALL, 5)

        self.loadBtn = wx.Button(
            self, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.Size(75, -1), 0)
        bSizer14.Add(self.loadBtn, 0, wx.ALL, 5)

        self.removeBtn = wx.Button(
            self, wx.ID_ANY, u"Remove", wx.DefaultPosition, wx.Size(75, -1), 0)
        bSizer14.Add(self.removeBtn, 0, wx.ALL, 5)

        bSizer10.Add(bSizer14, 1, wx.EXPAND, 5)

        bSizer9.Add(bSizer10, 1, wx.EXPAND, 5)

        bSizer12 = wx.BoxSizer(wx.VERTICAL)

        bSizer15 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer16 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText3 = wx.StaticText(
            self, wx.ID_ANY, u"SQL", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        self.m_staticText3.SetFont(wx.Font(
            9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Segoe UI"))

        bSizer16.Add(self.m_staticText3, 0, wx.ALL, 5)

        self.sqlBox = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(500, 200), 0)
        bSizer16.Add(self.sqlBox, 0, wx.ALL, 5)

        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        self.submitBtn = wx.Button(
            self, wx.ID_ANY, u"Submit", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.submitBtn, 0, wx.ALL, 5)

        self.progressBar = wx.Gauge(
            self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size(-1, 25), wx.GA_HORIZONTAL)
        self.progressBar.SetValue(0)
        bSizer8.Add(self.progressBar, 0, wx.ALL, 5)

        bSizer16.Add(bSizer8, 1, wx.EXPAND, 5)

        bSizer15.Add(bSizer16, 1, wx.EXPAND, 5)

        bSizer18 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText4 = wx.StaticText(
            self, wx.ID_ANY, u"Natural Language", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        self.m_staticText4.SetFont(wx.Font(
            9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Segoe UI"))

        bSizer18.Add(self.m_staticText4, 0, wx.ALL, 5)

        self.natLangBox = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(500, 200), 0)
        self.natLangBox.Enable(False)

        bSizer18.Add(self.natLangBox, 0, wx.ALL, 5)

        bSizer15.Add(bSizer18, 1, wx.EXPAND, 5)

        bSizer12.Add(bSizer15, 1, wx.EXPAND, 5)

        self.m_staticText5 = wx.StaticText(
            self, wx.ID_ANY, u"Result", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        self.m_staticText5.SetFont(wx.Font(
            9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Segoe UI"))

        bSizer12.Add(self.m_staticText5, 0, wx.ALL, 5)

        self.dataGrid = wx.grid.Grid(
            self, wx.ID_ANY, wx.DefaultPosition, wx.Size(1010, 440), 0)

        # Grid
        self.dataGrid.CreateGrid(5, 5)
        self.dataGrid.EnableEditing(True)
        self.dataGrid.EnableGridLines(True)
        self.dataGrid.EnableDragGridSize(False)
        self.dataGrid.SetMargins(0, 0)

        # Columns
        self.dataGrid.EnableDragColMove(False)
        self.dataGrid.EnableDragColSize(True)
        self.dataGrid.SetColLabelSize(30)
        self.dataGrid.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.dataGrid.EnableDragRowSize(True)
        self.dataGrid.SetRowLabelSize(80)
        self.dataGrid.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.dataGrid.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        bSizer12.Add(self.dataGrid, 0, wx.ALL, 5)

        bSizer9.Add(bSizer12, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer9)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass
