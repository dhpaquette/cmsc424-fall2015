import inspect
from operator import attrgetter
from disk_relations import *

# We will implement our operators using the iterator interface
# discussed in Section 12.7.2.1
class Operator:
	def init(self):
		return
	def get_next(self):
		return
	def close(self):
		return

# We will only support equality predicate for now
class Predicate:
	def __init__(self, attribute, value):
		self.attribute = attribute
		self.value = value
	def satisfiedBy(self, t):
		return t.getAttribute(self.attribute) == self.value

class SequentialScan(Operator):
	def __init__(self, relation, predicate = None):
		self.relation = relation
		self.predicate = predicate
	# Typically the init() here would open the appropriate file, etc. In our 
	# simple implementation, we don't need to do anything, especially when we
	# use "yield"
	def init(self):
		return

	# This is really simplified because of "yield", which allows us to return a value, 
	# and then continue where we left off when the next call comes
	def get_next(self):
		for i in range(0, len(self.relation.blocks)):
			b = self.relation.blocks[i]
			if Globals.printBlockAccesses:
				print "Retrieving " + str(b)
			for j in range(0, len(self.relation.blocks[i].tuples)):
				t = b.tuples[j]
				if t is not None and (self.predicate is None or self.predicate.satisfiedBy(t)):
					yield t
	# Typically you would close any open files etc.
	def close(self):
		return

# We will only support Equality joins
class NestedLoopsJoin(Operator):
	INNER_JOIN = 0
	LEFT_OUTER_JOIN = 1
	def __init__(self, left_child, right_child, left_attribute, right_attribute, jointype = INNER_JOIN):
		self.left_child = left_child
		self.right_child = right_child
		self.left_attribute = left_attribute
		self.right_attribute = right_attribute
		self.jointype = jointype

	# Call init() on the two children
	def init(self):
		self.left_child.init()
		self.right_child.init()

	# Again using "yield" greatly simplifies writing of this code -- otherwise we would have 
	# to keep track of current pointers etc
	def get_next(self):
		for l in self.left_child.get_next():
			foundAMatch = False
			for r in self.right_child.get_next():
				if l.getAttribute(self.left_attribute) == r.getAttribute(self.right_attribute):
					foundAMatch = True
					output = list(l.t)
					output.extend(list(r.t))
					yield Tuple(None, output)
			# If we are doing LEFT_OUTER_JOIN, we need to output a tuple if there is no match
			if self.jointype == NestedLoopsJoin.LEFT_OUTER_JOIN and not foundAMatch:
				output = list(l.t)
				for i in range(0, len(self.right_child.relation.schema)):
					output.append("NULL")
				yield Tuple(None, output)
			# NOTE: RIGHT_OUTER_JOIN is not easy to do with NestedLoopsJoin, so you would swap the children
			# if you wanted to do that

	# Typically you would close any open files etc.
	def close(self):
		return

# We will only support Equality joins
# Inner Hash Joins are very simple to implement, especially if you assume that the right relation fits in memory
# We start by loading the tuples from the right input into a hash table, and then for each tuple in the second
# input (left input) we look up matches
#
# You are supposed to implement the two outer hash join versions of this
class HashJoin(Operator):
	INNER_JOIN = 0
	LEFT_OUTER_JOIN = 1
	RIGHT_OUTER_JOIN = 2
	def __init__(self, left_child, right_child, left_attribute, right_attribute, jointype):
		self.left_child = left_child
		self.right_child = right_child
		self.left_attribute = left_attribute
		self.right_attribute = right_attribute
		self.jointype = jointype

	# Call init() on the two children
	def init(self):
		self.left_child.init()
		self.right_child.init()

	# We will use Python "dict" data structure as the hash table
	def get_next(self):
		if self.jointype == self.INNER_JOIN:
			# First, we load up all the tuples from the right input into the hash table
			hashtable = dict()
			for r in self.right_child.get_next():
				key = r.getAttribute(self.right_attribute)
				if key in hashtable:
					hashtable[r.getAttribute(self.right_attribute)].append(r)
				else: 
					hashtable[r.getAttribute(self.right_attribute)] = [r]
					
			# Then, for each tuple in the left input, we look for matches and output those
			# Using "yield" significantly simplifies this code
			for l in self.left_child.get_next():
				key = l.getAttribute(self.left_attribute)
				if key in hashtable:
					for r in hashtable[key]:
						output = list(l.t)
						output.extend(list(r.t))
						yield Tuple(None, output)

		elif self.jointype == self.LEFT_OUTER_JOIN:

			if not self.right_child.relation.blocks:
				for l in self.left_child.get_next():
					output = list(l.t)					
					for i in range(0, len(self.right_child.relation.schema)):
						output.append("NULL")
					yield Tuple(None, output)

			
			hashtable = dict()
			for r in self.right_child.get_next():
				key = r.getAttribute(self.right_attribute)
				if key in hashtable:
					hashtable[r.getAttribute(self.right_attribute)].append(r)
				else:
					hashtable[r.getAttribute(self.right_attribute)] = [r]
			
			for l in self.left_child.get_next():
				key = l.getAttribute(self.left_attribute)					
				if key in hashtable:					
					for r in hashtable[key]:
						output = list(l.t)						
						output.extend(list(r.t))
						yield Tuple(None,output)
				else:
					output = list(l.t)					
					for i in range(0, len(self.right_child.relation.schema)):
						output.append("NULL")
					yield Tuple(None, output)


				

		elif self.jointype == self.RIGHT_OUTER_JOIN:

			if not self.left_child.relation.blocks:
				for r in self.right_child.get_next():
					output = []			
					for i in range(0,len(self.left_child.relation.schema)):
						output.append("NULL")
					output.extend(r.t)					
					yield Tuple(None, output)


			hashtable = dict()
			output = []
			for l in self.left_child.get_next():
				key = l.getAttribute(self.left_attribute)
				if key in hashtable:
					hashtable[l.getAttribute(self.left_attribute)].append(l)
				else:
					hashtable[l.getAttribute(self.left_attribute)] = [l]
			
			for r in self.right_child.get_next():
				key = r.getAttribute(self.right_attribute)
				
				if key in hashtable:
					for l in hashtable[key]:
						output = list(l.t)
						output.extend(list(r.t))
						yield Tuple(None, output)
				else:
					output = []			
					for i in range(0,len(self.left_child.relation.schema)):
						output.append("NULL")
					output.extend(r.t)					
					yield Tuple(None, output)


		else:
			raise ValueError("This should not happen")

	# Typically you would close any open files, deallocate hash tables etc.
	def close(self):
		self.left_child.close()
		self.right_child.close()
		return

class GroupByAggregate(Operator):
	COUNT = 0
	SUM = 1
	MAX = 2
	MIN = 3
	@staticmethod
	def initial_value(aggregate_function):
		return (0, 0, None, None)[aggregate_function]
	@staticmethod
	def update_aggregate(aggregate_function, current_aggregate, new_value):
		if aggregate_function == GroupByAggregate.COUNT:
			return current_aggregate + 1
		elif aggregate_function == GroupByAggregate.SUM:
			return current_aggregate + int(new_value)
		elif aggregate_function == GroupByAggregate.MAX:
			if current_aggregate is None:
				return new_value
			else:
				return max(current_aggregate, new_value)
		elif aggregate_function == GroupByAggregate.MIN:
			if current_aggregate is None:
				return new_value
			else:
				return min(current_aggregate, new_value)
		else:
			raise ValueError("No such aggregate")

	def __init__(self, child, aggregate_attribute, aggregate_function, group_by_attribute = None):
		self.child = child
		self.group_by_attribute = group_by_attribute
		self.aggregate_attribute = aggregate_attribute
		# The following should be between 0 and 3, as interpreted above
		self.aggregate_function = aggregate_function

	def init(self):
		self.child.init()

	def get_next(self):
		if self.group_by_attribute is None:
			# We first use initial_value() to set up an appropriate initial value for the aggregate, e.g., 0 for COUNT and SUM
			aggr = GroupByAggregate.initial_value(self.aggregate_function)

			# Then, for each input tuple: we update the aggregate appropriately
			for t in self.child.get_next():
				aggr = GroupByAggregate.update_aggregate(self.aggregate_function, aggr, t.getAttribute(self.aggregate_attribute))

			# There is only one output here, but we must use "yield" since the "else" code needs to use "yield" (that code
			# may return multiple groups)
			yield aggr
		else:
			# for each different value "v" of the group by attribute, we should return a 2-tuple "(v, aggr_value)",
			# where aggr_value is the value of the aggregate for the group of tuples corresponding to "v"
			#while.child.get_next()
			visited = []
			for r in self.child.get_next():
				aggr_value = GroupByAggregate.initial_value(self.aggregate_function)
				v = r.getAttribute(self.group_by_attribute)							
				for s in self.child.get_next():					
					if r.getAttribute(self.group_by_attribute) == s.getAttribute(self.group_by_attribute):
						aggr_value = GroupByAggregate.update_aggregate(self.aggregate_function,aggr_value,s.getAttribute(self.aggregate_attribute))						
				if r.getAttribute(self.group_by_attribute) not in visited:
					yield (v,aggr_value)
					visited.append(r.getAttribute(self.group_by_attribute))			
						

# You are supposed to implement this join operator
class SortMergeJoin(Operator):
	def __init__(self, left_child, right_child, left_attribute, right_attribute):
		self.left_child = left_child
		self.right_child = right_child
		self.left_attribute = left_attribute
		self.right_attribute = right_attribute

	# Call init() on the two children
	def init(self):
		self.left_child.init()
		self.right_child.init()

	# In your implementation, you can assume that the two inputs are small enough to fit into memory,
	# so there is no need to do external sort
	# You can load the two relations into arrays and use Python sort routines to sort them, and then merge
	# Make sure to use "yield" to simplify your code
	def get_next(self):

		sorted_left_list = []
		sorted_right_list = []
		for l in self.left_child.get_next():
			sorted_left_list.append(l)
		sorted_left_list = sorted(sorted_left_list,key=lambda t: t.getAttribute(self.left_attribute))
		for r in self.right_child.get_next():
			sorted_right_list.append(r)
		sorted_right_list = sorted(sorted_right_list,key=lambda t: t.getAttribute(self.right_attribute))
		
		
		i = 0
		j = 0
		
		while i < len(sorted_left_list) and j < len(sorted_right_list):
			

			if sorted_left_list[i].getAttribute(self.left_attribute) > sorted_right_list[j].getAttribute(self.right_attribute):
				j = j + 1
			elif sorted_left_list[i].getAttribute(self.left_attribute) < sorted_right_list[j].getAttribute(self.right_attribute):
				i = i + 1
			else: # They are equal
				output = list(sorted_left_list[i].t)
				output.extend(list(sorted_right_list[j].t))
				yield Tuple(None,output)
				

				k = j+1
				while ((k < len(sorted_right_list)) and (sorted_left_list[i].getAttribute(self.left_attribute) == sorted_right_list[k].getAttribute(self.right_attribute))):
					output = list(sorted_left_list[i].t)
					output.extend(list(sorted_right_list[k].t))
					yield Tuple(None,output)
					k = k+1
					

				p = i+1
				while ((p < len(sorted_left_list)) and (sorted_left_list[p].getAttribute(self.left_attribute) == sorted_right_list[j].getAttribute(self.right_attribute))):
					output = list(sorted_left_list[p].t)
					output.extend(list(sorted_right_list[j].t))
					
					yield Tuple(None,output)
					p = p+1
					
				i = i+1
				j = j+1

		


		

	# Typically you would close any open files, deallocate hash tables etc.
	def close(self):
		self.left_child.close()
		self.right_child.close()
