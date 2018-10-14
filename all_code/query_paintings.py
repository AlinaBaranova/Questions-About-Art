import requests
import json
import io # to save json file in utf8
import re

from query_movements import get_year # extract year from dates
from query_movements import get_id # extract index from link
from query_movements import cases # make first character of string capital

# changing name of creator to format "[First name] [Last name]"
def make_name(str):
	regex_creator = re.compile('(.*?), (.*)')
	if ', ' in str:
		n = regex_creator.search(str)
		str = n.group(2) + ' ' + n.group(1)
	return str

# getting paintings
def get_paintings(filename):

	# creating new dictionary for movements - in order to get number of paintings for each movement
	new_movements = {}

	# creating dictionary for paintings
	new_paintings = {}

	# loading movements
	with open(filename) as file:
		movements = json.load(file)

		for movement in movements:

			print(movement)
			# count for paintings
			count = 0

			# getting movement's id
			id = movements[movement]['id']

			# writing movement's value to dictionary for movements
			new_movements[movement] = movements[movement]

			# sending the query
			# 200 first paintings for movement
			paintingsURL = "https://query.wikidata.org/sparql?query= SELECT ?painting ?paintingLabel WHERE { ?painting wdt:P31 wd:Q3305213. ?painting wdt:P135 wd:" + id + " . SERVICE wikibase:label { bd:serviceParam wikibase:language \"ru\". } } LIMIT 200"
			headers = {"Accept" : "application/json"}
			r2 = requests.get(paintingsURL, headers=headers)
			result = r2.json()
			
			paintings = result['results']['bindings']
			for i in paintings:
				
				label_painting = i['paintingLabel']['value']
				# checking if painting's name is written in Cyrillic
				if label_painting[0].lower() in 'йцукенгшщзъёхфывапролджэячсмитьбю':

					# getting index of painting
					id_painting = get_id(i['painting']['value'])
					
					# writing label and id of painting to dictionary for paintings
					new_paintings[cases(label_painting)] = {'id' : id_painting}

					# counting painting
					count += 1

			print(count)
			# writing number of paintings to dictionary for movements
			new_movements[movement]['paintings'] = count
			
		return new_paintings, new_movements

# getting paintings' properties
def get_paintings_properties(filename):

	# creating new dictionary for paintings and their properties
	new_paintings = {}

	# loading list of paintings
	with open(filename) as file:
		paintings = json.load(file)

	for painting in paintings:

		# print(painting)

		# write painting's id to new dictionary
		id = paintings[painting]['id']
		new_paintings[painting] = {'id' : id}

		# sending query (inception, movement, creator)
		propertiesURL = "https://query.wikidata.org/sparql?query= SELECT ?inception ?movement_label ?creator_label WHERE { OPTIONAL { wd:" + id + " wdt:P571 ?inception . } OPTIONAL { wd:" + id + " wdt:P135 ?movement . ?movement rdfs:label ?movement_label filter (lang(?movement_label) = \"ru\") . } OPTIONAL { wd:" + id + " wdt:P170 ?creator . ?creator rdfs:label ?creator_label filter (lang(?creator_label) = \"ru\") . } }"
		headers = {"Accept" : "application/json"}
		r2 = requests.get(propertiesURL, headers=headers)
		result = r2.json()

		options = result['results']['bindings']
		# making sure there are no paintings without info
		if options == []:
			print(painting)

		for option in options:
			for property in option:
				value = option[property]['value']

				# if value is number, leave only year
				if value[0] in '1234567890':
					value = get_year(value)

				# if property is "creator_label", change value if it is written with comma
				if property == 'creator_label':
					value = make_name(value)

				# if property is "movement_label", make first character of value capital
				if property == 'movement_label':
					value = cases(value)

				# add property to painting if property is not there
				if property not in new_paintings[painting]:
					new_paintings[painting][property] = [value]
				# add value of property to painting if value is not there
				elif value not in new_paintings[painting][property] and not property == 'inception':
					new_paintings[painting][property].append(value)

	return new_paintings

# getting paintings and writing them to file; counting number of paintings for each movement and adding it to file with movements

# results = get_paintings('movements.json')
# paintings = results[0]
# movements = results[1]
# with io.open('paintings.json', 'w', encoding='utf8') as file:
# 	json.dump(paintings, file, ensure_ascii=False)

# with io.open('movements.json', 'w', encoding='utf8') as file:
# 	json.dump(movements, file, ensure_ascii=False)


# getting paintings' properties and writing them to file

# paintings = get_paintings_properties('paintings.json')
# with io.open('paintings-with-properties.json', 'w', encoding='utf8') as file:
# 	json.dump(paintings, file, ensure_ascii=False)

# counting total number of paintings

# with open('paintings.json') as file:
# 	paintings = json.load(file)
# print('The number of paintings: ' + str(len(paintings)))

# finding out if some of paintings are written with non-capital letter

# for painting in paintings:
# 	if painting[0] in "йцукенгшщзхъёфывапролджэячсмитьбю":
# 		print(painting)
