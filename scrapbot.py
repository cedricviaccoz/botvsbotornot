#!/usr/bin/env python
from bs4 import BeautifulSoup 
import sys
from os import path
import json
from selenium import webdriver

SCRAP_URL = "http://botpoet.com/"

args = sys.argv

def main(file):
	browser = webdriver.Chrome()
	browser.get(SCRAP_URL)
	startLine = browser.find_element_by_link_text("Free play")
	startLine.click()
	itsAbot = browser.find_element_by_link_text("Bot")
	itsABot.clic()
	currUrl = browser.current_url

	duplicateThreshold = 100
	duplcates = 0
	page = BeautifulSoup(urllib2.urlopen(SCRAP_URL))




if len(args) < 2:
	print("please specify filename where to store poems in first line command argument.")
else:
	if not path.exists(args[1]):
		with open(args[1], 'w') as f:
			#initializing empty file with correct structure.
			toDump = json.dumps(
				{"titles":[],
				 "poems":[]
				})
			f.write(toDump)
	main(args[1])