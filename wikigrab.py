""" Program to scrape Wikipedia pages for main text content
    using pattern matching and HTTP requests
        Author: Nixy 
        Github: @phoenixrising1800
"""

import urllib.request
import re

url = 'https://en.wikipedia.org/wiki/'
page ='Ring_species' # this is to be changed

# Helper function to easily get index containing certain string
def getEleIndex(lst: list, s: str) -> int:
    for line in lst:
        for e in line:
            if s in e:
                print(lst.index(line)) # for debugging in live interpreter
                return lst.index(line)
    return -1 # nothing found, completion code

def deleteEle(lst: list, e):
    for sublst in lst:
        sublst.remove(e)

def makeString(lst: list) -> str:
    s = ''
    for ele in lst:
        s = s + ele
    return s

# Send HTML GET Req query to url page
req = urllib.request.Request(url+page)
res = urllib.request.urlopen(req)
html = res.read()
htmlStr = str(html, 'utf-8')
htmlList = htmlStr.splitlines(True) # List of HTML document lines [0-(n-1 index]

# Write initial response html to file 'output.txt' (for testing purposes)
with open('output0.txt', 'w+') as f:
    for line in htmlList:
        f.write(line)

patTitle = '<title>(.*)</title>'
patPara = r'\/?[\"\w+]>([\w\s\,\(\)\;\.\"\-\']*)\s?<?'

matchTitle = re.findall(patTitle, htmlStr)[0] # get 1st title found in tags
matches = [] # 2d list of matching lines (stored in a list)
for line in htmlList:
    tmp = re.findall(patPara, line)
    matches.append(tmp)

# Remove empty, single whitespace elements etc.
matches = [[e for e in line if e != '' and e != ' ' and e != 'citation needed'] for line in matches]
# Remove unneccessary elements from list
matches = [line for line in matches if line != [] and line != ['\n']] # remove empty lists/line ele
# Remove lines with smaller len than 2 (most likely not useful)
matches = [line for line in matches if len(line) >= 5]

with open('output.txt', 'w+') as f: # write matching content lines to outputf
    f.write(matchTitle + '\n')
    for line in matches:
        lineStr = makeString(line)
        f.write(lineStr)

