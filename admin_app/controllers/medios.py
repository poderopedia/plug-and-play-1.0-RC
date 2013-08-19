#!/usr/bin/python
# -*- coding: utf-8 -*-

def entity():
    import feedparser
    from urllib2 import quote
    alias = request.args(0)
    other = ''
    feedchannel = 'https://news.google.cl/news/feeds?gl=cl&gr=cl&pz=1&cf=all&ned=es_cl&hl=es&q="'+quote(alias)+'"+' \
            +other+'&as_eq=Boca+Peru+Bolivia+Colombia&as_occt=title&output=rss'
    feed = feedparser.parse( feedchannel )
    return dict(feeds=feed)
