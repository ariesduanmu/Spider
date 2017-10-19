
from general import *
from spider import Spider
import os

import threading
from queue import Queue
from general import *

PROJECT_NAME = 'xiachufang'
HOMEPAGE = "http://www.xiachufang.com"

CATEGORY_FILE_NAME = 'category.txt'
RECIPE_DIRECTORY = 'recipes'


queue = Queue()
NUMBER_OF_THREADS = 8
Spider(HOMEPAGE)

def create_workers():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target=work)
		t.daemon = True
		t.start()
def work():
	while True:
		url = queue.get()
		Spider.crawl_page(threading.current_thread().name,url)
		queue.task_done()
def create_jobs():
	for link in file_to_set(QUEUE_FILE):
		queue.put(link)
	queue.join()
	crawl()
def crawl():
	queue_links = file_to_set(QUEUE_FILE)
	if len(queue_links) > 0:
		create_jobs()


# categories = list(spider.categories_urls())
# set_to_file(categories, CATEGORY_FILE_NAME)

# create_directory(RECIPE_DIRECTORY)
# for category in categories:
# 	recipes, name = spider.recipes_urls(category)
# 	create_directory(os.path.join(RECIPE_DIRECTORY, name))
# 	set_to_file(recipes, os.path.join(RECIPE_DIRECTORY, name, name+'_urls.txt'))

# 	for recipe in list(recipes):
# 		r_name, recipe_detail = spider.recipe_details(recipe)
# 		save_recipe_to_file(recipe_detail, os.path.join(RECIPE_DIRECTORY, name, r_name + '.txt'))


