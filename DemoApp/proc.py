import html2text
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import Counter

url='https://www.indiatoday.in/news.html'
h = html2text.HTML2Text()
response = urlopen(url)
html = response.read()
#print(html)
soup = BeautifulSoup(html)
str=soup.get_text()
str_list = str.split() 
counts = Counter(str_list)
#print(counts['Download'])
warr=[]
farr=[]
for word, count in counts.most_common(10): 
    warr.append(word)
    farr.append(count)
for word in warr:
    print(word)
for freq in farr:
    print(freq)
