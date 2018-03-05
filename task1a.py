import os
from glob import glob
import time
from bs4 import BeautifulSoup
import re
import urllib.request as urllib2


SCRAPPEDLINKS = "/Users/rohitchawla/Desktop/Taashi_Khurana_HW1/ravi/"
SCRAPPEDHTML = "/Users/rohitchawla/Desktop/Taashi_Khurana_HW1/ravi/html/"


def begin():
    docs = glob(SCRAPPEDHTML + '\*.txt')
    list(map(lambda x: os.remove(x), docs))
    firstURL = "https://en.wikipedia.org/wiki/Solar_eclipse"
    depth = 6
    totalUniqueURL = 1000
    writetoDoc = open(SCRAPPEDLINKS + "\linksScrapped.txt", 'w')
    u = range(1, totalUniqueURL+1)
    list(map(lambda x, z: writetoDoc.write(str(z) + " " + x + "\n"), Spider(firstURL, int(depth), int(totalUniqueURL)), u))
    print("Raw HTML is recorded at %s" % SCRAPPEDHTML)
    print("Crawled Links recorded at %s" % SCRAPPEDLINKS)



def extractUrls(spiderResult):
    extractedUrls = []
    startingLink = "https://en.wikipedia.org"
    link = urllib2.urlopen(spiderResult)
    soup = BeautifulSoup(link, "html.parser")
    slasparts = spiderResult.split('/')
    url = slasparts[4]
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


def Spider(link, finalDepth, limit):
    makeListempty = []
    travelled = []
    initialDepth = 1
    firstLink = [link]
    followingSpider = []
    while len(firstLink)!=0 and initialDepth <= finalDepth and limit > len(travelled):
        presentSpider = firstLink.pop(0)
        if not travelled.__contains__(presentSpider):
            fetchedAddresses = extractUrls(presentSpider)
            if len(fetchedAddresses)!=0:
                q = list(filter(lambda x: x not in followingSpider, fetchedAddresses))
                i = list(map(lambda x: followingSpider.append(x), q))
                travelled.append(presentSpider)
                time.sleep(1)
        if len(firstLink)==0:
            firstLink = followingSpider
            followingSpider = makeListempty
            initialDepth += 1
    return travelled





begin()




