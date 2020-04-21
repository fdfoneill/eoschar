import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import json, pickle, sys
from .choice import Choice

def getModel(file_name):
	modelFile = os.path.join(os.path.dirname(os.path.dirname(__file__)),"resources",file_name)
	with open(modelFile,'r') as rf:
		return json.loads(rf.read())

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
	qualities: dict
	skills: dict
		Dictionary of skill names, levels, and linked
		qualities


	Methods
	-------
	load: bool
		Read pickled data from text file
	save: bool
		Write pickled data to text file
	apply: bool
		Apply a Choice to the character
		sheet.

	"""

	def __init__(self):
		self.options=[]
		self.data=[]

	def load(self,file_path):
		"""Read data from text file"""
		with open(file_path,'r') as rf:
			self.data = pickle.load(rf)

	def save(self,file_path):
		"""Write data to text file"""
		with open(file_path,'w') as wf:
			pickle.dump(self.data,wf)

	def apply(self,option)->bool:
		"""Apply a choice to the character sheet"""
		if not isinstance(option,Choice):
			raise SyntaxError("option must be a Choice object")
		option.implement(self)
		return True