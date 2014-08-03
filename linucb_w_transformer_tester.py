from core import ucb, logservice, item, util
import numpy as np
import sys
import random
from time import sleep
import signal
import transformer
import memoryDB

class user:
	id = None
	age = 0
	gender = None
	occupation = None
	zip = None

	def __init__(self, id, age, gender, occupation, zip):
		self.id = id
		self.age = age
		self.gender = gender
		self.occupation = occupation
		self.zip = zip

	def getFeatures(self):
		feats = dict()
		feats['age'] = self.age
		feats['occupation'] = self.occupation
		feats['gender'] = self.gender
		feats['zip'] = self.zip
		return feats

class movie:
	id = None
	name = None
	release_date = None
	categories = None

	def __init__(self, id, name, release_date, categories):
		self.id = id
		self.name = name
		self.release_date = release_date
		self.categories = categories


	def getFeatures(self):
		feats = dict()
		for idx, cat in  enumerate(self.categories):
			feats[str(idx)] = cat
		return feats


def signal_handler(signal, frame):
		print('You pressed Ctrl+C!')
		sys.exit(1)

def run_test(logservice, trainer, transformer, cv = False):
	if cv:
		raise Exception('CV not implemented')

	path = 'testing/dataset/ml-100k/'
	rating_data = open(path + 'u1.base')
	user_data = open(path + 'u.user')
	occupation_data = open(path + 'u.occupation')
	all_items = open(path + 'u.item')

	users = []
	items = []
	user_ratings = dict()
	occupations = []
	zips = []
	for line in occupation_data:
		occupations.append(line.strip())

	for  line in all_items: 
		# movie id | movie title | release date | video release date |
		# IMDb URL | unknown | Action | Adventure | Animation |
		# Children's | Comedy | Crime | Documentary | Drama | Fantasy |
		# Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi |
		# Thriller | War | Western |
 
		movie_info = line.split('|')
		id = movie_info[0]
		name = movie_info[1]
		descriptor = [1]
		descriptor.extend(map(float, movie_info[5:]))

		items.append(movie(id, name, None, descriptor))

	print 'Setting items'
	trainer.setItems([(o.id, transformer.transform(o, 20)) for o in items])
	print 'Set items'
	for line in user_data: # user id | age | gender | occupation | zip code
		user_info = line.split('|')
		
		userid = int(user_info[0])
		age = int(user_info[1])
		gender = user_info[2]
		occupation = user_info[3]
		zip = user_info[4].strip()

		users.append(user(userid, age, gender, occupation, zip))

	ratings = []
	for line in rating_data: # user id | item id | rating | timestamp. 
		userid, itemid, rating, timestamp = line.split('\t')
		user_ratings[str(userid) + "_" +  str(itemid)] = float(rating)
		ratings.append((userid, itemid, rating, timestamp))

	print 'Running...'
	c = 0

	total_rating = 0
	ratings_count = 0
	avg_ratings = []
	for userid, itemid, rating, timestamp in ratings:
		if c % 2 == 0:
			c += 1
			continue

		context = transformer.transform(users[int(userid)-1], 20)
		recommended_item = trainer.get(context)		

		key = str(userid) + "_" + str(recommended_item.id)
		if key in user_ratings:
			rated = user_ratings[key]
			total_rating += rated
			ratings_count += 1
			if(rated > 3):
				rated = 1
			else:
				rated = -1

			trainer.reward(recommended_item, context, rated)

		c += 1
		total = 10000
		if( c > total):
			break
		if c % 100 == 0:
			print '\n\n ' + "Evaluated %d/%d lines." % (c, total)
			print "Avg. Recommended Rating = %f" % (float(total_rating) / ratings_count)
			avg_ratings.append(float(total_rating) / ratings_count)
	
	print ''
	print '\n\n ' + "Evaluated %d/%d lines." % (c, total)
	print "Avg. Recommended Rating = %f" % (float(total_rating) / ratings_count)
	avg_ratings.append(float(total_rating) / ratings_count)
	print avg_ratings

trainer = ucb()
logger = logservice()
db = memoryDB.memoryDB()
transformer = transformer.transformer(db)
signal.signal(signal.SIGINT, signal_handler)
run_test(logger, trainer,transformer)
