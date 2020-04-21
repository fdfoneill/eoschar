import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

class Weapon:
	"""A class to represent an EoS weapon

	Notably does NOT inherit from Choice. This class
	exists in the rendered stage of the character, not
	the prerender stage.
	"""
	def __init__(self,**kwargs):
		self.name = kwargs['name']
		self.range = kwargs.get('range',None)
		self.reach = kwargs.get('reach',None)
		if self.range is None and self.reach is None:
			self.reach = 1
		self.ap = kwargs.get("ap",1)
		self.special=[kwargs.get("special",None)]