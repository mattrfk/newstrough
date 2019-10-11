# non-standard
import feedparser
from pytz import timezone
from dateutil import parser

import os
import csv
import html
import io
import re
from datetime import datetime
from subprocess import call
from string import Template

ENCODING = 'utf-8'
TSFORMAT = '%l:%M%p %Z, %b %d, %Y'

FEEDLIMIT = 15
FEEDLIST = "sources.csv"

# OUT_DIR = "../www/news/"
OUT_DIR = "out"
SRC_DIR = "src/"
INDEX = "index.html"

CWD = os.path.realpath('.')
SRCINDEX = os.path.join(CWD,SRC_DIR, "index.html")
FSTUB = os.path.join(CWD,SRC_DIR, "feedstub.html")
ISTUB = os.path.join(CWD,SRC_DIR, "itemstub.html")

FEEDS = []

def make_stub(path):
    return Template(open(path).read())

def sh(cmd):
    call(cmd, shell=True)

def generate_ts_tag(s):
    d = parser.parse(s)
    return "<span utcts='{}'class='timestamp'>{}</span>".format(
        d.timestamp(),
        d.strftime(TSFORMAT))

# get the published date from the entry
# return an html tag (string) with the formatted timestamp
def get_date(entry):
    s = None
    if 'published' in entry:
        s = entry['published'] 
    elif 'updated' in entry:
        s = entry['updated']

    if not s: 
        return ""  
    else: 
        return generate_ts_tag(s)

def get_reddit_data(entry):
    return "submitted by <a href='{}'>{}</a> {}".format(
        entry['author_detail']['href'],
        entry['author'],
        get_date(entry))

def get_hn_data(entry):
    return "<a href='{}'>comments</a> • submitted by '{}' {}".format(
        entry['comments'],
        entry['author'],
        get_date(entry))

# get info for entry such as published date, article summary
# return a touple: 
#   summary - for articles that have one
#   meta - includes author and date, or other relevant info
def get_data(feed, entry):
    summary = ""
    meta = ""
    if "reddit.com" in feed.href:
        meta = get_reddit_data(entry)
    elif "hnrss" in feed.href:
        meta = get_hn_data(entry)
    else:
        try:
            summary = re.sub("<.*>", "", entry.summary)
        except: pass

        meta = "{} {}".format(
            "by " + entry['author'] + "," if 'author' in entry else "",
            get_date(entry)
        )
    return (summary, meta)

def gather_items(feed):
    items = []
    for i, entry in enumerate(feed.entries):
        if i > FEEDLIMIT: break
        link = entry.link
        headline = html.escape(entry.title, quote=True)
        summary, meta = get_data(feed, entry)
        item = itemstub.substitute(
            link=link, 
            headline=headline,
            summary=summary,
            metadata=meta)
        items.append(item)
    return items


indexstub = make_stub(SRCINDEX)
feedstub = make_stub(FSTUB)
itemstub = make_stub(ISTUB)

feedpath = os.path.join(SRC_DIR, FEEDLIST)

with io.open(feedpath, 'r', encoding=ENCODING) as fl:
    sources = csv.reader(
        fl, delimiter=',', quotechar='"')
    for row in sources:
        FEEDS.append(row)

sources = []
feeds = []
for title,desc,url in FEEDS:
    print("retrieving", title.encode(ENCODING), " - ", url)
    d = feedparser.parse(url)
    
    feeds.append(d)

    items = gather_items(d)

    source = feedstub.substitute(
            title=title, desc='['+desc+']', items=''.join(items))

    sources.append(source)
    print("done")

time = datetime.now(timezone('US/Pacific'))
timestring = time.strftime(TSFORMAT)
t = "This trough was filled {}".format(generate_ts_tag(timestring))

index = indexstub.substitute(timestamp=t, feedstubs=''.join(sources))

# cleanup
if(os.path.exists(OUT_DIR)):
    sh("rm {}/*".format(OUT_DIR))
else:
    sh("mkdir -p {}".format(OUT_DIR))

sh("cp {}*.css {}".format(SRC_DIR, OUT_DIR))
sh("cp {}*.js {}".format(SRC_DIR, OUT_DIR))
sh("cp {} {}".format(SRCINDEX, OUT_DIR))

out = open(os.path.join(OUT_DIR, INDEX), 'w')
out.write(index.encode('ascii', 'xmlcharrefreplace').decode(ENCODING))