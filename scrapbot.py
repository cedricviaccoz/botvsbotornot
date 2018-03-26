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
	itsABot = browser.find_elements_by_name("submit")
	itsABot[0].click()
	currUrl = browser.current_url
	
	soup = BeautifulSoup(browser.page_source, 'html.parser')
	print(soup.title)




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