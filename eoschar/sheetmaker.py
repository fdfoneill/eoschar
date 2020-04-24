import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

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
		"""Make the sheet

		***

		Parameters
		----------
		out_path: str
			Path on disk where sheet will be created
		"""
		pdf = FPDF("p","in","Letter")
		pdf.add_page()
		pdf.set_margins(0,0,0)
		pdf.set_auto_page_break(False)
		pdf.set_font('Arial',size=12)

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
		pdf.set_xy(4.12,1.02)
		pdf.cell(0.37,0.13,"Species",align="C")
		# training
		pdf.set_font('Times',size=8,style="I")
		pdf.set_xy(4.12,1.02)
		pdf.cell(0.37,0.13,"Training",align="C")
		# background
		## label
		pdf.set_font('Times',size=8,style="I")
		pdf.set_xy(4.12,1.02)
		pdf.cell(0.37,0.13,"Background",align="C")
		# focus
		pdf.set_font('Times',size=8,style="I")
		pdf.set_xy(4.12,1.02)
		pdf.cell(0.37,0.13,"Focus",align="C")
		# motivation
		pdf.set_font('Times',size=8,style="I")
		pdf.set_xy(4.12,1.02)
		pdf.cell(0.37,0.13,"Motivation",align="C")
		# combat_specialty
		pdf.set_font('Times',size=8,style="I")
		pdf.set_xy(4.12,1.02)
		pdf.cell(0.37,0.13,"Combat Specialty",align="C")

		# add name
		## box
		pdf.set_xy(0.62,1.14)
		pdf.cell(2.76,0.64,border=1,align="C")
		## label
		pdf.set_font('Times',size=10,style="I")
		pdf.set_xy(1.8,1.59)
		pdf.cell(0.37,0.15,"Name",align="C")

		# set box label font
		pdf.set_font('Times',size=12,style="B")

		# add quality box
		## box
		pdf.set_xy(0.62,2.02)
		pdf.cell(0.89,3.39,border=1)
		## label
		pdf.set_xy(0.64,2.04)
		pdf.cell(0.8,0.2,"Qualities")

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
		pdf.cell(4.35,1.65,border=1)
		## label
		pdf.set_xy(0.64,7.2)
		pdf.cell(0.8,0.2,"Weapons")

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

		# recursively add SKILLS
		pdf.set_xy(1.77,2.32)
		pdf.set_font('Times',size=8)
		for s in self.sheet.skills.keys():
			pdf.set_x(1.77)
			sLevel = self.sheet.skills[s]['level']
			sQual = self.sheet.skills[s]['quality']
			sDie = str(self.sheet.qualities[sQual])
			# add skill name / linked quality
			sContent = f"{s} ({sQual})"
			pdf.cell(1.41,0.22,sContent)
			# add player dice
			pdf.set_x(2.82)
			sContent = f"{sLevel}{sDie}"
			pdf.cell(0.6,0.22,sContent,ln=1)

		# output result
		pdf.output(out_path)