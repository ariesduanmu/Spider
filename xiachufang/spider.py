from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os

from general import *
from content_finder import ContentFinder
class Spider(object):
	
	def __init__(self, base_url, project_name):
		Spider.base_url = base_url
		Spider.categoty_pattern = '(?<=/category/)[0-9]+'
		Spider.recipe_pattern = '(?<=/recipe/)[0-9]+'

		Spider.project_name = project_name
		Spider.category_queue_file = Spider.project_name + '/category_queue.txt'
		Spider.recipe_queue_file = Spider.project_name + '/recipe_queue.txt'
		Spider.crawled_category_file = Spider.project_name + '/crawled_category.txt'
		Spider.crawled_recipe_file = Spider.project_name + '/crawled_recipe.txt'
		self.boot()
		self.crawl_home_page('Category spider')

	@staticmethod
	def boot():
		create_directory(Spider.project_name)
		create_data_files(Spider.category_queue_file, Spider.recipe_queue_file, Spider.crawled_category_file, Spider.crawled_recipe_file, Spider.base_url)
		Spider.category_queue = file_to_set(Spider.category_queue_file)
		Spider.crawled_category = file_to_set(Spider.crawled_category_file)
		Spider.recipe_queue = file_to_set(Spider.recipe_queue_file)
		Spider.crawled_recipe = file_to_set(Spider.crawled_recipe_file)
	@staticmethod
	def crawl_home_page(thread_name):
		if Spider.base_url not in Spider.crawled_category:
			categories = list(Spider.categories_urls())
			Spider.add_links_to_queue(categories, Spider.category_queue, Spider.crawled_category)
			Spider.category_queue.remove(Spider.base_url)
			Spider.crawled_category.add(Spider.base_url)
			Spider.update_files()

	@staticmethod
	def crawl_category_page(thread_name, page_url):
		if page_url not in Spider.crawled_category:
			recipes,_ = Spider.recipes_urls(page_url)
			recipes = list(recipes)
			Spider.add_links_to_queue(recipes, Spider.recipe_queue, Spider.crawled_category)
			Spider.category_queue.remove(page_url)
			Spider.crawled_category.add(page_url)
			Spider.update_files()

	@staticmethod
	def crawl_recipe_page(thread_name, page_url):
		if page_url not in Spider.crawled_recipe:
			soup = Spider.get_html_doc(page_url)
			content = ContentFinder(soup)
			name, recipe = content.recipe_details()

			Spider.recipe_queue.remove(page_url)
			Spider.crawled_recipe.add(page_url)
			Spider.update_files()

	@staticmethod
	def add_links_to_queue(links, queue_set, crawled_set):
		for url in links:
			if url in queue_set or url in crawled_set:
				continue
			queue_set.add(url)

	@staticmethod
	def update_files():
		set_to_file(Spider.category_queue, Spider.category_queue_file)
		set_to_file(Spider.crawled_category, Spider.crawled_category_file)
		set_to_file(Spider.recipe_queue, Spider.recipe_queue_file)
		set_to_file(Spider.crawled_recipe, Spider.crawled_recipe_file)
	@staticmethod
	def get_html_doc(page_url):
		response = urlopen(page_url)
		html_doc = response.read().decode('utf-8')
		soup = BeautifulSoup(html_doc)
		return soup
	@staticmethod
	def categories_urls():
		soup = Spider.get_html_doc(Spider.base_url)
		categories = Spider.__get_links(soup, Spider.categoty_pattern, '/category/')
		return categories
	@staticmethod
	def recipes_urls(category_url):
		soup = Spider.get_html_doc(category_url)
		recipes = Spider.__get_links(soup, Spider.recipe_pattern, '/recipe/')
		next_page_url = Spider.__next_page(soup)
		if next_page_url:
			next_recipes,_ = Spider.recipes_urls(next_page_url)
			recipes = recipes | next_recipes
		category_name = soup.find('h1', class_=re.compile('page-title'))
		if category_name is None:
			
			print(category_url)
		else:
			category_name = category_name.string
		return recipes, category_name
	@staticmethod
	def __next_page(soup):
		pager = soup.find('div', class_='pager')
		next_page = pager.find('a', class_='next')
		if next_page:
			link = next_page.get('href')
			return Spider.base_url + link
		return None
	@staticmethod
	def __get_links(soup, pattern, target_url_mid_name):
		links = set()
		for link in soup.find_all('a'):
			h = link.get('href')
			m = re.search(pattern, h)
			if m:
				links.add(Spider.base_url + target_url_mid_name + m.group(0))
		return links