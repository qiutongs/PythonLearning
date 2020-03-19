"""
- create SQLite database and table
- web scraping 
- insert data into table
"""

from bs4 import BeautifulSoup
import urllib.request
import sqlite3
import matplotlib.pyplot as plt

# Source URL
url = 'https://en.wikipedia.org/wiki/2018_Winter_Olympics_medal_table'

database_name = "wiki.db"
table_name = "medals"
table_schema = '(rank INTEGER, name TEXT, gold INTEGER, silver INTEGER, bronze INTEGER, total INTEGER)'

# Create a new table; drop the old one if it exists
def create_database():
    with sqlite3.connect(database_name) as connection:
        cur = connection.cursor()
        cur.execute("DROP TABLE IF EXISTS {}".format(table_name))
        cur.execute("CREATE TABLE {} {}".format(table_name, table_schema))
    print("Create database done!")

# Insert every row to the database, compliant to schema
def insert_data(data):
    with sqlite3.connect(database_name) as connection:
        cur = connection.cursor()
        for row in data:
            insert_statement = "INSERT INTO {} VALUES({},'{}',{},{},{},{})".format(table_name, row['Rank'], row['Country'], row['Gold'], row['Silver'], row['Bronze'], row['Total'])
            cur.execute(insert_statement)

    print("Insert data done!")

# Fetch all the medals data and return a list of dictionaries
def web_scrape():

    # Create connection and get response
    client_connection = urllib.request.urlopen(url)
    html_text = client_connection.read()
    client_connection.close()

    # Parse the html
    soup = BeautifulSoup(html_text, "html.parser")

    # Traverse information needed
    dataList=[]
    TempRank=1
    for trs in soup.find_all('tr'):
        dict={}
        tds = trs.find_all('td')
        try:
            totalmedal = tds[-1].get_text()
            totalmedal = totalmedal.encode('ascii','ignore')
            if int(totalmedal) >= 1 and int(totalmedal) <= 100 and totalmedal.isdigit():
                Cname = trs.find_all('a')[0].get_text().encode('ascii','ignore')
                
                dict['Country'] = trs.find_all('a')[0].get_text()
                dict['Gold'] = tds[-4].get_text()
                dict['Silver'] = tds[-3].get_text()
                dict['Bronze'] = tds[-2].get_text()
                dict['Total'] = tds[-1].get_text()
                
                try:
                    TempRank = int(tds[-5].get_text())
                except:
                    pass
                
                dict['Rank'] = TempRank
                dataList.append(dict)
        except:
            pass

    print("Web scraping done!")
    return dataList

# Generate an image of the scrapped data
def visualize(dataList):
    country_list = [a['Country'] for a in dataList[0:10]]
    gold_count = [a['Gold'] for a in dataList[0:10]]
    silver_count = [a['Silver'] for a in dataList[0:10]]
    bronze_count = [a['Bronze'] for a in dataList[0:10]]

    fig, ax1 = plt.subplots()
    ax1.plot(country_list, gold_count, color='gold', linewidth='2.5')
    ax1.plot(country_list, silver_count, color='silver',linewidth='2.5')
    ax1.plot(country_list, bronze_count, color='brown',linewidth='2.5')
    plt.gca().invert_yaxis()
    plt.xticks(rotation=50)
    plt.legend(('Gold', 'Silver', 'Bronze'))
    plt.gcf().subplots_adjust(bottom=0.3)
    plt.savefig('./static/Winter2018.png')
    print("Image generation done!")

# Main workflow

create_database()
data = web_scrape()
insert_data(data)
visualize(data)

