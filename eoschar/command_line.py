import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import sys
from .charactersheet import CharacterSheet
from .choice import Choice, Item
from .interface import Interface
from ._version import __version__
import argparse


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

	args = parser.parse_args()

	## if no command was selected, print
	## general help
	try:
		assert args.command
	except:
		parser.print_help(sys.stderr)
		sys.exit(1)

	if args.command == "new":
		# behavior for creating a new character
		print("Creating a new character from scratch.")
		pass
	elif args.command == "load":
		# behavior for loading an existing character
		print(f"Loading an existing character from file.\nSource file: {args.file}")
		pass