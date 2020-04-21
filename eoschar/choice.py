import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import random, sys

class Choice:
	"""A class to represent an EoS character creation choice point

	Each point in the Era of Silence character creation process
	that requires a choice by the player can be represented by
	an instance of the Choice class.

	If the character creation process is visualized as a set of
	trees, each Choice object represents a node. If the 'children'
	attribute is empty, the Choice is a terminal node. If not,
	the Choice itself opens up more options.

	If the 'category' attribute is None, the Choice is considered
	a root node, and should be used to set a unique root_id for 
	its tree.

	***

	Attributes
	----------
	category: str
		Should be None if root node, otherwise inherited from
		parent.
	children: list
		Further choices opened by the selection of this Choice.
		Each list item is an instance of Choice.
	children_category: str
		Name of the category of child choices. For example, 
		for a Choice of species (e.g. 'Elek'), the subchoice
		category would be 'Species Trait'
	name: str
		Unique name of this Choice. e.g. 'Close Combat'
	prerequisites: dict
		Prerequisites for taking this Choice. Dictionary keys 
		are categories, values are names of choices within that
		category. E.g. for choice 'Vian Moves Slowly',
		prerequisites = {'Species':'Elek'}
	root_id: int
		Unique identifier of "tree" to which this choice belongs.
	unique: bool
		Whether this Choice should be the only one in its
		category. For example: True for species, False for
		gear. Default True.

	Methods
	-------
	addChild: int
		Append a child Choice to self.children. Returns
		current number of children after appending.
	cascadeRootId: bool
		Set all descendants to have the same root_id as this Choice.
		Should only be manually called from a root node.
	coerceChildrenCategory: bool
		Changes 'category' attribute of each Choice in children
		to match this Choice's child_category.
	getChildren(): bool
		Generator that yields the name attribute for each child
		in children.
	implement(CharacterSheet): bool
		Adds the Choice to a CharacterSheet object

	
	"""

	def __init__(self,**kwargs):
		self.category = kwargs.get("category",None)
		self.children = []
		self.children_category = kwargs.get("children_category",None)
		self.name = kwargs.get("name",None)
		self.prerequisites = kwargs.get("prerequisites",{})
		self.root_id = kwargs.get("root_id",{})
		self.unique = kwargs.get("unique",{})

	def __repr__(self):
		nodeType = f"{self.category} option" if (self.category is not None) else "root node"
		if len(self.children) < 1:
			childType = "terminal node"
		elif len(self.children) == 1:
			childType = "1 child"
		else:
			childType = f"{len(self.children)} children"
		return f"<Instance of Choice: '{self.name}', {childType}, {nodeType}>"

	def addChild(self,new_child):
		"""Append a child Choice to self.children

		Returns number of children after appending

		***

		Parameters
		----------
		new_child: eoschar.Choice
			New child Choice object
		"""
		if not isinstance(new_child,Choice):
			raise SyntaxError("new_child must be a Choice object")
		self.children.append(new_child)

	def cascadeRootId(self,override_root=False) -> bool:
		"""Set all children to have the same root_id as this Choice

		***

		Parameters
		----------
		override_root: bool
			Default False. If override_root is not set, calling 
			cascadeRootId() from a non-root Choice will raise
			an exception.
		"""
		if self.category is not None and not override_root:
			raise Exception(f"{self.name} is not a root Choice. Cannot cascade root_id if override_root is False.")
		for child in self.children:
			child.root_id = self.root_id
			child.cascadeRootId(override_root=True)
		return True
	
	def implement(self,character_sheet) -> bool:
		pass

	def getChildren(self) -> bool:
		"""Returns a list of 'name' for each child in self.children"""
		return [child.name for child in self.children]

	def cascadeChildrenCategory(self) -> bool:
		"""
		Coerces the 'category' attribute of each descendant in
		self.children to be equal to its parent's
		children_category
		"""
		try:
			for child in self.children:
				child.category = self.children_category
				child.cascadeChildrenCategory()
			return True
		except:
			log.exception("Failed to coerce child categories to match children_category.")
			return False


class Item(Choice):
	"""A class to represent an EoS gear item
	

	"""
	def __init__(self):
		self.__super__.__init__()
		self.category="Gear Item"