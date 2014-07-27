import numpy as np

def getS(obj,db,len):
	s0 = db.get(obj.__class__.__name__ + "?s0")
	s1 = db.get(obj.__class__.__name__ + "?s1")
	s2 = db.get(obj.__class__.__name__ + "?s2")
	if s0 is None:
		s0 = [0.]*len
		s1 = [0.]*len
		s2 = [0.]*len

	return s0,s1,s2
def setS(obj, db, s0,s1,s2):
	db.set(obj.__class__.__name__ + "?s0",s0)
	db.set(obj.__class__.__name__ + "?s1",s1)
	db.set(obj.__class__.__name__ + "?s2",s2)

def transform(obj,db):

	ret = []
	if hasattr(obj, "getFeatures"):
		feats = obj.getFeatures()

		for key, val in feats.iteritems():
			if isinstance( val, str ):
				dbKey = obj.__class__.__name__ + ":" + key
				listOfThisType = db.get(dbKey)
				if listOfThisType is None:
					listOfThisType = []

				listOfThisType.append(val)
				db.set(dbKey, listOfThisType)
				feats[key] = listOfThisType.index(val)+1

		ret = feats.values()
	else:
		for k in obj.__dict__:
			var = obj.__dict__[k]
			if isinstance( var, ( int, long ) ):
				ret.append(var)
		return ret

	s0,s1,s2 = getS(obj, db, len(ret))	
	s0 = np.add(s0,1.)
	s1 = np.add(s1, ret)
	s2 = np.add(s2, np.multiply(ret,ret))

	mean = np.divide(s1,s0)
	if np.sum(s0) == 1.*len(ret):
		std = 1.
	else:
		std = np.divide(
			np.sqrt(
				np.subtract(
					np.multiply(s0,s2),
					np.multiply(s1,s1))),
			s0)

	setS(obj,db,s0,s1,s2)

	return np.nan_to_num(np.divide(np.subtract(ret, mean), std))

