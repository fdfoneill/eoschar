#! /usr/bin/env python

import pathlib
from setuptools import setup

# the directory containing this file
HERE = pathlib.Path(__file__).parent

def readme():
	with open('README.md') as f:
		return f.read()

exec(open('eoschar/_version.py').read())

setup(name='eoschar',
	version=__version__,
	description='Era of Silence character creation tools',
	long_description=readme(),
	long_description_content_type='text/markdown',
	author="F. Dan O'Neill",
	author_email='foneill@umd.edu',
	license="MIT",
	packages=['eoschar'],
	include_package_data=True,
	# third-party dependencies
	install_requires=[
		"fpdf"
		],
	# tests
	test_suite='nose.collector',
	tests_require=[
		'nose'
		],
	zip_safe=False,
	# console scripts
	entry_points = {
		'console_scripts': [
			'eoschar=eoschar.command_line:main',
			'eoscharexample=eoschar.command_line:makeExample'
			]
		}
	)