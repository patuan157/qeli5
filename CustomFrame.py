import wx
import json
import psycopg2 as database

from constant import DB_NAME, USER, HOST, PASSWORD
from MainFrame import MainFrame

class CustomFrame(MainFrame):
	def __init__(self, parent):
		MainFrame.__init__(self, parent)
		self.connection = None
		self.start_db_connection()
		self.query = None
		self.load_saved_query()
		self.rootNode = None
		self.create_tree_view()

        # Binding Event to Button
		self.saveBtn.Bind(wx.EVT_BUTTON, self.onSave)
		self.loadBtn.Bind(wx.EVT_BUTTON, self.onLoad)
		self.removeBtn.Bind(wx.EVT_BUTTON, self.onRemove)
		self.submitBtn.Bind(wx.EVT_BUTTON, self.onSubmit)
		self.vocalBtn.Bind(wx.EVT_BUTTON, self.onVocalize)


	def start_db_connection(self):
		"""Create new connection instance to PostgreSQL local database."""
		try:
			self.connection = database.connect("dbname="+DB_NAME+" user="+USER+" host="+HOST+" password="+PASSWORD)
		except:
			print("Error connection to database")

	def load_saved_query(self):
		"""Load Saved Query to display in TreeView"""
		with open('query.json') as query_file:
			self.query = json.load(query_file)

	def create_tree_view(self):
		"""Show Tree View. Create a root node and every query as its children."""
		self.rootNode = self.saveBox.AddRoot(text="Saved Query", data=None)
		for key in self.query:
			self.saveBox.AppendItem(parent=self.rootNode, text=key, data=self.query[key])

	def onSubmit(self, event):
		"""onSubmit function when click button. Submit query to Database and get back the QUERY PLAN."""
		query = self.sqlBox.GetValue()				# Get The Query String submitted

		cur = self.connection.cursor()				# Open new cursor
		cur.execute("EXPLAIN ANALYZE " + query)		# EXPLAIN or EXPLAIN ANALYZE
		rows = cur.fetchall()						# rows contain result
		# print(rows)
		cur.close()									# Close cursor
		text_send_to_vocalizer = ""
		for row in rows:
			text_send_to_vocalizer += (row[0] + "\n")

		# self.natLangBox.SetStyle(0, self.natLangBox.get_size(), wx.TE_MULTILINE)		# Multiple Line Style Box
		self.natLangBox.SetValue(text_send_to_vocalizer)

	def onSave(self, event):
		"""onSave function when click button. Save new query with a prompt name to the Tree."""
		box = wx.TextEntryDialog(parent=None, message="Enter name of Query")
		box.ShowModal()
		name = box.Value
		if name == "":				# No Name is given or Cancel pressed
			return
		elif name in self.query:	# Name already used
			return				
		elif self.sqlBox.GetValue() == "":		# No query content
			return
		else:
			self.query[name] = self.sqlBox.GetValue()
			self.saveBox.AppendItem(parent=self.rootNode, text=name, data=self.sqlBox.GetValue())					

	def onLoad(self, event):
		"""onLoad function when click button. Load the chosen query to SQL Query Box."""
		selected_item = self.saveBox.GetSelection()
		if selected_item == None:				# Ignore if no item is selected
			return
		elif selected_item == self.rootNode:	# Ignore if this is the root node
			return
		else:									# Other item should have data
			self.sqlBox.SetValue(self.saveBox.GetItemData(selected_item))

	def onRemove(self, event):
		"""onRemove function when click button. Remove the chosen query from TreeView"""
		selected_item = self.saveBox.GetSelection()
		if selected_item == None:				# Ignore if no item is selected
			return
		elif selected_item == self.rootNode:	# Ignore if this is the root node
			return
		else:									# Other item should have data
			self.query.pop(self.saveBox.GetItemText(selected_item))
			self.saveBox.Delete(selected_item)

	def onVocalize(self, event):
		"""onVocalize function when click button. Vocalize the QUERY PLAN, show descriptive text and speak output."""
		print("Vocalize the Query")
		pass

	def __del__(self):
		self.connection.close()			# Close connection when complete the program
		with open('query.json', 'w') as query_file:
			json.dump(self.query, query_file)

