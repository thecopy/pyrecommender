import numpy as np

def transform(obj,db):
	if obj is np.array:
		return obj

	if hasattr(obj, "getFeatures"):
		feats = obj.getFeatures()

		for key, val in feats.iteritems():
			if isinstance( val, str ):
				dbKey = obj.__class__.__name__ + ":" + key
				listOfThisType = db.get(dbKey)
				if listOfThisType is None:
					listOfThisType = []

				listOfThisType.append(val)
				db.set(key, listOfThisType)
				feats[key] = listOfThisType.index(val)+1

		return feats.values()


	ret = []
	for k in obj.__dict__:
		var = obj.__dict__[k]
		if isinstance( var, ( int, long ) ):
			ret.append(var)
	return ret