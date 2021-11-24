from bs4 import BeautifulSoup
import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
}

base_url = 'http://beeradvocate.com'

url = base_url + '/lists/top/'

session = requests.Session()
response = session.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

rows = soup.findAll('tr')
beer_rows = rows[2:]

top_beers = []

# To Do: persist this data to a file to reduce web page calls on subsequent runs
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
    burl = base_url + brewer_page
    brewer_page = session.get(burl, headers=headers)
    bsoup = BeautifulSoup(brewer_page.text, 'html.parser')

    state = bsoup.findAll(property="og:title")[0]["content"].split(" | ")[1].split(", ")[1]

    # avg = bsoup.findAll(class_="ba-score")[0].text
    avg_score = bsoup.findAll(class_="ba-score")
    if len(avg_score) > 0:
      avg = avg_score[0].text
    else:
      avg = ""

    brewer_state[brewer_name] = state
    brewer_avg[brewer_name] = avg


  top_beers.append([rank, beer_name, brewer_name, state, beer_style, abv_wr[0], abv_wr[1], avg])

print( "| Rank | Beer | Brewer | State | Style | ABV | WR | Brewer AVG |")
print( "| --- | --- | --- | --- | --- | --- | --- | --- |")
for beer in top_beers:
  print( "| " + beer[0] + " | " + beer[1] + " | " + beer[2] + " | " + beer[3] + " | " + beer[4] + " | " + beer[5] + " | " + beer[7] + " | " + beer[6] + " |")
