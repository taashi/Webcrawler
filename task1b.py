import os
from glob import glob
import time
from bs4 import BeautifulSoup
import re
import urllib.request as urllib2

SCRAPPEDLINKS = "/Users/rohitchawla/Desktop/Taashi_Khurana_HW1/test/hmtl2/"
SCRAPPEDHTML = "/Users/rohitchawla/Desktop/Taashi_Khurana_HW1/test/hmtl2/test1/"


def begin():
    docs = glob(SCRAPPEDHTML + '\*.txt')
    list(map(lambda x: os.remove(x), docs))
    firstURL = "https://en.wikipedia.org/wiki/Solar_eclipse"
    depth = 6
    totalUniqueURL = 1000
    writetoDoc = open(SCRAPPEDLINKS + "\linksScrapped.txt", 'w')
    u = range(1, totalUniqueURL+1)
    list(map(lambda x, z: writetoDoc.write(str(z) + " " + x + "\n"), Spider(firstURL, int(depth), int(totalUniqueURL),[]), u))
    print("Raw HTML is recorded at %s" % SCRAPPEDHTML)
    print("Crawled Links recorded at %s" % SCRAPPEDLINKS)



def extractUrls(spiderResult):
    extractedUrls = []
    startingLink = "https://en.wikipedia.org"
    link = urllib2.urlopen(spiderResult)
    soup = BeautifulSoup(link, "html.parser")
    slasparts = spiderResult.split('/')
    url = slasparts[4]
    # url = urlSplit.replace('_', "")
    new = SCRAPPEDHTML + "\\" + url + ".txt"
    streamOutput = open(new, 'w', encoding="UTF-8")
    streamOutput.write(spiderResult)
    newSoup = soup.prettify()
    streamOutput.write("\n" + newSoup)
    divMaterial = soup.findAll("div", attrs={"id": "bodyContent"})
    for div in divMaterial:
        wiki = div.findAll('a', href=re.compile('^/wiki'))
    filteredWiki = list(filter(lambda x: ":" not in x.get('href'), wiki))
    for bind in filteredWiki:
        wikiCompare = bind.get('href')
        address = ''.join((startingLink,wikiCompare))
        if "#" in wikiCompare:
            y = address.find('#')
            address = address[:y]
        if not extractedUrls.__contains__(address):
            extractedUrls.append(address)
    return extractedUrls


def Spider(link, finalDepth, limit, travelled):
    makeListempty = []
    initialDepth = 1
    if initialDepth <= finalDepth and limit > len(travelled):
            fetchedAddresses = extractUrls(link)
            if not travelled.__contains__(link):
                travelled.append(link)
            pl = list(map(lambda recentLink: (fn(travelled, limit, finalDepth, initialDepth, recentLink)),fetchedAddresses))
            time.sleep(1)
    else :
        return makeListempty
    return travelled


def fn(travelled, limit, finalDepth, initialDepth, recentLink):
    if len(travelled) < limit and finalDepth > initialDepth and recentLink not in travelled:
        y = Spider(recentLink, finalDepth-1, limit, travelled)
        q = list(filter(lambda x: x not in travelled,y))
        return q





begin()




