# graph = {}
# visited = {}
# urls = ["sd","dsgd","dgsg","gdsg"]

# for url in urls:
# 	if url not in graph:
# 		graph[url] = []
# 	for u in urls:
# 		if u != url:
# 			graph[url].append(u)

# for key, value in graph.items():
# 	print(key, value)	

# def dfs(graph, visted, key):
# 	print(key)
# 	visited[key] = True
# 	for val in graph[key]:
# 		if val not in visited:
# 			dfs(graph, visited, val)
# 	return None	

# dfs(graph, visited, "sd")

# import time
# from selenium import webdriver

# driver = webdriver.Chrome('/home/kartikey/Desktop/Files/WebTree/chromedriver')  # Optional argument, if not specified will search path.
# driver.get('http://www.google.com/xhtml');
# time.sleep(5) # Let the user actually see something!
# search_box = driver.find_element_by_name('q')
# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5) # Let the user actually see something!
# driver.quit()
# import pdfkit
# pdfkit.from_url('https://www.reddit.com/r/Python/comments/6ujq2p/how_to_print_pdf_of_a_page_using_selenium/', 'child.pdf')

import os
import hashlib

def remove_duplicates(dir):
	unique = []
	for filename in os.listdir(dir):
		filename = dir + filename		
		if os.path.isfile(filename):			
			file_object = open(filename, 'rb') 
			filehash = hashlib.sha256(file_object.read()).hexdigest()
			print(filename, filehash)
			if filehash not in unique:
				unique.append(filehash)
				
			else: 
				os.remove(filename)

remove_duplicates('files_to_merge/')            


from PyPDF2 import PdfFileMerger



def pdf_merger(dir):
	pdfs = os.listdir(dir)
	merger = PdfFileMerger()
	for pdf in pdfs:
	    merger.append(dir + pdf)
	merger.write("result.pdf")
	merger.close()	
	return None

def file_remove(dir):
	files = os.listdir(dir)	
	for file in files:
		os.remove(dir + file)

# file_remove('files_to_merge/')