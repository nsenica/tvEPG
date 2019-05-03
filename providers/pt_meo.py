# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import xml.dom.minidom
import time
import logging
import re
from datetime import datetime,timedelta
from classes.xmltv.Channel import Channel
from classes.xmltv.Programme import Programme
from classes.xmltv.XMLTV import XMLTV

# Implements basic client for services.sapo.pt
# List of channels: http://services.sapo.pt/EPG/GetChannelList
baseUrl = "http://www.meo.pt"
url="http://services.sapo.pt/EPG/GetChannelByDateInterval?channelSigla={0}&startDate={1}+00%3A00%3A00&endDate={2}+23%3A59%3A59"

def getEPG(list, nr_days):

    #get current and next day
    today= datetime.now()
    sDate=str(today.year)+"-"+str(today.month).zfill(2)+"-"+str(today.day).zfill(2)
    tomorrow=today+timedelta(days=nr_days)
    eDate=str(tomorrow.year)+"-"+str(tomorrow.month).zfill(2)+"-"+str(tomorrow.day).zfill(2)

    dstOffset = " +0000"
    if time.localtime( ).tm_isdst: dstOffset = " +0100"

    xmltv = XMLTV()
    supportedChannels = _getSupportedChannels()

    for item in list:

        if (supportedChannels != None and item.getProviderCode() in supportedChannels):

            for channelInfo in item.getChannelList():
                channel = Channel(channelInfo.getId(), channelInfo.getDisplayName(), "pt", channelInfo.getIconSrc())
                channel.setUrl(baseUrl)
                xmltv.addChannel(channel)
                logging.debug("[MEO] Adding %s (%s)", channelInfo.getId(), channelInfo.getDisplayName())

        else:
            logging.warning("MEO: %s - Channel id not available." % format(item.getProviderCode()))
            continue

        link = url.format(urllib.parse.quote(item.getProviderCode()), sDate, eDate)
        logging.debug(link)
        #read web-service
        content = urllib.request.urlopen(link)
        myfile = content.read()

        #xml parse
        DOMTree = xml.dom.minidom.parseString(myfile)
        collection = DOMTree.documentElement
        programs = collection.getElementsByTagName("Program")

        for program in programs:
            title = program.getElementsByTagName("Title")[0].firstChild.data
            desc = program.getElementsByTagName("Description")[0].firstChild.data
            sTime = program.getElementsByTagName("StartTime")[0].firstChild.data
            eTime = program.getElementsByTagName("EndTime")[0].firstChild.data
            startTime = program.getElementsByTagName('StartTime')[0]
            endTime = program.getElementsByTagName('EndTime')[0]

            dstSTime = datetime.strptime(startTime.firstChild.data, "%Y-%m-%d %H:%M:%S")
            dstETime = datetime.strptime(endTime.firstChild.data, "%Y-%m-%d %H:%M:%S")
            
            if dstSTime >= datetime(2019,3,31,1,0,0) and dstSTime <= datetime(2019,3,31,4,0,0):
                logging.info("[MEO] Skipping due to erroneous datetime handling during DST transition...")
                continue

            if dstETime >= datetime(2019,3,31,1,0,0) and dstETime <= datetime(2019,3,31,4,0,0):
                logging.info("[MEO] Skipping due to erroneous datetime handling during DST transition...")
                continue
            
            transt = dict.fromkeys(map(ord, '-: '), None)
            sTime=str(startTime.firstChild.data).translate(transt) + dstOffset
            eTime=str(endTime.firstChild.data).translate(transt) + dstOffset

            

            for channelInfo in item.getChannelList():
                p = Programme(channelInfo.getId(), sTime, eTime, title, desc, "pt", None)
                _findSeasonEpisode(title,p)
                xmltv.addProgramme(p)


        #break

    return xmltv

def _findSeasonEpisode(title,p):
    m = re.match(r'.*(\s+|:)T(\d+)(?:\s+-?\s*Ep.\s*)?(\d+)?$', title)
    if m:
        season = m.group(2)
        if season:
            p.setSeasonNumber(season)
        episode = m.group(3)
        if episode:
            p.setEpisodeNumber(episode)
    else:
        m = re.match(r'.*\s+Ep.\s*(\d+)$', title)
        if m:
            episode = m.group(1)
            if episode:
                p.setEpisodeNumber(episode)

def _getSupportedChannels():

    url = "http://services.sapo.pt/EPG/GetChannelList"

    channels = set()

    content = urllib.request.urlopen(url)
    myfile = content.read()
    DOMTree = xml.dom.minidom.parseString(myfile)
    collection = DOMTree.documentElement
    siglas = collection.getElementsByTagName("Sigla")

    for sigla in siglas:
        channels.add(sigla.firstChild.data)

    return channels
