import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import json, pickle, sys

def getModel():
	modelFile = os.path.join(os.path.dirname(os.path.dirname(__file__)),"resources/char_model.json")
	with open(modelFile,'r') as rf:
		return json.loads(rf.read())

MODEL = getModel()

class CharacterSheet:
	""" A class to represent an EoS character sheet
	
	***

	Attributes
	----------
	options: list
		List of all creation trees. Each item is a Choice
		object.
	data: list
		List of all user selections for given character

	Methods
	-------
	load: bool
		Read pickled data from text file
	save: bool
		Write pickled data to text file


	"""

	def __init__(self):
		pass

	def load(self):
		pass

	def save(self):
		pass