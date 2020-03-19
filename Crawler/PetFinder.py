"""
1. create SQLite database and table
2. web scraping 
3. insert data into table
"""

from bs4 import BeautifulSoup
import sqlite3
from requests_html import HTMLSession

import smtplib
from email.message import EmailMessage
from datetime import date

# Source URL
url = 'https://www.seattlehumane.org/pets/cats/'

database_name = "pets.db"
table_name = "cats"
table_schema = '(id INTEGER PRIMARY KEY, name TEXT, desp TEXT, link TEXT)'

# Create a new table; drop the old one if it exists
def create_database():
    with sqlite3.connect(database_name) as connection:
        cur = connection.cursor()
        # cur.execute("DROP TABLE IF EXISTS {}".format(table_name))
        cur.execute("CREATE TABLE IF NOT EXISTS {} {}".format(table_name, table_schema))
    print("Create database done!")

# Insert every row to the database, compliant to schema
def insert_data(data):
    with sqlite3.connect(database_name) as connection:
        cur = connection.cursor()
        for row in data:
            insert_statement = "INSERT INTO {} VALUES({},'{}','{}','{}')".format(table_name, row['id'], row['name'], row['desp'], row['link'])
            cur.execute(insert_statement)

    print("Insert data done!")

def web_scrape():

    # Create connection and get response
    session = HTMLSession()
    r = session.get(url)
    # Give enough time for rendering
    r.html.render(sleep=10)
    soup = BeautifulSoup(r.html.html, "html.parser")

    dataList=[]

    petsList = soup.find("div", {"class": "pets"})
    for pet in petsList.findChildren("div", recursive=False):
        dict={}
        try:
            desp= pet.find("div", {"class": "description"}).get_text()
            # Less than 1 year
            if "year" not in desp:
            	# Remove first 3 characters 'pet' and convert to integer
                dict['id'] = int(pet.get("id")[3:]) 
                dict['name'] = pet.find("h4", {"class": "name"}).find("a").get_text()
                dict['desp'] = desp
                dict['link'] = pet.find("h4", {"class": "name"}).find("a").get("href")
                dataList.append(dict)
        except:
            pass

    print("Web scraping done!")
    return dataList

def filter(data):
    db = sqlite3.connect(database_name)
    # Select all the rows
    cur = db.execute('select * from ' + table_name)
    # Transform to a list of dictionaris
    cats = [row[0] for row in cur.fetchall()]
    db.close()
    new_data = []
    # Find all the new cats
    for row in data:
    	if row['id'] not in cats:
    		new_data.append(row)
    return new_data

def email(data):
    if len(data) == 0:
        return
    msg = EmailMessage()
    msg['Subject'] = "Cats Update " + str(date.today())
    msg['From'] = "songqt02@hotmail.com"
    msg['To'] = "shiyd01@hotmail.com"

    message = ""
    for row in data:
    	message += row['name'] + ' ' + row['desp'] + ' ' + row['link'] + '\n'
    msg.set_content(message)
    
    s = smtplib.SMTP("smtp.live.com",587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('songqt02@hotmail.com', '')
    s.send_message(msg)
    s.quit()
    print("Email sent done!")
    

# Main workflow
create_database()
data = web_scrape()
new_data = filter(data)
print(new_data)
insert_data(data)
email(new_data)

'''
Ref: 
- https://requests-html.readthedocs.io/en/latest/
- https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python
- https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping
- https://stackoverflow.com/questions/13411486/send-email-via-hotmail-in-python
'''