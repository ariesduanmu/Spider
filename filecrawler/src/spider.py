# -*- coding: utf-8 -*-
from src.path_finder import next_files
from src.util import UtilFile

class Spider:
	base_path = ''
	queue_file = ''
	crawled_file = ''
	path_file = ''
	queue = set()
	crawled = set()
	path = set()

	def __init__(self, base_path, queue_file, crawled_file, path_file, rule):
		Spider.base_path = base_path
		Spider.queue_file = queue_file
		Spider.crawled_file = crawled_file
		Spider.path_file = path_file
		Spider.rule = rule
		self.boot()
		self.crawl_paths('First spider', Spider.base_path)

	@staticmethod
	def boot():
		UtilFile.create_data_files(Spider.base_path, 
			                       Spider.queue_file, 
			                       Spider.crawled_file,
			                       Spider.path_file)
		Spider.queue = UtilFile.file_to_set(Spider.queue_file)
		Spider.crawled = UtilFile.file_to_set(Spider.crawled_file)
		Spider.path = UtilFile.file_to_set(Spider.path_file)

	@staticmethod
	def crawl_paths(thread_name, directory_path):
		if directory_path not in Spider.crawled:
			links = Spider.gather_files(directory_path)
			Spider.add_links_to_path(links[0])
			Spider.add_links_to_queue(links[1])

			Spider.queue.remove(directory_path)
			Spider.crawled.add(directory_path)
			Spider.update_files()
	
	@staticmethod
	def gather_files(directory_path):
		return next_files(directory_path, Spider.rule)
			
	@staticmethod
	def add_links_to_queue(links):
		for url in links:
			if (url in Spider.queue) or (url in Spider.crawled):
				continue
			Spider.queue.add(url)

	@staticmethod
	def add_links_to_path(links):
		for link in links:
			Spider.path.add(link)

	@staticmethod
	def update_files():
		UtilFile.set_to_file(Spider.queue, Spider.queue_file)
		UtilFile.set_to_file(Spider.crawled, Spider.crawled_file)
		UtilFile.set_to_file(Spider.path, Spider.path_file)
