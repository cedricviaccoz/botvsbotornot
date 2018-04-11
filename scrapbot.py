#!/usr/bin/env python
from bs4 import BeautifulSoup 
import sys
import re
import csv
from os import path
import json
from selenium import webdriver
import pandas as pd

SCRAP_URL = "http://botpoet.com/"
ToRemove = SCRAP_URL+"vote/"
BotMadeRE = "Generated by (.*) using (.*)"
firstRow = "title;isBot;madeBy;using;botPercentage;humanPercentage;text\n"

args = sys.argv

def parseAnswer(ans):
	isBot = False
	madeBy = None
	using = None
	search_res = re.search(BotMadeRE, ans, re.IGNORECASE)
	if search_res:
		isBot = True
		madeBy = search_res.group(1)
		using = search_res.group(2)
	else:
		madeBy = ans
	return isBot, madeBy, using

def extractTitles(filename):
	df = pd.read_csv(filename, sep=';')
	return df['title'].toList()

def dumpTitles(filename):
	with open(titlesJson, 'w') as f:
			#initializing empty file with correct structure.
			toDump = json.dumps(
				{"titles": titlesArray
				})
			f.write(toDump)


def extractResults(soup):
	bot = soup.find("div", {"class": "bot-progress-bar"}).get_text()[1:3]
	orNot = soup.find("div", {"class": "not-progress-bar"}).get_text()[1:3]
	return bot, orNot

def scraploop(titles, titlesJson, poems_file, browser):
	scrapped = 0
	duplicates = 0
	currDuplicates = 0
	writer = csv.writer(poems_file, delimiter=';')
	try :
		while(currDuplicates < 1000):
			itsABot = browser.find_elements_by_name("submit")
			itsABot[0].click()
			currUrl = browser.current_url
			#Each poem use its title as a unique ID to get it by URL. THis is why I extract it from 
			poemTitle = currUrl[len(ToRemove):-1]
			if poemTitle in titlesArray:
				duplicates += 1
				currDuplicates += 1
			else:
				currDuplicates = 0
				soup = BeautifulSoup(browser.page_source, 'html.parser')
				result = soup.p.string #EITHER "Generated by ..." or the name of the human
				isBot, madeBy, using = parseAnswer(result)
				Bot, OrNot = extractResults(soup)
				poem = soup.find("pre", {"class": "poem"}).get_text()
				writer.writerow([
					poemTitle,
					isBot,
					madeBy,
					using,
					int(Bot),
					int(OrNot),
					poem.replace('\"', '°')
					])
				titles.append(poemTitle)

			scrapped += 1

			sys.stdout.write("\r"+str(scrapped)+" poems scrapped so far, "+str(duplicates)+" duplicates in total, current duplicate strike : "+str(currDuplicates))
			sys.stdout.flush()
			nextLink = browser.find_element_by_link_text("Vote on another poem?")
			nextLink.click()
	except :
		print("An error occured : " +str(sys.exc_info()[0]))
		dumpTitles(titlesJson)
		print("titles Saved")
		poems_file.close()
		print("Poems saved")
		browser.close()
		print("browser closed")
		raise


def main(title_array, poem_filename, titles_filename):
	#Initial connection to the website, and access  to the free play mode.
	browser = webdriver.Chrome()
	browser.get(SCRAP_URL)
	startLine = browser.find_element_by_link_text("Free play")
	startLine.click()

	with open(poem_filename, 'a') as f:
		scraploop(title_array, titles_filename, f, browser)
	browser.close()


if len(args) < 2:
	print("please specify filename where to store poems in first line command argument.")
else:
	prelude = args[1]
	titlesJson = prelude + "_titles.json"
	poemsFile = prelude + "_poems.csv"
	if len(args) == 3 and args[2] == 'genTitle':
		titlesArray = extractTitles(poemsFile)
		with open(titlesJson, 'w') as f:
			toDump = json.dumps(
				{"titles": titlesArray
				})
			f.write(toDump)

	else:
		titlesArray = []
		if path.exists(titlesJson):
			with open(titlesJson, 'r') as f:
				if not path.exists(poemsFile):
					raise Exception("Titles exists for all poem but the actual poem data is lost ! Please locate the file of poem, or restart the scrapping.")
				titlesArray = json.load(f)['titles']
				
		if not path.exists(poemsFile):
			with open(poemsFile, 'w') as f:
				f.write(firstRow)

		main(titlesArray, poemsFile, titlesJson)
		dumpTitles(titlesJson)
