import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import copy
from .choice import Choice, Species, Training, Focus, CombatSpecialty, Background, TextInput, Trait, Item, PointBuy, AssignAbstractGear
from .weapon import Weapon
from .dietype import DieType
from .func import getModel

trees = []

#########
# species
#########

species_model = getModel("model_species.json")
species = Choice(name="Species",children_category="Species",root_id=1)

# human
human = Species(name="Human",children_category="Species Trait",base_qualities=species_model['Human']['base_qualities']) # root choice
## add race traits
# for q in getModel("model_qualities.json"): # add all human traits
# 	# pwg = Trait(name=f"People of the Wandering God ({q})",description=f"Improve {q} die type by 1 (already included).")
# 	# pwg.addImplementation(lambda character_sheet: character_sheet.qualities[q].improve())
# 	# human.addChild(pwg)
# 	human.addChild(Trait(name=f"People of the Wandering God ({q})",description=f"Improve {q} die type by 1 (already included).",implementation=lambda character_sheet: character_sheet.qualities[f"{q}"].improve()))
### brawn
human.addChild(Trait(name=f"People of the Wandering God (Brawn)",description=f"Improve Brawn die type by 1 (already included).",implementation=lambda character_sheet: character_sheet.qualities["Brawn"].improve()))
### grace
human.addChild(Trait(name=f"People of the Wandering God (Grace)",description=f"Improve Grace die type by 1 (already included).",implementation=lambda character_sheet: character_sheet.qualities["Grace"].improve()))
### wits
human.addChild(Trait(name=f"People of the Wandering God (Wits)",description=f"Improve Wits die type by 1 (already included).",implementation=lambda character_sheet: character_sheet.qualities["Wits"].improve()))
### spirit
human.addChild(Trait(name=f"People of the Wandering God (Spirit)",description=f"Improve Spirit die type by 1 (already included).",implementation=lambda character_sheet: character_sheet.qualities["Spirit"].improve()))
## add as child to species
species.addChild(human)

# elek
elek = Species(name="Elek",children_category="Species Trait",base_qualities=species_model['Elek']['base_qualities']) # root choice
## add race traits
for t in species_model['Elek']["Species Traits"]:
	trait = Trait(name=t["name"],description=t['description'])
	elek.addChild(trait)
## add as a child to species
species.addChild(elek)

# parathan
parathan = Species(name="Parathan",children_category="Species Trait",base_qualities=species_model['Parathan']['base_qualities']) # root choice
## add race traits
for t in species_model['Parathan']["Species Traits"]:
	trait = Trait(name=t["name"],description=t['description'])
	parathan.addChild(trait)
## add as a child to species
species.addChild(parathan)

# primas-ika
primas_ika = Species(name="Primas-Ika",children_category="Species Trait",base_qualities=species_model['Primas-Ika']['base_qualities']) # root choice
## add race traits
for t in species_model['Primas-Ika']["Species Traits"]:
	trait = Trait(name=t["name"],description=t['description'])
	primas_ika.addChild(trait)
## add as a child species
species.addChild(primas_ika)

# yasre
yasre = Species(name="Yasre",children_category="Species Trait",base_qualities=species_model['Yasre']['base_qualities']) # root choice
## add race traits
for t in species_model['Yasre']["Species Traits"]:
	trait = Trait(name=t["name"],description=t['description'])
	yasre.addChild(trait)
## add as a child to species
species.addChild(yasre)

# cascade and append
species.cascadeRootId()
species.cascadeChildrenCategory()
trees.append(species)


########
# talent 
########

talent = Choice(name="Talent",children_category="Talent",root_id=2)

# add individual talents
## talent prerequisite factory
def make_tlnt_preq(qual):
	def tlnt_preq(character_sheet):
		for choice in character_sheet.data:
			if choice.name == f"People of the Wandering God ({qual})":
				return False
		return True
	return tlnt_preq
## brawn
talent.addChild(Choice(name="Brawn",implementation=lambda character_sheet: character_sheet.qualities["Brawn"].improve(),prerequisites=[make_tlnt_preq("Brawn")]))
## grace
talent.addChild(Choice(name="Grace",implementation=lambda character_sheet: character_sheet.qualities["Grace"].improve(),prerequisites=[make_tlnt_preq("Grace")]))
## wits
talent.addChild(Choice(name="Wits",implementation=lambda character_sheet: character_sheet.qualities["Wits"].improve(),prerequisites=[make_tlnt_preq("Wits")]))
## spirit
talent.addChild(Choice(name="Spirit",implementation=lambda character_sheet: character_sheet.qualities["Spirit"].improve(),prerequisites=[make_tlnt_preq("Spirit")]))

# cascade and append
talent.cascadeRootId()
talent.cascadeChildrenCategory()
trees.append(talent)


#####################
# shooting & fighting
#####################

shooting_fighting = Choice(name="Shooting and Fighting Dice",children_category="Die to Boost",root_id=3)

# shooting die
shooting_fighting.addChild(Choice(name="Shooting Die",implementation = lambda character_sheet: character_sheet.combat_stats["Shooting Die"].improve()))

# fighting die
shooting_fighting.addChild(Choice(name="Fighting Die",implementation = lambda character_sheet: character_sheet.combat_stats["Fighting Die"].improve()))

# cascade and append
shooting_fighting.cascadeRootId()
shooting_fighting.cascadeChildrenCategory()
trees.append(shooting_fighting)


##########
# training
##########

training = Choice(name="Training",children_category="Training",root_id=4)

# martial
martial = Training(name="Martial",children_category="Gear Option",skill="Athletics")
## add default gear
martial.addImplementation(lambda character_sheet: character_sheet._abstract_potions.update({'B':character_sheet._abstract_potions['B']+1}))
## add gear choices
martial.addChild(Item(name="Choose 3 rounds of alchemical ammunition",abstract=True,gear_type="ammunition",level="C",n=3))
martial.addChild(Item(name="Choose 1 level B grenade",abstract=True,gear_type="grenade",level="B",n=1))
martial.addChild(Item(name="Choose 1 level A weapon modification",abstract=True,gear_type="modification",level="A",n=1))
## add as a child to training
training.addChild(martial)

# underworld
underworld = Training(name="Underworld",children_category="Gear Option",skill="Lie",gear=["Smoke Grenade"])
## add default gear
underworld.addImplementation(lambda character_sheet: character_sheet._abstract_potions.update({'B':character_sheet._abstract_potions['B']+3}))
## add gear choices
ugc1 = Item(name="A blade with the chem-pipes modification and choose 3 rounds of alchemical ammunition",abstract=False,gear_type="custom")
ugc1.addImplementation(lambda character_sheet: character_sheet.weapons.append(Weapon(name="Poison Blade",reach=1,ap=1,special="This weapon may take alchemical ammunition as if it were a ranged weapon."))) # blade with chem-pipes
ugc1.addImplementation(lambda character_sheet: character_sheet._abstract_ammunition.update({'A':character_sheet._abstract_ammunition['A']+3})) # 3 rounds of alchemical ammunition
underworld.addChild(ugc1) # add the complicated choice as a child
underworld.addChild(Item(name="Sniper Rifle",gear_type="weapon"))
## add as a child to training
training.addChild(underworld)

# magic
magic = Training(name="Magic",children_category="Gear Option",skill="Resist Mental")
## add gear choices
magic.addChild(Item(name="3 doses of Wizard's Select",item_name="Wizard's Select",gear_type="potion",n=3))
magic.addChild(Item(name="3 smoke grenades",item_name="Smoke Grenade",gear_type="grenade",n=3))
## add as child to training
training.addChild(magic)

# technology
technology = Training(name="Technology",children_category="Gear Option",skill="Interface")
## add default gear
technology.addImplementation(lambda character_sheet: character_sheet._abstract_potions.update({'B':character_sheet._abstract_potions['B']+1}))
technology.addImplementation(lambda character_sheet: character_sheet._abstract_grenades.update({'B':character_sheet._abstract_grenades['B']+1}))
## add gear choices
technology.addChild(Item(name="A Personal Shield Generator",item_name="Personal Shield Generator"))
tgc2 = Choice(name="Choose a ranged weapon with 1 level B modification")
tgc2.addChild(Item(name="Pistol",gear_type="weapon"))
tgc2.addChild(Item(name="Long Arm",gear_type="weapon"))
tgc2.addImplementation(lambda character_sheet: character_sheet._abstract_modifications.update({'B':character_sheet._abstract_modifications['B']+1}))
technology.addChild(tgc2)

## add as child to training
training.addChild(technology)

# cascade and append
training.cascadeRootId()
training.cascadeChildrenCategory()
trees.append(training)


#######
# focus
#######

focus = Choice(name="Focus",children_category="Focus",root_id=5)

# add individual foci
for f in getModel('model_focus.json'):
	focus.addChild(Focus(name=f['name'],skills=f['skills'],trait=f['trait']))

# cascade and append
focus.cascadeRootId()
focus.cascadeChildrenCategory()
trees.append(focus)


########
# skills
########

# How to implement skills? They don't fit well in the framework of tree-choices. You must be able to see the skills
# you already have, because you're forbidden from going over a certain number of levels. But skills don't get added
# up from Training and Focus until the implementation stage. What to do?

# Maybe: implement() each Choice *as* it's being added to CharacterSheet.data? Also could checkPrerequisites() at that
# time. Then, when actually fully building, you flush() the sheet, which reloads it cleanly.

skills = PointBuy(name="Skills",max_level=3,starting_level=1,point_per_level = {2:1,3:3},categories=getModel('model_skills.json'),root_id=6)
trees.append(skills)


##################
# combat specialty
##################

combat_specialty = Choice(name="Combat Specialty",children_category="Combat Specialty",root_id=7)
model = getModel('model_combat_specialty.json')

# close combat
cso1 = CombatSpecialty(**model['Close Combat'],children_category= "Gear Option")
cso1.addChild(Item(name="2 level A modifications",level="A",n=2,gear_type="modification",abstract=True))
cso1.addChild(Item(name="1 level B modification",level="B",n=1,gear_type="modification",abstract=True))
# add as child to combat_specialty
combat_specialty.addChild(cso1)

# ranged
cso2 = CombatSpecialty(**model['Ranged'],children_category= "Gear Option")
# sub-option 1
cso2_o1 = Item(name="Long Arm and choice of modifications",n=1,gear_type="weapon",item_name="Long Arm",abstract=True,children_category= "Gear Sub-Option")
cso2_o1.addChild(Item(name="2 level A modifications",level="A",n=2,gear_type="modification",abstract=True))
cso2_o1.addChild(Item(name="1 level B modification",level="B",n=1,gear_type="modification",abstract=True))
cso2.addChild(cso2_o1)
# sub-option 2
cso2.addChild(Item(name="Sniper Rifle",n=1,gear_type="weapon"))
# add as child to combat_specialty
combat_specialty.addChild(cso2)

# tactician
cso3 = CombatSpecialty(**model['Tactician'],children_category= "Gear Option")
cso3.addImplementation(lambda character_sheet: character_sheet._abstract_weapons.update({'Any':character_sheet._abstract_weapons['Any'] + 1}))
cso3.addChild(Item(name="2 level A modifications",level="A",n=2,gear_type="modification",abstract=True))
cso3.addChild(Item(name="1 level B modification",level="B",n=1,gear_type="modification",abstract=True))
# add as child to combat_specialty
combat_specialty.addChild(cso3)

# healer
cso4 = CombatSpecialty(**model['Healer'],children_category= "Gear Option")
cso4.addChild(Item(name="Long Arm",abstract=True,gear_type="weapon"))
cso4_o2 = Item(name="Melee Weapon (Blade or Hammer)",gear_type="custom")
cso4_o2.addImplementation(lambda character_sheet: character_sheet._abstract_weapons.update({'Melee':character_sheet._abstract_weapons['Melee'] + 1}))
cso4.addChild(cso4_o2)
# add as child to combat_specialty
combat_specialty.addChild(cso4)

# cascade and append
combat_specialty.cascadeRootId()
combat_specialty.cascadeChildrenCategory()
trees.append(combat_specialty)


############
# background
############

background = Choice(name="Background",children_category="Background",root_id=8)

# add individual backgrounds
for b in getModel('model_background.json'):
	background.addChild(Background(**b))

# cascade and append
background.cascadeRootId()
background.cascadeChildrenCategory()
trees.append(background)


########
# trivia
########

trivia = PointBuy(name="Trivia",max_level=1,starting_level=0,point_per_level = {1:1},categories=getModel('model_trivia.json'),root_id=9)
trees.append(trivia)


############
# motivation
############

motivation = TextInput(name="Motivation",root_id=10)

# append
trees.append(motivation)


#########################
# assigning abstract gear
#########################

assign_abstract_gear = AssignAbstractGear(name="Assign Abstract Gear",root_id=11)

# append
trees.append(assign_abstract_gear)


######
# name
######

charName = TextInput(name="Name",root_id=12)

# append
trees.append(charName)