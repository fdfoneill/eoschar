import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import sys
from collections import namedtuple
from .func import getYesNo
from .charactersheet import CharacterSheet
from .choice import Choice, Weapon
from .options import trees as TREES



PROMPT = "# "


def chooseOne(choices:list,symbol=PROMPT,exit_message="Abort character creation process?"):
	"""Returns input prompted with 'symbol'"""
	valid = [i for i in range(len(choices))]
	for i in valid:
		try:
			cName = choices[i].name
		except AttributeError:
			try:
				cName = choices[i]['name']
			except (KeyError,TypeError) as e:
				try:
					cName = choices[i]['Name']
				except (KeyError,TypeError) as e:
					cName = choices[i]
		print(f"[{i}] {cName}")
	try:
		selection = input(symbol)
		if selection == "exit":
			if getYesNo(exit_message):
				return (-1,False)
			else:
				return chooseOne(choices,symbol)
		elif int(selection) in valid:
			return (int(selection),choices[int(selection)])
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
	saveCharacter: bool
	loadCharacter: bool
	editCharacter: bool
	printCharacter: bool
	menu: None
		Main interface menu. Prompts user to choose
		from new, load, save, print, or exit

	"""
	def __init__(self,**kwargs):
		self.sheet = kwargs.get('character_sheet',CharacterSheet())

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
			if not retry and node.name not in ["Trivia",'Skills','Name','Motivation','Assign Abstract Gear']:
				log.debug(f"Applying {node.name}")
				character_sheet.apply(node)
				character_sheet.data.append(node)
			if node.category is not None:
				print(f"Successfully selected {node.name} for your {node.category}.")

			# now offer up next level of choices
			if node.name == "Trivia":
				node.load(self.sheet.trivia)
				keepGoing = True
				direction = 0
				directionList = ["up","down"]
				action = None
				while keepGoing:
					print("Current trivia:")
					for topic in node.categories.keys():
						sLevel = node.categories[topic]['bought_levels']+node.categories[topic]['base_levels']
						if sLevel >0:
							print(f"{topic}: {sLevel}")
					if node.current_points == 0 and direction == 0:
						keepGoing = (not getYesNo("All points spent. Accept these trivia?"))
						if keepGoing:
							direction = (direction+1) % 2
							action = 'switched'
					else:
						if action is None:
							pass
						elif action == 'switched':
							print(["You are now adding Trivia.","You are now removing Trivia."][direction])
						else:
							print(f"Successfully {['added','removed'][direction]} {action}!")
						print(f"You have {node.current_points} trivia points remaining.")
						print(["Enter name of trivia to add. To switch to removing trivia, enter 'switch'.","Enter name of trivia to remove. To switch to adding trivia, enter 'switch'."][direction])
						response = input(PROMPT)
						# if the user asks to switch leveling directions
						if response == 'switch':
							direction = (direction+1) % 2
							action = "switched"
						# if the user asks to EXIT
						elif response == 'exit':
							if getYesNo("Abort character creation process?"):
								return False
						# anything else is interpreted as trivia
						else:
							# level up or down
							if direction == 0:
								worked = node.levelUp(response)
							elif direction == 1:
								worked = node.levelDown(response)
							action = response if worked else None
					continue
				character_sheet.apply(node)
				character_sheet.data.append(node)
			## SKILLS
			elif node.name == "Skills":
				node.load(self.sheet.skills)
				keepGoing = True
				direction = 0
				directionList = ["up","down"]
				action = None
				while keepGoing:
					print("Current skill levels:")
					for skill in node.categories.keys():
						sLevel = node.categories[skill]['bought_levels']+node.categories[skill]['base_levels']
						print(f"{skill}: {sLevel}")
					if node.current_points == 0 and direction ==0:
						keepGoing = (not getYesNo("All points spent. Accept these skills?"))
						if keepGoing:
							direction = (direction+1) % 2
							action = "switched"
					else:
						if action is None:
							pass
						elif action == 'switched':
							print(f"You are now leveling skills {directionList[direction]}.")
						else:
							print(f"Successfully leveled {directionList[direction]} {action}!")
						print(f"You have {node.current_points} skill points remaining.")
						print(f"Enter name of skill to level {directionList[direction]}. To switch to leveling skills {directionList[(direction+1)%2]}, enter 'switch'.")
						response = input(PROMPT)
						# if the user asks to switch leveling directions
						if response == 'switch':
							direction = (direction+1) % 2
							action = "switched"
						# if the user asks to EXIT
						elif response == 'exit':
							if getYesNo("Abort character creation process?"):
								return False
						# valid skill selection
						elif response in node.categories.keys():
							# level up or down
							if direction == 0:
								worked = node.levelUp(response)
							elif direction == 1:
								worked = node.levelDown(response)
							action = response if worked else None
						# INVALID selection
						else:
							print(f"Invalid selection '{response}'. Expected a skill name, 'switch', or 'exit'.")
					continue
				character_sheet.apply(node)
				character_sheet.data.append(node)
			elif node.name in ["Name","Motivation"]:
				node.promptUser(PROMPT)
				character_sheet.apply(node)
				character_sheet.data.append(node)
			elif node.name == "Assign Abstract Gear":
				print("Throughout character creation, you have gained some 'abstract' gear (e.g. '1 level B grenade'). You will now assign those options.")
				# This is complicated
				# LOAD DATA
				node.assign(character_sheet)
				# ABSTRACT WEAPONS -> RAW WEAPONS
				for variety in node.abstract_weapons.keys():
					if variety == "Any":
						vString = ""
						weaponOptions = node.ref_weapons["Melee"]+node.ref_weapons["Ranged"]
					else:
						vString = f"{variety} "
						weaponOptions = node.ref_weapons[variety]
					while node.abstract_weapons[variety] > 0:
						print(f"Choose {node.abstract_weapons[variety]} more {vString}weapon(s):")
						intSelection,selection = chooseOne(weaponOptions)
						if selection == False:
							return False
						else:
							node.raw_weapons.append(selection)
							node.abstract_weapons[variety] -= 1
							print(f"Successfully added a {selection['name']}.")
					print(f"No more {vString}weapons to assign. Moving on.")
				# MODIFICATIONS (ASSIGN TO WEAPONS)
				## TODO
				print("Assign modifications.")
				for w in node.raw_weapons:
					try:
						weapon = Weapon(**w)
					# sometimes a weapon object sneaks in?
					except TypeError:
						log.debug(type(w))
						weapon = w
					more = True
					while more:
						# if there are no mods left
						nModsAvailable = sum([node.abstract_modifications[k] for k in node.abstract_modifications.keys()])
						if nModsAvailable < 1:
							print("No modifications to assign.")
							more = False
						# if there ARE mods left
						else:
							modLevels = []
							print(f"You have {nModsAvailable} modifications available to assign to your {weapon.name}. Choose a level:")
							for level in node.abstract_modifications.keys():
								if node.abstract_modifications[level] > 0:
									modLevels.append(level)
							modLevels.append("Done adding modifications to this weapon")
							i, levelSelection = chooseOne(modLevels)
							if levelSelection == False:
								return False
							elif levelSelection == "Done adding modifications to this weapon":
								more = False
								continue
							print(f"Choose a level {levelSelection} modification to add to your {weapon.name}:")
							modOptions = None
							modOptions = node.ref_modifications[levelSelection]
							modOptions = [m for m in modOptions if any([(p == weapon.type) for p in m.prerequisites])]
							modOptions.append("No modification")
							i,modSelection = chooseOne(modOptions)
							if modSelection == False:
								return False
							elif modSelection == "No modification":
								continue
							modRes = modSelection.apply(weapon)
							if not modRes:
								print("Modification not applied.")
							else:
								print(f"Successfully applied {modSelection.name} to {weapon.name}!")
								node.abstract_modifications[levelSelection] -= 1
					print("Finished adding modifications to this weapon.")
					if getYesNo(f"Rename this weapon from '{weapon.name}'?"):
						weapon.name = input("Enter new name:\n# ")
						print(f"Successfully renamed to '{weapon.name}'.")
					node.weapons.append(weapon)
				# check for unassigned mods
				if sum([node.abstract_modifications[k] for k in node.abstract_modifications.keys()]) >0:
					log.warning(f"You have {sum([node.abstract_modifications[k] for k in node.abstract_modifications.keys()])} unassigned modifications remaining!")
				print("All weapon modifications assigned. Moving on.")
				# AMMUNITION
				for level in node.abstract_ammunition.keys():
					ammunitionOptions = node.ref_ammunition[level]
					while node.abstract_ammunition[level] > 0:
						print(f"Choose {node.abstract_ammunition[level]} more round(s) of ammunition:") # NOTE: no level for ammo. Default "B"
						intSelection,selection = chooseOne(ammunitionOptions)
						if selection == False:
							return False
						else:
							node.gear.append(selection)
							node.abstract_ammunition[level] -= 1
				# POTIONS
				for level in node.abstract_potions.keys():
					potionOptions = node.ref_potions[level]
					while node.abstract_potions[level] > 0:
						print(f"Choose {node.abstract_potions[level]} more level {level} potion(s):")
						intSelection,selection = chooseOne(potionOptions)
						if selection == False:
							return False
						else:
							node.gear.append(selection)
							node.abstract_potions[level] -= 1
				# GRENADES
				for level in node.abstract_grenades.keys():
					grenadeOptions = node.ref_grenades[level]
					while node.abstract_grenades[level] > 0:
						print(f"Choose {node.abstract_grenades[level]} more level {level} grenades(s):")
						intSelection,selection = chooseOne(grenadeOptions)
						if selection == False:
							return False
						else:
							node.gear.append(selection)
							node.abstract_grenades[level] -= 1
				# KITS
				for level in node.abstract_kits.keys():
					kitOptions = node.ref_kits[level]
					while node.abstract_kits[level] > 0:
						print(f"Choose {node.abstract_kits[level]} more kits(s):") # NOTE: no level for kits. Default "A"
						intSelection,selection = chooseOne(kitOptions)
						if selection == False:
							return False
						else:
							node.gear.append(selection)
							node.abstract_kits[level] -= 1

				# Finally, apply this node
				character_sheet.apply(node)
				character_sheet.data.append(node)
			if len(node.children) > 0:
				if node.category is not None:
					print(f"Selection opens up new options.")
				print(f"Choose a {node.children_category}:")
				intChoice,selection = chooseOne(node.children)
				if selection == False:
					return False
				if not selection.checkPrerequisites(character_sheet):
					log.warning("Prerequisites violation! Try again.")
					return self.runTree(node,character_sheet,retry=True)
				character_sheet.treePath.append(intChoice)
				return self.runTree(selection,character_sheet)
			else:
				print("Done with this choice tree! Moving on.")
			return True
		except:
			log.exception(f"Failed in {node.name}")
			return False

	def createNewCharacter(self)->bool:
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
		return True

	def saveCharacter(self,file_path) -> bool:
		"""Wrapper for self.sheet.save"""
		self.sheet.save(file_path)
		print(f"Successfully saved character data to {file_path}!")
		return True

	def loadCharacter(self,file_path) -> bool:
		"""Imports previously created character from file"""
		self.sheet = CharacterSheet()
		print(f"Loading an existing character from file.\nSource file: {file_path}")
		self.sheet.load(file_path)
		print(f"Successfully loaded character '{self.sheet.choice_names['Name']}' from file!")
		return True

	def editCharacter(self) -> bool:
		"""Wrapper for self.sheet.edit"""
		result = self.sheet.edit()
		if not result:
			log.error("Edit failed in CharacterSheet object")
		return result

	def printCharacter(self,path) -> bool:
		"""Wrapper for self.sheet.save"""
		self.sheet.output(path)
		print(f"Successfully output character sheet to PDF!")
		return True

	def menu(self) -> None:
		"""menu function

		Choices
		-------
		new
		load
		save
		edit
		print
		exit
		"""
		MenuOption = namedtuple("MenuOption",["name","function","args"])
		menu_options = []
		menu_options.append(MenuOption("Create New Character",self.createNewCharacter,[]))
		menu_options.append(MenuOption("Load Character from File",self.loadCharacter,["path to input character data file"]))
		menu_options.append(MenuOption("Save Character",self.saveCharacter,["path to output character data file"]))
		menu_options.append(MenuOption("Edit Character",self.editCharacter,[]))

		menu_options.append(MenuOption("Output Character Sheet to PDF",self.printCharacter,["path to output PDF file"]))
		menu_options.append(MenuOption("Exit (or type 'exit')",sys.exit,[]))

		currentName = self.sheet.choice_names['Name'] if len(self.sheet.choice_names['Name']) > 0 else "None"
		print(f"\nMAIN MENU\n---------\nCurrent character: {currentName}\nChoose an option:")
		selection = chooseOne(menu_options,exit_message="Exit character creator?")[1]
		if selection == False:
			sys.exit()
		args = []
		for a in selection.args:
			args.append(input(f"Enter {a}:\n{PROMPT}"))
		try:
			if not selection.function(*args):
				log.error(f"Failed to {selection.name}")
		except SystemExit:
			sys.exit()
		except Exception as e:
			log.exception(f"Failed to {selection.name}")
			log.debug(e)
		self.menu()
