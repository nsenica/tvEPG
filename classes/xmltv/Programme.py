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
        self._episodeNumber = None
        self._seasonNumber = None

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

    def setEpisodeNumber(self, episodeNumber):
        self._episodeNumber = episodeNumber
    
    def setSeasonNumber(self, seasonNumber):
        self._seasonNumber = seasonNumber

    def getEpisodeNumXmltvNS(self):
        season = ""
        if (self._seasonNumber != None and int(self._seasonNumber) > 0):
            season = int(self._seasonNumber) - 1
        episode = ""
        if (self._episodeNumber != None and int(self._episodeNumber) > 0):
            episode = int(self._episodeNumber) - 1

        if (season == "" and episode == ""):
            return None

        return "%s.%s." % (str(season), str(episode))


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

        #episode-num
        xmltv_ns = self.getEpisodeNumXmltvNS()
        if (xmltv_ns != None):
            en = doc.createElement("episode-num")
            en.setAttribute("system","xmltv_ns")
            en.appendChild(doc.createTextNode(xmltv_ns))
            programme.appendChild(en)

        if (self._iconSrc != None):
            #icon
            icon = doc.createElement("icon")
            icon.setAttribute("src",str(self._iconSrc))
            programme.appendChild(icon)

        doc.appendChild(programme)
        return programme
