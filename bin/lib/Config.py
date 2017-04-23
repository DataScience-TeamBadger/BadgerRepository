# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 14:07:57 2017

@author: Alex Kerzner
"""


import ConfigParser

def getConfig():
	parser = ConfigParser.SafeConfigParser()
	# Load default settings
	parser.read('defaults.cfg')
	
	# Load custom settings, if defined
	parser.read('settings.cfg')
	
	return parser