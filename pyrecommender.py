from core import const, logservice, ucb 
import configuration as c
import random
import transformer
import memoryDB

class api:
	mode = const.EXPLORE

	items = ['dummy1', 'dummy2']
	logservice = None
	trainer = ucb()
	db = None
	transformer = None
	sizeOfTarget = 1
	def __init__(self, items, mode=const.EXPLORE):
		self.mode = mode
		self.logservice = logservice()
		self.db = memoryDB.memoryDB()
		self.transformer = transformer.transformer(self.db)
		self.sizeOfTarget = 20
		self.trainer.setItems([(o.id, self.transformer.transform(o, 20)) for o in items])

	def get(self, context):
		context = self.transformer.transform(context,20)
		item = None

		itemid = self.trainer.get(context)
		if(itemid is None):
			print 'Got none from trainer!'
			return None

		id = self.logservice.log(itemid,context)
		return (itemid, id)

	def reward(self, id, reward):
		self.logservice.reward(id, reward)

		# Should happen somewhere else so that we dont nececarily train every round, especially
		# on the same thread at the same time the reward is made
		item, context = self.logservice.getItemMetadata(id);
		self.trainer.train(item, context, reward)

