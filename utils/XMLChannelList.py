# -*- coding: utf-8 -*-

import os.path
from xml.dom.minidom import parse
from collections import defaultdict
from classes.ChannelGroup import ChannelGroup

def load(filename):

    if (not os.path.isfile(filename)):
        return False

    try:
        DOMTree = parse(filename)
    except Error as e:
        print("Error parsing channels file (" + filename + "). Error: " + e)
        return False

    collection = DOMTree.documentElement
    channels = collection.getElementsByTagName("channel")

    channelList = []
    for ch in channels:
        provider = ch.getElementsByTagName('provider')[0]
        provCode = provider.getAttribute('code')
        provPath = provider.getAttribute('xmlfile')
        provider = provider.firstChild.data
        ci = ChannelGroup(provider, provCode);
        tvgIDs = ch.getElementsByTagName('tvg-id')
        for tvgID in tvgIDs:
            ci.addChannel(tvgID.firstChild.data, tvgID.getAttribute('name'), tvgID.getAttribute('icon'))
            ci.setFilename(provPath)
        channelList.append(ci)
    return channelList

def sortByProvider(channelList):

    ret = defaultdict(list)
    for channel in channelList:
        provider = channel.getProvider()
        ret[provider].append(channel)

    return ret
