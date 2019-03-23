# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import time
import logging
import json
from datetime import datetime,timedelta
from classes.xmltv.Channel import Channel
from classes.xmltv.Programme import Programme
from classes.xmltv.XMLTV import XMLTV

# Implements basic client for https://meogo.meo.pt/tv/guia-tv
# List of channels: https://meogo.meo.pt/_layouts/15/Ptsi.Isites.GridTv/GridTvMng.asmx/getGridAnon
baseUrl = "https://meogo.meo.pt/tv/guia-tv"

def getEPG(list, nr_days):

    #get current and next day
    today= datetime.now()
    sDate=str(today.year)+"-"+str(today.month).zfill(2)+"-"+str(today.day).zfill(2)
    tomorrow=today+timedelta(days=nr_days)
    eDate=str(tomorrow.year)+"-"+str(tomorrow.month).zfill(2)+"-"+str(tomorrow.day).zfill(2)

    xmltv = XMLTV()
    supportedChannels = _getSupportedChannels()

    for item in list:

        if (supportedChannels != None and item.getProviderCode() in supportedChannels):

            for channelInfo in item.getChannelList():
                channel = Channel(channelInfo.getId(), channelInfo.getDisplayName(), "pt", channelInfo.getIconSrc())
                channel.setUrl(baseUrl)
                xmltv.addChannel(channel)
                logging.debug("[MEOGO] Adding %s (%s)", channelInfo.getId(), channelInfo.getDisplayName())

        else:
            logging.warning("MEOGO: %s - Channel id not available." % format(item.getProviderCode()))
            continue

        programIds = _getProgramIdsForChannel(item.getProviderCode(), sDate, eDate)

        for pid in programIds:
            d = _getProgramDetailsById(pid)
            if d is None:
                continue
                
            for channelInfo in item.getChannelList():
                p = Programme(channelInfo.getId(), d["sTime"], d["eTime"], d["title"], d["desc"], "pt", d["icon"])
                xmltv.addProgramme(p)

    return xmltv


def _getSupportedChannels():

    myfile = _getContents("https://meogo.meo.pt/_layouts/15/Ptsi.Isites.GridTv/GridTvMng.asmx/getGridAnon",{"service":"allchannels"})
    channels = set()

    if myfile is None:
        return channels

    for channel in myfile["d"]["channels"]:
        channels.add(channel["sigla"])

    return channels

def _getProgramIdsForChannel(sigla, sDate, eDate):

    payload = {"service":"channelsguide", "dateStart": sDate+"T00:00:00.000Z", "dateEnd": eDate+"T23:59:59.000Z","accountID":"", "channels": [( sigla )] }
    myfile = _getContents("https://meogo.meo.pt/_layouts/15/Ptsi.Isites.GridTv/GridTvMng.asmx/getProgramsFromChannels",payload)
    programs = list()

    if myfile is None:
        return programs

    for channel in myfile["d"]["channels"]:
        for program in channel["programs"]:
            programs.append(program["uniqueId"])

    return programs

def _getProgramDetailsById(progId):

    myfile = _getContents("https://meogo.meo.pt/_layouts/15/Ptsi.Isites.GridTv/GridTvMng.asmx/getProgramDetails",{"service":"programdetail","accountID":"", "programID": progId })
    
    if myfile is None:
        return None

    info = myfile["d"]
    
    dstOffset = " +0000"
    if time.localtime( ).tm_isdst: dstOffset = " +0100"

    date = info["date"].split('-')
    sTime = info["startTime"]
    eTime = info["endTime"]

    sTime = datetime(int(date[2]), int(date[1]), int(date[0]), int(sTime.split(":")[0]), int(sTime.split(":")[1]), 0)
    eTime = datetime(int(date[2]), int(date[1]), int(date[0]), int(eTime.split(":")[0]), int(eTime.split(":")[1]), 0)
    
    if (eTime < sTime):
        eTime += timedelta(days=1)

    sTime = sTime.strftime("%Y%m%d%H%M%S") + dstOffset
    eTime = eTime.strftime("%Y%m%d%H%M%S") + dstOffset

    return { "sTime": sTime , "eTime": eTime , "icon": info["progImageXL"], "title" : info["progName"], "desc" : info["description"] }

def _getContents(url,payload):

    data = json.dumps(payload).encode('utf-8')
    handler = urllib.request.HTTPSHandler(debuglevel=0)
    opener = urllib.request.build_opener(handler)
    request = urllib.request.Request(url, data=data, headers={'Content-type': 'application/json; charset=UTF-8', 'Accept': '*/*'})
    content = opener.open(request)

    if content.getcode() != 200: return None
    myfile = content.read().decode('utf8')
    try:
        myfile = json.loads(myfile)
    except ValueError:
        return None

    return myfile