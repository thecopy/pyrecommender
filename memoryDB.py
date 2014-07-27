import shelve

class memoryDB:
	d = None
	def __init__(self):
		self.d = shelve.open("memoryDB.db")

	def get(self, key):
		if self.d.has_key(key):
			return self.d[key]
		else:
			return None

	def set(self, key, val):
		self.d[key] = val
		self.d.sync()

