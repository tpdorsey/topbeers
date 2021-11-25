from bs4 import BeautifulSoup
import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
}

base_url = 'http://beeradvocate.com'
top_url = base_url + '/lists/top/'

top_beers = []

session = requests.Session()
response = session.get(top_url, headers=headers)
page = BeautifulSoup(response.text, "html.parser")

table_rows = page.findAll('tr')
rows = table_rows[1:]

for row in rows:

  cells = row.findAll('td')
  a_tags = cells[1].findAll('a')

  beer = {}
  beer['rank'] = cells[0].text
  beer['name'] = a_tags[0].text
  beer['page'] = a_tags[0].get('href')
  beer['brewer_name'] = a_tags[1].text
  beer['brewer_page'] = a_tags[1].get('href')
  beer['brewer_id'] = beer['brewer_page'].split("/")[-2]
  beer['style'] = a_tags[2].text
  beer['ratings'] = cells[2].text
  beer['avg_rating'] = cells[3].text

  abv = cells[1].text.rsplit(" | ")
  if len(abv) > 1:
    beer['abv'] = abv[-1]
  else:
    beer['abv'] = ""
  
  burl = base_url + beer['brewer_page']
  brewer_page = session.get(burl, headers=headers)
  bpage = BeautifulSoup(brewer_page.text, 'html.parser')
  beer['brewer_state'] = bpage.findAll(id="info_box")[0].findAll('a')[1].text
  beer['brewer_avg_rating'] = bpage.findAll(id="stats_box")[0].findAll('dd')[0].text

  top_beers.append(beer)

print( "| Rank | Beer | Brewer | State | Style | ABV | AVG Rating | Ratings | Brewer AVG |")
print( "| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
for beer in top_beers:
  print( "| " + beer['rank'] + " | " + beer['name'] + " | " + beer['brewer_name'] + " | " + beer['brewer_state'] + " | " + beer['style'] + " | " + beer['abv'] + " | " + beer['avg_rating'] + " | " + beer['ratings'] + " | " + beer['brewer_avg_rating'] + " |")
