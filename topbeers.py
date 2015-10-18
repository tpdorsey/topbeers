

from bs4 import BeautifulSoup
from urllib import urlopen
from urllib import FancyURLopener

class MyOpener(FancyURLopener):
  version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

myopener = MyOpener()

url = 'http://www.beeradvocate.com/lists/top/'

html = myopener.open(url)
soup = BeautifulSoup(html, 'html.parser')

rows = soup.findAll('tr')
beer_rows = rows[2:13]

top_beers = []
brewer_states = {}

for row in beer_rows:

  a_tags = row.findAll('td')[1].findAll('a')

  beer_name = a_tags[0].text
  beer_page = a_tags[0].get('href')
  brewer_name = a_tags[1].text
  brewer_page = a_tags[1].get('href')
  beer_style = a_tags[2].text

  weighted_rating = row.findAll('b')[1].text

  top_beers.append([beer_name, brewer_name, beer_style])


for beer in top_beers:
  print beer[0] + " | " + beer[1] + " | " + beer[2]
