import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import pickle, sys
from .charactersheet import CharacterSheet
from .choice import Choice, Item

def getInput(symbol=">>>") -> str:
	"""Returns input prompted with 'symbol'"""
	return input(symbol)

class Interface:
	"""Class representing the command-line user interface

	***

	Attributes
	----------
	sheet: CharacterSheet
		Active character sheet object

	Methods
	-------
	createNewCharacter: bool
	loadCharacter: bool
	editCharacter: bool

	"""
	def __init__(self):
		self.sheet = None

	def createNewCharacter(self) -> bool:
		pass

	def loadCharacter(self,file_path) -> bool:
		pass

	def editCharacter(self) -> bool:
		"""Edit active character sheet object"""
		pass