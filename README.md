# WebTree

## An application which creates a PDF by using the structured graph of a webpage and it's related webpages through the use of URL's.

### It uses the connection between webpages to join them together and create an offline PDF of the webpage that resembles a parent-child web structure in the pdf with the help of depth first search (DFS).

#### Directory
>WebTree/
>>env/ (Virtual environment)
>>files_to_merge/ (Stores all child PDF's for a particular script run)
>>results/ (Final PDF's stroage of all script runs)
>>`info.py` (To get more information about the script)
>>`linkExtraction.py` (Main script)	

## Future work
- Improve PDF's layout.
- Apply multiprocessing to PDF making
- Giving weights(number of link hits) to graph edges and using djikstra's algorithm to sort the pages.