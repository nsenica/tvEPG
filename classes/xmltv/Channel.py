# -*- coding: utf-8 -*-

from xml.dom import minidom

class Channel:

    def __init__(self, id, displayName, lang, iconSrc):
        self._id = id
        self._displayName = displayName
        self._iconSrc = iconSrc
        self._url = None
        self._category = None
        self._lang = lang

    def getId(self):
        return self._id

    def getDisplayName(self):
        return self._displayName

    def getIconSrc(self):
        return self._iconSrc

    def setUrl(self, url):
        self._url = url

    def setCategory(self, category):
        self._category = category

    def getCategory(self):
        return self._category

    def toxmltv(self):
        doc = minidom.Document()
        channel = doc.createElement("channel")
        channel.setAttribute("id",self._id)
        displayName = doc.createElement("display-name")
        displayName.setAttribute("lang",self._lang)
        displayName.appendChild(doc.createTextNode(self._displayName))
        channel.appendChild(displayName)

        if (self._iconSrc != None):
            icon = doc.createElement("icon")
            icon.setAttribute("src",str(self._iconSrc))
            channel.appendChild(icon)

        if (self._url != None):
            url = doc.createElement("url")
            url.appendChild(doc.createTextNode(self._url))
            channel.appendChild(url)

        if (self._category != None):
            cat = doc.createElement("category")
            cat.appendChild(doc.createTextNode(self._category))
            channel.appendChild(cat)

        return channel

