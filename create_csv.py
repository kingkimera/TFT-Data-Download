import csv
import json
import os

myDir = 'downloads/matches/12.15'


with open('tftcsv.csv', 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(["companion", "placement", "3Stars","2Stars","1Stars","ChromaticTrait","GoldTrait","SilverTrait","BronzeTrait","NoTrait"])
	for fn in os.listdir(myDir):
		j = json.load(open(os.path.join(myDir,fn),'r'))
		prisma = "No"
		
		if j["info"].get("tft_game_type", None) != 'turbo':
			# do not look into the game and pull out the player data
			continue
			# this makes the main loop continue looking instead of proceeding down below


		for i in range(8):
			#iterate through all 8 players


			units =  j["info"]["participants"][i]["units"]
			UnitList = []
			for item in units:
				UnitList.append(item["tier"])


			traits =  j["info"]["participants"][i]["traits"]
			TraitList = []
			for badge in traits:
				TraitList.append(badge["style"])
				pass

		
			writer.writerow([j["info"]["participants"][i]["companion"],
			j["info"]["participants"][i]["placement"],
			UnitList.count(3),
			UnitList.count(2),
			UnitList.count(1),
			TraitList.count(4),
			TraitList.count(3),
			TraitList.count(2),
			TraitList.count(1),
			TraitList.count(0)
		])
		
			

			# "2Stars",
			# "3Stars",
			# "HasPrismatic",
			# "GoldTraits",
			# "SilverTraits",
			# "BronzeTraits"])
	

# with open('tftsheet.csv', 'w', newline='') as file:
#  	writer = csv.writer(file)
# 	writer.writerow(["Level", "Placement", "1Stars","2Stars","3Stars","HasPrismatic","GoldTraits","SilverTraits","BronzeTraits"])
	






	# These variables are as follows:

	# 	 Level: what level the player was when they died. This strongly (but not completely) governs team size.
	# 	 Placement: How the player placed 1-8. 1-4 are going to be considered our 'winners' and 5-8 our 'losers'
	# 	 1Stars: A numeric total for how many 1-star units the player had on the board when they died/won
	# 	 2Stars: A numeric total for how many 2-star units the player had on the board when they died/won
	# 	 3Stars: A numeric total for how many 3-star units the player had on the board when they died/won
	# 	 HasPrismatic: A catergorical variable for whether or not the player had a prismatic trait active
	# 	 GoldTraits: A numeric total for how many gold traits the player had active when they died/won
	# 	 SilverTraits: A numeric total for how many silver traits the player had active when they died/won
	# 	 BronzeTraits: A numeric total for how many bronze traits the player had active when they died/won


	# 	 variables I wish I had: Roll data, ie number of rolls per game, maybe rolls per level even
