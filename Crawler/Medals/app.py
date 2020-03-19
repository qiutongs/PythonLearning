"""
Based on Flask framework.
"""

from flask import Flask, render_template, redirect, url_for, request, g
import sqlite3

app = Flask(__name__)

app.database = "wiki.db"
app.table_name = "medals"

@app.route('/', methods=['GET', 'POST'])
def home():
	# 'g' is a temporary flask object, reset after each request
	g.db = connect_db()
	# Select all the rows
	cur = g.db.execute('select * from ' + app.table_name)
	# Transform to a list of dictionaris
	medals = [dict(rank=row[0], name=row[1], gold=row[2], silver=row[3], bronze=row[4], total=row[5]) for row in cur.fetchall()]
	
	g.db.close()

    # If this comes from the form submit
	if request.method == 'POST':
		# Get the sorted column and sort order
		sort_by = request.form['cols']
		if request.form['order'] == "asc":
			sort_order = False
		else:
			sort_order = True
	else:
		sort_by = "rank"
		sort_order = False

    # Do the real sort
	medals = sorted(medals, key=lambda d: d[sort_by], reverse=sort_order)

	return render_template("index.html", medals=medals)

# connect to database
def connect_db():
	return sqlite3.connect(app.database)

if __name__ == '__main__':
	app.run()