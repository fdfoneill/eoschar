import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import sys
from .charactersheet import CharacterSheet
from .choice import Choice
from .options import trees as TREES


PROMPT = "#"

def getYesNo(message:str) -> bool:
	response = input(message+"\n[Y/N]: ")
	if response.lower() in ["y","yes"]:
		return True
	elif response.lower() in ['n','no']:
		return False
	else:
		log.warning(f"Expected Y or N; got {response}")
		getYesNo(message)

def chooseOne(choices:list,symbol=PROMPT):
	"""Returns input prompted with 'symbol'"""
	valid = [i for i in range(len(choices))]
	for i in valid:
		print(f"[{i}] {choices[i].name}")
	try:
		selection = input(symbol)
		if selection == "exit":
			if getYesNo("Exit character creator?"):
				return False
		elif int(selection) in valid:
			return choices[int(selection)]
		else:
			raise ValueError
	except ValueError:
		print(f"Invalid selection: '{selection}'. Please enter a valid integer choice ID or 'exit'.")
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

	def runTree(self,node:Choice,character_sheet,retry = False) -> bool:
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
		retry: bool
			Whether this node has already been implemented
		"""
		try:

			# first implement this node
			if not retry:
				log.debug(f"Applying {node.name}")
				character_sheet.apply(node)
				character_sheet.data.append(node)
			if node.category is not None:
				print(f"Successfully selected {node.name} for your {node.category}.")

			# now offer up next level of choices
			if node.name in ["Skills","Trivia"]:
				log.warning(f"Skipping {node.name}: Point-buy choices not implemented")
			if node.name in ["Name","Motivation"]:
				node.promptUser(PROMPT)
			if node.name == "Assign Abstract Gear":
				log.warning(f"Skipping {node.name}: Not implemented")
			elif len(node.children) > 0:
				if node.category is not None:
					print(f"Selection opens up new options.")
				print(f"Choose a {node.children_category}:")
				selection = chooseOne(node.children)
				if selection == False:
					return False
				if not selection.checkPrerequisites(character_sheet):
					log.warning("Prerequisites violation! Try again.")
					return self.runTree(node,character_sheet,retry=True)
				return self.runTree(selection,character_sheet)
			else:
				print("Done with this choice tree! Moving on.")
			return True
		except:
			log.exception(f"Failed in {node.name}")
			return False

	def createNewCharacter(self)->None:
		"""Walks user through the steps of creating a new character from scratch"""
		self.sheet = CharacterSheet()
		print("Creating new character from scratch.\n\nYou will be guided through the steps of character creations. At each step, you will be presented with a series of options.\nTo exit character creator, enter 'exit'")
		for tree in TREES:
			if self.runTree(tree,self.sheet) == False:
				print("Aborted character creation.")
				return
		self.sheet.filled=True
		self.sheet.flush()
		print(f"Successfully created '{self.sheet.choice_names['Name']}'!")


	def loadCharacter(self,file_path) -> bool:
		"""Imports previously created character from file"""
		self.sheet = CharacterSheet()
		self.sheet.load(file_path)
		return True

	def editCharacter(self) -> bool:
		"""Edit active character sheet object"""
		log.warning("Interface.editCharacter() not implemented")
		return False