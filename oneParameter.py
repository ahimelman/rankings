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

# set up database connection
client = MongoClient()

db = client.fbdb

scores = db.scores
rankings = db.rankings

# define functions to use as mle parameters
def f(x):
  return 1.5 / (1 + math.exp(-x))

def cosh(x):
	return (math.exp(x) - math.exp(-x)) / 2

def erf(x):
	return math.erf(x)

def d(x):
	return math.log(7 * math.exp(x) / ((math.exp(x) + 1) * (math.exp(x) + 1)))

# for years 2010-2013
for year in range(2010, 2013):
	
	# get all Teams, win counts data structures
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

	# for each week
	for week in range(8, 16):
		print week, year

		teamWeights = {}

		teamWeights = dict.fromkeys(allTeams)

		gamesPlayed = []

		# define mle function as parameter to optimization function
		def mle(x):
			product = 1
			for i in gamesPlayed:
				if (gameCounts[i[0]] > 3 and gameCounts[i[1]] > 3):
					product *= (f(x[i[0]] - x[i[1]]))
			return -1 * product

		# populate win counts, data stucture for mle product
		for s in scores.find({"year": year, "week" : { "$lt" : week}}):
				game = []
				if (int(s['teamVScore']) > int(s['teamHScore'])):
					game.append(allTeamsDict[s['teamV']])
					game.append(allTeamsDict[s['teamH']])
					winCounts[allTeamsDict[s['teamV']]] += 1
				else:
					game.append(allTeamsDict[s['teamH']])
					game.append(allTeamsDict[s['teamV']])
					winCounts[allTeamsDict[s['teamH']]] += 1

				gamesPlayed.append(game)


		# call optimize function
		npList = []
		for i in range(0, len(allTeams)):
			npList.append(30)

		x0 = np.array(npList)


		res = scipy.optimize.fmin_powell(mle, x0, xtol=1e-9, maxfun=100000000, maxiter=100000000)

		# enumerate over results
		for idx, item in enumerate(res):
			if (gameCounts[idx] > 5):
				teamWeights[allTeamsList[idx]] = item

		for idx, w in enumerate(sorted(teamWeights.items(), key=itemgetter(1), reverse=True)):
			print idx+1, w[0], teamWeights[w[0]]
		print


# do the same as above for year 2013
for year in range(2013, 2014):
	
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

	for week in range(9, 17):
		print week, year

		teamWeights = {}

		teamWeights = dict.fromkeys(allTeams)

		gamesPlayed = []

		def mle(x):
			product = 1
			for i in gamesPlayed:
				if (gameCounts[i[0]] > 3 and gameCounts[i[1]] > 3):
					product *= (f(x[i[0]] - x[i[1]]))
			return -1 * product

		for s in scores.find({"year": year, "week" : { "$lt" : week}}):
				game = []
				if (int(s['teamVScore']) > int(s['teamHScore'])):
					game.append(allTeamsDict[s['teamV']])
					game.append(allTeamsDict[s['teamH']])
					winCounts[allTeamsDict[s['teamV']]] += 1
				else:
					game.append(allTeamsDict[s['teamH']])
					game.append(allTeamsDict[s['teamV']])
					winCounts[allTeamsDict[s['teamH']]] += 1

				gamesPlayed.append(game)

		npList = []
		for i in range(0, len(allTeams)):
			npList.append(30)

		x0 = np.array(npList)

		res = scipy.optimize.fmin_powell(mle, x0, xtol=1e-9, maxfun=100000000, maxiter=100000000)

		for idx, item in enumerate(res):
			if (gameCounts[idx] > 5):
				teamWeights[allTeamsList[idx]] = item

		for idx, w in enumerate(sorted(teamWeights.items(), key=itemgetter(1), reverse=True)):
			print idx+1, w[0], teamWeights[w[0]]
		print

