#! /usr/bin/env python

#################################################
# Author: F. Dan O'Neill
# Date: 2020-04-20
#################################################

"""eoschar

This module provides functionality for the easy creation
of character sheets for the Era of Silence (herein: EoS)
Role-Playing Game system. The eoschar module currently 
works through a command-line interface, but future versions
will incorporate a graphic user interface (GUI).

To generate a new character sheet, 
"""


import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

from ._version import __version__
import json, sys