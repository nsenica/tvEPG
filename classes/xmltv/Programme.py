# -*- coding: utf-8 -*-

from xml.dom import minidom

class Programme:

    def __init__(self, channel, startTime, endTime, title, desc, lang, iconSrc):
        self._channel = channel
        self._sTime = startTime
        self._eTime = endTime
        self._title = title
        self._desc = desc
        self._lang = lang
        self._iconSrc = iconSrc

    def getChannel(self):
        return self._channel

    def getStartTime(self):
        return self._sTime

    def getEndTime(self):
        return self._eTime

    def getTitle(self):
        return self._title

    def getDesc(self):
        return self._desc

    def getIconSrc(self):
        return self._iconSrc

    def toxmltv(self):
        doc = minidom.Document()
        programme = doc.createElement("programme")
        programme.setAttribute("channel",self._channel)
        programme.setAttribute("start",self._sTime)
        programme.setAttribute("stop",self._eTime)

        #title
        title = doc.createElement("title")
        title.setAttribute("lang",self._lang)
        title.appendChild(doc.createTextNode(str(self._title)))
        programme.appendChild(title)

        #desc
        desc = doc.createElement("desc")
        desc.setAttribute("lang",self._lang)
        desc.appendChild(doc.createTextNode(format(self._desc)))
        programme.appendChild(desc)

        if (self._iconSrc != None):
            #icon
            icon = doc.createElement("icon")
            icon.setAttribute("src",str(self._iconSrc))
            programme.appendChild(icon)

        doc.appendChild(programme)
        return programme
