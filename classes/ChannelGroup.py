# -*- coding: utf-8 -*-

from xml.dom import minidom
from classes.ChannelInfo import ChannelInfo

class ChannelGroup:

    def __init__(self, provider, provCode):
        self._provider = provider
        self._providerCode = provCode
        self._channelList = []

    def getProvider(self):
        return self._provider;

    def getProviderCode(self):
        return self._providerCode

    def getChannelList(self):
        return self._channelList

    def setFilename(self, xmlFilename):
        self._xmlFilename = xmlFilename

    def getFilename(self):
        return self._xmlFilename

    def addChannel(self, id, displayName, iconSrc):
        ci = ChannelInfo(id, displayName, iconSrc)
        self._channelList.append(ci)
