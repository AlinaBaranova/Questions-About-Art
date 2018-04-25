import json
import io # to save file in utf8

# make table out of info stored in array
# filename1 - file with array, filename2 - file with table, properties_dic - dictionary of properties of objects in array
def make_table(filename1, filename2, properties_dic):

	# get array
	with open(filename1) as file:
		info = json.load(file)

	# number of element so far
	count = 0

	# new array for objects' names
	names = []
	for element in info:
		# extract name of object and its properties
		name = element[0]
		properties = element[1]

		# write name of object to name array
		names.append(name)

		# add empty strings to all properties in dic
		for prop in properties_dic:
			properties_dic[prop].append("")
		# rewrite properties that have value for this object
		for prop in properties:
			properties_dic[prop[0]][count] = prop[1]

		count += 1

	# write info to csv file (; as delimiter)
	with io.open(filename2, 'w', encoding='utf8') as file:
		# write headings
		file.write("name")
		for p in properties_dic:
			file.write(';' + p)
		file.write('\n')

		# write contents
		for i in range(0, len(names)):
			file.write(names[i])
			for p in properties_dic:
				file.write(';' + properties_dic[p][i])
			file.write('\n')

# making tables for movements, painters and creators

# make_table("movements_q.json", "movements_answers.csv", {"starttime" : [], "endtime" : [], "followedby_label" : [], "follows_label" : []})

# make_table("paintings_q.json", "paintings_answers.csv", {"creator_label" : [], "movement_label" : [], "inception" : []})

#make_table("creators_q.json", "creators_answers.csv", {"dateofbirth" : [], "dateofdeath" : [], "movement_label" : [], "country_label" : []})