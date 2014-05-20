from __future__ import division
import math
import numpy as np
from scipy.optimize import minimize, fmin
from pymongo import MongoClient
from ordereddict import OrderedDict
from operator import itemgetter
from decimal import *
import random
import scipy
import scipy.stats

# set up database connections
client = MongoClient()
db = client.fbdb
scores = db.scores
rankings = db.rankings

MEAN = 24;

resultX = []
resultY = []

# input parameter to optimization function
def f(x):
	return x

def do_calcs(year1, year2, week1, week2):

	# for all years
	for year in range(year1, year2):
		allTeams = set()
		gameCounts = {}
		winCounts = {}

		for s in scores.find({"year": year}):
			allTeams.add(s['teamV'])
			allTeams.add(s['teamH'])

		allTeamsList = list(allTeams)

		allTeamsDict = {}
		for idx, item in enumerate(allTeamsList):
			allTeamsDict[item] = idx
			winCounts[idx] = 0
			gameCounts[idx] = 0

		for s in scores.find({"year" : year}):
			gameCounts[allTeamsDict[s['teamV']]] += 1
			gameCounts[allTeamsDict[s['teamH']]] += 1

		for week in range(week1, week2):
			print week, year

			teamWeights = {}

			teamWeights = dict.fromkeys(allTeams)

			gamesPlayed = []

			# define error function, using both parameters
			def mle(x):
				error = 0
				for i in gamesPlayed:
						a = (i[2] - f(x[i[0]*2] - x[i[1]*2 + 1])) # winning offense - losing defense
						b = (i[3] - f(x[i[1]*2] - x[i[0]*2 + 1])) # losing offense - winning defense
						error += a * a
						error += b * b
				return error

			for s in scores.find({"year": year, "week" : { "$lt" : week}}):
				game = []
				if (int(s['teamVScore']) > int(s['teamHScore'])):
					game.append(allTeamsDict[s['teamV']])
					game.append(allTeamsDict[s['teamH']])
					game.append(int(s['teamVScore']))
					game.append(int(s['teamHScore']))
					winCounts[allTeamsDict[s['teamV']]] += 1
				else:
					game.append(allTeamsDict[s['teamH']])
					game.append(allTeamsDict[s['teamV']])
					game.append(int(s['teamHScore']))
					game.append(int(s['teamVScore']))
					winCounts[allTeamsDict[s['teamH']]] += 1

				gamesPlayed.append(game)

			npList = []

			# initial guess
			for i in range(0, len(allTeams)*2):
				npList.append(30)

			x0 = np.array(npList)
			y0 = np.array(npList)

			# solve optimization
			res = scipy.optimize.fmin_powell(mle, x0, xtol=1e-9, maxfun=100000000, maxiter=100000000)
			resCombined = []

			# get combined results
			for i in range(0, len(allTeams)):
				resCombined.append(math.sqrt(res[2*i] * res[2*i] + res[2*i+1] * res[2*i+1]))
			
			# print results
			for idx, item in enumerate(resCombined):
				if (gameCounts[idx] > 5):
					teamWeights[allTeamsList[idx]] = item

			for idx, w in enumerate(sorted(teamWeights.items(), key=itemgetter(1), reverse=True)):
				print idx+1, w[0], teamWeights[w[0]]
			print

if __name__ == "__main__":
	do_calcs(2010, 2013, 8, 16)
	do_calcs(2013, 2014, 9, 17)


