class memoryDB:
	storage = dict()
	def __init__(self):
		storage = dict()

	def get(self, key):
		if key in self.storage:
			return self.storage(key)
		return None

	def set(self, key, val):
		self.storage[key] = val

