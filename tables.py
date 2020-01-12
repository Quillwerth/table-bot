import os
import json
import errno
import random

def load():
	library = TableLibrary()
	# r=root path, d=directory names, f=file names
	for root, dirname, filenames in os.walk("./tables/"):
		for name in filenames:
			if '.json' in name:
				try:
					with open(root+name) as f:
						tablib = json.load(f)
						print("Loaded "+tablib["collectionName"])
						library.AddCollection(tablib)
				except IOError as exc:
					if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
						raise # Propagate other kinds of IOError.
	return library

class TableLibrary:
	def __init__(self):
		self.collections = {}
	def AddCollection(self, src):
		collection = TableCollection(src)
		self.collections[collection.collectionName] = collection
	def GetValue(self, name):
		nameParts = name.split(".")
		if nameParts[0] in self.collections:
			return self.collections[nameParts[0]].GetValue(nameParts[1])

class TableCollection:
	def __init__(self, src):
		self.collectionName = src["collectionName"]
		self.tables = {}
		for table in src["tables"]:
			self.tables[table["tableName"]] = GenerationTable(table)
	def GetValue(self, name):
		if name in self.tables:
			return self.tables[name].GetValue()

class GenerationTable:
	def __init__(self, src):
		self.tableName = src["tableName"]
		self.tableValues = src["values"]
	def GetValue(self):
		return random.choice(self.tableValues)