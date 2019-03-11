# -*- coding: utf-8 -*-

from xml.dom import minidom

class ChannelInfo:

    def __init__(self, id, displayName, iconSrc):
        self._id = id
        self._displayName = displayName
        self._iconSrc = iconSrc
        self._lang = "pt"

    def getId(self):
        return self._id

    def getDisplayName(self):
        return self._displayName

    def getIconSrc(self):
        return self._iconSrc

    def getLang(self):
        return self._lang

    # def __repr__(self):
    #     return str(self.__dict__)
