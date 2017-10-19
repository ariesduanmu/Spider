from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os



class ContentFinder(object):

	def __init__(self, soup):
		self.soup = soup
	def recipe_details(self):
		recipe = {}
		name = self.__recipe_name().replace('/','_')
		recipe['name'] = name
		recipe['ingredients'] = self.__recipe_ingredients()
		recipe['steps'] = self.__recipe_steps()

		return name,recipe	
		
	def __recipe_name(self):
		
		return self.soup.find('meta', property='og:title')['content']

	def __recipe_ingredients(self):
		ingredients = []
		ingres = self.soup.find_all(itemprop='recipeIngredient')
		for ingre in ingres:
			ingredient = {}
			ingre_name = ingre.find('td',class_='name')
			if ingre_name:
				if ingre_name.a:
					ingredient['name'] = ingre_name.a.string.strip(' \n')
				else:
					ingredient['name'] = ingre_name.string.strip(' \n')
			ingre_unit = ingre.find('td',class_='unit')
			if ingre_unit:
				ingredient['unit'] = ingre_unit.string.strip(' \n')
			ingredients.append(ingredient)
		return ingredients
			
	def __recipe_steps(self):
		steps = []
		instructions = self.soup.find_all(itemprop='recipeInstructions')
		for instruction in instructions:
			steps.append(instruction.p.string)
		return steps


		
