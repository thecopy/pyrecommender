import transformer
import memoryDB

class naiveClass:
	param1 = 0
	param2 = 0
	param3 = "Male"
	param4 = 90210
	def __init__(self, param1, param2, param3):
		self.param1 = param1
		self.param2 = param2
		self.param3 = param3
		self.param4 = 90210

class improvedClass:
	param1 = 0
	param2 = 0
	param3 = ""
	param4 = 0
	def __init__(self, param1, param2, param3):
		self.param1 = param1
		self.param2 = param2
		self.param3 = param3
		self.param4 = 90210

	def getFeatures(self):
		male = 0
		if self.param3 == "Male":
			male = 1

		feats = dict()
		feats['param1'] = self.param1
		feats['param2'] = self.param2
		feats['param3'] = male
		feats['param4'] = self.param4
		return feats


class smartestClass:
	param1 = 0
	param2 = 0
	param3 = ""
	param4 = 0
	def __init__(self, param1, param2, param3):
		self.param1 = param1
		self.param2 = param2
		self.param3 = param3
		self.param4 = 90210

	def getFeatures(self):
		feats = dict()
		feats['param1'] = self.param1
		feats['param2'] = self.param2
		feats['param3'] = self.param3
		feats['param4'] = str(self.param4)
		return feats


c = transformer.transform(naiveClass(1,2,"Male"), None)
print "Naive Class = \t\t" + str(c)


c = transformer.transform(improvedClass(1,2,"Male"), None)
print "Improved Class = \t" + str(c)


db = memoryDB.memoryDB()
c = transformer.transform(smartestClass(1,2,"Male"), db)
print "Smart Class = \t\t" + str(c)