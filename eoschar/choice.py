import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import random, sys
from collections import defaultdict
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
	prerequisites: list
		List of functions to apply to character_sheet object. If
		all return True, prerequisites are met. Call with 
		checkPrerequisites() method.
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
	checkPrerequisites: bool
		Checks character sheet to ensure that this Choice's
		prerequisites have not been violated.
	cascadeChildrenCategory: bool
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
		self.prerequisites = []
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
			if self.root_id is not None:
				outString += f" | <tree {self.root_id}>"
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

	def checkPrerequisites(self,character_sheet) -> bool:
		"""Checks that this choice's prerequisites are met

		Returns True if no violations are found, False
		otherwise. For example, if this Choice is Talent:Brawn
		and the character_sheet also included the Human trait
		Brawn Boost, this function would return False.

		***

		Parameters
		----------
		character_sheet: eoschar.charactersheet.CharacterSheet
			Character sheet object for which to check the prerequisites
		"""
		if  all([f(character_sheet) for f in self.prerequisites]):
			return True
		else:
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
		character_sheet.choice_names['Species'] = self.name
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
		character_sheet.choice_names['Training'] = self.name
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
		character_sheet.choice_names['Focus'] = self.name
		for s in self.skills:
			character_sheet.skills[s].level += 1
		character_sheet.traits.append({"Name":self.trait["name"],"Description":self.trait["description"]})


class CombatSpecialty(Choice):
	"""A class to represent an EoS Combat Specialty"""
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.traits = kwargs['traits']
		self.gear = kwargs['gear']

	def implement(self,character_sheet,*args,**kwargs):
		character_sheet.choice_names['Combat Specialty'] = self.name
		for t in self.traits:
			character_sheet.traits.append(t)
		for item in self.gear:
			parts = item.split()
			if parts[0] == "!":
				if parts[1] == 'abstract':
					pass
				elif parts[1] == 'weapon':
					character_sheet._raw_weapons.append(getModel('model_weapons.json')[parts[2]])
				else:
					log.warning(f"'{item}' failed to parse in CombatSpecialty.implement()")
			else:
				character_sheet.gear.append(item)


class Background(Choice):
	"""A class to represent an EoS background"""
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.trait = kwargs['trait']
		self.trivia = kwargs['trivia']
		self.gear = kwargs['gear']
		self.money = kwargs['money']

	def implement(self,character_sheet,*args,**kwargs):
		character_sheet.choice_names['Background'] = self.name
		character_sheet.traits.append(self.trait)
		character_sheet.trivia += self.trivia
		character_sheet.trivia = list(set(character_sheet.trivia)) # delete duplicate trivia
		for item in gear:
			parts = item.split()
			if parts[0] == "!": # signals abstract gear choice
				{
				"potion":character_sheet._abstract_potions,
				"grenade":character_sheet._abstract_grenades,
				"ammunition":character_sheet._abstract_ammunition,
				"modification":character_sheet._abstract_modifications,
				"kit":character_sheet._abstract_kits
				}[parts[1]][parts[2]] += parts[3]
			else:
				character_sheet.append(item)
		character_sheet.money += self.money

class Motivation(Choice):
	"""A class to represent an EoS motivation."""
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.motivation = ""

	def implement(self,character_sheet,*args,**kwargs):
		character_sheet.choice_names['Motivation'] = self.motivation


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
			self.profile = Weapon(**getModel("model_weapons.json")[self.item_name])

	def implement(self,character_sheet,*args,**kwargs):
		if self.abstract:
			if self.gear_type=="potion":
				character_sheet._abstract_potions[self.level]+=self.n
			elif self.gear_type == "ammunition":
				character_sheet._abstract_ammunition[self.level]+=self.n
			elif self.gear_type == "modification":
				character_sheet._abstract_modifications[self.level]+=self.n
			elif self.gear_type == "weapon":
				character_sheet._raw_weapons.append(self.profile)
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


class PointBuy(Choice):
	"""A class to represent the two point-buy stages of EoS character creation: Skills and Trivia

	***

	Attributes
	----------
	name: str
	starting_points: int
	starting_level: int
		Default 0. The base level from which all categories
		increase. 1 for Skills, 0 for Trivia.
	max_level: int
	points_per_level: dict
		Mapping of additional levels to points. For
		example, if it costs 1 point to level from 1 to 2,
		and two point to level from 2 to 3, the dictionary
		would be: {2:1,3:2}
	categories: dict
		What are we buying levels in? Maps category names to
		the current level. Structured as: {name:{bought_levels,
		base_levels}} where base_levels is the number of levels
		imported through the load() method.
	current_points: int
		Dynamic tracker of points as they are spent and
		redeemed by leveling up and down.

	Methods
	-------
	implement: None
	display: None
		What to print if stored alongside Choice objects.
	load: bool
		Pull in a category dictionary from an external 
		CharacterSheet object.
	levelUp: bool
		Raise a given category by a single level.
	levelDown: bool
		Lower a given category by a single level.
	"""

	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.starting_points = kwargs.get('starting_points',0)
		self.starting_level = kwargs.get('starting_level',0)
		self.max_level = kwargs.get('max_level',None)
		self.point_per_level = kwargs.get('points_per_level',defaultdict(lambda:1))
		self.categories = {}
		# try loading passed categories
		try:
			baseCats = kwargs['categories']
			if self.name=="Skills":
				for c in baseCats:
					self.categories[c['name']] = {'bought_levels':0,'base_levels':0}
			elif self.name=="Trivia":
				for c in baseCats:
					self.categories[c] = {'bought_levels':0,'base_levels':0}
			else:
				log.error(f"PointBuy.name expected one of ['Skills','Trivia'], got '{self.name}'.")
		except KeyError:
			pass
		self.current_points = self.starting_points

	# def display(self,level=0):
	# 	"""What to print if stored alongside Choice objects

	# 	The display() method is intended to show off the tree
	# 	structure of Choice object groups. Although PointBuy
	# 	objects have no such structure, they are stored alongside
	# 	Choice objects and will thus sometimes have display()
	# 	called.

	# 	This method simply prints the object's name alongside
	# 	the appropriate number of pipes and dashes.
	# 	"""
	# 	if level==0:
	# 		outString = self.name
	# 		if self.root_id is not None:
	# 			outString += f" | <tree {self.root_id}>"
	# 	else:
	# 		outString = ("| " * (level-1)) + "|-" + f"{self.name}"
	# 	print(outString)

	def implement(self,character_sheet):
		if self.name == "Skills":
			for skill in self.categories.keys():
				if skill['bought_levels']> 0:
					character_sheet.skills[skill]['level'] += skill['bought_levels']
		elif self.name == "Trivia":
			for topic in self.categories.keys():
				if topic['bought_levels'] > 0:
					character_sheet.trivia.append(topic)
			character_sheet.trivia = list(set(character_sheet.trivia))
		else:
			log.error(f"PointBuy.name expected one of ['Skills','Trivia'], got '{self.name}'.")

	def load(self,category_obj):
		"""Reads external skills or trivia levels

		NOTE: This method must be called *before*
		any calls to levelUp() or levelDown(). Calls
		to load() after skills have been bought may
		result in violations of the max_level
		attribute.

		***

		Parameters
		----------
		category_obj
			A list or dictionary of previously bought
			trivia or skills. Should be loaded from
			a CharacterSheet object.
		"""
		if isinstance(category_obj,list):
			for topic in category_obj:
				self.categories[topic]['base_levels'] += 1
		elif isinstance(category_obj,dict):
			for skill in category_obj.keys():
				self.categories[skill]['base_levels'] += category_obj[skill]['level']
		else:
			log.error("PointBuy.load() 'category_obj' argument must be list or dict")

	def levelUp(self,category_name)->bool:
		"""Robustly levels a category up by one level

		If the necessary points are unavailable or if
		the category is already at max_level, logs a 
		warning and returns False. Otherwise returns
		True.
		"""
		try:
			currentLevel = self.categories['category_name']['bought_levels']+self.categories['category_name']['base_levels']
		except KeyError:
			# add the category if it does not exist (i.e. new Trivia topic)
			self.categories['category_name'] = {'bought_levels':0,'base_levels':0}
			currentLevel = self.categories['category_name']['bought_levels']+self.categories['category_name']['base_levels']
		required_points = self.points_per_level[currentLevel+1]
		if currentLevel >= self.max_level:
			log.warning(f"{category_name} is already at maximum level of {self.max_level}!")
			return False
		if required_points > self.current_points:
			log.warning(f"Insufficient points to level up {category_name}! Raising to level {currentLevel+1} requires {required_points} points; you have {self.current_points}.")
			return False
		self.current_points -= required_points
		self.categories['category_name']['bought_levels'] += 1
		return True

	def levelDown(self,category_name)->bool:
		"""Robustly levels a category up by one level

		If the category is already at zero, or does
		not exist, returns False. Otherwise returns
		True.
		"""
		try:
			currentLevel = self.categories[category_name]['bought_levels']+self.categories['category_name']['base_levels']
		except KeyError:
			log.warning(f"{category_name} not found")
			return False
		redeemed_points = self.points_per_level[currentLevel]
		if self.categories['category_name']['bought_levels'] <= self.starting_level:
			log.warning(f"No levels of {category_name} to redeem. Any remaining levels are from another source (e.g. Training, Focus, Background).")
			return False
		self.current_points += redeemed_points
		self.categories['category_name']['bought_levels'] -= 1
		return True
