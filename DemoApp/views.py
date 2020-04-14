from django.shortcuts import render
from django.http import HttpResponse
from . models import Destination
import html2text
import random
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import Counter

stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', '^', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', '→','↵','0','1','2','3','4','5','6','otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please','7','8','9']
stopwords += ['put','A','You','The', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
stopwords += ['show', 'side', 'since','You','A','We','—','Here’s' 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
stopwords += ['ten', 'than', 'that', 'the', 'The', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these','–', 'they']
stopwords += ['thick', 'thin', 'third', 'this', 'those','Do','|','2018.', 'though', 'three']
stopwords += ['three', 'through','If', 'throughout', 'thru', 'thus', 'to']
stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
stopwords += ['yours', 'yourself', 'yourselves']

def removeStopwords(wordlist, stopwords):
    return [w for w in wordlist if w not in stopwords]

# Create your views here.


def frequency(request):
    return render(request,'home.html')

def result(request):
    alr=0
    url=request.POST['url']
    # To fetch data from db
    if Destination.objects.filter(url=url).count():
        alr=1
        obj = Destination.objects.get(url=url)
        print(obj)
        print(obj.url)
        print("Exists")
        farr=[]
        return render(request,'result.html',{'url':obj.url,
        'alr':alr,
        'w1':obj.w1,
        'w2':obj.w2,
        'w3':obj.w3,
        'w4':obj.w4,
        'w5':obj.w5,
        'w6':obj.w6,
        'w7':obj.w7,
        'w8':obj.w8,
        'w9':obj.w9,
        'w91':obj.w91,
        'f1':obj.f1,
        'f2':obj.f2,
        'f3':obj.f3,
        'f4':obj.f4,
        'f5':obj.f5,
        'f6':obj.f6,
        'f7':obj.f7,
        'f8':obj.f8,
        'f9':obj.f9,
        'f91':obj.f91,
        })
    else:
        # Find the words...
        h = html2text.HTML2Text()
        response = urlopen(url)
        html = response.read()
        #print(html)
        soup = BeautifulSoup(html)
        str=soup.get_text()
        fullwordlist = str.split() 
        wordlist = removeStopwords(fullwordlist,stopwords)
        counts = Counter(wordlist)
        warr=[]
        farr=[]
        for word, count in counts.most_common(10): 
            warr.append(word)
            farr.append(count)
        nr = Destination(id=random.randrange(1,2000, 3),url = url,w1=warr[0],f1=farr[0],w2=warr[1],f2=farr[1],w3=warr[2],f3=farr[2],w4=warr[3],f4=farr[3],w5=warr[4],f5=farr[4],w6=warr[5],f6=farr[5],w7=warr[6],f7=farr[6],w8=warr[7],f8=farr[7],w9=warr[8],f9=farr[8],w91=warr[9],f91=farr[9])
        nr.save()
        
        return render(request,'result.html',{'url':url,
        'alr':alr,
        'w1':warr[0],
        'w2':warr[1],
        'w3':warr[2],
        'w4':warr[3],
        'w5':warr[4],
        'w6':warr[5],
        'w7':warr[6],
        'w8':warr[7],
        'w9':warr[8],
        'w91':warr[9],
        'f1':farr[0],
        'f2':farr[1],
        'f3':farr[2],
        'f4':farr[3],
        'f5':farr[4],
        'f6':farr[5],
        'f7':farr[6],
        'f8':farr[7],
        'f9':farr[8],
        'f91':farr[9],
        })

    

