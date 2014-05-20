from __future__ import division
from pymongo import MongoClient

client = MongoClient()

db = client.fbdb

scores = db.scores
rankings = db.rankings


def top(week, year):
   team = [i['team'] for i in  rankings.find({"osn": {"$lt":51}, "week": week, "year": year})]
   rank = [i['tsn'] for i in  rankings.find({"osn": {"$lt":51}, "week": week, "year": year})]

   print "week:", week, "year:", year
   for idx, value in enumerate(zip(*sorted(zip(rank,team)))[1]):
      print idx + 1, value

for year in range(2010, 2013):
   for week in range(8, 16):
      top(week, year)

for year in range(2013, 2014):
   for week in range(9, 17):
      top(week, year)