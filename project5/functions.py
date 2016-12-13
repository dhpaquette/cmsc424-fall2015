from pyspark import SparkContext, SparkConf
import collections
import re

def f(line):
	res = []		
	line = line.split(" ")
	i = 0
	
	while i < len(line) -1:
		res.append(((line[i],line[i+1]),1))
		i+=1
	return res

def g(line,host):
	res = []
	#host = re.search("^([ -~]+)(?=\s-\s-)",line).group(0) #SHOULD grab the host

	if host in line:		
		url = re.search("[GET|POST|HEAD]\s([ -~]+)\sHTTP[ -~]+$",line) #Should get url
		if url:
			val = url.group(1)
			res.append(val)
			return res
		else:
			return []
	else:
		return []

def h(line):

	res = []
	url = re.search("[GET|POST|HEAD]\s([ -~]+)\sHTTP[ -~]+$",line)
	if url:
		val = url.group(1)
		res.append(val)
		return res
	else:
		return []

def i(bigram):
	res = []
	res.append((bigram[0][0],(bigram[0],bigram[1])))
	res.append((bigram[0][1],(bigram[0],bigram[1])))	

	return res

def j(lst):

	arr = sorted(lst,key=lambda x: x[1],reverse=True)

	return arr[0:5]

def k(input,vertices,sinks):
	sum = 0
	lst = input[1]

	for i in lst:
		sum += (i[2]/i[1]*1.0)

	
	prevPgRank = 1.0/vertices
	val = ((1-0.85)/vertices)+(0.85*sum)+ ((prevPgRank*sinks)/(vertices-1))
	return (input[0],val)


# Given the playRDD and a list of words: for each word, count the number of lines that contain it -- the return should be a list 
# with the same length as list_of_words containing the counts
def task1_count_lines(playRDD, list_of_words):	
	lst = []	
	for l in list_of_words:
		val = playRDD.filter(lambda line: l in line).count()
		lst.append(val)
	return lst
# The following function should solve the bigram counting problem; the return should be an RDD
def task2_count_bigrams(playRDD):	
	counts = playRDD.flatMap(f).reduceByKey(lambda a,b: a+b)
	bigrams = counts.flatMap(i).groupByKey().mapValues(j)
	
	return bigrams

# Given two hosts (see example below), find the Jaccard Similarity Coefficient between them based on
# the URLs they visited. i.e., count the number of URLs that they both visited (ignoring duplicates),
# and divide by the total number of unique URLs visited by either
# The return value should be a Double
def task3_find_similarity(logsRDD, host1, host2):
	
	host1Counts = logsRDD.flatMap(lambda line: g(line,host1)).distinct().map(lambda x: (x,1)).reduceByKey(lambda a,b: a+b)
	host2Counts = logsRDD.flatMap(lambda line: g(line,host2)).distinct().map(lambda x: (x,1)).reduceByKey(lambda a,b: a+b)
	
	inter = host1Counts.intersection(host2Counts)
	uni = host1Counts.union(host2Counts)
	
	jaccardIdx = (inter.count()*1.0)/(uni.distinct().count()*1.0)
	
	return jaccardIdx

# The following function should find the top 5 URLs that were accessed most frequently in the provided logs
# The result should be simply a list with 5 strings, denoting the URLs
def task4_top_5_URLs(logsRDD):
	top5Urls = []
	top5RDD = logsRDD.flatMap(h).map(lambda x: (x,1)).reduceByKey(lambda a,b: a+b)
	top5Urls = top5RDD.sortBy(lambda x: x[1],False).take(5)
	top5Urls = [x[0] for x in top5Urls]
	
	return top5Urls

# Implement one iteration of PageRank on the socialnetRDD. Specifically, the input is 2 RDDs, the socialnetRDD and another RDD containing the 
# current PageRank for the vertices
# Compute the new PageRank for the vertices and return that RDD
def task5_pagerank(socialnetRDDs, pagerankPreviousIterationRDD):
	
	pages = socialnetRDDs.keys().distinct().count()
	vertices = socialnetRDDs.flatMap(lambda x: [x[0],x[1]]).distinct().count()
	sinks = vertices - pages
	#print sinks
	
	
	lenOfOutboundLinksRDD = socialnetRDDs.groupByKey().mapValues(list).map(lambda v: (v[0], len(v[1])))
	socialnetRDDs = socialnetRDDs.join(lenOfOutboundLinksRDD)
	socialnetRDDs = socialnetRDDs.join(pagerankPreviousIterationRDD)
	socialnetRDDs = socialnetRDDs.map(lambda x: (x[1][0][0],(x[0],x[1][0][1],x[1][1])))
	socialnetRDDs = socialnetRDDs.groupByKey().mapValues(list)

	socialnetRDDs = socialnetRDDs.map(lambda x: k(x,vertices,sinks))
	
	return socialnetRDDs
	
