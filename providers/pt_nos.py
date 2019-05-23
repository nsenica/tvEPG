# -*- coding: utf-8 -*-

# Implements basic scapper for http://www.nos.pt/particulares/televisao/guia-tv/Pages/default.aspx
# List of channels as of 2018-10-24
# ChannelName, ChannelId
# 1+1,24
# 24Kitchen HD,243
# ACOLH,193
# Afro Music Channel,272
# Al Jazeera,108
# AMC HD,415
# AMC,436
# Angelus TV,439
# ARD,502
# ARTE,41
# ARTV,49
# Ativação NOS,395
# AXN Black HD,194
# AXN Black,164
# AXN HD,161
# AXN White HD,75
# AXN White,163
# AXN,77
# Baby TV,448
# BBC Entertainment,38
# BBC World News,45
# Biggs,176
# Blaze HD,509
# Blaze,81
# Bloomberg,44
# BNT World,124
# BTV1 HD,245
# BTV1,249
# BVN,28
# Canal 180,58
# Canal de Teste,349
# Canal Hollywood HD,14
# Canal Hollywood,13
# Canal NOS 1,518
# Canal NOS 2,519
# Canal NOS,408
# Canal NOS,999
# Canal Panda,31
# Canal Q,235
# Canal UM Europa,376
# Canção Nova,142
# Cartoon Network,252
# Caça e Pesca,129
# CCTV 4,316
# CGTN,312
# Chegou o Ultra HD 4K,88
# CMTV HD,425
# CMTV,381
# CNBC,52
# CNN,26
# Crime + Investigation,411
# Cubavisión Internacional,121
# Demonstração,4
# Discovery Channel,22
# Discovery HD Showcase,21
# Disney Channel,66
# Disney Junior,226
# DOGTV,371
# DSF,506
# DW,115
# E! Entertainment HD,202
# E! Entertainment,130
# Euronews,25
# Eurosport 1 HD,145
# Eurosport 1,10
# Eurosport 2,128
# Fight Network HD,236
# Fine Living Network HD,270
# Food Network HD,62
# FOX Comedy HD,113
# FOX Comedy,116
# FOX Crime HD,244
# FOX Crime,114
# FOX HD,174
# FOX Life HD,175
# FOX Life,86
# FOX Movies HD,242
# FOX Movies,177
# FOX,85
# France 24 (F),132
# France 24 (I),109
# FTV HD,47
# FTV,51
# Fuel TV HD,72
# Fuel TV,78
# Globo HD,447
# Globo Now HD,111
# Globo,230
# Globovision,500
# História,19
# HOT HD,222
# HOT,171
# ID Investigation Discovery,530
# IUTV,521
# KBS World HD,234
# Kuriakos TV,426
# Localvisão TV HD,229
# M6,37
# MAX,143
# MCM Pop,368
# MCM Top,34
# Mezzo Live HD,356
# Mezzo,50
# Motorvision HD,354
# MTV Dance,92
# MTV Music,91
# MTV Portugal HD,377
# MTV Portugal,36
# MTV Rocks,90
# MVM,133
# MyZen TV,167
# Nat Geo Wild HD,83
# Nat Geo Wild,82
# National Geographic HD,134
# National Geographic,59
# NHK World TV,46
# NICK JR,444
# Nickelodeon,94
# NOS Ultra HD 4K,389
# ODISSEIA HD,441
# Odisseia,20
# Outdoor Channel HD,60
# Penthouse HD1,365
# PFC,112
# Phoenix CNE,119
# Phoenix Infonews,120
# Playboy HD,69
# Porto Canal HD,423
# Porto Canal,105
# ProSieben,503
# Rai 1,507
# Rai 2,508
# Rai News 24,55
# Record News,30
# Record TV HD,350
# Record TV,101
# Regiões TV,149
# RTL,40
# RTP 1 HD,139
# RTP 1,5
# RTP 2,3
# RTP 3,64
# RTP Açores,106
# RTP Madeira,107
# RTP Memória,80
# RTP África,27
# RTR Planeta,117
# Russia Today,165
# S+ HD,510
# SAT 1,501
# SET Asia,144
# Sextreme,364
# SIC Caras HD,421
# SIC Caras,251
# SIC HD,418
# SIC Mulher HD,420
# SIC Mulher,71
# SIC Notícias HD,419
# SIC Notícias,9
# SIC Radical HD,422
# SIC Radical,61
# SIC,7
# Sky News,39
# SPORT TV 4K UHD,443
# SPORT TV+ HD,417
# SPORT TV+,416
# SPORT TV1 HD,137
# SPORT TV1,17
# SPORT TV2 HD,187
# SPORT TV2,95
# SPORT TV3 HD,188
# SPORT TV3,136
# SPORT TV4 HD,247
# SPORT TV4,246
# SPORT TV5 HD,180
# SPORT TV5,179
# Sporting TV HD,352
# Sporting TV,351
# Stingray iConcerts HD,42
# STV Notícias,343
# Sundance Channel HD,190
# Super RTL,200
# Syfy HD,201
# TCV Internacional,237
# TeleSUR,33
# Tiji,297
# TLC,23
# Toros TV HD,181
# TPA Internacional,138
# Trace Urban HD,65
# Travel Channel HD,70
# Travel Channel,100
# TV Galicia,54
# TV5 Monde,53
# TVCine 1 HD,141
# TVCine 1,16
# TVCine 2 HD,74
# TVCine 2,18
# TVCine 3 HD,223
# TVCine 3,76
# TVCine 4 HD,224
# TVCine 4,84
# TVE 24h,172
# TVEi,48
# TVI 24,160
# TVI Reality - Câmara 1,383
# TVI Reality - Câmara 2,384
# TVI Reality - Câmara 3,385
# TVI Reality - Câmara 4,386
# TVI Reality - Mosaico,387
# TVI Reality,382
# TVI,8
# TVR Internacional,123
# TVSéries HD,191
# TVSéries,186
# Venus,393
# VH1 Classic,93
# VH1,35
# VIVA Germany,505
# ZDF,504
# Zee TV,57

import urllib
import datetime
import time
import json
import logging
import re
from bs4 import BeautifulSoup
from classes.xmltv.Channel import Channel
from classes.xmltv.Programme import Programme
from classes.xmltv.XMLTV import XMLTV

baseUrl = "http://www.nos.pt"
url="https://www.nos.pt/particulares/televisao/guia-tv/Pages/channel.aspx?channel={0}"
programmeDetailsUrl = "https://www.nos.pt/_layouts/15/Armstrong/ApplicationPages/EPGGetProgramsAndDetails.aspx/GetProgramDetails"
iconUrlPrefix = "http://images.nos.pt/"

def getEPG(list, nrDays):

    today = sDate = datetime.date.today()

    dstOffset = " +0000"
    if time.localtime( ).tm_isdst: dstOffset = " +0100"

    xmltv = XMLTV()

    for item in list:

        for channelInfo in item.getChannelList():
            c = Channel(channelInfo.getId(), channelInfo.getDisplayName(), "pt", channelInfo.getIconSrc())
            c.setUrl(baseUrl)
            xmltv.addChannel(c)
            logging.debug("[NOS] Adding %s (%s)", channelInfo.getId(), channelInfo.getDisplayName())

        link = url.format(item.getProviderCode())
        logging.debug(link)

        f = urllib.request.urlopen(link)
        if f.getcode() != 200:
            logging.warning("Couldn't retrieve information for %s, HTTP Error code: %s " % item.getProviderCode(), f.getCode() )
            continue
        myfile = f.read()

        soup = BeautifulSoup(myfile, 'html.parser')

        cLogo = soup.find("div", id="channel-logo")
        cAcronym = cLogo.find("img").get("alt")

        all_days = soup.find_all("div", class_="programs-day-list")

        days_count = 0
        for day in all_days:
            sDate = today + datetime.timedelta(days = days_count )

            current_day = re.match(r'^day([\d]+)$', day.get("id"))

            current_day = current_day.group(1)

            if (int(current_day) != int(sDate.day)):
                logging.info("[NOS] Current day is not the same as the element being analyzed")
                continue

            if days_count >= nrDays:
                break

            logging.debug("[NOS] Processing date %s", sDate)

            days_count += 1

            items_count = 0
            for program in day.find_all("span", style="height: 55px"):
                # print(program)
                aNode = program.find("a")
                #title = aNode.get("title")
                #category = aNode.get("class")
                id = aNode.get("id")

                programNode = aNode.find("span", class_="program")
                desc = title = programNode.getText(strip=True)
                durationNode = aNode.find("span", class_="duration")
                duration = durationNode.getText(strip=True)
                duration = duration.split('-')
                sTime = duration[0].strip()
                eTime = duration[1].strip()
                eDate = sDate
                isDate = sDate

                if (eTime < sTime):
                    # First entry - Program from yesterday that continues today
                    if (items_count == 0):
                        isDate = sDate - datetime.timedelta(days = 1 )
                    # Last entry - Program from today that continues tomorrow, skip it as we'll catch it "tomorrow"
                    else:
                        continue
                items_count += 1

                sTime = datetime.datetime(isDate.year, isDate.month, isDate.day, int(sTime.split(":")[0]), int(sTime.split(":")[1]), 0)
                eTime = datetime.datetime(eDate.year, eDate.month, eDate.day, int(eTime.split(":")[0]), int(eTime.split(":")[1]), 0)

                if sTime >= datetime.datetime(2019,3,31,1,0,0) and sTime <= datetime.datetime(2019,3,31,4,0,0):
                    logging.info("[NOS] Skipping due to erroneous datetime handling during DST transition...")
                    continue

                if eTime >= datetime.datetime(2019,3,31,1,0,0) and eTime <= datetime.datetime(2019,3,31,4,0,0):
                    logging.info("[NOS] Skipping due to erroneous datetime handling during DST transition...")
                    continue

                sTime = sTime.strftime("%Y%m%d%H%M%S") + dstOffset
                eTime = eTime.strftime("%Y%m%d%H%M%S") + dstOffset
                icon = None

                logging.debug("[NOS] %s : Getting program details for %s (%s)", isDate, cAcronym, id)
                (_title, _desc, _icon, _sTime, _eTime) = _getProgrammeDetails(id, cAcronym, duration)

                if _title != None:
                    title = _title
                if _desc != None:
                    desc = _desc
                if _icon != None:
                    icon = _icon
#                if _sTime != None:
#                    sTime = _sTime
#                if _eTime != None:
#                    eTime = _eTime

                for channelInfo in item.getChannelList():
                    p = Programme(channelInfo.getId(), sTime, eTime, title, desc, "pt", icon)
                    xmltv.addProgramme(p)
                    _findSeasonEpisode(title,p)
                    logging.debug("[NOS] %s : Programme for %s (%s - %s) added", sDate, channelInfo.getId(), sTime, eTime)


    return xmltv

def _findSeasonEpisode(title,p):
    m = re.match(r'.*(\s+|:)T\.?(\d+)(?:\s+-?\s*Ep.\s*)?(\d+)?$', title)
    if m:
        season = m.group(2)
        if season:
            p.setSeasonNumber(season)
        episode = m.group(3)
        if episode:
            # Small hack because NOS adds the season to the episode number
            # so Season 2 Episode 10 becomes: Season 2 Episode 210
            # This attempts to solve it to the generic case.
            actual_episode_nr = (int(episode) - int(season)*100)
            if season and actual_episode_nr < 100 and actual_episode_nr > 0:
                episode = actual_episode_nr
            p.setEpisodeNumber(episode)
    else:
        m = re.match(r'.*\s+Ep.\s*(\d+)$', title)
        if m:
            episode = m.group(1)
            if episode:
                p.setEpisodeNumber(episode)

def _getProgrammeDetails(id, cAcronym, d):
    payload = {'programId':id,'channelAcronym':cAcronym,'hour':'0','startHour':d[0].strip(),'endHour':d[1].strip()}
    params = json.dumps(payload).encode('utf8')
    req = urllib.request.Request(programmeDetailsUrl, data=params, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)

    if response.getcode() == 200:
        data = response.read().decode('utf8')
        try:
            data = json.loads(data)
        except ValueError:
            logging.error("Error parsing json")
            return (None, None, None, None, None)

        values = data["d"]
        values = values.split("_#|$_")
        # print(values)
        title = values[0]
        desc = values[1]
        icon = iconUrlPrefix + values[2]
        transt = dict.fromkeys(map(ord, '-: T'), None)
        transt[ord('+')] = ' +'
        sTime = str(values[6]).translate(transt)
        eTime = str(values[7]).translate(transt)

        if (title == "Sem título..." or eTime == "false"):
            logging.debug(data)
            return (None, None, None, None, None)

    return (title, desc, icon, sTime, eTime)
















