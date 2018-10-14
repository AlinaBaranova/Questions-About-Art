import json
import io # to save json file in utf8

# delete movements that do not have any properties, any paintings and any creators
def clean_movements(filename1, filename2):

	# loading list of movements
	with open(filename1) as file:
		movements = json.load(file)

	# loading list of movements with properties
	with open(filename2) as file:
		movements_properties = json.load(file)

	# creating copies of both lists - to delete useless movements from them
	new_movements = dict(movements)
	new_movements_properties = dict(movements_properties)

	for movement in movements:
		# if movement does not have any properties, any paintings and any creators, delete it from both lists
		if movements[movement]['paintings'] == 0 and movements[movement]['creators'] == 0 and len(movements_properties[movement]) == 1:
			print(movement)

			del new_movements[movement]
			del new_movements_properties[movement]

	return new_movements, new_movements_properties

# prepare files for using them for question templates - delete elements that do not have any properties; delete ids; delete value arrays that have more than 1 element; get rid of arrays
def prepare_for_questions(filename):

	arr = []

	# loading list of items
	with open(filename) as file:
		dic = json.load(file)

	for item in dic:
		# getting rid of elements that do not have any properties
		if len(dic[item]) > 1:
			new_props = []
			props = dic[item]
			# deleting id
			del props["id"]
			for prop in props:
				# getting rid of value arrays that have more than 1 element
				if len(props[prop]) == 1:
					new_props.append([prop, props[prop][0]])
		arr.append([item, new_props])

	return arr

# deleting movements that do not have any properties, any paintings and any creators from list of movements and list of movements with properties

# results = clean_movements('movements.json', 'movements-with-properties.json')
# movements = results[0]
# movements_properties = results[1]
# with io.open('movements.json', 'w', encoding='utf8') as file:
# 	json.dump(movements, file, ensure_ascii=False)

# with io.open('movements-with-properties.json', 'w', encoding='utf8') as file:
# 	json.dump(movements_properties, file, ensure_ascii=False)


# preparing lists of movements, paintings and creators for using them for question templates

movements = prepare_for_questions('movements-with-properties.json')
with io.open('movements_q.json', 'w', encoding='utf8') as file:
	json.dump(movements, file, ensure_ascii=False)

paintings = prepare_for_questions('paintings-with-properties.json')
with io.open('paintings_q.json', 'w', encoding='utf8') as file:
	json.dump(paintings, file, ensure_ascii=False)

creators = prepare_for_questions('creators-with-properties.json')
with io.open('creators_q.json', 'w', encoding='utf8') as file:
	json.dump(creators, file, ensure_ascii=False)



