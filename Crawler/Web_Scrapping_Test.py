
import urllib.request
from bs4 import BeautifulSoup

# Set URL
url = 'http://web.mta.info/developers/turnstile.html'

# Get Response
client = urllib.request.urlopen(url)
html = client.read()
client.close()

# Parse the html
soup = BeautifulSoup(html, "html.parser")

# Locate one "a" tag 
one_a_tag = soup.findAll('a')[36]

# Get the href
link = one_a_tag['href']

print(link)

#download_url = 'http://web.mta.info/developers/'+ link

#urllib.urlretrieve(download_url,'./'+link[link.find('/turnstile_')+1:]) 
#urllib.request.urlretrieve(download_url,'somefile') 

#print("Download finishes.")