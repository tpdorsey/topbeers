

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
brewer_state = {}
brewer_avg = {}

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

  if brewer_name in brewer_state:
    state = brewer_state[brewer_name]
    avg = brewer_avg[brewer_name]

  else:
    burl = "http://www.beeradvocate.com" + brewer_page
    brewer_page = myopener.open(burl)
    bsoup = BeautifulSoup(brewer_page, 'html.parser')

    state = bsoup.findAll(property="og:title")[0]["content"].split(" | ")[1].split(", ")[1]

    avg = bsoup.findAll(class_="BAscore_big ba-score")[0].text

    brewer_state[brewer_name] = state
    brewer_avg[brewer_name] = avg


  top_beers.append([rank, beer_name, brewer_name, state, beer_style, abv_wr[0], abv_wr[1], avg])

print "| Rank | Beer | Brewer | State | Style | ABV | WR | Brewer AVG |"
print "| --- | --- | --- | --- | --- | --- | --- | --- |"

for beer in top_beers:
  print "| " + beer[0] + " | " + beer[1] + " | " + beer[2] + " | " + beer[3] + " | " + beer[4] + " | " + beer[5] + " | " + beer[7] + " | " + beer[6] + " |"
