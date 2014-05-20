from pymongo import MongoClient

# register database connections
client = MongoClient()
db = client.fbdb
collection = db.test_collection
scores = db.scores

from bs4 import BeautifulSoup
import requests

# web scrape score data
def populateScores():

	r = requests.get("http://scores.espn.go.com/ncf/scoreboard?confId=80&seasonYear="+ str(year) + "&seasonType=3&weekNumber=" + str(week))
	data = r.text

	soup = BeautifulSoup(data)

	teamV = ''
	teamH = ''
	teamVScore = ''
	teamHScore = ''
	teamVPrev = ''

	for link in soup.find_all("div", {"class": "mod-content"}):
		for i in link.find_all("div", {"class": "team visitor"}):
			try:
				teamV = i.find("a")["title"]
			except KeyError:
				teamV = 'keyError'
			for j in i.find_all("li", {"class": "final"}):
				teamVScore = j.getText()

		for i in link.find_all("div", {"class": "team home"}):
			try:
				teamH = i.find("a")["title"]
			except KeyError:
				teamH = 'keyError'
			for j in i.find_all("li", {"class": "final"}):
				teamHScore = j.getText()
		if teamVPrev == teamV:
			continue
		
		post = {}
		post['teamV'] = teamV
		teamVPrev = teamV
		post['teamVScore'] = teamVScore
		post['teamH'] = teamH
		post['teamHScore'] = teamHScore
		post['week'] = 'final'
		post['year'] = year
		# print teamV, teamVScore, teamH, teamHScore
		print post
		post_id = scores.insert(post)

for year in range(2013, 2014):
	for week in range(16,17):
		populateScores()


rankings = db.rankings

# webscrape ranking data
for year in range(2010,2013):
	for week in range(15,16):
		r = requests.get("http://espn.go.com/college-football/bcs/_/week/" + str(week) + "/year/" + str(year))
		soup = BeautifulSoup(r.text)

		team = ''
		bcs = ''
		harris = ''
		usa = ''
		avg = ''
		ah = ''
		rb = ''
		cm = ''
		km = ''
		js = ''
		pw = ''

		for link in soup.find_all("tr"):
			td = link.find_all("td")
			bcs = td[0].getText()
			if not bcs.isdigit():
				continue
			team = td[1].getText()
			harris = td[4].getText()
			usa = td[7].getText()
			avg = td[10].getText()
			ah = td[11].getText()
			rb = td[12].getText()
			cm = td[13].getText()
			km = td[14].getText()
			js = td[15].getText()
			pw = td[16].getText()

			post = {}

			post['bcs'] = bcs 
			post['team'] = team 
			post['harris'] = harris 
			post['usa'] = usa 
			post['avg'] = avg 
			post['ah'] = ah
			post['rb'] = rb 
			post['cm'] = cm
			post['km'] = km
			post['js'] = js 
			post['pw'] = pw
			post['year'] = year
			post['week'] = week

			print post
			post_id = rankings.insert(post)





