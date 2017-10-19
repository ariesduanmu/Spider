import os



def create_directory(directory):
	if len(directory) > 0 and not os.path.exists(directory):
		os.makedirs(directory)

def create_data_files(category_queue_file, recipe_queue_file, crawled_category_file, crawled_recipe_file, base_url):
	
	if not os.path.isfile(category_queue_file):
		with open(category_queue_file,'w+') as f:
			f.write(base_url)
	if not os.path.isfile(recipe_queue_file):
		with open(recipe_queue_file,'w+') as f:
			f.write(base_url)
	if not os.path.isfile(crawled_category_file):
		with open(crawled_category_file,'w+') as f:
			f.write('')
	if not os.path.isfile(crawled_recipe_file):
		with open(crawled_recipe_file,'w+') as f:
			f.write('')

def file_to_set(filename):
	result = set()
	if os.path.exists(filename):
		with open(filename, 'rt') as f:
			for line in f:
				result.add(line.replace('\n',''))
	return result

def set_to_file(links, filename):
	with open(filename, 'w+') as f:
		for l in sorted(links):
			f.write(l + '\n')

def save_recipe_to_file(recipe, filename):
	name = recipe['name']
	ingredients = recipe['ingredients']
	steps = recipe['steps']
	with open(filename, 'w+') as f:
		f.write(name + '\n\n')
		f.write('用料\n')
		for ingredient in ingredients:
			i_name = ingredient['name']
			f.write(i_name + '    ')
			if 'unit' in ingredient:
				i_unit = ingredient['unit']
				f.write(i_unit)
			f.write('\n')
		f.write('\n')
		f.write(name + '的做法\n')
		for i in range(len(steps)):
			step = steps[i]
			if step:
				f.write(str(i+1) + ' ' + step + '\n')

