import numpy as np
import math

class const:
	EXPLOIT = 1
	EXPLORE = 2

class logservice:
	logList = dict()
	def __init__(self):
		self.logList = dict()
	def log(self, item, context):
		id = len(self.logList)
		self.logList[id] = (item, context)
		return id
	def get(self, id):
		return self.logList[id]

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

class aitem:
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
			id = item[0]
			context = item[1]
			self.M[id] = np.identity(self.d)
			self.B[id] = np.zeros(self.d).astype(float)
			self.all_known_items.append((id, context))

	def reward(self, item, user_context, reward):
		self.M[item] = self.M[item] + np.outer(user_context, user_context)
		self.B[item] = self.B[item] + np.multiply(reward, user_context)

	def get(self,user_context):
		max_ucb = [(-10000, None)] #value, id

		if len(self.all_known_items) == 0:
			print 'LinUCB: No items in self.all_known_items'
			return None

		for (itemid, descriptor) in self.all_known_items:

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
				max_ucb = [(ucb, itemid)]
			elif ucb == max_ucb[0][0]:
				max_ucb.append((ucb, itemid))

		result = max_ucb[np.random.choice(len(max_ucb),1)][1]
		print 'Result:', result
		return result

		