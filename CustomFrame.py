import wx
import events
import psycopg2
from constant import *
from MainFrame import MainFrame

class CustomFrame(MainFrame):
	def __init__(self, parent):
		MainFrame.__init__(self, parent)

        # Binding Event to Button
		self.saveBtn.Bind(wx.EVT_BUTTON, events.onSaveBtnClick)
		self.loadBtn.Bind(wx.EVT_BUTTON, events.onLoadBtnClick)
		self.removeBtn.Bind(wx.EVT_BUTTON, events.onRemoveBtnClick)
		self.submitBtn.Bind(wx.EVT_BUTTON, self.onSubmit)
		self.vocalBtn.Bind(wx.EVT_BUTTON, events.onVocalBtnClick)

		# Init Connection to Postgresql Database
		try:
			self.conn = psycopg2.connect("dbname="+DB_NAME+" user="+USER+" host="+HOST+" password="+PASSWORD)
		except:
			print("Error connection to database")

	def onSubmit(self, event):
		query = self.sqlBox.GetValue()				# Get The Query String submitted
		text_send_to_vocalizer = events.onSubmitBtnClick(self.conn, query)
		# self.natLangBox.SetStyle(0, self.natLangBox.get_size(), wx.TE_MULTILINE)		# Multiple Line
		self.natLangBox.SetValue(text_send_to_vocalizer)

	def __del__(self):
		self.conn.close()			# Close connection when complete the program
		pass

