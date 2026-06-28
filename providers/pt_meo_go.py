# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import time
import logging
import json
import re
import ssl
import pytz
from datetime import datetime, timedelta
from classes.xmltv.Channel import Channel
from classes.xmltv.Programme import Programme
from classes.xmltv.XMLTV import XMLTV

# Implements client for meogouser.apps.meo.pt APIs
baseUrl = "https://www.meo.pt"

ssl._create_default_https_context = ssl._create_unverified_context

def getEPG(list, nr_days):
    xmltv = XMLTV()
    supportedChannels = _getSupportedChannels()

    tz = pytz.timezone("Europe/Lisbon")

    for item in list:
        provider_code = item.getProviderCode()
        if supportedChannels is not None and provider_code in supportedChannels:
            for channelInfo in item.getChannelList():
                channel = Channel(channelInfo.getId(), channelInfo.getDisplayName(), "pt", channelInfo.getIconSrc())
                channel.setUrl(baseUrl)
                xmltv.addChannel(channel)
                logging.debug("[MEOGO] Adding %s (%s)", channelInfo.getId(), channelInfo.getDisplayName())
        else:
            logging.warning("[MEOGO] %s - Channel id not available." % format(provider_code))
            continue

        # Fetch programs day-by-day
        today = datetime.now(tz)
        for i in range(nr_days):
            current_day = today + timedelta(days=i)
            date_str = current_day.strftime("%Y-%m-%d")
            
            programs_data = _getProgramsForChannel(provider_code, date_str)
            if not programs_data:
                continue
            
            for prog in programs_data:
                try:
                    sTime_naive = datetime.strptime(prog["StartDate"], "%Y-%m-%dT%H:%M:%S")
                    eTime_naive = datetime.strptime(prog["EndDate"], "%Y-%m-%dT%H:%M:%S")

                    # The MEO API returns times in UTC. Treat them as UTC, then
                    # convert to Lisbon local time so the +0000/+0100 offset is
                    # correct year-round (was off by one hour during DST/WEST).
                    sTime_loc = pytz.utc.localize(sTime_naive).astimezone(tz)
                    eTime_loc = pytz.utc.localize(eTime_naive).astimezone(tz)

                    sTime = sTime_loc.strftime("%Y%m%d%H%M%S %z")
                    eTime = eTime_loc.strftime("%Y%m%d%H%M%S %z")
                except Exception as e:
                    logging.error("[MEOGO] Error parsing program date: %s", e)
                    continue

                title = prog.get("Title") or "Sem título"
                desc = prog.get("Synopsis") or ""
                
                # Construct image URL using program title
                icon = None
                if title:
                    encodedTitle = urllib.parse.quote(title)
                    icon = f"https://cdn-er-images.online.meo.pt/eemstb/ImageHandler.ashx?chCallLetter={provider_code}&progTitle={encodedTitle}&profile=16_9&profileFallback=false&noFallback=true&appSource=PC_CHROME_PWA&width=1920&csf"

                for channelInfo in item.getChannelList():
                    p = Programme(channelInfo.getId(), sTime, eTime, title, desc, "pt", icon)
                    _findSeasonEpisode(title, p)
                    xmltv.addProgramme(p)
                    logging.debug("[MEOGO] Programme for %s (%s - %s) added", channelInfo.getId(), sTime, eTime)

    return xmltv

def _findSeasonEpisode(title, p):
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

def _getContents(url):
    req = urllib.request.Request(
        url,
        headers={
            'Origin': 'https://www.meo.pt',
            'Referer': 'https://www.meo.pt/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36',
            'Accept': '*/*'
        }
    )
    try:
        content = urllib.request.urlopen(req, timeout=10)
        if content.getcode() != 200:
            return None
        myfile = content.read().decode('utf-8')
        return json.loads(myfile)
    except Exception as e:
        logging.error("[MEOGO] HTTP request failed: %s", e)
        return None

def _getSupportedChannels():
    url = "https://meogouser.apps.meo.pt/Services/GridTv/GridTv.svc/GetContentsForChannels?userAgent=IPTV_OFR_GTV"
    data = _getContents(url)
    channels = set()
    if data is None or data.get("Status") != "OK":
        return channels
    for channel in data.get("Result", []):
        if channel.get("CallLetter"):
            channels.add(channel["CallLetter"])
    return channels

def _getProgramsForChannel(sigla, date_str):
    url = f"https://meogouser.apps.meo.pt/Services/GridTv/GridTv.svc/GetLiveChannelProgramsByDate?callLetter={urllib.parse.quote(sigla)}&date={date_str}&userAgent=IPTV_OFR_GTV"
    data = _getContents(url)
    if data is None or data.get("Status") != "OK":
        return []
    return data.get("Result", [])
