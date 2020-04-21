import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

from .choice import Choice, Species, Training, Trait, Item
from .weapon import Weapon
from .dietype import DieType
from .func import getModel

##############
# species tree
##############

species_model = getModel("model_species.json")
species = Choice(name="Species",children_category="Species",root_id=1)

# human
human = Species(name="Human",children_category="Species Trait",base_qualities=species_model['Human']['base_qualities']) # root choice
## add race traits
for q in getModel("model_qualities.json"): # add all human traits
	pwg = Trait(name=f"People of the Wandering God ({q})",description=f"Improve {q} die type by 1 (already included).")
	pwg.addImplementation(lambda character_sheet: character_sheet.qualities[q].improve())
	human.addChild(pwg)
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

# cascade
species.cascadeRootId()
species.cascadeChildrenCategory()


########
# talent 
########

talent = Choice(name="Talent",children_category="Talent",root_id=2)
# add individual talents
for q in getModel("model_qualities.json"): # add all human traits
	tlnt = Choice(name=q)
	tlnt.addImplementation(lambda character_sheet: character_sheet.qualities[q].improve())
	talent.addChild(tlnt)
# cascade
talent.cascadeRootId()
talent.cascadeChildrenCategory()


##########
# training
##########

training = Choice(name="Training",children_category="Training",root_id=3)

# martial
martial = Training(name="Martial",children_category="Gear Option",skill="Athletics")
## add default gear
martial.addImplementation(lambda character_sheet: character_sheet._abstract_potions.update(['B'],character_sheet._abstract_potions['B']+1))
## add gear choices
martial.addChild(Item(name="Choose 3 rounds of alchemical ammunition",abstract=True,gear_type="ammunition",level="C",n=3))
martial.addChild(Item(name="Choose 1 level B grenade",abstract=True,gear_type="grenade",level="B",n=1))
martial.addChild(Item(name="Choose 1 level A weapon modification",abstract=True,gear_type="modification",level="A",n=1))
## add as a child to training
training.addChild(martial)

# underworld
underworld = Training(name="Underworld",children_category="Gear Option",skill="Lie",gear=["Smoke Grenade"])
## add default gear
underworld.addImplementation(lambda character_sheet: character_sheet._abstract_potions.update(['B'],character_sheet._abstract_potions['B']+3))
## add gear choices
ugc1 = Item(name="A blade with the chem-pipes modification and choose 3 rounds of alchemical ammunition",abstract=False,gear_type="custom")
ugc1.addImplementation(lambda character_sheet: character_sheet.weapons.append(Weapon(name="Poison Blade",reach=1,ap=1,special="This weapon may take alchemical ammunition as if it were a ranged weapon."))) # blade with chem-pipes
ugc1.addImplementation(lambda character_sheet: character_sheet._abstract_ammunition.update(['A'],character_sheet._abstract_ammunition['A']+3)) # 3 rounds of alchemical ammunition
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
technology.addImplementation(lambda character_sheet: character_sheet._abstract_potions.update(['B'],character_sheet._abstract_potions['B']+1))
technology.addImplementation(lambda character_sheet: character_sheet._abstract_grenades.update(['B'],character_sheet._abstract_grenades['B']+1))
## add gear choices
technology.addChild(Item(name="A Personal Shield Generator",item_name="Personal Shield Generator"))
tgc2 = Choice(name="Choose a ranged weapon with 1 level B modification")
tgc2.addChild(Item(name="Pistol",gear_type="weapon"))
tgc2.addChild(Item(name="Long Arm",gear_type="weapon"))
tgc2.addImplementation(lambda character_sheet: character_sheet._abstract_modifications.update(['B'],character_sheet._abstract_modifications['B']+1))
technology.addChild(tgc2)

## add as child to training
training.addChild(technology)

# cascade
training.cascadeRootId()
training.cascadeChildrenCategory()

#######
# focus
#######

focus = Choice(name="Focus",children_category="Focus",root_id=4)


##################
# combat specialty
##################

combat_specialty = Choice(name="Combat Specialty",children_category="Combat Specialty",root_id=5)


############
# background
############

background = Choice(name="Background",children_category="Background",root_id=6)