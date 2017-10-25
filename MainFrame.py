# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"PostgreSQL Query Plan Vocalizer", pos = wx.DefaultPosition, size = wx.Size( 1282,789 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Saved Queries", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Segoe UI" ) )
		
		bSizer10.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.m_treeCtrl4 = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 245,675 ), wx.TR_DEFAULT_STYLE )
		bSizer10.Add( self.m_treeCtrl4, 0, wx.ALL, 5 )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button12 = wx.Button( self, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		bSizer14.Add( self.m_button12, 0, wx.ALL, 5 )
		
		self.m_button13 = wx.Button( self, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		bSizer14.Add( self.m_button13, 0, wx.ALL, 5 )
		
		self.m_button14 = wx.Button( self, wx.ID_ANY, u"Remove", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		bSizer14.Add( self.m_button14, 0, wx.ALL, 5 )
		
		
		bSizer10.Add( bSizer14, 1, wx.EXPAND, 5 )
		
		
		bSizer9.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"SQL", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		self.m_staticText3.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Segoe UI" ) )
		
		bSizer16.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		self.m_textCtrl12 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,200 ), 0 )
		bSizer16.Add( self.m_textCtrl12, 0, wx.ALL, 5 )
		
		self.m_button17 = wx.Button( self, wx.ID_ANY, u"Submit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.m_button17, 0, wx.ALL, 5 )
		
		
		bSizer15.Add( bSizer16, 1, wx.EXPAND, 5 )
		
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Natural Language", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		self.m_staticText4.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Segoe UI" ) )
		
		bSizer18.Add( self.m_staticText4, 0, wx.ALL, 5 )
		
		self.m_textCtrl13 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,200 ), 0 )
		self.m_textCtrl13.Enable( False )
		
		bSizer18.Add( self.m_textCtrl13, 0, wx.ALL, 5 )
		
		
		bSizer15.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		
		bSizer12.Add( bSizer15, 1, wx.EXPAND, 5 )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Result", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_staticText5.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Segoe UI" ) )
		
		bSizer12.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.m_grid4 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 1010,440 ), 0 )
		
		# Grid
		self.m_grid4.CreateGrid( 5, 5 )
		self.m_grid4.EnableEditing( True )
		self.m_grid4.EnableGridLines( True )
		self.m_grid4.EnableDragGridSize( False )
		self.m_grid4.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid4.EnableDragColMove( False )
		self.m_grid4.EnableDragColSize( True )
		self.m_grid4.SetColLabelSize( 30 )
		self.m_grid4.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid4.EnableDragRowSize( True )
		self.m_grid4.SetRowLabelSize( 80 )
		self.m_grid4.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid4.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer12.Add( self.m_grid4, 0, wx.ALL, 5 )
		
		
		bSizer9.Add( bSizer12, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer9 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

