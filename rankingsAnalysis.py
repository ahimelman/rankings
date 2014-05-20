from __future__ import division
from pymongo import MongoClient

# set up database connection
client = MongoClient()
db = client.fbdb
scores = db.scores
rankings = db.rankings

count = 0
pollCounts = {}
totalCounts = {}
percent = {}
polls = ['bcs', 'harris', 'usa', 'avg', 'ah', 'rb', 'cm', 'km', 'js', 'pw', 'one_simple', 'two_simple']
for i in polls:
	pollCounts[i] = 0
	totalCounts[i] = 0
	percent[i] = 0
winner = ''

# iterate over all polls
for poll in polls:
	for s in scores.find():
		higher = ''
		lower = ''
		# week x's rankings predict scores from week x
		# week x's rankings are gathered from scores from week 1:(x-1)
		ra = rankings.find({"week": s['week'], "year": s['year'], 'js': {"$exists":True}, "$or": [{"team": s['teamV']}, {"team": s['teamH']}]})
		
		# determine winners, more highly ranked teams
		if ra.count() == 0:
			continue
		if ra.count() == 1:
			higher = ra[0]['team']
		elif ra.count() == 2:
			if not ra[0][poll].isdigit():
				higher = ra[1]['team']
			elif not ra[1][poll].isdigit():
				higher = ra[0]['team']
			elif int(ra[0][poll]) < int(ra[1][poll]):
				higher = ra[0]['team']
			else:
				higher = ra[1]['team']
		if (int(s['teamVScore']) > int(s['teamHScore'])):
			winner = s['teamV']
		else:
			winner = s['teamH']

		totalCounts[poll] += 1
		if winner != higher:
			pollCounts[poll] += 1

# print results
for i in pollCounts:
	percent[i] = pollCounts[i] / totalCounts[i]
print pollCounts
print totalCounts
print percent
