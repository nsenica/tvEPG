# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import json
import logging
import re
import ssl
from datetime import datetime, timedelta
from classes.xmltv.Channel import Channel
from classes.xmltv.Programme import Programme
from classes.xmltv.XMLTV import XMLTV

# Implements client for nostv.pt API
baseUrl = "https://nostv.pt"
apiKey = "xe1dgrShwdR1DVOKGmsj8Ut4QLlGyOFI"

ssl._create_default_https_context = ssl._create_unverified_context

def getEPG(list, nrDays):
    xmltv = XMLTV()

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,pt;q=0.6,cs;q=0.5',
        'cache-control': 'no-cache',
        'origin': 'https://nostv.pt',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://nostv.pt/',
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36',
        'x-apikey': apiKey,
        'x-core-appversion': '2.20.2.2',
        'x-core-contentratinglimit': '0',
        'x-core-deviceid': '',
        'x-core-devicetype': 'web',
        'x-core-timezoneoffset': '3600000'
    }

    # Fetch supported channels to validate
    supportedChannels = _getSupportedChannels(headers)

    for item in list:
        provider_code = item.getProviderCode()
        if supportedChannels is not None and provider_code in supportedChannels:
            for channelInfo in item.getChannelList():
                c = Channel(channelInfo.getId(), channelInfo.getDisplayName(), "pt", channelInfo.getIconSrc())
                c.setUrl(baseUrl)
                xmltv.addChannel(c)
                logging.debug("[NOS] Adding %s (%s)", channelInfo.getId(), channelInfo.getDisplayName())
        else:
            logging.warning("NOS: %s - Channel id not available." % format(provider_code))
            continue

        # Fetch EPG range
        today = datetime.utcnow()
        minDate = today.strftime("%Y-%m-%d") + "T00:00:00Z"
        maxDate = (today + timedelta(days=nrDays-1)).strftime("%Y-%m-%d") + "T23:59:59Z"

        url = f"https://api.clg.nos.pt/nostv/ott/schedule/range/contents/guest?channels={provider_code}&minDate={minDate}&maxDate={maxDate}&isDateInclusive=true&client_id={apiKey}"
        
        req = urllib.request.Request(url, headers=headers)
        try:
            content = urllib.request.urlopen(req, timeout=10)
            if content.getcode() != 200:
                logging.warning("Couldn't retrieve information for %s" % provider_code)
                continue
            
            myfile = content.read().decode('utf-8')
            programs_data = json.loads(myfile)
            
            for program in programs_data:
                # The dates are in UTC, e.g. "UtcDateTimeStart":"2026-06-08T23:51:00Z"
                try:
                    sTime_naive = datetime.strptime(program["UtcDateTimeStart"], "%Y-%m-%dT%H:%M:%SZ")
                    eTime_naive = datetime.strptime(program["UtcDateTimeEnd"], "%Y-%m-%dT%H:%M:%SZ")
                    
                    # Convert UTC dates to string format with +0000 timezone
                    sTime = sTime_naive.strftime("%Y%m%d%H%M%S") + " +0000"
                    eTime = eTime_naive.strftime("%Y%m%d%H%M%S") + " +0000"
                except Exception as e:
                    logging.error("[NOS] Error parsing dates: %s", e)
                    continue

                metadata = program.get("Metadata", {})
                title = metadata.get("Title") or "Sem título"
                desc = metadata.get("Description") or ""
                
                # Check for images
                icon = None
                images = program.get("Images")
                if images and len(images) > 0:
                    icon_url = images[0].get("Url")
                    if icon_url:
                        icon = f"https://mage.stream.nos.pt/mage/v1/Images?sourceUri={urllib.parse.quote(icon_url)}&profile=ott_1_452x340&client_id={apiKey}"

                for channelInfo in item.getChannelList():
                    p = Programme(channelInfo.getId(), sTime, eTime, title, desc, "pt", icon)
                    _findSeasonEpisode(title, p)
                    xmltv.addProgramme(p)
                    logging.debug("[NOS] Programme for %s (%s - %s) added", channelInfo.getId(), sTime, eTime)
                    
        except Exception as e:
            logging.error("[NOS] Failed fetching EPG for %s: %s", provider_code, e)

    return xmltv

def _findSeasonEpisode(title, p):
    m = re.match(r'.*(\s+|:)T\.?(\d+)(?:\s+-?\s*Ep.\s*)?(\d+)?$', title)
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

def _getSupportedChannels(headers):
    url = f"https://api.clg.nos.pt/nostv/ott/channels/guest?client_id={apiKey}"
    req = urllib.request.Request(url, headers=headers)
    try:
        content = urllib.request.urlopen(req, timeout=10)
        if content.getcode() != 200:
            return None
        myfile = content.read().decode('utf-8')
        channels_data = json.loads(myfile)
        channels = set()
        for item in channels_data:
            if item.get("ServiceId"):
                channels.add(str(item["ServiceId"]))
        return channels
    except Exception as e:
        logging.error("[NOS] Error fetching channels: %s", e)
        return None
