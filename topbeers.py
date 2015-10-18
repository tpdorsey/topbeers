

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
beer_rows = rows[2:]

top_beers = []
brewer_states = {}

for row in beer_rows:

  a_tags = row.findAll('td')[1].findAll('a')

  rank = row.findAll('td')[0].text
  beer_name = a_tags[0].text
  beer_page = a_tags[0].get('href')
  brewer_name = a_tags[1].text
  brewer_page = a_tags[1].get('href')
  beer_style = a_tags[2].text

  remove_string = rank + beer_name + brewer_name + beer_style

  raw_abv_wr = row.text.replace(remove_string,"")

  if " / " in raw_abv_wr:
    abv_wr = raw_abv_wr.replace(" / ","").split("% ABV")
  else:
    abv_wr = ["", raw_abv_wr]

  # print "| " + rank + " | " + beer_name + " | " + brewer_name + " | " + beer_style + " | " + abv_wr[0] + " | " + abv_wr[1] + " |"

  top_beers.append([rank, beer_name, brewer_name, beer_style, abv_wr[0], abv_wr[1]])

print "| Rank | Beer | Brewer | Style | ABV | WR |"
print "| --- | --- | --- | --- | --- | --- |"

for beer in top_beers:
  print "| " + beer[0] + " | " + beer[1] + " | " + beer[2] + " | " + beer[3] + " | " + beer[4] + " | " + beer[5] + " |"
