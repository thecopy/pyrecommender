import numpy as np
import math

class const:
	EXPLOIT = 1
	EXPLORE = 2

class logservice:
	def log(self, item, context):
		return 1
	def reward(self, id, reward):
		pass

class util:
	@staticmethod
	def normalize(items):
		mean = np.mean(items, axis=0)
		std =  np.std(items, axis=0)
		normalized = np.subtract(items, mean)
		normalized = np.divide(normalized, std)
		return np.nan_to_num(normalized)

	@staticmethod
	def transformFeatureVectorToCorrentShape(z, l):
		diff = l-len(z)
		if diff > 0:
			return np.concatenate((z,np.array([0]*diff)),axis=1).astype(float)
		return z

class item:
	id = None;
	name = None;
	descriptor = None;

	def __str__(self):
		return "ID:"+str(self.id)+" '"+self.name+"'"

	def __init__(self, id, descriptor, name = ""):
		self.id = id
		self.descriptor = descriptor
		self.name = name

class ucb:
	M = dict()
	B = dict()
	all_known_items = []
	d = 20
	alpha = 0.2

	def setItems(self, items):
		for item in items:
			self.M[item] = np.identity(self.d)
			self.B[item] = np.zeros(self.d).astype(float)
			self.all_known_items.append(item)

	def reward(self, item, user_context, reward):
		self.M[item] = self.M[item] + np.outer(user_context, user_context)
		self.B[item] = self.B[item] + np.multiply(reward, user_context)

	def get(self,user_context):
		max_ucb = [(-10000, None)] #value, id

		for itemid, descriptor in self.all_known_items:
			if item not in self.all_known_items:
				self.M[itemid] = np.identity(self.d)
				self.B[itemid] = np.zeros(self.d).astype(float) 
				self.all_known_items.append(itemid)

			w = np.dot(np.linalg.inv(self.M[itemid]), self.B[itemid])
			ucb = np.dot(w, descriptor + user_context) + \
				self.alpha * math.sqrt(
					np.dot(
						np.dot(
							w,
							np.linalg.inv(self.M[itemid])
						),
						w
					)
				)


			if ucb > max_ucb[0][0]:
				max_ucb = [(ucb, item)]
			elif ucb == max_ucb[0][0]:
				max_ucb.append((ucb, item))

		return max_ucb[np.random.choice(len(max_ucb),1)][1]

		