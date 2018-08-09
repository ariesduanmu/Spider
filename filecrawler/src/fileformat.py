# -*- coding: utf-8 -*-
class FileFormat():
    def __init__(self, name, formats, directory=True, empty=False, crawl=True):
        self.name = name
        self.formats = formats
        self.directory = directory
        self.empty = empty
        self.crawl = crawl