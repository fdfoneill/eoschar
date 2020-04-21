import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import json, pickle, sys
from .choice import Choice
from .dietype import DieType
from .func import getModel

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
	choice_names: dict
		Names of user selections to be displayed in upper
		right box of character sheet
	qualities: dict
		Dictionary of quality names and values
	skills: dict
		Dictionary of skill names, levels, and linked
		qualities
	combat_stats: dict
		Dictionary of Speed, AV, Toughness, and
		Shooting / Fighting Dice
	trivia: list
		List of trained trivia
	traits: list
		List of traits
	weapons: list
		List of weapons
	gear: list
	money: int
	_abstract_potions: dict
		Tracks number of each level the character is
		owed.
	_abstract_weapons: list
		List base weapons owned (before modifications).
	_abstract_modifications: dict
		Tracks number of each level the character is
		owed.
	_abstract_ammunition: dict
		Tracks number of each level the character is
		owed.
	_abstract_grenades: dict
		Tracks number of each level the character is
		owed.


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

		# blank options and data
		self.options=[]
		self.data=[]

		# initialize default game stats
		## choice_names
		self.choice_names = {
			"Name":'',
			"Species":'',
			"Background":'',
			"Motivation":'',
			"Training":'',
			"Focus":'',
			"Combat Specialty":''
		}
		## qualities
		self.qualities = {}
		for q in getModel('model_qualities.json'):
			self.qualities[q] = DieType(10)
		## skills
		self.skills = {}
		for s in getModel('model_skills.json'):
			self.skills[s['name']] = {"level":1,"quality":s['quality']}
		## combat_stats
		self.combat_stats = {
			"Speed":"15 yards",
			"AV":0,
			"Toughness":20-int(self.qualities['Brawn']),
			"Shooting Die":DieType(12),
			"Fighting Die":DieType(12)
		}
		## trivia
		self.trivia = []
		## traits
		self.traits = []
		## weapons
		self.weapons = []
		## gear
		self.gear = []
		## money
		self.money = 0
		## abstract dictionaries
		self._abstract_potions = {"A":0,"B":0,"C":0}
		self._abstract_weapons = []
		self._abstract_modifications = {"A":0,"B":0,"C":0}
		self._abstract_ammunition = {"A":0,"B":0,"C":0}
		self._abstract_grenades = {"A":0,"B":0,"C":0}

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
		try:
			option.implement(self)
		except:
			log.exception("Failed to apply")
			return False
		return True