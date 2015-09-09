import sys
import math
import copy
from collections import deque

debug = True

class Pipe(object):
	def __init__(self, start, end):
		self.start = start
		self.end = end
		self.distance = 1
		self.off_hours = []
	def sef_off_hours(self, distance, detail):
		self.distance = distance
		tokens = detail.split(' ')
		if len(tokens) > 1:
			for i in tokens:
				if '-' in i:
					temp = i.split('-')
					for k in xrange(int(temp[0]), int(temp[1])+1):
						kk = k % 24
						if kk not in self.off_hours:
							self.off_hours.append(kk)
		self.off_hours.sort()
		
	def __str__(self):
		if len(self.off_hours) == 0:
			off_str = 'none'	
		else:
			off_str = ' '.join([str(x) for x in self.off_hours])
		edge = "(%s,%s)L:%s;Off:%s" % (self.start.get_label(), self.end.get_label(), self.distance, off_str )
		return edge
	def __repr__(self):
		return self.__str__()
	def get_end(self):
		return self.end
	def get_start(self):
		return self.start
	def get_distance(self):
		return self.distance
	def is_valid(self, cur_time):
		return (cur_time not in self.off_hours)										
class Node(object):
	def __init__(self, label):
		self.pipe_to_next = []
		self.reach_time = float('inf')
		self.label = label
	def set_pipe(self, next, distance, detail):
		new_pipe = Pipe(self, next)
		new_pipe.sef_off_hours(distance, detail)
		self.pipe_to_next.append(new_pipe)
	def set_reach_time(self, reach_time):
		self.reach_time = reach_time
	def get_reach_time(self):
		return self.reach_time
	def get_label(self):
		return self.label
	def get_nexts(self):
		next_nodes = []
		for i in self.pipe_to_next:
			next_nodes.append(i.get_end())
		next_nodes.sort()	#sort nexts alphabetically
		return next_nodes
	def get_ucs_nexts(self, cur_time):
		next_nodes = []
		for i in self.pipe_to_next:
			if i.is_valid(cur_time)	:
				temp = copy.deepcopy(i.get_end())
				temp.set_reach_time(cur_time + i.get_distance())
				next_nodes.append(temp)
		if debug:	
			print 'Pipes:', str(self.pipe_to_next)
			print 'Valid nexts:', next_nodes
		return next_nodes
	def __str__(self):
		output = "%s(%s)" % (self.label, self.reach_time)
		return output
	def __repr__(self):
		return self.__str__()
	def __cmp__(self, other):
		return cmp(self.label, other.label)
	def __eq__(self, other):
		return (self.label == other.label)
	def __ne__(self, other):
		return not self == other		
		
def get_sorted_queue(open_queue, next_list):
	temp = []
	for i in open_queue:
		temp.append(i)
	temp.extend(next_list)
	temp.sort(key = lambda x: x.reach_time)
	return deque(temp)
	
def print_queue(input_queue):
	queue_list = []
	for i in input_queue:
		queue_list.append(str(i))	
		
	list_str = ';'.join(queue_list)
	print '[%s]' % (list_str)

def print_debug_info(cur_node, cur_time, open_queue, closed_queue):
	print 'cur_time = %s, cur_node = %s' % (cur_time, cur_node)
	print 'open_queue: ',
	print_queue(open_queue)
	print 'closed_queue: ', 
	print_queue(closed_queue)
	
def search(nodes, source, goal, start_time, algo):
	open_queue = deque([])
	closed_queue = deque([])
	source_node = nodes[source]
	source_node.set_reach_time(start_time)
	open_queue.append(source_node)
	
	if debug:
		print 'Algorithm: %s' % (algo)
		print 'Goal: %s' % goal
		print_debug_info('none', start_time, open_queue, closed_queue)
		print '-----------------------------------'	
	if algo == 'BFS':
		while len(open_queue) != 0:
			cur_node = open_queue.popleft()
			#print 'cur_node =', cur_node.get_label()
			cur_time = cur_node.get_reach_time()
			
			if debug:
				print 'Pop node %s from open_queue.' % (str(cur_node))
				print_debug_info(cur_node, cur_time, open_queue, closed_queue)
			
			if cur_node.get_label() in goal:
				#goal achieved, break
				if debug:
					print 'Goal achieved!'
					print '-----------------------------------'
				return cur_node
			if debug:	
				print 'Pipes:', str(cur_node.pipe_to_next)
			for i in cur_node.get_nexts():
				if i not in closed_queue:	#only unvisited ones
					i.set_reach_time(cur_time+1)
					open_queue.append(i)
					if debug:
						print 'Add %s to open_queue' % i
			#print 'size of open_queue =', len(open_queue)
			closed_queue.append(cur_node)
			if debug:
				print 'Add %s to closed_queue' % cur_node
				print 'New open_queue:', 
				print_queue(open_queue)
				print 'New closed_queue:',
				print_queue(closed_queue)
				print '-----------------------------------'
		else:
			#return fail		
			return 'None'		
	elif algo == 'DFS':
		while len(open_queue) != 0:
			cur_node = open_queue.popleft()
			cur_time = cur_node.get_reach_time()
			
			if debug:
				print 'Pop node %s from open_queue.' % (str(cur_node))
				print_debug_info(cur_node, cur_time, open_queue, closed_queue)
			
			if cur_node.get_label() in goal:
				#goal achieved, break
				if debug:
					print 'Goal achieved!'
					print '-----------------------------------'
				return cur_node
			
			if debug:	
				print 'Pipes:', str(cur_node.pipe_to_next)
			
			temp = []
			for i in cur_node.get_nexts():
				if i not in closed_queue and i not in open_queue:					#only unvisited ones
					i.set_reach_time(cur_time+1)
					temp.append(i)
				if debug:
					print 'Add %s to open_queue' % i
			temp.sort()		#keep the alphabetical order
			for i in open_queue:
				temp.append(i)
			open_queue = deque(temp)
			closed_queue.append(cur_node)
			if debug:
				print 'Add %s to closed_queue' % cur_node
				print 'New open_queue:', 
				print_queue(open_queue)
				print 'New closed_queue:',
				print_queue(closed_queue)
				print '-----------------------------------'
		else:
			#return fail		
			return 'None'	
	else:
		while len(open_queue) != 0:
			cur_node = open_queue.popleft()
			cur_time = cur_node.get_reach_time()
		
			if debug:
				print 'Pop node %s from open_queue.' % (str(cur_node))
				print_debug_info(cur_node, cur_time, open_queue, closed_queue)

			if cur_node.get_label() in goal:
				if debug:
					print 'Goal achieved!'
					print '-----------------------------------'
				return cur_node
			next_list = []
			for i in cur_node.get_ucs_nexts(cur_time):
				if i not in closed_queue and i not in open_queue:					#brand-new state; unvisited
					if debug:
						print 'Add brand-new node %s to open_queue' % str(i)
					next_list.append(i)
				elif i in open_queue:
					old_idx = list(open_queue).index(i)
					if i.get_reach_time() < open_queue[old_idx].get_reach_time():
						open_queue[old_idx].set_reach_time(i.get_reach_time())
						if debug:
							print 'Found lower-cost existing node(unvisied) => update cost of %s in open_queue' % str(i)
						#update the cost to a smaller one
				elif i in closed_queue:
					old_idx = list(closed_queue).index(i)
					if i.get_reach_time() < closed_queue[old_idx].get_reach_time():
						if debug:
							print 'Found lower-cost existing node(visited) => put %s back to open_queue' % str(i)
						closed_queue.remove(i)
						open_queue.append(i)
			open_queue = get_sorted_queue(open_queue, next_list)
			closed_queue.append(cur_node)
			if debug:
				print 'sorted open_queue:',
				print_queue(open_queue)
				print 'Add %s to closed_queue' % cur_node
				print 'New open_queue:', 
				print_queue(open_queue)
				print 'New closed_queue:',
				print_queue(closed_queue)
				print '-----------------------------------'
		else:
			return 'None'		
					
def process(pack):
	task = pack[0]
	source = pack[1]
	goal = pack[2].split(' ')
	mid_nodes = pack[3].split(' ')
	no_pipes = int(pack[4])
	pipe_lines = []
	for i in xrange(5, 5+no_pipes):
		pipe_lines.append(pack[i])
	start_time = int(pack[5+no_pipes])
	
	nodes = {}	#dictionary to hold all nodes
	for i in pipe_lines:
		tokens = i.split(' ')
		
		start_node = Node(tokens[0])	
		end_node = Node(tokens[1])
		
		if tokens[0] not in nodes:	#new node
			nodes[tokens[0]] = start_node #add to dictionary
		else:						#existing node
			start_node = nodes[tokens[0]]	#use the existing one
			
		if tokens[1] not in nodes:
			nodes[tokens[1]] = end_node
		else:
			end_node = nodes[tokens[1]]
		
		#start_nodes keep track of every pipe coming out from itself
		if task == 'UCS':
			start_node.set_pipe(end_node, int(tokens[2]), ' '.join(tokens[3:]))
		else:
			start_node.set_pipe(end_node, 1, '')
		nodes[tokens[0]] = start_node		#update to dictionary
	
	result = search(nodes, source, goal, start_time, task)
	
	if type(result) is Node:
		temp = ('%s %s') % (result.get_label(), result.get_reach_time())
		print temp
		if debug:
			print '==================================='
		return temp
	else:
		print result
		if debug:
			print '==================================='
		return result

file = open(sys.argv[1], 'r')
out_file = open('output.txt', 'w')
tasks = []
buff = []
total_case = int(file.readline().strip())

for line in file:
	if line in ['\n', '\r\n']:
		tasks.append(buff)
		buff = []
	else:
		buff.append(line.strip())
if len(buff) != 0:
	tasks.append(buff)

for i in tasks:
	out_file.write(process(i) + '\n')
	
