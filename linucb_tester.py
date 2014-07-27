from core import ucb, logservice, item, util
import numpy as np
import sys
import random
from time import sleep
import signal
import transformer
from memoryDB import memoryDB

def signal_handler(signal, frame):
		print('You pressed Ctrl+C!')
		sys.exit(1)

def run_test(logservice, trainer, cv = False):
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

		descriptor_raw = [1]
		descriptor_raw.extend(map(float, movie_info[5:]))

		descriptor = np.array(descriptor_raw).T
		items.append(item(id, descriptor, name))

	for line in user_data: # user id | age | gender | occupation | zip code
		user_info = line.split('|')
		userid = int(user_info[0])

		age = float(user_info[1])
		gender = 0
		if user_info[2] == 'M':
			gender = 1

		occupation = occupations.index(user_info[3])

		zip = user_info[4].strip()
		if zip not in zips:
			zips.append(zip)
		zip = zips.index(zip)

		user_descriptor = np.array([1,age,gender,occupation,zip])

		users.append(trainer.transformFeatureVectorToCorrentShape(user_descriptor))

	users = util.normalize(users)
	print users
	print len(users)
	for line in rating_data: # user id | item id | rating | timestamp. 
		userid, itemid, rating, timestamp = line.split('\t')
		user_ratings[str(userid) + "_" +  str(itemid)] = float(rating)
	
	rating_data.seek(0)
	print 'Running...'
	c = 0
	selected_items = dict()
	ratings = []

	for line in rating_data: # user id | item id | rating | timestamp. 
		userid, itemid, rating, timestamp = line.split('\t')
		ratings.append((userid, itemid, rating, timestamp))

	random.shuffle(ratings)
	total_rating = 0
	ratings_count = 0
	avg_ratings = []
	for userid, itemid, rating, timestamp in ratings:
		context = users[int(userid)-1]
		
		recommended_item = trainer.get(items, context)
		if recommended_item.id not in selected_items:
			selected_items[recommended_item.id] = 0
		selected_items[recommended_item.id] += 1
		#print 'Recommended ' + str(recommended_item) + ' to user ' + str(userid)

		key = str(userid) + "_" + str(recommended_item.id)
		if key in user_ratings:
			rated = user_ratings[key]
			total_rating += rated
			ratings_count += 1
			#print " = User " + str(userid) + " rated " + recommended_item.name + " " + str(rated)
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

signal.signal(signal.SIGINT, signal_handler)
run_test(logger, trainer)
