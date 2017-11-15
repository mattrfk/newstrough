import feedparser
import os
from subprocess import call
from string import Template
import cgi
import time
import random


OUT_DIR = "../www/news/"
SRC_DIR = "src/"
INDEX = "index.html"
CWD = os.path.realpath('.') 
SRCINDEX = os.path.join(CWD,SRC_DIR, "index.html")
FSTUB = os.path.join(CWD,SRC_DIR, "feedstub.html")
ISTUB = os.path.join(CWD,SRC_DIR, "itemstub.html")

def makeStub(path):
    return Template(open(path).read())

indexstub = makeStub(SRCINDEX)
feedstub = makeStub(FSTUB)
itemstub = makeStub(ISTUB)

def sh(cmd):
    call(cmd, shell=True)


QUOTELIST = "quotes.txt"
QUOTES = []
try:
    with open(os.path.join(SRC_DIR, QUOTELIST)) as ql:
        for line in ql:
            if not line.startswith('#'):
                QUOTES.append(x.strip() for x in line.rsplit('―', 1))

    quote,attr = QUOTES[random.randint(0,len(QUOTES)-1)]
except:
    quote,attr =( "Who controls the past controls the future. Who controls the present controls the past.", "George Orwell")

FEEDLIST = "sources.txt"
FEEDS = []
FEEDLIMIT = 15
with open(os.path.join(SRC_DIR, FEEDLIST)) as fl:
    for line in fl:
        if not line.startswith('#'):
            FEEDS.append(x.strip() for x in line.split(','))

sources = []
for t,f in FEEDS:
    print("retrieving", t, " - ", f)
    d = feedparser.parse(f)

    items = []
    i = 0
    for e in d.entries:
        if i > FEEDLIMIT:
            break
        i += 1
        item = itemstub.substitute(link=e.link, headline=cgi.escape(e.title, quote=True))
        items.append(item)

    source = feedstub.substitute(title=t, items=''.join(items))
    sources.append(source)
    print("done")

t = "As of: {}".format(time.strftime('%l:%M%p %Z on %b %d, %Y'))
index = indexstub.substitute(timestamp=t, quote=quote, attribution="-"+attr, feedstubs=''.join(sources))

# cleanup
if(os.path.exists(OUT_DIR)):
    sh("rm {}/*".format(OUT_DIR))
    sh("rmdir {}".format(OUT_DIR))

sh("mkdir -p {}".format(OUT_DIR))
sh("cp {}*.css {}".format(SRC_DIR, OUT_DIR))
sh("cp {} {}".format(SRCINDEX, OUT_DIR))

open(os.path.join(OUT_DIR, INDEX), 'w').write(index.encode('ascii', 'xmlcharrefreplace').decode('utf-8'))
