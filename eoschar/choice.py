import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import random, sys
from .func import getModel
from .weapon import Weapon

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
	display: None
		Print visualization of Choice and its descendants as 
		a tree, with Choice as the root node
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
		self.root_id = kwargs.get("root_id",None)
		self.unique = kwargs.get("unique",{})

	def __repr__(self):
		nodeType = f"{self.category} option" if (self.category is not None) else "root node"
		if len(self.children) < 1:
			childType = "terminal node"
		elif len(self.children) == 1:
			childType = "1 child"
		else:
			childType = f"{len(self.children)} children"
		if self.root_id is None:
			tree = "no tree"
		else:
			tree = f"tree {self.root_id}"
		return f"<Instance of Choice, {tree} | {nodeType} : '{self.name}', {childType}>"

	def display(self,level=0):
		if level==0:
			if self.category is not None:
				outString = f"{self.name} ({self.category})"
			else:
				outString = self.name
		else:
			if self.category is not None:
				outString = ("| " * (level-1)) + "|-" + f"{self.name} ({self.category})"
			else:
				outString = ("| " * (level-1)) + "|-" + f"{self.name}"
		print(outString)
		for child in self.children:
			child.display(level=level+1)

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
	
	def implement(self,character_sheet,*args,**kwargs) -> bool:
		pass

	def addImplementation(self,new_function) -> bool:
		"""Adds new behavior to end of implement() function
		"""
		oldImplement = self.implement
		def newImplement(*args,**kwargs):
			oldImplement(*args,**kwargs)
			new_function(*args,**kwargs)
		self.implement= newImplement
		return True

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


class Species(Choice):
	"""A class to represent an EoS species option
	
	***

	Attributes
	----------
	base_qualities:dict
	speed: str

	"""
	def __init__(self,base_qualities={"Brawn":10,"Grace":10,"Wits":10,"Spirit":10},speed="15 yards",**kwargs):
		super().__init__(**kwargs)
		self.base_qualities = base_qualities
		self.speed=speed

	def implement(self,character_sheet,*args,**kwargs) -> bool:
		for q in self.base_qualities.keys():
			character_sheet.qualities[q] = DieType(self.base_qualities[q])
		character_sheet.combat_stats['Speed'] = self.speed
		return True


class Training(Choice):
	"""A class to represent an EoS Training

	***

	Attributes
	----------

	"""
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.skill = kwargs['skill'] # str
		self.gear = kwargs.get('gear',[]) # list

	def implement(self,character_sheet,*args,**kwargs) ->bool:
		model = getModel('model_training.json')[self.name]
		character_sheet.skills[self.skill][level] += 1
		for item in self.gear:
			character_sheet.gear.append(item)
		character_sheet.traits.append({"Name":model["Training Trait"]["name"],"Description":model["Training Trait"]["description"]})
		return True


class Focus(Choice):
	"""A class to represent an EoS character Focus"""
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.skills = kwargs['skills']
		self.trait = kwargs['trait']

	def implement(self,character_sheet,*args,**kwargs):
		for s in self.skills:
			character_sheet.skills[s].level += 1
		character_sheet.traits.append({"Name":self.trait["name"],"Description":self.trait["description"]})


class Trait(Choice):
	"""A class to represent an EoS Trait

	***

	Attributes
	----------

	"""
	def __init__(self,description,**kwargs):
		super().__init__(**kwargs)
		self.description = description

	def implement(self,character_sheet,*args,**kwargs):
		character_sheet.traits.append({"Name":self.name,"Description":self.description})


class CombatSpecialty(Choice):
	"""A class to represent an EoS Combat Specialty"""
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.traits = kwargs['traits']

	def implement(self,character_sheet,*args,**kwargs) -> bool:
		return True


class Background(Choice):
	"""A class to represent an EoS background"""
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.trait = kwargs['trait']
		self.trivia = kwargs['trivia']
		self.gear = kwargs['gear']
		self.money = kwargs['money']

	def implement(self,character_sheet,*args,**kwargs):
		character_sheet.traits.append(self.trait)
		character_sheet.trivia += self.trivia
		for item in gear:
			parts = item.split()
			if parts[0] == "!": # signals abstract gear choice
				{
				"potions":character_sheet._abstract_potions,
				"grenades":character_sheet._abstract_grenades,
				"ammunition":character_sheet._abstract_ammunition,
				"modifications":character_sheet._abstract_modifications,
				"kits":character_sheet._abstract_kits
				}[parts[1]][parts[2]] += parts[3]
			else:
				character_sheet.append(item)
		character_sheet.money += self.money


class Item(Choice):
	"""A class to represent an item of EoS gear"""
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.gear_type = kwargs.get("gear_type","general")
		self.level = kwargs.get("level","A")
		self.abstract=kwargs.get("abstract",False)
		self.item_name = kwargs.get("item_name",self.name)
		self.n=kwargs.get("n",1)
		if self.gear_type == "weapon":
			profile = Weapon(**getModel("model_weapons.json")[self.item_name])

	def implement(self,character_sheet,*args,**kwargs):
		if self.abstract:
			if self.gear_type=="potion":
				character_sheet._abstract_potions[self.level]+=self.n
			elif self.gear_type == "ammunition":
				character_sheet._abstract_ammunition[self.level]+=self.n
			elif self.gear_type == "modification":
				character_sheet._abstract_modifications[self.level]+=self.n
			elif self.gear_type == "weapon":
				character_sheet._abstract_weapons.append(self.profile)
			elif self.gear_type == "grenade":
				character_sheet._abstract_grenades[self.level]+=self.n
			else:
				raise SyntaxError(f"No such thing as an abstract '{self.gear_type}'. Must be one of 'potion', 'ammunition', 'weapon', or 'modification'.")
		elif self.gear_type == "weapon":
			character_sheet.weapons.append(self.profile)
		elif self.gear_type == "custom":
			pass
		else:
			character_sheet.gear.append(self.item_name)

