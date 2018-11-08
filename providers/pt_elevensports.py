# -*- coding: utf-8 -*-

import urllib
import datetime
import time
import json
from classes.xmltv.Channel import Channel
from classes.xmltv.Programme import Programme
from classes.xmltv.XMLTV import XMLTV

baseUrl = "http://www.elevensports.pt"
url="https://neulionmdnyc-a.akamaihd.net/u/mt1/elevensportspt/epg/{0}/{1}/{2}/{3}.js?"
iconUrlPrefix = "https://neulionsmbnyc-a.akamaihd.net/u/mt1/elevensportspt/thumbs/epg/"

def getEPG(list, nrDays):

    sDate = datetime.date.today()
    delta = datetime.timedelta(days=1)
    eDate = sDate + datetime.timedelta(days = nrDays)

    dstOffset = " +0000"
    if time.localtime( ).tm_isdst: dstOffset = " +0100"

    xmltv = XMLTV()
    provCodes = []

    for item in list:

        for channelInfo in item.getChannelList():
            c = Channel(channelInfo.getId(), channelInfo.getDisplayName(), "pt", channelInfo.getIconSrc())
            c.setUrl(baseUrl)
            xmltv.addChannel(c)

        while sDate < eDate:
            link = url.format(item.getProviderCode(),sDate.strftime("%Y"),sDate.strftime("%m"),sDate.strftime("%d"))
            #print(link)
            sDate += delta

            try:
                content = urllib.request.urlopen(link)
            except urllib.error.URLError as e:
                #print(e.reason)
                continue

            if content.getcode() != 200: continue
            myfile = content.read()
            myfile = myfile.replace(b'handleEPGCallback(',b'')
            myfile = myfile.rsplit(b')', 1)[0]
            try:
                myfile = json.loads(myfile)
            except ValueError:
                continue
            for program in myfile[0]["items"]:
                sTime = datetime.datetime.strptime(program["su"], "%Y-%m-%dT%H:%M:%S.000")
                sTime = sTime.strftime("%Y%m%d%H%M%S") + dstOffset
                eTime = datetime.datetime.strptime(program["sl"], "%Y-%m-%dT%H:%M:%S.000")
                eTime = eTime.strftime("%Y%m%d%H%M%S") + dstOffset
                title = program["e"]
                desc = program["t"] + " - " + program["e"]
                if "img" in program:
                    iconsrc = iconUrlPrefix + program["img"]

                for channelInfo in item.getChannelList():
                    p = Programme(channelInfo.getId(), sTime, eTime, title, desc, "pt", iconsrc)
                    xmltv.addProgramme(p)

    return xmltv
