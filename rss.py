# non-standard
import feedparser
from pytz import timezone

import os
import csv
import cgi
import random
from datetime import datetime
from subprocess import call
from string import Template

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

FEEDLIST = "sources.csv"
FEEDS = []
FEEDLIMIT = 15
with open(os.path.join(SRC_DIR, FEEDLIST)) as fl:
    sources = csv.reader(fl, delimiter=',', quotechar='"')
    for row in sources:
        FEEDS.append(row)


    for line in fl:
        if not line.startswith('#'):
            FEEDS.append(x.strip() for x in line.rsplit(',', 1))

sources = []
published = []
for title,desc,url in FEEDS:
    print("retrieving", title, " - ", url)
    d = feedparser.parse(url)

    items = []
    i = 0
    for e in d.entries:
        if i > FEEDLIMIT:
            break
        i += 1
        item = itemstub.substitute(link=e.link, headline=cgi.escape(e.title, quote=True))
        items.append(item)

        try:
            pubdate = e.published
        except:
            pubdate = "no published date supplied"
        published.append((title + " => " + e.title, pubdate))

    source = feedstub.substitute(title=title, desc='['+desc+']', items=''.join(items))
    sources.append(source)
    print("done")

t = "As of: {}".format(datetime.now(timezone('US/Pacific')).strftime('%l:%M%p %Z on %b %d, %Y'))
index = indexstub.substitute(timestamp=t, feedstubs=''.join(sources))

# cleanup
if(os.path.exists(OUT_DIR)):
    sh("rm {}/*".format(OUT_DIR))
    sh("rmdir {}".format(OUT_DIR))

sh("mkdir -p {}".format(OUT_DIR))
sh("cp {}*.css {}".format(SRC_DIR, OUT_DIR))
sh("cp {} {}".format(SRCINDEX, OUT_DIR))

open(os.path.join(OUT_DIR, INDEX), 'w').write(index.encode('ascii', 'xmlcharrefreplace').decode('utf-8'))
