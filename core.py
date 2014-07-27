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
			self.M[item.id] = np.identity(self.d)
			self.B[item.id] = np.zeros(self.d).astype(float)
			self.all_known_items.append(item.id)

	def transformFeatureVectorToCorrentShape(self, z):
		diff = self.d-len(z)
		if diff > 0:
			return np.concatenate((z,np.array([0]*diff)),axis=1).astype(float)
		return z

	def reward(self, item, user_context, reward):
		#print " = Rewarded " + str(reward) + " to " + str(item)
		user_context = self.transformFeatureVectorToCorrentShape(user_context)
		self.M[item.id] = self.M[item.id] + np.outer(user_context, user_context)
		self.B[item.id] = self.B[item.id] + np.multiply(reward, user_context)

	def get(self, items, user_context):
		max_ucb = [(-10000, None)] #value, id

		for item in items:
			if item.id not in self.all_known_items:
				self.M[item.id] = np.identity(self.d)
				self.B[item.id] = np.zeros(self.d).astype(float) 
				self.all_known_items.append(item.id)

			w = np.dot(np.linalg.inv(self.M[item.id]), self.B[item.id])
			ucb = np.dot(w, item.descriptor + user_context) + \
				self.alpha * math.sqrt(
					np.dot(
						np.dot(
							w,
							np.linalg.inv(self.M[item.id])
						),
						w
					)
				)


			if ucb > max_ucb[0][0]:
				max_ucb = [(ucb, item)]
			elif ucb == max_ucb[0][0]:
				max_ucb.append((ucb, item))

		return max_ucb[np.random.choice(len(max_ucb),1)][1]

		