import psycopg2
from constant import DB_NAME, USER, HOST, PASSWORD

def onSaveBtnClick(event):
    print('Save btn clicked.')

def onLoadBtnClick(event):
    print('Load btn clicked.')

def onRemoveBtnClick(event):
    print('Remove btn clicked.')
    
def onSubmitBtnClick(conn, query):
	cur = conn.cursor()					# Open new cursor
	cur.execute("EXPLAIN ANALYZE " + query)		# EXPLAIN or EXPLAIN ANALYZE
	rows = cur.fetchall()
	# print(rows)
	cur.close()							# Close cursor when complete query
	# Write to output
	output = ""
	for row in rows:
		output += row[0] + "\n"
	print(output)
	return output

def onVocalBtnClick(event):
    print('Vocal btn clicked.')