import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

class Weapon:
	"""A class to represent an EoS weapon

	Notably does NOT inherit from Choice. This class
	exists in the rendered stage of the character, not
	the prerender stage.

	***

	Attributes
	----------
	Many attributes are paired with a leading underscore
	version of itself. The _attributes are the raw
	values for this weapon, while the normal attributes
	are those values after modifications.
	"""
	def __init__(self,**kwargs):
		# immutable version of paired attributes
		self._range = kwargs.get('range',None)
		self._reach = kwargs.get('reach',None)
		if self._range is None and self._reach is None:
			self._reach = 1
		self._accuracy = kwargs.get('accuracy',0)
		self._ap = kwargs.get("ap",1)
		# live version of paired attribues
		self.range = self._range
		self.reach = self._reach
		self.accuracy = self._accuracy
		self.ap = self._ap
		# non-paired attributes
		self.name = kwargs['name']
		self.type = kwargs.get('type',self.name)
		self.heavy = kwargs.get("heavy",False)
		self.special=[i for i in [kwargs.get("special","")] if i != ""]
		self.modifications = {"A":[],"B":[],"C":[]}

	def __repr__(self):
		return f"<Instance of Weapon | name={self.name}>"

class Modification:
	"""A class to represent an EoS modification

	***

	Attributes
	----------
	name
	level
	special
	prerequisites

	Methods
	-------
	apply: -> bool
		Applies the modification to a weapon. If
		the weapon has insufficient slots or does
		not meet the prerequisites, returns False.
		Otherwise returns True.
	range: int
		Takes input range and modifies it according
		to how the mod works.
	reach: int
		Takes input reach and modifies it according
		to how the mod works.
	ap: int
		Takes input ap and modifies it according
		to how the mod works.
	accuracy: int
		Takes input accuracy and modifies it according
		to how the mod works.
	"""
	def __init__(self,**kwargs):
		# required attributes
		self.name = kwargs['name']
		self.level = kwargs['level']
		# optional attributes
		## range, ap, and accuracy are functions
		## that modify or replace input
		self.range = kwargs.get('range',lambda r: r)
		self.reach = kwargs.get('reach',lambda r: r)
		self.ap = kwargs.get('ap',lambda a: a)
		self.accuracy = kwargs.get('accuracy',lambda a: a)
		## specials get appended
		self.special = kwargs.get('special',None)
		self.prerequisites = kwargs.get('prerequisites',[])

	def apply(self,weapon:Weapon) -> bool:
		"""Applies the modification to a weapon

		If the weapon has insufficient slots or 
		does not meet the prerequisites, returns
		False. Otherwise returns True.

		***

		Parameters
		----------
		weapon: Weapon
			Weapon object to which the modification
			is being applied.
		"""
		# check if slots are available
		if self.level in ["B","C"]:
			if (len(weapon.modifications["B"]) + len(weapon.modifications["C"])) > 0:
				log.warning(f"Cannot add a new level {self.level} modification; {weapon.name} already has a level B or C modification.")
				return False
		elif self.level == "A":
			nMods = len(weapon.modifications['A'])
			if nMods > 2:
				log.warning(f"Cannot add a new level {self.level} modification; {weapon.name} already has {nMods} level A modification(s).")
				return False
		# check prerequisites
		if len(self.prerequisites) != 0:
			if not any([(p == weapon.type) for p in self.prerequisites]):
				log.warning(f"Failed to meet prerequisites. Weapon must be one of {self.prerequisites}")
				return False
		try:
			# actually do the application
			weapon.range = self.range(weapon.range)
			weapon.reach = self.range(weapon.reach)
			weapon.ap = self.range(weapon.ap)
			weapon.accuracy = self.range(weapon.accuracy)
			if self.special is not None:
				weapon.special.append(self.special)
		except:
			log.exception(f"Failed to apply {self.name} to {weapon.name}")
			return False
		return True

	def remove(self,weapon:Weapon) -> bool:
		"""Attempts to remove modification from weapon
		
		If modification is not on weapon, returns False.
		Otherwise returns True.

		***

		Parameters
		----------
		weapon: Weapon
		"""
		if self.name not in weapon.modifications[self.level]:
			log.warning(f"{weapon.name} does not have {self.name} applied.")
			return False
		log.warning("Remove method not implemented because it's very hard. Reach/ap/accuracy functions are not guaranteed reversable.")
		return False