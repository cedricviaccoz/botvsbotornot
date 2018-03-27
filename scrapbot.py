#!/usr/bin/env python
from bs4 import BeautifulSoup 
import sys
from os import path
import json
from selenium import webdriver

SCRAP_URL = "http://botpoet.com/"
ToRemove = SCRAP_URL+"vote/"
BotMade = "Generated by {} using {}"


args = sys.argv

def parseAnswer(ans):
	pass

def extractResults(soup)

def main(title_array):

	#Initial connection to the website, and access  to the free play mode.
	browser = webdriver.Chrome()
	browser.get(SCRAP_URL)
	startLine = browser.find_element_by_link_text("Free play")
	startLine.click()

	###BEGIN OF THE SCRAP LOOP
	itsABot = browser.find_elements_by_name("submit")
	itsABot[0].click()
	currUrl = browser.current_url
	print(currUrl)
	#print(browser.page_source)
	#Each poem use its title as a unique ID to get it by URL. THis is why I extract it from 
	poemTitle = currUrl[len(ToRemove):-1]
	soup = BeautifulSoup(browser.page_source, 'html.parser')
	result = soup.p.string #EITHER "Generated by ..." or the name of the human
	isBot = parseAnswer(result)
	Bot, OrNot = extractResults(soup)

	nextLink = browser.find_element_by_link_text("Vote on another poem?")
	nextLink.click()
	#END OF SCRAP LOOP
	browser.close()


if len(args) < 2:
	print("please specify filename where to store poems in first line command argument.")
else:
	prelude = args[1]
	titlesJson = prelude + "_titles.json"
	poemsJson = prelude + "_poems.json"
	titlesArray = []
	if path.exists(titlesJson):
		with open(titlesJson, 'r') as f:
			if not path.exists(poemsJson):
				raise Exception("???")
			json.load(f)
			#load titles into titlesArray (TODO)

	if not path.exists(args[1]):
		with open(args[1], 'w') as f:
			#initializing empty file with correct structure.
			toDump = json.dumps(
				{"titles":[],
				 "poems":[]
				})
			f.write(toDump)
	with open(args[1]) as f:

		main(f)