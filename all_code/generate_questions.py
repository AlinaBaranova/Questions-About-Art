import json
from random import randint
import re
import io # to save file in utf8

# generate questions about art
def generate_questions(filename_q, filenames_c):
	# open question templates
	with open('questions.json') as file:
		questions = json.load(file)

	# load categories (movements, paintings, creators) with their information
	contents = []
	regex_name = re.compile('(.+?)(_q.json)')
	 
	for filename in filenames_c:
		
		# extract category from filename
		n = regex_name.search(filename)
		if n != None:
			name = n.group(1)

		with open(filename) as file:
			contents.append([name, json.load(file)])


	if_continue = ''

	# generate questions
	while if_continue != 'no':
		# use function question to get random question and answer
		result = question(questions, contents)
		que = result[0]
		ans = result[1]

		# print question and ask for answer
		print(que)
		answer_user = input('')
		# if answer is right, print "Right!", if wrong - print "Wrong." and the right answer
		if answer_user == ans:
			print('Right!')
		else:
			print('Wrong.\nRight answer: ' + ans)

		# ask if user wants to continue
		if_continue = input('One more question? (to exit type in "no") ')

	# write examples for evaluation
	# with io.open('evaluation.csv', 'w', encoding='UTF-8') as file:
	# 	file.write("question;answer")
	# 	i = 0
	# 	while i < 200:
	# 		result = question(questions, contents)
	# 		que = result[0]
	# 		ans = result[1]
	# 		file.write("\n" + que + ";" + ans)
	# 		i+=1

def question(questions, contents):
	
	# randomly choose category (movements, paintings, creators)
	i = randint(0, len(contents)-1)
	info_kind = contents[i]
	kind = info_kind[0]

	# randomly choose object of category
	i = randint(0, len(info_kind[1])-1)
	item = info_kind[1][i]
	
	# randomly choose property if there are more than 1, else - take the only property
	name = item[0]
	properties = item[1]
	if len(properties) > 1:
		i = randint(0, len(properties)-1)
		prop = properties[i]
	else:
		prop = properties[0]
	# separate property name and property value
	prop_name = prop[0]
	prop_value = prop[1]

	# choose question corresponding to the right category and the right property
	question_template = questions[kind][prop_name]

	# compose question
	question = question_template + name

	# finish question with interoggative sign/ quote and interrogative sign
	if question_template.endswith('"'):
		question += '"?'
	else:
		question += '?'
		
	return question, prop_value

generate_questions('questions.json', ['movements_q.json', 'paintings_q.json', 'creators_q.json'])