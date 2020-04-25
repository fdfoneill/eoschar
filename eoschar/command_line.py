import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import sys
from .charactersheet import CharacterSheet
from .choice import Choice, Item
from .options import trees as TREES
from .interface import Interface
from .sheetmaker import SheetMaker
from ._version import __version__
import argparse


def makeExample():
	maker = SheetMaker()
	sheet = CharacterSheet()
	sheet.load('/Users/DanO/Documents/Games/Design/char_builder_v4/eoschar/temp/example_saved_character.txt')
	maker.read(sheet)
	maker.make(os.path.join(os.path.dirname(os.path.dirname(__file__)),"temp","example_output_sheet.pdf"))


def main():
	parser = argparse.ArgumentParser(description="Create, save, and export Era of Silence characters")
	## use subparsers https://pymotw.com/3/argparse/#nesting-parsers

	subparsers = parser.add_subparsers(help='commands',dest="command")

	## create-new command
	new_parser = subparsers.add_parser(
		'new',
		help='Create new Era of Silence character from scratch')

	## load-existing command
	load_parser = subparsers.add_parser(
		'load',
		help="Load existing character from file")

	load_parser.add_argument('file',
		type=str,
		help="File path to saved character data"
		)


	## tree display command
	new_parser = subparsers.add_parser(
		'tree',
		help='Display character creation choice trees and exit'
		)

	args = parser.parse_args()

	## create interface object
	interface = Interface()

	## if no command was selected, print
	## general help
	try:
		assert args.command
	except:
		print("Welcome to the Era of Silence Character Creator!")
		interface.menu()

	if args.command == "new":
		# behavior for creating a new character
		interface.createNewCharacter()
		interface.menu()
	elif args.command == "load":
		# behavior for loading an existing character
		print(f"Loading an existing character from file.\nSource file: {args.file}")
		interface.loadCharacter(args.file)
		interface.menu()
	elif args.command == "tree":
		for t in TREES:
			t.display()