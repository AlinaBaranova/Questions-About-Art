import requests
import json
import io

from query_movements import get_year # extract year from dates
from query_movements import get_id # extract index from link
from query_movements import cases # make first character of string capital
from query_paintings import make_name # # change name of creator to format "[First name] [Last name]"

# getting creators
def get_creators(filename):

	# creating new dictionary for movements - in order to get number of creators for each movement
	new_movements = {}

	# creating dictionary for creators
	new_creators = {}

	# loading movements
	with open(filename) as file:
		movements = json.load(file)

	for movement in movements:

		print(movement)
		# count for creators
		count = 0

		# getting movement's id
		id = movements[movement]['id']

		# writing movement's value to dictionary for movements
		new_movements[movement] = movements[movement]

		# sending the query
		# 30 first creators for movement
		creatorsURL = "https://query.wikidata.org/sparql?query= SELECT ?painter ?painterLabel WHERE { ?painter wdt:P106 wd:Q1028181. ?painter wdt:P135 wd:" + id + " . SERVICE wikibase:label { bd:serviceParam wikibase:language \"ru\". } } LIMIT 30"
		headers = {"Accept" : "application/json"}
		r2 = requests.get(creatorsURL, headers=headers)
		result = r2.json()

		creators = result['results']['bindings']
		for creator in creators:

			label = make_name(creator['painterLabel']['value'])
			# checking if creator's name is written in Cyrillic
			if label[0].lower() in 'йцукенгшщзхъёфывапролджэячсмитьбю':

				# getting index of creator
				id_creator = get_id(creator['painter']['value'])

				# writing label and if of creator to dictionary for creators
				new_creators[label] = {'id' : id_creator}

				# counting creator
				count += 1

		print(count)
		# writing number of creators to dictionary for creators
		new_movements[movement]['creators'] = count

	return new_creators, new_movements

# getting creators' properties
def get_creators_properties(filename):

	# creating new dictionary for creators and their properties
	new_creators = {}

	# loading list of creators
	with open(filename) as file:
		creators = json.load(file)

	for creator in creators:

		# print(creator)

		# writing creator's id to new dictionary
		id = creators[creator]['id']
		new_creators[creator] = {'id': id}

		# sending query (date of birth, date of death, movement, country)
		propertiesURL = "https://query.wikidata.org/sparql?query= SELECT ?dateofbirth ?dateofdeath ?movement_label ?country_label WHERE { OPTIONAL { wd:" + id + " wdt:P569 ?dateofbirth . } OPTIONAL { wd:" + id + " wdt:P570 ?dateofdeath . } OPTIONAL { wd:" + id + " wdt:P135 ?movement . ?movement rdfs:label ?movement_label filter (lang(?movement_label) = \"ru\") . } OPTIONAL { wd:" + id + " wdt:P27 ?country . ?country rdfs:label ?country_label filter (lang(?country_label) = \"ru\") . } } "
		headers = {"Accept" : "application/json"}
		r2 = requests.get(propertiesURL, headers=headers)
		result = r2.json()

		options = result['results']['bindings']
		# making sure there are no creators without info
		if options == []:
			print(creator)

		for option in options:
			for property in option:
				value = option[property]['value']

				# if value is number, leave only year
				if value[0] in '1234567890':
					value = get_year(value)

				# property is "movement_label", make first character of value capital
				if property == "movement_label":
					value = cases(value)

				# add property to creator if property is not there
				if property not in new_creators[creator]:
					new_creators[creator][property] = [value]
				# add value of property if value is not there
				elif value not in new_creators[creator][property]:
					new_creators[creator][property].append(value)

	return new_creators

# getting creators and writing them to file; counting number of creators for each movement and adding it to file with movements

# results = get_creators('movements.json')
# creators = results[0]
# movements = results[1]
# with io.open('creators.json', 'w', encoding='utf8') as file:
# 	json.dump(creators, file, ensure_ascii=False)

# with io.open('movements.json', 'w', encoding='utf8') as file:
# 	json.dump(movements, file, ensure_ascii=False)


# getting creators' properties and writing them to file

creators = get_creators_properties('creators.json')
with io.open('creators-with-properties.json', 'w', encoding='utf8') as file:
	json.dump(creators, file, ensure_ascii=False)


# counting total number of creators

# with open('creators.json') as file:
# 	creators = json.load(file)
# print('The number of creators: ' + str(len(creators)))