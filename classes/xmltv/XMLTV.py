# -*- coding: utf-8 -*-

from xml.dom.minidom import getDOMImplementation

class XMLTV:

    def __init__(self):
        self._channels = []
        self._programmes = []

    def addChannel(self, channel):
        self._channels.append(channel)

    def getChannels(self):
        return self._channels

    def addProgramme(self, programme):
        self._programmes.append(programme)

    def getProgrammes(self):
        return self._programmes

    def addFromXMLTV(self, xmltv):
        channels = xmltv.getChannels()
        if channels != None and len(channels) > 0:
            self._channels.extend(channels)

        programmes = xmltv.getProgrammes()
        if (programmes != None and len(programmes) > 0):
            self._programmes.extend(programmes)

    def print(self):
        xmldoc = self._generateXML()
        print(xmldoc.toprettyxml())

    def writeXML(self, filename):
        xmldoc = self._generateXML()

        file_handle = open(filename,"w")
        xmldoc.writexml(file_handle,indent="  ",addindent="  ", newl='\n')
        file_handle.close()

    def _generateXML(self):
        _impl = getDOMImplementation()
        _newdoc = _impl.createDocument(None, "tv", None)
        _root = _newdoc.documentElement

        for ch in self._channels:
            _root.appendChild(ch.toxmltv())

        for p in self._programmes:
            _root.appendChild(p.toxmltv())

        _newdoc.appendChild(_root)

        return _newdoc