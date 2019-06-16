# non-standard
import feedparser
from pytz import timezone

import os
import csv
import cgi
import io
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
FEEDLIST = "sources.csv"
FEEDS = []
FEEDLIMIT = 15
UTF8 = 'utf-8'


def make_stub(path):
    return Template(open(path).read())


def sh(cmd):
    call(cmd, shell=True)

def gather_items(d):
    items = []
    for i, e in enumerate(d.entries):
        if i > FEEDLIMIT: break

        link = e.link
        headline = cgi.escape(e.title, quote=True)
        item = itemstub.substitute(
            link=link, headline=headline)
        items.append(item)

        try:
            pubdate = e.published
        except:
            pubdate = "no  date supplied"

        published.append((title + " => " + e.title, pubdate))
    return items


indexstub = make_stub(SRCINDEX)
feedstub = make_stub(FSTUB)
itemstub = make_stub(ISTUB)

feedpath = os.path.join(SRC_DIR, FEEDLIST)

with io.open(feedpath, 'r', encoding=UTF8) as fl:
    sources = csv.reader(
        fl, delimiter=',', quotechar='"')
    for row in sources:
        FEEDS.append(row)

sources = []
published = []
for title,desc,url in FEEDS:
    print("retrieving", title.encode(UTF8), " - ", url)
    d = feedparser.parse(url)

    items = gather_items(d)

    source = feedstub.substitute(
            title=title, desc='['+desc+']', items=''.join(items))

    sources.append(source)
    print("done")


time = datetime.now(timezone('US/Pacific'))
format = '%l:%M%p %Z on %b %d, %Y'
t = "As of: {}".format(time.strftime(format))

index = indexstub.substitute(timestamp=t, feedstubs=''.join(sources))

# cleanup
if(os.path.exists(OUT_DIR)):
    sh("rm {}/*".format(OUT_DIR))
    sh("rmdir {}".format(OUT_DIR))

sh("mkdir -p {}".format(OUT_DIR))
sh("cp {}*.css {}".format(SRC_DIR, OUT_DIR))
sh("cp {}*.js {}".format(SRC_DIR, OUT_DIR))
sh("cp {} {}".format(SRCINDEX, OUT_DIR))

out = open(os.path.join(OUT_DIR, INDEX), 'w')
out.write(index.encode('ascii', 'xmlcharrefreplace').decode(UTF8))
