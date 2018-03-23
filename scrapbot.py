import BeautifulSoup as soup 
import os
import path
import json

SCRAP_URL = "http://botpoet.com/vote/random/"

args = os.argv

def main(file):
	pass



if len(args) < 2:
	print("please specify filename where to store poems in line command argument.")
else:
	if not path.exists(args[1]):
		pass
		#TODO create the file with empty json file structure.