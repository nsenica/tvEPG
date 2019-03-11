# -*- coding: utf-8 -*-

# # Implements basic scapper for https://tvnetvoz.vodafone.pt/sempre-consigo/
# List of channels: https://tvnetvoz.vodafone.pt/sempre-consigo/datajson/epg/channels.jsp

# As of 2018-10-19
# ChannelId, ChannelName
# 157,24Kitchen
# 196,24Kitchen HD
# 480,AMC
# 479,AMC HD
# 47,AXN
# 45,AXN Black
# 183,AXN Black HD
# 108,AXN HD
# 46,AXN White
# 184,AXN White HD
# 345,AfroMusic Portugal
# 100,Al Jazeera English
# 488,Angelus TV
# 499,Arirang TV
# 341,BBC Entertainment
# 37,BBC World News
# 35,Baby TV
# 230,Benfica TV
# 231,Benfica TV HD
# 21,Blaze
# 508,Blaze HD
# 59,Bloomberg
# 507,Boomerang
# 128,Brava TV HD
# 34,C Music TV
# 372,CANAL Q
# 498,CMTV HD
# 497,CMTV Portugal
# 42,CNBC
# 95,CNN
# 160,Canal 180
# 161,Canal 180 HD
# 16,Canal Parlamento
# 373,Canal Q HD
# 202,Canção Nova TV
# 236,Cartoon Network
# 241,Caza & Pesca
# 473,Caçavision
# 352,Cinemundo
# 355,Cinemundo SD
# 101,Cubavision
# 344,DJAZZ
# 348,DOGTV
# 94,Deutche Welle
# 89,Discovery
# 387,Discovery HD
# 48,Disney Channel
# 193,Disney Junior
# 412,Docubox HD
# 52,E!
# 188,E! HD
# 511,Eurochannel FR
# 510,Eurochannel PT
# 39,Euronews
# 481,Euronews EN
# 51,Eurosport
# 53,Eurosport 2
# 54,Eurosport HD
# 18,FOX
# 105,FOX Comedy
# 363,FOX Comedy HD
# 17,FOX Crime
# 30,Fashion TV
# 391,Fashion TV HD
# 351,FastnFunbox HD
# 374,Fight Network HD
# 350,Fightbox HD
# 127,Food Network
# 476,Food Network HD
# 199,Fox Crime HD
# 107,Fox HD
# 103,Fox Life
# 104,Fox Life HD
# 106,Fox Movies
# 197,Fox Movies HD
# 81,France 24 Eng
# 82,France 24 FR
# 9,Fuel TV
# 177,Fuel TV HD
# 125,GINX
# 15,Globo Now
# 417,Globo Now HD
# 20,História
# 19,Hollywood
# 478,Hollywood HD
# 368,KBS
# 405,Kuriakos TV
# 194,Localvisão
# 195,Localvisão HD
# 62,Luxe TV HD
# 240,M6
# 93,MCM POP
# 92,MCM TOP
# 356,MCM TOP SD
# 61,MEZZO
# 409,MEZZO Live HD
# 38,MTV Portugal
# 403,MTV Portugal HD
# 69,Melody Zen. TV
# 63,NGC Wild
# 360,NHK WORLD TV
# 36,Nat Geo
# 31,Nat Geo HD
# 198,Nat Geo Wild HD
# 73,Nautical Channel
# 22,Odisseia
# 490,Odisseia HD
# 66,PFC
# 375,PORTOC HD
# 55,PRO TV International
# 27,Panda
# 146,Panda Biggs
# 76,Phoenix InfoNews
# 80,Porto Canal
# 382,QYOU HD
# 380,QYOU SD
# 84,RAI 1
# 85,RAI News
# 243,RTL
# 1,RTP 1
# 171,RTP 1 HD
# 2,RTP 2
# 172,RTP 2 HD
# 3,RTP 3
# 5,RTP Africa
# 347,RTP Açores
# 504,RTP HD
# 342,RTP Madeira
# 4,RTP Memoria
# 110,RTPHD
# 155,Record News
# 91,Russia Today
# 489,Russia Today Documentary
# 130,SET Max
# 129,SET Ásia
# 11,SIC
# 371,SIC Caras
# 415,SIC Caras HD
# 173,SIC H
# 390,SIC HD
# 386,SIC K
# 416,SIC K HD
# 12,SIC Mulher
# 414,SIC Mulher HD
# 13,SIC Notícias
# 413,SIC Notícias HD
# 14,SIC Radical
# 392,SIC Radical HD
# 6,SPORT TV1
# 7,SPORT TV2
# 8,SPORT TV3
# 154,SPORT TV4
# 111,SPORT TV5
# 206,Sky News
# 407,Sport TV +
# 408,Sport TV + HD
# 151,Sport TV 1 HD
# 152,Sport TV 2 HD
# 153,Sport TV 3 HD
# 10,Sport TV 4 HD
# 112,Sport TV 5 HD
# 486,Sporting TV
# 487,Sporting TV HD
# 144,Star Gold
# 145,Star Plus
# 244,Super RTL
# 228,SyFy HD
# 227,SyFy SD
# 485,TCVi
# 385,TLC
# 43,TPA Internacional
# 149,TV Cine 1 HD
# 150,TV Cine 2 HD
# 200,TV Galicia
# 410,TV Globo Básico
# 501,TV Globo Básico HD
# 88,TV Record
# 238,TV Record HD
# 158,TV Series
# 159,TV Series HD
# 33,TV5 Monde
# 181,TVC 3 HD
# 182,TVC 4 HD
# 349,TVC NEWS
# 23,TVCine 1
# 24,TVCine 2
# 25,TVCine 3
# 26,TVCine 4
# 41,TVE 24h
# 40,TVE Internacional
# 28,TVI
# 174,TVI HD
# 113,TVI24
# 239,Touros
# 68,Trace TV
# 495,Trace TV HD
# 471,Trace Toca
# 56,Travel
# 475,Travel HD
# 50,VH1 Europe
# 245,VOX

import urllib.request
import datetime
import time
import json
from collections import defaultdict
from classes.xmltv.Channel import Channel
from classes.xmltv.Programme import Programme
from classes.xmltv.XMLTV import XMLTV
import logging


baseUrl = "http://www.vodafone.pt"
url="https://tvnetvoz.vodafone.pt/sempre-consigo/epg.do?action=getPrograms&chanids={0}&day={1}-{2}-{3}"
iconUrlPrefix = "http://web.ottimg.vodafone.pt/iptvimageserver/Get/{0}_{1}/16_9/325/244"

def getEPG(items, nr_days):

    sDate = datetime.date.today()
    delta = datetime.timedelta(days=1)
    eDate = sDate + datetime.timedelta(days = nr_days)

    dstOffset = " +0000"
    if time.localtime( ).tm_isdst: dstOffset = " +0100"

    provCodes = defaultdict(list)
    xmltv = XMLTV()

    supportedChannels = _getSupportedChannels()
    #print(supportedChannels)

    for item in items:

        if (supportedChannels != None and item.getProviderCode() in supportedChannels):
            for channelInfo in item.getChannelList():

                channel = Channel(channelInfo.getId(), channelInfo.getDisplayName(), "pt", channelInfo.getIconSrc())
                channel.setUrl(baseUrl)
                xmltv.addChannel(channel)
                provCodes[item.getProviderCode()].append(channelInfo.getId())
                logging.debug("[VODAFONE] Adding %s (%s)", channelInfo.getId(), channelInfo.getDisplayName())
        else:
            logging.warning("Vodafone: {0} - Channel id not available.".format(item.getProviderCode()))


    while sDate < eDate:
        link = url.format(",".join(provCodes.keys()),sDate.strftime("%Y"),sDate.strftime("%m"),sDate.strftime("%d"))
        sDate += delta

        content = urllib.request.urlopen(link)
        if content.getcode() != 200:
            logging.warning("Couldn't retrieve information for channels. HTTP Error code: %s " % content.getCode() )
            continue
        myfile = content.read().decode('utf8')
        try:
            myfile = json.loads(myfile)
        except ValueError:
            continue
        for channel in myfile["result"]["channels"]:
            for program in channel["programList"]:
                sTime = datetime.datetime.strptime(program["date"]+"T"+program["startTime"], "%d-%m-%YT%H:%M")
                eTime = sTime + datetime.timedelta( minutes=program["duration"])
                sTime = sTime.strftime("%Y%m%d%H%M%S") + dstOffset
                eTime = eTime.strftime("%Y%m%d%H%M%S") + dstOffset
                title = program["programTitle"]
                desc = program["programDetails"]
                iconSrc = iconUrlPrefix.format(urllib.parse.quote(channel["callLetter"]),program["pid"])
                for cid in provCodes[channel["id"]]:
                    p = Programme(cid, sTime, eTime, title, desc, "pt", iconSrc)
                    xmltv.addProgramme(p)

    return xmltv

def _getSupportedChannels():

    url = "https://tvnetvoz.vodafone.pt/sempre-consigo/datajson/epg/channels.jsp"

    channels = set()

    content = urllib.request.urlopen(url)
    if content.getcode() != 200: return None
    myfile = content.read().decode('utf8')
    try:
        myfile = json.loads(myfile)
    except ValueError:
        return None

    for channel in myfile["result"]["channels"]:
        channels.add(channel["id"])

    return channels
