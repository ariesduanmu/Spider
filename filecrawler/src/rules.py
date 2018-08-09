# -*- coding: utf-8 -*-

class Rules():
    def filter_directors(self):
        return None

class FileRules(Rules):
    def __init__(self, extensions=None):
        self.extensions = extensions

    def filter_directors(self):
        return set([".svn"])
    

