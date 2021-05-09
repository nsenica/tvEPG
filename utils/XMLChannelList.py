# -*- coding: utf-8 -*-

import os.path
from xml.dom.minidom import parse
from collections import defaultdict
from classes.ChannelGroup import ChannelGroup
import logging

def load(filename, filter_provider, filterChannel):

    if (not os.path.isfile(filename)):
        logging.error("File not found (" + filename + ").")
        return False

    try:
        DOMTree = parse(filename)
    except:
        logging.error("Error parsing channels file (" + filename + ").")
        return False

    collection = DOMTree.documentElement
    channels = collection.getElementsByTagName("channel")

    channelList = defaultdict(list)
    for ch in channels:
        provider = ch.getElementsByTagName('provider')[0]
        provCode = provider.getAttribute('code')
        provPath = provider.getAttribute('xmlfile')
        provider = provider.firstChild.data

        if filter_provider != None and filter_provider != provider:
            continue

        ci = ChannelGroup(provider, provCode)
        tvgIDs = ch.getElementsByTagName('tvg-id')
        for tvgID in tvgIDs:
            channelName = tvgID.getAttribute('name')

            if filterChannel != None and filterChannel != channelName:
                continue

            ci.addChannel(tvgID.firstChild.data, channelName, tvgID.getAttribute('icon'))
            ci.setFilename(provPath)

        if ci.nrChannels() > 0:
            channelList[provider].append(ci)
    return channelList
