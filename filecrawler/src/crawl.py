# -*- coding: utf-8 -*-
import threading
import os
from queue import Queue
from src.spider import Spider
from src.util import UtilFile


def create_workers(queue, number_of_threads):
	for _ in range(number_of_threads):
		t = threading.Thread(target=work, args=(queue,))
		t.daemon = True
		t.start()

def work(queue):
	while True:
		path = queue.get()
		Spider.crawl_paths(threading.current_thread().name, path)
		queue.task_done()

def create_jobs(queue, queue_file):
	for path in UtilFile.file_to_set(queue_file):
		queue.put(path)
	queue.join()
	crawl(queue, queue_file)

def crawl(queue, queue_file):
	queue_paths = UtilFile.file_to_set(queue_file)
	if len(queue_paths) > 0:
		create_jobs(queue, queue_file)

def delete_files(files):
	for file in files:
		os.remove(file)

def crawl_directories(base_path, rule, number_of_threads, queue_file='queue.txt', 
	                  crawled_file='crawled.txt', path_file='path.txt'):
	queue = Queue()	
	Spider(base_path, queue_file, crawled_file, path_file, rule)

	create_workers(queue, number_of_threads)
	crawl(queue, queue_file)
	paths = UtilFile.file_to_set(path_file)
	delete_files([queue_file, crawled_file, path_file])
	return paths
