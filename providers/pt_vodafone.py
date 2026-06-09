# -*- coding: utf-8 -*-

# Vodafone TV EPG via the public Kaltura "vtv" API.
#
#   GET https://cdn.pt.vtv.vodafone.com/epg/{site_id}/{YYYY}/{MM}/{DD}/{slot}
#
# Each day is fetched in four 6-hour windows (Europe/Lisbon time): 00-06,
# 06-12, 12-18, 18-00. The provider "code" in channelList.xml is the Vodafone
# site_id (e.g. 2687 = Sport TV 1). site_id <-> channel mappings come from:
#   https://github.com/iptv-org/epg/blob/master/sites/vodafone.pt/vodafone.pt.channels.xml

import urllib.request
from urllib.error import HTTPError, URLError
import datetime
import time
import json
import logging
import pytz
from classes.xmltv.Channel import Channel
from classes.xmltv.Programme import Programme
from classes.xmltv.XMLTV import XMLTV

API_ENDPOINT = "https://cdn.pt.vtv.vodafone.com/epg"
SLOTS = ["00-06", "06-12", "12-18", "18-00"]
HEADERS = {
    "Origin": "https://www.vodafone.pt",
    "Referer": "https://www.vodafone.pt/",
    "User-Agent": "Mozilla/5.0 (compatible; tv_grab_pt_vodafone)",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

tz = pytz.timezone("Europe/Lisbon")


def getEPG(items, nr_days):

    xmltv = XMLTV()
    today = datetime.datetime.now(tz)

    for item in items:

        site_id = item.getProviderCode()
        channelInfos = item.getChannelList()

        for channelInfo in channelInfos:
            channel = Channel(channelInfo.getId(), channelInfo.getDisplayName(), "pt", channelInfo.getIconSrc())
            channel.setUrl("https://www.vodafone.pt/")
            xmltv.addChannel(channel)
            logging.debug("[VODAFONE] Adding %s (%s)", channelInfo.getId(), channelInfo.getDisplayName())

        seen = set()
        got = 0

        for day in range(nr_days):
            d = today + datetime.timedelta(days=day)
            for slot in SLOTS:
                link = "%s/%s/%04d/%02d/%02d/%s" % (API_ENDPOINT, site_id, d.year, d.month, d.day, slot)
                logging.debug("[VODAFONE] Requesting %s", link)

                data = _get_json(link)
                if not data:
                    continue

                for obj in data.get("result", {}).get("objects", []):
                    pid = obj.get("id") or obj.get("crid")
                    if pid is not None and pid in seen:
                        continue
                    seen.add(pid)

                    for programme in _build_programmes(obj, channelInfos):
                        xmltv.addProgramme(programme)
                        got += 1

        if got == 0:
            logging.warning("[VODAFONE] %s - no programmes returned.", site_id)

    return xmltv


def _build_programmes(obj, channelInfos):

    try:
        start = int(obj["startDate"])
        end = int(obj["endDate"])
    except (KeyError, ValueError, TypeError):
        return []

    sTime = datetime.datetime.fromtimestamp(start, tz).strftime("%Y%m%d%H%M%S %z")
    eTime = datetime.datetime.fromtimestamp(end, tz).strftime("%Y%m%d%H%M%S %z")

    title = obj.get("name", "")
    desc = obj.get("description", "")

    iconSrc = None
    images = obj.get("images") or []
    if images:
        iconSrc = images[0].get("url")

    season = _meta(obj, "season number")

    programmes = []
    for channelInfo in channelInfos:
        p = Programme(channelInfo.getId(), sTime, eTime, title, desc, "pt", iconSrc)
        if season and season.isdigit() and int(season) > 0:
            p.setSeasonNumber(season)
        programmes.append(p)

    return programmes


def _meta(obj, key):
    meta = obj.get("metas", {}).get(key)
    if meta:
        return meta.get("value")
    return None


def _get_json(url):

    req = urllib.request.Request(url, headers=HEADERS)

    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.getcode() != 200:
                    return None
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            if e.code == 404:
                return None  # no listing for this day/slot
            logging.debug("[VODAFONE] HTTP %s for %s (attempt %d)", e.code, url, attempt)
        except (URLError, ValueError) as e:
            logging.debug("[VODAFONE] error %s for %s (attempt %d)", e, url, attempt)
        time.sleep(1)

    logging.warning("[VODAFONE] failed after retries: %s", url)
    return None
