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
	def __init__(self, param1, param2, param3, param4):
		self.param1 = param1
		self.param2 = param2
		self.param3 = param3
		self.param4 = param4

	def getFeatures(self):
		feats = dict()
		feats['param1'] = self.param1
		feats['param2'] = self.param2
		feats['param3'] = self.param3
		feats['param4'] = str(self.param4)
		return feats


t = transformer.transformer(None)
c = t.transform(naiveClass(1,2,"Male"))
print "Naive Class = \t\t" + str(c)

db = memoryDB.memoryDB()
t = transformer.transformer(db)
c = t.transform(smartestClass(2.,2.,"Male",2))
c = t.transform(smartestClass(2.,2.,"Female",3))
c = t.transform(smartestClass(1.,1.,"Female",3))
print "Smart Class = \t\t" + str(c)