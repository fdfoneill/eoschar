import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import base64, json, pickle, sys
from ._version import __version__
from .choice import Choice,TextInput,PointBuy,AssignAbstractGear
from .dietype import DieType
from .sheetmaker import SheetMaker
from .func import getModel
from .options import trees as TREES

class CharacterSheet:
	""" A class to represent an EoS character sheet
	
	***

	Attributes
	----------
	filled: bool
		Whether the character sheet has all its valid options
		filled out in self.data. If False, cannot save or flush.
		Set to True when character is loaded or when choices
		are made through an Interface object.
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
	_abstract_kits: dict
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
	flush
	output: bool
		Print the character sheet to a
		beautiful pdf file.
	edit: bool
		TODO

	"""

	def __init__(self):
		# blank options and data
		self.__version__ = __version__
		self.options=TREES
		self.data=[]
		self.treePath = []
		self.filled = False

		# initialize default game stats
		self.loadBlank()

	def loadBlank(self):
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
		## weapons before modifications
		self._raw_weapons = []
		## abstract dictionaries
		self._abstract_potions = {"A":0,"B":0,"C":0}
		self._abstract_weapons = {"Melee":0,"Ranged":0,"Any":0}
		self._abstract_modifications = {"A":0,"B":0,"C":0}
		self._abstract_ammunition = {"A":0,"B":0,"C":0}
		self._abstract_grenades = {"A":0,"B":0,"C":0}
		self._abstract_kits = {"A":0,"B":0,"C":0}

	def load(self,file_path) -> bool:
		"""Read data from text file"""
		def autoTree(tree,path):
			def doSelection(node,j) -> "node":
				selection = node.children[j]
				if not selection.checkPrerequisites(self):
					log.warning("Prerequisites violation! Try again.")
				self.apply(selection)
				self.data.append(selection)
				return selection
			i = 0
			node = tree
			while len(node.children) > 0:
				node = doSelection(node,path[i])
				i += 1
			return path[i:]

		file_path = file_path.strip("'").strip('"')
		with open(file_path,'rb') as rf:
			loadedPickle = pickle.loads(rf.read())
		if self.__version__ != loadedPickle['__version__']:
			log.warning(f"Loaded character created in version {loadedPickle['__version__']}, you are running version {self.__version__}. Potential compatibility issues.")
		self.treePath = loadedPickle['treePath']

		# load text input stuff
		self.data.append(TextInput(name="Name",value = loadedPickle['name']))
		self.data.append(TextInput(name="Motivation",value=loadedPickle['motivation']))

		# run trees
		treePath = self.treePath
		try:
			for t in TREES:
				if t.name in ["Skills","Trivia","Name","Motivation","Assign Abstract Gear"]:
					log.debug(f"Skipping {t.name}")
				else:
					treePath = autoTree(t,treePath)
		except:
			log.exception("Loaded tree path incompatible with options.trees")
			return False

		# load skills
		skills = PointBuy(name="Skills",max_level=3,starting_level=0,categories=getModel('model_skills.json'),starting_points=5,points_per_level = {1:0,2:1,3:3},root_id=6)
		skills.categories = loadedPickle['skills']
		self.data.append(skills)

		# load trivia
		trivia = PointBuy(name="Trivia",max_level=1,starting_level=0,point_per_level = {0:0,1:1},categories=getModel('model_trivia.json'),root_id=9)
		trivia.categories = loadedPickle['trivia']
		self.data.append(trivia)

		# load gear assignments
		## TODO
		assign_abstract_gear = AssignAbstractGear(name="Assign Abstract Gear")
		assign_abstract_gear.assign(self)
		assign_abstract_gear.gear += loadedPickle['assigned_gear']
		for weapon_pickle in loadedPickle['weapon_pickles']:
			assign_abstract_gear.weapons.append(pickle.loads(weapon_pickle))
		self.data.append(assign_abstract_gear)

		# flush and return
		self.filled=True
		self.flush()
		return True

	def save(self,file_path) ->bool:
		"""Write data to text file"""
		if not self.filled:
			log.warning("Cannot save incomplete character")
			return False
		# create dictionary of values
		outDict = {}
		outDict['__version__'] = self.__version__
		outDict['treePath'] = self.treePath
		outDict['name'] = self.choice_names["Name"]
		outDict['motivation'] = self.choice_names["Motivation"]
		for node in self.data:
			if node.name == "Skills":
				# skills
				outDict["skills"] = dict(node.categories)
			elif node.name == "Trivia":
				# trivia
				outDict["trivia"]=dict(node.categories)
			elif node.name == "Assign Abstract Gear":
				# non-weapon gear
				outDict["assigned_gear"]=node.gear
				# modded weapons
				outDict["weapon_pickles"]=[]
				for weapon in self.weapons:
					outDict["weapon_pickles"].append(pickle.dumps(weapon))
		with open(file_path,'wb') as wf:
			# wf.write('{')
			# # version
			# wf.write(f'"__version__":"{self.__version__}"')
			# # treePath
			# wf.write(',"treePath":')
			# wf.write(json.dumps(self.treePath))
			# # text fields
			# wf.write(f',"name":"{self.choice_names["Name"]}"')
			# wf.write(f',"motivation":"{self.choice_names["Motivation"]}"')
			# for node in self.data:
			# 	if node.name == "Skills":
			# 		# skills
			# 		wf.write(f',"skills":{json.dumps(node.categories)}')
			# 	elif node.name == "Trivia":
			# 		# trivia
			# 		wf.write(f',"trivia":{json.dumps(node.categories)}')
			# 	elif node.name == "Assign Abstract Gear":
			# 		# non-weapon gear
			# 		wf.write(f',"assigned_gear":{json.dumps(node.gear)}')
			# 		# modded weapons
			# 		wf.write(f',"weapon_pickles":["')
			# 		wf.write('","'.join(["weapon_pickled="+str(base64.b64encode(pickle.dumps(weapon))) for weapon in self.weapons]))
			# 		wf.write(f'"]')
			# wf.write('}')
			pickle.dump(outDict,wf)
		return True

	def apply(self,option)->bool:
		"""Apply a choice to the character sheet"""
		try:
			option.implement(self)
		except:
			log.exception("Failed to apply")
			return False
		return True

	def flush(self) -> bool:
		"""Reset character and apply all current choices"""
		if not self.filled:
			log.warning("Character data incomplete, cannot flush")
			return False
		self.loadBlank()
		for c in self.data:
			self.apply(c)
		return True

	def output(self,pdf_path) -> bool:
		"""Print the character sheet to a beautiful PDF file

		***

		Parameters
		----------
		pdf_path:str
			Path to output file. Must end in .pdf extension.
			If file exists, it will be overwritten.
		"""
		if not self.flush():
			log.warning("Failed to flush, cannot output sheet")
			return False
		maker = SheetMaker()
		try:
			maker.read(self)
			maker.make(pdf_path)
			return True
		except:
			log.exception("Failed to output")
			return False

	def edit(self) -> bool:
		"""TODO"""
		return False