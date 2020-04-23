import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import sys
from .charactersheet import CharacterSheet
from .choice import Choice
from .options import trees as TREES


def getYesNo(message:str) -> bool:
	response = input(message+"\n[Y/N]: ")
	if response.lower() in ["y","yes",'1']:
		return True
	elif response.lower() in ['n','no','0']:
		return False
	else:
		log.warning(f"Expected Y or N; got {response}")
		getYesNo(message)

def chooseOne(choices:list,symbol=">>>"):
	"""Returns input prompted with 'symbol'"""
	valid = [i for i in range(len(choices))]
	for i in valid:
		print(f"[{i}] {choices[i].name}")
	selection = input(symbol)
	if selection in valid:
		return choices[selection]
	elif selection == "exit":
		if getYesNo("Exit character creator?"):
			sys.exit()
	else:
		print(f"Invalid selection: {selection}. Please enter a valid integer choice ID.")
		return chooseOne(choices,symbol)


class Interface:
	"""Class representing the command-line user interface

	***

	Attributes
	----------
	sheet: CharacterSheet
		Active character sheet object

	Methods
	-------
	runTree: str
		Recursively offers up all choices in passed 
		Choice object and its children.
	createNewCharacter: bool
	loadCharacter: bool
	editCharacter: bool

	"""
	def __init__(self):
		self.sheet = None

	def runTree(self,node:Choice,character_sheet):
		"""Recursivley offers up all choices in tree
		
		Returns name of root node

		***

		Parameters
		----------
		node: Choice
			Root node of choice tree
		character_sheet: CharacterSheet
			Sheet to which choices will be
			applied
		"""
		try:
			if node.name in ["Skills","Trivia"]:
				log.warning("Skills and Trivia not implemented")
			if node.name in ["Name"]:
				log.warning("Name not implemented")
			elif len(node.children) > 0:
				if node.category is not None:
					print(f"Selection of {node.name} opens up new options.")
				print(f"Choose a {node.children_category}:")
				selection = chooseOne(node.children)
				if not selection.checkPrerequisites(character_sheet):
					log.warning("Prerequisites violation! Try again.")
					self.runTree(node,character_sheet)
				selection.implement(character_sheet)
				character_sheet.data.append(selection)
				self.runTree(selection,character_sheet)
			else:
				print("Done with this choice tree! Moving on.")
		except:
			log.exception(f"Failed in {node.name}")

	def createNewCharacter(self) -> bool:
		"""Walks user through the steps of creating a new character from scratch"""
		self.sheet = CharacterSheet()
		print("Creating new character from scratch.\n\nYou will be guided through the steps of character creations. At each step, you will be presented with a series of options.\nTo exit character creator, enter 'exit'")
		for tree in TREES:
			self.runTree(tree,self.sheet)
		self.sheet.flush()
		print(f"Successfully created '{self.sheet.choice_names['Name']}'!")
		self.sheet.filled=True
		return True



	def loadCharacter(self,file_path) -> bool:
		"""Imports previously created character from file"""
		self.sheet = CharacterSheet()
		self.sheet.load(file_path)
		return True

	def editCharacter(self) -> bool:
		"""Edit active character sheet object"""
		pass