# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 14:07:57 2017

@author: Alex Kerzner
"""

# Import library for simplifying OS file paths
import os

# Import library for parsing a configuration file
from ConfigParser import SafeConfigParser

import ConfigParser

def getConfig():
	parser = ConfigParser.SafeConfigParser()
	# Load default settings
	parser.read(os.path.relpath('etc/defaults.cfg'))
	
	# Load custom settings, if defined
	parser.read(os.path.relpath('etc/settings.cfg'))
	
	return parser