# ========================== MODULES TO IMPORT ============================== #
import sys

# ============================ GLOBAL VARS ================================== #
# Global Variables for Graph
GRAPH = []
MAX_ELEM = -1
MIN_ELEM = -1
CONNECTED_COMPONENTS = []

# ========================== INPUT PARSE METHODS ============================ #
def determine_max_min(first, second):
	global MAX_ELEM
	global MIN_ELEM
	# Default values. Will only be assigned once
	if(MAX_ELEM == -1):
		MAX_ELEM = first
	if(MIN_ELEM == -1):
		MIN_ELEM = first
	# Check against first & second
	update_max(first)
	update_max(second)
	update_min(first)
	update_min(second)

def update_min(elem):
	global MIN_ELEM
	if(elem < MIN_ELEM):
		MIN_ELEM = elem
def update_max(elem):
	global MAX_ELEM
	if(elem > MAX_ELEM):
		MAX_ELEM = elem

def check_valid_operation(op):
	return (op == "add") or (op == "remove") or (op == "is linked")

def check_valid_nodes(first, second):
	return first.isdigit() and second.isdigit()

def transform_index(index):
	return index - MIN_ELEM

def parse_lines(stream):
	allLines = [line.rstrip() for line in stream.readlines()]
	validLines = []
	for line in allLines:
		lineElements = line.split(" ")
		# If there are 4 elements, convert to three to accomodate is linked
		if(len(lineElements) == 4):
			lineElements = [lineElements[0] + " " + lineElements[1], 
			lineElements[2], lineElements[3]]
		# Parse the current line only if there are exactly 3 elements
		# Note: is linked is already taken care of
		if(len(lineElements) == 3):
			# Check for valid operation and nodes, and add it to validLines
			if(check_valid_operation(lineElements[0]) 
				and check_valid_nodes(lineElements[1], lineElements[2])):
				# Okay since we have already checked for integers
				validLines.append(lineElements)
				determine_max_min(int(lineElements[1]), int(lineElements[2]))
	validLines = formatLines(validLines)
	return validLines			

def formatLines(lines):
	validLines = []
	for line in lines:
		line = [line[0], transform_index(int(line[1])), 
		transform_index(int(line[2]))]
		validLines.append(line)
	return validLines


# ========================= GRAPH METHODS =================================== #
# The max and min should be initialized at this point
def init_graph():
	global GRAPH
	# No node has links right now
	GRAPH = [set([]) for node in range(MAX_ELEM - MIN_ELEM + 1)]

def add_link(first, second):
	if(second not in GRAPH[first]):
		GRAPH[first].add(second)
	if(first not in GRAPH[second]):
		GRAPH[second].add(first)
	update_connected_components()
	return

def remove_link(first, second):
	if(first in GRAPH[second]):
		GRAPH[second].remove(first)
	if(second in GRAPH[first]):
		GRAPH[first].remove(second)
	update_connected_components()
	return

def is_linked(first, second):
	return CONNECTED_COMPONENTS[first] == CONNECTED_COMPONENTS[second]

# =============================== PRIVATE METHODS ============================ #
def init_connected_components():
	global CONNECTED_COMPONENTS
	CONNECTED_COMPONENTS = [0 for i in range(MAX_ELEM - MIN_ELEM + 1)]

def update_connected_components():
	explored = set([])
	index = 1
	for i in range(len(GRAPH)):
		if i not in explored:
			component = run_bfs(i)
			update_connected_component(component, index)
			index += 1
			explored = explored | component
			continue

def update_connected_component(component, index):
	for node in component:
		CONNECTED_COMPONENTS[node] = index

def run_bfs(first):
	visited = set()
	queue = [first]
	while queue:
		node = queue.pop()
		if node not in visited:
			visited.add(node)
			queue.extend(GRAPH[node] - visited)
	return visited


def update_component(component, index):
	global CONNECTED_COMPONENTS
	for node in component:
		CONNECTED_COMPONENTS[node] = index


def is_linked(first, second):
	global CONNECTED_COMPONENTS
	return CONNECTED_COMPONENTS[first] == CONNECTED_COMPONENTS[second]

# =========================== MAIN PROGRAM ================================== #
if __name__ == "__main__":
	stream = open(sys.argv[1])
	# Each line is a list of elements: [operation, node1 , node2]
	lines = parse_lines(stream)
	init_graph()
	init_connected_components()
	# DEBUG: print MAX_ELEM
	# DEBUG: print MIN_ELEM
	# DEBUG: print lines
	for line in lines:
		if(line[0] == "add"):
			add_link(line[1], line[2])
		elif(line[0] == "remove"):
			remove_link(line[1], line[2])
		else:
			result = is_linked(line[1], line[2])
			print result
	