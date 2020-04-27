import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import math
from fpdf import FPDF

class SheetMaker:
	"""A class for producing beautiful character sheets

	***

	Methods
	-------
	make: None
		Saves a character sheet to 
	"""
	def __init__(self):
		self.sheet = None

	def read(self,character_sheet):
		self.sheet = character_sheet

	def make(self,out_path) -> None:
		"""Print self.sheet to a beautiful PDF file

		***

		Parameters
		----------
		out_path: str
			Path on disk where sheet will be created.
			Must end in .pdf extension. If the file
			exists already, it will be overwritten.
		"""

		######
		# meta
		######

		pdf = FPDF("p","in","Letter")
		pdf.add_page()
		pdf.set_margins(0,0,0)
		pdf.set_fill_color(0,0,0)
		pdf.set_auto_page_break(False)
		pdf.set_font('Arial',size=12)



		#############
		# blank sheet
		#############

		# add logo
		pdf.set_xy(0.62,0.53)
		pdf.image(os.path.join(os.path.dirname(os.path.dirname(__file__)),"resources","shrike_logo_1.png"),w=0.54)

		# add title
		## set title font
		pdf.set_font('Arial',size=24,style="BI")
		## draw title box
		pdf.set_xy(1.16,0.53)
		pdf.cell(2.46,0.53,"Era of Silence",align="C")

		# add choice_names box
		# set font
		# box outline
		pdf.set_xy(3.62,0.62)
		pdf.cell(4.26,1.14,border=1)
		# species
		pdf.set_font('Times',size=8,style="I")
		pdf.set_xy(3.75,1)
		pdf.cell(1.11,0.13,"Species",align="C")
		# training
		pdf.set_font('Times',size=8,style="I")
		pdf.set_xy(3.75,1.5)
		pdf.cell(1.11,0.13,"Training",align="C")
		# background
		## label
		pdf.set_font('Times',size=8,style="I")
		pdf.set_xy(5.13,1)
		pdf.cell(1.11,0.13,"Background",align="C")
		# focus
		pdf.set_font('Times',size=8,style="I")
		pdf.set_xy(5.13,1.5)
		pdf.cell(1.11,0.13,"Focus",align="C")
		# motivation
		pdf.set_font('Times',size=8,style="I")
		pdf.set_xy(6.55,1)
		pdf.cell(1.11,0.13,"Motivation",align="C")
		# combat_specialty
		pdf.set_font('Times',size=8,style="I")
		pdf.set_xy(6.55,1.5)
		pdf.cell(1.11,0.13,"Combat Specialty",align="C")

		# add 'name' box
		## box border
		pdf.set_xy(0.62,1.14)
		pdf.cell(2.76,0.64,border=1,align="C")
		## label
		pdf.set_font('Times',size=10,style="I")
		pdf.set_xy(1.8,1.59)
		pdf.cell(0.37,0.15,"Name",align="C")

		# set box label font
		pdf.set_font('Times',size=12,style="B")

		# add 'quality' box
		## bounding box
		pdf.set_xy(0.62,2.02)
		pdf.cell(0.89,3.39,border=1)
		## label
		pdf.set_xy(0.64,2.04)
		pdf.cell(0.8,0.2,"Qualities")
		## individual quality boxes
		pdf.set_font('Times',size=8,style="I")
		### brawn
		pdf.set_xy(0.74,2.39)
		pdf.cell(0.63,0.64,border=1)
		pdf.set_xy(0.78,2.43)
		pdf.cell(0.34,0.12,"Brawn")
		### grace
		pdf.set_xy(0.74,3.14)
		pdf.cell(0.63,0.64,border=1)
		pdf.set_xy(0.78,3.18)
		pdf.cell(0.34,0.12,"Grace")
		### wits
		pdf.set_xy(0.74,3.89)
		pdf.cell(0.63,0.64,border=1)
		pdf.set_xy(0.78,3.93)
		pdf.cell(0.34,0.12,"Wits")
		### spirit
		pdf.set_xy(0.74,4.64)
		pdf.cell(0.63,0.64,border=1)
		pdf.set_xy(0.78,4.68)
		pdf.cell(0.34,0.12,"Spirit")

		# reset box label font
		pdf.set_font('Times',size=12,style="B")

		# add skills
		## box
		pdf.set_xy(1.75,2.02)
		pdf.cell(1.63,5.01,border=1)
		## label
		pdf.set_xy(1.77,2.04)
		pdf.cell(0.8,0.2,"Skills")

		# add trivia
		## box
		pdf.set_xy(0.62,5.52)
		pdf.cell(0.89,1.51,border=1)
		## label
		pdf.set_xy(0.64,5.54)
		pdf.cell(0.8,0.2,"Trivia")

		# add speed
		## box
		pdf.set_xy(3.62,2.02)
		pdf.cell(1.35,0.89,border=1)
		## label
		pdf.set_xy(3.62,2.02)
		pdf.cell(1.35,0.30,"Speed",align="C")

		# add AV
		## box
		pdf.set_xy(3.62,3.02)
		pdf.cell(1.35,0.89,border=1)
		## label
		pdf.set_xy(3.62,3.02)
		pdf.cell(1.35,0.30,"AV",align="C")

		# add Toughness
		## Box
		pdf.set_xy(3.62,4.02)
		pdf.cell(1.35,0.89,border=1)
		## label
		pdf.set_xy(3.62,4.02)
		pdf.cell(1.35,0.30,"Toughness",align="C")

		# add Fighting Die
		## box
		pdf.set_xy(3.62,5.02)
		pdf.cell(1.35,0.89,border=1)
		## label
		pdf.set_xy(3.62,5.02)
		pdf.cell(1.35,0.30,"Fighting Die",align="C")

		# add Shooting Die
		## box
		pdf.set_xy(3.62,6.02)
		pdf.cell(1.35,0.89,border=1)
		## label
		pdf.set_xy(3.62,6.02)
		pdf.cell(1.35,0.30,"Shooting Die",align="C")

		# add Weapons
		## box
		pdf.set_xy(0.62,7.18)
		w_total_width = 4.35
		pdf.cell(w_total_width,1.65,border=1)
		## label
		pdf.set_xy(0.64,7.2)
		pdf.cell(0.8,0.2,"Weapons")
		## column_titles
		pdf.set_font('Times',size=6,style="I")
		pdf.set_y(7.45)
		w_name_x = 0.62
		w_name_width = 0.82
		pdf.set_x(w_name_x)
		pdf.cell(w_name_width,0.11,"Name")
		w_range_x = w_name_x + w_name_width
		w_range_width = 0.48
		pdf.set_x(w_range_x)
		pdf.cell(w_range_width,0.11,"Range/Reach",align="C")
		w_accuracy_x = w_range_x + w_range_width
		w_accuracy_width = 0.35
		pdf.set_x(w_accuracy_x)
		pdf.cell(w_accuracy_width,0.11,"Accuracy",align="C")
		#w_ap_x = 2.28
		w_ap_x = w_accuracy_x+w_accuracy_width
		w_ap_width = 0.17
		pdf.set_x(w_ap_x)
		pdf.cell(w_ap_width,0.11,"AP",align="C")
		#pdf.set_x(2.34)
		w_special_width = w_total_width - (w_name_width+w_range_width+w_accuracy_width+w_ap_width)
		pdf.cell(w_special_width,0.11,"Special")

		# reset box label font
		pdf.set_font('Times',size=12,style="B")

		# add Money
		## box
		pdf.set_xy(0.62,9.02)
		pdf.cell(1.26,1.39,border=1)
		## label
		pdf.set_xy(0.64,9.04)
		pdf.cell(0.8,0.2,"Money")

		# add Gear
		## box
		pdf.set_xy(2,9.02)
		pdf.cell(3,1.39,border=1)
		## label
		pdf.set_xy(2.02,9.04)
		pdf.cell(0.8,0.2,"Gear")

		# add Traits
		## box
		pdf.set_xy(5.24,2.02)
		pdf.cell(2.64,8.39,border=1)
		## label
		pdf.set_xy(5.26,2.04)
		pdf.cell(0.8,0.2,"Traits")



		#########
		# Content
		#########

		# CHARACTER NAME
		maxWidth = 2.65
		fontSize = 20
		pdf.set_font('Arial',size=fontSize,style="")
		nameText = self.sheet.choice_names['Name']
		while pdf.get_string_width(nameText) > maxWidth:
			fontSize -= 0.1
			pdf.set_font('Arial',size=fontSize,style="")
		pdf.set_xy(0.62,1.23)
		pdf.cell(2.76,0.36,nameText,align="C")

		# CHOICE NAMES (upper right box)
		pdf.set_font('Arial',size=10,style="U")
		# Species
		pdf.set_xy(3.68,0.84)
		pdf.cell(1.25,0.15,self.sheet.choice_names['Species'],align="C")
		# training
		pdf.set_xy(3.68,1.34)
		pdf.cell(1.25,0.15,self.sheet.choice_names['Training'],align="C")
		# background
		pdf.set_xy(5.05,0.84)
		pdf.cell(1.25,0.15,self.sheet.choice_names['Background'],align="C")
		# focus
		pdf.set_xy(5.05,1.34)
		pdf.cell(1.25,0.15,self.sheet.choice_names['Focus'],align="C")
		# combat specialty
		pdf.set_xy(6.47,1.34)
		pdf.cell(1.25,0.15,self.sheet.choice_names['Combat Specialty'],align="C")
		# motivation
		## font has to scale because user input
		motivationText = self.sheet.choice_names['Motivation']
		fontSize = 10
		while pdf.get_string_width(motivationText) > 1.25:
			fontSize -= 0.1
			pdf.set_font('Arial',size=fontSize,style="U")
		## actually write the motivation text
		pdf.set_xy(6.47,0.84)
		pdf.cell(1.25,0.15,motivationText,align="C")


		# QUALITIES
		pdf.set_font('Arial',size=16,style="")
		### brawn
		pdf.set_xy(0.74,2.65)
		pdf.cell(0.63,0.31,str(self.sheet.qualities["Brawn"]),align="C")
		### grace
		pdf.set_xy(0.74,3.34)
		pdf.cell(0.63,0.31,str(self.sheet.qualities["Grace"]),align="C")
		### wits
		pdf.set_xy(0.74,4.11)
		pdf.cell(0.63,0.31,str(self.sheet.qualities["Wits"]),align="C")
		### spirit
		pdf.set_xy(0.74,4.86)
		pdf.cell(0.63,0.31,str(self.sheet.qualities["Spirit"]),align="C")

		# MIDDLE BOXES (combat_stats)
		## set font for speed
		pdf.set_font('Arial',size=16)
		## speed
		pdf.set_xy(3.62,2.33)
		pdf.cell(1.35,0.4,str(self.sheet.combat_stats["Speed"]),align="C")
		## set font for rest
		pdf.set_font('Arial',size=25)
		## AV
		pdf.set_xy(3.62,3.33)
		pdf.cell(1.35,0.4,str(self.sheet.combat_stats["AV"]),align="C")
		## toughness
		pdf.set_xy(3.62,4.33)
		pdf.cell(1.35,0.4,str(self.sheet.combat_stats["Toughness"]),align="C")
		## fighting die
		pdf.set_xy(3.62,5.33)
		pdf.cell(1.35,0.4,str(self.sheet.combat_stats["Fighting Die"]),align="C")
		## shooting die
		pdf.set_xy(3.62,6.33)
		pdf.cell(1.35,0.4,str(self.sheet.combat_stats["Shooting Die"]),align="C")

		# SKILLS
		pdf.set_xy(1.77,2.32)
		for s in self.sheet.skills.keys():
			# add skill name
			pdf.set_font('Times',size=8)
			pdf.set_x(1.77)
			sLevel = self.sheet.skills[s]['level']
			sQual = self.sheet.skills[s]['quality']
			sDie = str(self.sheet.qualities[sQual])
			sContent = f"{s} ({sQual})"
			pdf.cell(pdf.get_string_width(sContent),0.22,sContent)
			# add player dice
			pdf.set_font('Arial',size=8)
			pdf.set_x(3)
			sContent = f"{sLevel}{sDie}"
			pdf.cell(0.3,0.22,sContent,ln=1,align="R")
			#pdf.cell(pdf.get_string_width(sContent),0.22,sContent,ln=1,fill=True)

		# TRIVIA
		pdf.set_font('Arial',size=8,style='')
		pdf.set_y(5.82)
		for t in self.sheet.trivia:
			pdf.set_x(0.64)
			pdf.multi_cell(0.83,0.11,"* "+t,align="L")
			pdf.ln(.02)

		# TRAITS
		pdf.set_y(2.35)
		for t in self.sheet.traits:
			# trait name
			pdf.set_x(5.26)
			pdf.set_font('Arial',size=10,style='B')
			pdf.cell(2.35,0.2,t['Name'],ln=1)
			# trait description
			pdf.set_x(5.26)
			pdf.set_font('Arial',size=10,style='')
			pdf.multi_cell(2.35,0.15,t['Description'],align="L")
			pdf.ln()

		# GEAR
		pdf.set_font('Arial',size=10,style='')
		# pdf.set_y(9.35)
		# for item in self.sheet.gear:
		# 	pdf.set_x(2.02)
		# 	pdf.multi_cell(2.35,0.11,item,align="L")
		# 	pdf.ln(.02)
		pdf.set_xy(2.02,9.26)
		pdf.multi_cell(2.85,0.19,", ".join(self.sheet.gear).strip(","),align="L")

		# MONEY
		pdf.set_font('Arial',size=10,style='')
		pdf.set_xy(0.64,9.26)
		pdf.cell(1.16,0.15,f"SA: {self.sheet.money}")

		# WEAPONS
		## make vertical lines
		line_height = 1.26
		pdf.set_y(7.57)
		### name_border
		pdf.set_x(w_name_x)
		pdf.cell(w_name_width,line_height,border="R")
		### range_border
		pdf.set_x(w_range_x)
		pdf.cell(w_range_width,line_height,border="R")
		### accuracy_border
		pdf.set_x(w_accuracy_x)
		pdf.cell(w_accuracy_width,line_height,border="R")
		### ap_border
		pdf.set_x(w_ap_x)
		pdf.cell(w_ap_width,line_height,border="R")
		## add each weapon
		pdf.set_font('Arial',size=8,style='')
		### calculate how to share vertical space
		size_index = [] # list of dicts: {"textLen":int,"textPct":int,"fontPoint":int,"cellY":int}
		totalTextLen = 0
		maxTotalHeight = 1.25
		special_cell_width = w_special_width
		for weapon in self.sheet.weapons: # individual info
			if len(weapon.special) > 0:
				specials = " ".join(weapon.special) 
			else:
				specials = " "
			textLen = pdf.get_string_width(specials)
			if textLen < special_cell_width:
				textLen = special_cell_width
			totalTextLen += textLen
			size_index.append({"text":specials,"textLen":textLen,"textPct":1.0,"maxHeight":0,"fontPoint":8,"cellY":0.11})
		for d in size_index:
			d['textPct'] = d['textLen']/totalTextLen
			d['maxHeight'] = d['textPct'] * maxTotalHeight
		for d in size_index:
			fits = False
			while not fits:
				fake_pdf = FPDF("p","in","Letter")
				fake_pdf.add_page()
				fake_pdf.set_margins(0,0,0)
				fake_pdf.set_fill_color(0,0,0)
				fake_pdf.set_auto_page_break(False)
				fake_pdf.set_font('Arial',size=d["fontPoint"])
				## DO CALC
				fake_pdf.set_xy(1,1)
				fake_pdf.multi_cell(special_cell_width,d['cellY'],d['text'])
				if fake_pdf.get_y() - 1 <= d['maxHeight']:
					fits = True
				else:
					d['fontPoint'] = d['fontPoint'] - 0.01
				del fake_pdf
			d['cellY'] = d["fontPoint"] / 72

		### do the writing
		i = 0
		for weapon in self.sheet.weapons: # each one is a Weapon object
			# name
			font_size = 8
			pdf.set_font('Arial',size=font_size,style='')
			while pdf.get_string_width(weapon.name) > (w_name_width-0.1):
				font_size -= 0.05
				pdf.set_font('Arial',size=font_size,style='')
			pdf.set_x(w_name_x)
			pdf.cell(w_name_width,0.12,weapon.name,align="L",border="T")
			# range / reach
			pdf.set_font('Arial',size=8,style='')
			if (weapon.range is None) or (weapon.range <= 0):
				r =weapon.reach
			else:
				r = weapon.range
			pdf.set_x(w_range_x)
			pdf.cell(w_range_width,0.12,str(r),align="C",border="T")
			# accuracy
			if weapon.accuracy == 0:
				acc = "NA"
			else:
				acc = weapon.accuracy
			pdf.set_x(w_accuracy_x)
			pdf.cell(w_accuracy_width,0.12,str(acc),align="C",border="T")
			# ap
			pdf.set_x(w_ap_x)
			pdf.cell(w_ap_width,0.12,str(weapon.ap),align="C",border="T")
			# special 
			index = size_index[i] # get meta-info about size calculated above
			specials = index['text']
			font_size = index['fontPoint']
			row_height = index['cellY']
			cell_width = special_cell_width
			pdf.set_font('Arial',size=font_size,style='')
			# METHOD A
			# if len(weapon.special) > 0:
			# 	specials = " ".join(weapon.special) 
			# else:
			# 	specials = " "
			# specials = specials.strip()
			# max_height = 0.2
			# line_length_adjust_factor = 0.05
			# fits = False
			# pdf_fake = FPDF()
			# pdf_fake.add_page()
			# pdf_fake.set_margins(0,0,0)
			# pdf_fake.set_fill_color(0,0,0)
			# pdf_fake.set_auto_page_break(False)
			# while not fits:
			# 	pdf_fake.set_font('Arial',size=font_size,style='')
			# 	pdf_fake.set_xy(2.34,1.0)
			# 	pdf_fake.multi_cell(cell_width,row_height,specials,border="T")
			# 	diff = pdf_fake.get_y() - 1.0
			# 	if diff <= max_height:
			# 		fits = True
			# 	else:
			# 		font_size = font_size * 0.99
			# 		row_height = row_height * 0.99
			# pdf.set_font('Arial',size=font_size,style='')
			# print(font_size)
			# print(row_height)
			# del pdf_fake
			# METHOD B
			# while math.ceil(((pdf.get_string_width(specials)+(line_length_adjust_factor*2))/cell_width)) * row_height > max_height:
			# 	font_size = font_size * 0.99
			# 	row_height = row_height * 0.99
			# 	pdf.set_font('Arial',size=font_size,style='')
			# END METHODS
			pdf.multi_cell(cell_width,row_height,specials,border="T")
			pdf.ln(0.05)
			i += 1


		########	
		# output
		########

		# write result to file
		pdf.output(out_path)