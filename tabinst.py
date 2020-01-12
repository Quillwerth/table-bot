import os
import json
import errno

def load():
	library = {}
	# r=root path, d=directory names, f=file names
	for root, dirname, filenames in os.walk("./tabinst/"):
		for name in filenames:
			if '.json' in name:
				try:
					with open(root+name) as f:
						tablib = json.load(f)
						print("Loaded "+tablib["groupName"])
						library[tablib["groupName"].lower()] = TableInstructionGroup(tablib)
				except IOError as exc:
					if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
						raise # Propagate other kinds of IOError.
	return library


class TableInstructionGroup:
	def __init__(self, src):
		self.name = src["groupName"]
		self.instructions = {}
		for srcInst in src["instructions"]:
			self.instructions[srcInst["instructionName"].lower()] = TableInstruction(srcInst)

class TableInstruction:
	def __init__(self, src):
		self.name = src["instructionName"]
		self.lines = src["instructionLines"]

load()