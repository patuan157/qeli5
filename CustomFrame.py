import wx
import os
import platform
import json
import psycopg2 as database
import re
from gtts import gTTS
from playsound import playsound

import settings
from MainFrame import MainFrame
from qplex import parse


class CustomFrame(MainFrame):
    DATA_LOAD_LIMIT = 5

    def __init__(self, parent):
        MainFrame.__init__(self, parent)
        self.connection = None
        self.start_db_connection()
        self.query = None
        self.load_saved_query()
        self.rootNode = None
        self.create_tree_view()
        self.dataCursor = None

        # Binding Event to Button
        self.saveBtn.Bind(wx.EVT_BUTTON, self.onSave)
        self.loadBtn.Bind(wx.EVT_BUTTON, self.onLoad)
        self.removeBtn.Bind(wx.EVT_BUTTON, self.onRemove)
        self.submitBtn.Bind(wx.EVT_BUTTON, self.onSubmit)
        self.sqlBox.Bind(wx.EVT_TEXT, self.onSqlChange)
        self.natLangBox.Bind(wx.EVT_TEXT, self.onNatLangChange)
        self.vocalBtn.Bind(wx.EVT_BUTTON, self.onVocalize)
        self.loadMoreDataBtn.Bind(wx.EVT_BUTTON, self.onLoadMoreData)
        self.saveBox.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onLoad)

    def start_db_connection(self):
        """Create new connection instance to PostgreSQL local database."""
        try:
            dbName = os.environ.get('DB_NAME')
            dbUser = os.environ.get('DB_USER')
            dbHost = os.environ.get('DB_HOST')
            dbPwd = os.environ.get('DB_PWD')
            dbConnectionString = "dbname={} user={} host={}".format(dbName, dbUser, dbHost) + \
                (" password={}".format(dbPwd) if dbPwd is not None else "")
            self.connection = database.connect(dbConnectionString)
        except Exception as err:
            print(err)

    def load_saved_query(self):
        """Load Saved Query to display in TreeView"""
        with open('query.json') as query_file:
            self.query = json.load(query_file)

    def create_tree_view(self):
        """Show Tree View. Create a root node and every query as its children."""
        self.rootNode = self.saveBox.AddRoot(text="Saved Query", data=None)
        for key in self.query:
            self.saveBox.AppendItem(
                parent=self.rootNode, text=key, data=self.query[key])
        self.saveBox.ExpandAll()
    
    def populateGrid(self, isAppendMode = False):
        # fetch data
        data = self.dataCursor.fetchmany(self.DATA_LOAD_LIMIT)
        if len(data) == 0:
            self.loadMoreDataBtn.Enable(False)
            return
        else:
            self.loadMoreDataBtn.Enable()
        colNames = [desc[0] for desc in self.dataCursor.description]

        # data dimensions
        rowDim = min(len(data), self.DATA_LOAD_LIMIT)
        colDim = len(data[0])

        # fix grid dimensions
        if not isAppendMode:
            if self.dataGrid.GetNumberRows() != 0:
                self.dataGrid.DeleteRows(numRows = self.dataGrid.GetNumberRows())
                self.dataGrid.DeleteCols(numCols = self.dataGrid.GetNumberCols())
            self.dataGrid.AppendCols(colDim)
        self.dataGrid.AppendRows(rowDim)

        # populate column labels
        if not isAppendMode:
            for i in range(len(colNames)):
                self.dataGrid.SetColLabelValue(i, colNames[i])

        # populate grid with data
        offset = rowDim if isAppendMode else 0
        for i in range(rowDim):
            for j in range(colDim):
                self.dataGrid.SetCellValue(i + offset, j, str(data[i][j]))
                self.dataGrid.SetReadOnly(i + offset, j)

    def onSqlChange(self, event):
        cond = len(self.sqlBox.GetValue()) > 0
        self.submitBtn.Enable(cond)
        self.saveBtn.Enable(cond)

    def onNatLangChange(self, event):
        cond = len(self.natLangBox.GetValue()) > 0
        self.vocalBtn.Enable(cond)

    def onSubmit(self, event):
        """onSubmit function when click button. Submit query to Database and get back the QUERY PLAN."""
        if self.dataGrid.GetNumberRows() != 0:
            self.dataGrid.DeleteRows(numRows = self.dataGrid.GetNumberRows())
            self.dataGrid.DeleteCols(numCols = self.dataGrid.GetNumberCols())
        query = self.sqlBox.GetValue()				# Get The Query String submitted

        cur = self.connection.cursor()				# Open new cursor
        cur.execute("EXPLAIN " + query)		# EXPLAIN or EXPLAIN ANALYZE
        rows = cur.fetchall()						# rows contain result
        cur.close()									# Close cursor
        query_plan = ' '.join(list(map(lambda x: x[0], rows)))  # convert list of tuples to list of string
        text_send_to_vocalizer = parse(query_plan)  # convert query plan to human-readable text

        # self.natLangBox.SetStyle(0, self.natLangBox.get_size(), wx.TE_MULTILINE)		# Multiple Line Style Box
        
        self.natLangBox.SetValue(text_send_to_vocalizer)
        		  
        #if self.dataCursor is not None and not self.dataCursor.closed:
        #    self.dataCursor.close()
        self.dataCursor = self.connection.cursor()
        self.dataCursor.execute(query)
        self.populateGrid()

        # cur = self.connection.cursor()
        # cur.execute(query + ' LIMIT 10')
        # results = cur.fetchall()
        # colNames = [desc[0] for desc in cur.description]
        # cur.close()
        # self.populateGrid(results, colNames)

    def onSave(self, event):
        """onSave function when click button. Save new query with a prompt name to the Tree."""
        box = wx.TextEntryDialog(parent=None, message="Enter name of Query")
        box.ShowModal()
        name = box.Value
        if name == "":				# No Name is given or Cancel pressed
            return
        elif name in self.query:  # Name already used
            return
        elif self.sqlBox.GetValue() == "":		# No query content
            return
        else:
            self.query[name] = self.sqlBox.GetValue()
            self.saveBox.AppendItem(
                parent=self.rootNode, text=name, data=self.sqlBox.GetValue())

    def onLoad(self, event):
        """onLoad function when click button. Load the chosen query to SQL Query Box."""
        selected_item = self.saveBox.GetSelection()
        if selected_item == None:				# Ignore if no item is selected
            return
        elif selected_item == self.rootNode:  # Ignore if this is the root node
            return
        else:									# Other item should have data
            self.sqlBox.SetValue(self.saveBox.GetItemData(selected_item))

    def onRemove(self, event):
        """onRemove function when click button. Remove the chosen query from TreeView"""
        selected_item = self.saveBox.GetSelection()
        if selected_item == None:				# Ignore if no item is selected
            return
        elif selected_item == self.rootNode:  # Ignore if this is the root node
            return
        else:									# Other item should have data
            self.query.pop(self.saveBox.GetItemText(selected_item))
            self.saveBox.Delete(selected_item)

    def onVocalize(self, event):
        """onVocalize function when click button. Vocalize the QUERY PLAN, show descriptive text and speak output."""
        print("Vocalize the Query")
        text_to_read = self.converFloatToReadableText(self.natLangBox.GetValue())
        tts = gTTS(text=text_to_read, lang='en')
        tts.save("output.mp3")
        playsound("output.mp3")

    def converFloatToReadableText(self, input_text):
        pattern = re.compile('[0-9]\d*')
        vocalized_text = input_text
        vocalized_text_list = list(vocalized_text)
        for i in range(len(vocalized_text_list)):
            if(vocalized_text_list[i] == '.' and i != len(vocalized_text_list)-1):
                if(pattern.match(str(vocalized_text_list[i-1])) != None and pattern.match(str(vocalized_text_list[i+1])) != None):
                    vocalized_text_list[i] = ' point '
        vocalized_text = ''.join(vocalized_text_list)
        return vocalized_text

    def onLoadMoreData(self, event):
        self.populateGrid(isAppendMode = True)

    def __del__(self):
        self.dataCursor.close() # DO NOT move it somewhere else
        self.connection.close()			# Close connection when complete the program
        with open('query.json', 'w') as query_file:
            json.dump(self.query, query_file)
