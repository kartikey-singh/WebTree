import re
import os
import sys
import pdfkit
import datetime
import hashlib
import urllib.request
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileMerger


def start():	
	'''
	Take link as input and extract its base url and for the 
	given depth do traversal and find all child links and create
	a graph out of it and then remove duplicate pdf's and merge
	all child pdfs into single pdf as outputted by dfs.
	'''
	input_url = input("Enter the webpage: ")
	url = input_url	
	url_splits = input_url.split("/")	
	base_url = url_splits[2]	
	default_depth = 2
	initial_depth = 0
	urls = [url]
	graph = {}
	visited = {}
	merger_dir = 'files_to_merge/'

	while initial_depth != default_depth:		
		all_child_urls = []		
		for url in urls:			
			try:
				child_urls = find_links(graph, url)
				all_child_urls.append(child_urls)
			except:	
				continue				
		all_child_urls = sum(all_child_urls, [])	
		initial_depth = initial_depth + 1
		urls = all_child_urls		

	dfs(graph, visited, url, 0)	
	remove_duplicates(merger_dir)
	pdf_merger(base_url, merger_dir)
	file_remove(merger_dir)
	return None


def url_fixer(base_url, link):
	'''
	Many urls have tree structure and base url 
	has to be appended to them.
	'''
	link.strip()	
	try:
		if link[:8] == "https://" or link[:7] == "http://":			
			return link
		elif link[0] == '/':
			return base_url + link
		else:
			return base_url + "/" + link		
	except:
		return None		


def create_graph(graph, urls):
	'''
	Create an adjacency list of urls.
	'''
	for url in urls:
		if url not in graph:
			graph[url] = []
		for u in urls:
			if u != url:
				graph[url].append(u)
	return None			


def find_links(graph, url):	
	'''
	Find all the link in the DOM of webpage and appende 
	them to a list and send them for graph creation.
	'''
	resp = urllib.request.urlopen(url)
	url_splits = url.split("/")
	base_url = "/".join(url_splits[:3])	
	soup = BeautifulSoup(resp, "lxml", from_encoding=resp.info().get_param('charset'))
	urls = []
	for link in soup.find_all('a', href=True):
		fixed_url = url_fixer(base_url, link['href'])
		if fixed_url != None:			
			urls.append(fixed_url)
	create_graph(graph, urls)		
	return urls


def remove_duplicates(dir):
	'''
	Remove duplicate files who have same sha256 hash.
	'''
	unique = []
	for filename in os.listdir(dir):
		filename = dir + filename		
		if os.path.isfile(filename):			
			file_object = open(filename, 'rb') 
			filehash = hashlib.sha256(file_object.read()).hexdigest()
			# print(filename, filehash)
			if filehash not in unique:
				unique.append(filehash)
				
			else: 
				os.remove(filename)
	return None			


def pdf_merger(base_url,dir):
	'''
	Merge all child pdf's to single pdf.
	'''
	time = ' {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
	pdfs = os.listdir(dir)
	merger = PdfFileMerger()
	for pdf in pdfs:
	    merger.append(dir + pdf)
	merger.write("results/" + base_url + time + ".pdf")
	merger.close()	
	return None


def dfs(graph, visited, key, index):	
	'''
	DO depth first traversal and download each child webpage as a pdf.
	'''
	# print(key, index)
	try:
		pdfkit.from_url(key, 'files_to_merge/' + str(index) + '_child.pdf')
	except:
		print("Couldn't print " + key)	
	visited[key] = True
	for val in graph[key]:
		if val not in visited:
			index = index + 1
			dfs(graph, visited, val, index)
	return None	


def print_graph(graph):
	'''
	Print the graph of url's created.
	'''
	for key, value in graph.items():
		print(key, value)	
	return None	


def file_remove(dir):
	'''
	Remove all the child pdf's after merge operation.
	'''
	files = os.listdir(dir)	
	for file in files:
		os.remove(dir + file)

if __name__ == '__main__':
	start()
