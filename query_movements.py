import requests
import json
import re
import io # to save json file in utf8

# extracting year from date
def get_year(str):
	# regex for extracting the year
	regex_date = re.compile('([0-9]+)-')

	if str.endswith('T00:00:00Z'):
		n = regex_date.search(str)
		if n != None:
			return n.group(1)
	return str

# extracting index of object from link
def get_id(str):
	# regex for index of object on Wikidata
	regex_id = re.compile('\/([^\/]+$)')

	n = regex_id.search(str)
	if n != None:
		return n.group(1)
	return str

# making first character of string capital, others - lowercase
def cases(str):
	str = str[0].upper() + str[1:]
	return str

# getting art movements
def get_movements():

	# creating dictionary for movements
	new_movements = {}

	# sending the query
	# 50 art movements with the greatest number of paintings
	movementsURL = "https://query.wikidata.org/sparql?query= SELECT ?movement ?movementLabel ?count WHERE { { SELECT ?movement (COUNT(?painting) AS ?count) WHERE { ?painting wdt:P31 wd:Q3305213. ?painting wdt:P135 ?movement. } GROUP BY ?movement } SERVICE wikibase:label { bd:serviceParam wikibase:language \"ru\". } } ORDER BY DESC(?count) LIMIT 50 &format = JSON"
	headers = {"Accept" : "application/json"}
	r2 = requests.get(movementsURL, headers=headers)
	result = r2.json()

	movements = result['results']['bindings']
	for movement in movements:

		label = movement['movementLabel']['value']
		# checking if movement's name is written in Cyrillic
		if label[0].lower() in 'йцукенгшщзъёхфывапролджэячсмитьбю':
			# making first character of string capital, others - lowercase
			label = cases(label)

			# getting index of movement
			id = get_id(movement['movement']['value'])
			
			new_movements[label] = {'id': id}

	return new_movements

# getting movements' properties
def get_movements_properties(filename):

	# creating new dictionary for movements and their properties
	new_movements = {}

	# loading list of movements
	with open(filename) as file:
		movements = json.load(file)

	for movement in movements:

		print(movement)

		# writing movement's id to new dictionary
		id = movements[movement]['id']
		new_movements[movement] = {'id': id}

		# sending the query (start time/ inception, end time, movements that follow, movements that are followed)
		propertiesURL = "https://query.wikidata.org/sparql?query= SELECT ?follows_label ?followedby_label ?starttime ?endtime WHERE { OPTIONAL { wd:" + id + " wdt:P156 ?followedby . ?followedby rdfs:label ?followedby_label filter (lang(?followedby_label) = \"ru\") . } OPTIONAL { wd:" + id + " wdt:P155 ?follows . ?follows rdfs:label ?follows_label filter (lang(?follows_label) = \"ru\") . } OPTIONAL { wd:" + id + " wdt:P580 ?starttime . } OPTIONAL { wd:" + id + " wdt:P571 ?inception . } OPTIONAL { wd:" + id + " wdt:P582 ?endtime . } }"

		headers = {"Accept" : "application/json"}
		r2 = requests.get(propertiesURL, headers=headers)
		result = r2.json()
		options = result['results']['bindings']

		if options != []:
			for option in options:
				for property in option:
					value = option[property]['value']

					# if value is word, make first letter capital, and others - lower case
					if value[0].lower() in 'йцукенгшщзъёхфывапролджэячсмитьбю':
						value = value[0].upper() + value[1:].lower()
					
					# if the value is number, leave only year
					elif value[0] in '1234567890':
						value = get_year(value)

					# just in case
					else:
						print(value)

					# make inception equal the start time
					if property == 'inception':
						property = 'starttime'

					# add property to movement if property is not there			
					if property not in new_movements[movement]:
						new_movements[movement][property] = [value]

					# add value of property to movement if value is not there
					elif value not in new_movements[movement][property] and not property == 'starttime' and not property == 'endtime':
						new_movements[movement][property].append(value)

	return new_movements

# getting movements and writing them to file

# movements = get_movements()
# with io.open('movements.json', 'w', encoding='utf8') as file:
# 	json.dump(movements, file, ensure_ascii=False)


# getting movements' properties and writing them to file

# movements = get_movements_properties('movements.json')
# with io.open('movements-with-properties.json', 'w', encoding='utf8') as file:
# 	json.dump(movements, file, ensure_ascii=False)