import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

class DieType:
	"""Class to represent a polyhedral die size

	***

	Attributes
	----------
	_sides: int
		Number of sides; one of self.valid.
	_valid: list
		List of valid die sizes: [4,6,8,10,12,20]

	Methods
	-------
	improve: bool
		Decreases _sides by one category. Returns
		False if _sides was already 4, otherwise
		returns True.
	worsen: bool
		Increases _sides by one category. Returns
		False if _sides was already 20, otherwise
		returns True.
	"""
	def __init__(self,sides=10):
		self._valid = [4,6,8,10,12,20]
		if sides not in self._valid:
			raise SyntaxError(f"Die size '{n}' not one of allowed values: [4,6,8,10,12,20]")
		self._sides = sides

	def __repr__(self):
		return f"<Instance of DieType with {self._sides} sides>"

	def __int__(self):
		return self._sides

	def __str__(self):
		return f"d{self._sides}"d

	def improve(self):
		"""Decrease _sides by one category

		Returns False if _sides is already 4,
		otherwise returns True.

		"""
		for i in range(len(self._valid)):
			if self._sides == self._valid[i]:
				try:
					self._sides = self._valid[i-1]
					return True
				except IndexError:
					return False

	def worsen(self):
		"""Increase _sides by one category

		Returns False if _sides is already 20,
		otherwise returns True.

		"""
		for i in range(len(self._valid)):
			if self._sides == self._valid[i]:
				try:
					self._sides = self._valid[i+1]
					return True
				except IndexError:
					return False