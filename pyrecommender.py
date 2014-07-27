from core import const, logservice, ucb, item
import configuration as c
import random
import transformer
class api:
	mode = const.EXPLORE

	items = ['dummy1', 'dummy2']
	logservice = None
	trainer = ucb()

	def __init__(self, mode=const.EXPLORE):
		self.mode = mode
		self.logservice = logservice()

	def get(self, context):
		item = None

		if self.mode == const.EXPLORE:
			item = random.choice(self.items)
		elif self.mode == const.EXPLOIT:
			raise Exception('get() for mode EXPLOIT it not yet impletented') 
		else:
			raise Exception('Invalid mode') 

		id = self.logservice.log(self.mode, item, context)
		return (item, id)

	def reward(self, id, reward):
		self.logservice.reward(id, reward)

		# Should happen somewhere else so that we dont nececarily train every round, especially
		# on the same thread at the same time the reward is made
		item, context = self.logservice.getItemMetadata(id);
		self.trainer.train(item, context, reward)

