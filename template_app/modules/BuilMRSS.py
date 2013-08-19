import xml.etree.ElementTree as ET

class MRSSChannel:
    """
    Class that represent channel node of the Sonettic playlist MRRS.
    """
    def __init__(self, id, items = None, nodes = None, poster = None, ads = None):
        self.items = items
        self.nodes = nodes
        self.poster = poster
        self.id = id
        self.ads = ads


class MRSSItem:
    """
    Class representing item node of the Sonettic playlist MRSS feed.
    """
    def __init__(self, id, nodes = None, ads = None, poster = None, contents = None):
        self.id = id
        self.nodes = nodes
        self.ads = ads
        self.poster = poster
        self.contents = contents

class MRSSMediaChapter:
    """
    Class represent media:chapter node of the Sonettic playlist MRSS feed.
    """
    def __init__(self, timemark, duration = None, nodes = None):
        self.timemark = timemark
        self.duration = duration
        self.nodes = nodes

    def xml(self):
        data = {}
        data["timemark"] = self.timemark
        if self.duration: data["duration"] = self.duration
        return data

class MRSSMediaContent:
    """
    Class represent media:content node of the Sonettic playlist MRSS feed.
    """
    def __init__(self, url, duration = None, lang = None, start = None, mediaPoprating = None,
                 thumbnails = None, chapters = None, nodes = None):
        self.url = url
        self.duration = duration
        self.lang = lang
        self.start = start
        self.mediaPoprating = mediaPoprating
        self.thumbnails  = thumbnails
        self.chapters = chapters
        self.nodes = nodes

    def xml(self):
        data = {}
        data["url"] = self.url
        if self.lang: data["lang"] = self.lang
        if self.duration: data["duration"] = self.duration
        if self.start: data["start"] = self.start
        return data

class MRSSMediaThumbnail:
    """
    Class representing media:thumbnail node of the Sonettic playlist MRSS feed.
    """
    def __init__(self, url, width = None, height = None):
        self.url = url
        self.width = width
        self.height = height

    def xml(self):
        data = {}
        data["url"] = self.url
        if self.width: data["width"] = self.width
        if self.height: data["height"] = self.height
        return data


class MRSSNode:
    """
    Class representing XML node.
    """
    def __init__(self, name, value = None, attributes = {}):
        self.attributes = attributes
        self.name = name
        self.value = value

class MRSSPoster:
    """
    Class represents poster node of the Sonettic playlist MRSS feed.
    """
    def __init__(self, url, width, height):
        self.url = url
        self.width = width
        self.height = height

class MRSSAds:
    """
    Class represent ads node of the Sonettic playlist MRSS feed.
    """
    def __init__(self, url, value = None, settings = None):
        self.url = url
        self.value = value
        self.settings = settings

    def xml(self):
        data = {}
        data["url"] = self.url
        if self.value: data["value"] = self.value
        if self.settings: data["settings"] = self.settings
        return data

def channel_to_mrss(channel):
    """
    Return MRSS feed from the channel node.
    """
    channel_el = ET.Element('channel')
    ET.SubElement(channel_el, "id").text = channel.id
    if channel.poster:
        ET.SubElement(channel_el, 'poster', {"url" : channel.poster.url,
                                             "width" : channel.poster.width,
                                             "height" : channel.poster.height,})
    if channel.ads:
        ET.SubElement(channel_el, 'ads', channel.ads.xml())
    if channel.nodes:
        for node in channel.nodes:
            ET.SubElement(channel_el, node.name, node.attributes).text = node.value
    for item in channel.items:
        item_el = ET.SubElement(channel_el, 'item')
        ET.SubElement(item_el, 'id').text = item.id
        if item.poster:
            ET.SubElement(item_el, 'poster', {"url" : item.poster.url,
                                              "width" : item.poster.width,
                                              "height" : item.poster.height,})
        if item.ads:
            ET.SubElement(item_el, 'ads', item.ads.xml())
        if item.nodes:
            for node in item.nodes:
                ET.SubElement(item_el, node.name, node.attributes).text = node.value
        if item.contents:
            for content in item.contents:
                content_el = ET.SubElement(item_el, 'media:content', content.xml())
                if content.mediaPoprating:
                    ET.SubElement(content_el, 'media:poprating').text = content.mediaPoprating
                if content.nodes:
                    for node in content.nodes:
                        ET.SubElement(content_el, 'media:'+node.name, node.attributes).text = node.value
                if content.thumbnails:
                    for thumbnail in content.thumbnails:
                        ET.SubElement(content_el, "media:thumbnail", thumbnail.xml())
                if content.chapters:
                    for chapter in content.chapters:
                        chapter_el = ET.SubElement(content_el, 'media:chapter', chapter.xml())
                        if chapter.nodes:
                            for node in chapter.nodes:
                                ET.SubElement(chapter_el, node.name, node.attributes).text = node.value

    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?><rss xmlns:media=\"http://search.yahoo.com/mrss/\" version=\"2.0\">'+ET.tostring(channel_el)+'</rss>'

