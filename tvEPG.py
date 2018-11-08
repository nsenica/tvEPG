#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################
# tvEPG.py - EPG per channel per EPG provider
# Some logos taken from: https://grelha-tv.blogspot.nl/p/logos.html
# by nsenica
# v1.0 - 2018
#########################################

import utils.XMLChannelList as XMLChannelList
import providers.pt_meo
import providers.pt_vodafone
import providers.pt_elevensports
import providers.pt_nos
import sys
import time
import argparse
from classes.xmltv.Channel import Channel
from classes.xmltv.XMLTV import XMLTV

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Specify the input channel list file", default="channelList.xml")
parser.add_argument("-o", "--output", help="Specify the output XMLTV filename", default="guide.xml")
parser.add_argument("-d", "--days", help="Specify the number of days to process", type=int, default=8)
args = parser.parse_args()

##########################################
## channelFilename - Full filename (including path) for file which contains channels
## File format:
##  tvg-id - EPG code ID for channel under m3u list
##      name - channel name under m3u list
##      icon - Channel icon URL
##  provider - provider where to retrieve the information from
##      code - Code for which channel is recognized in EPG Service
channelFilename=args.input
##########################################

cList = XMLChannelList.load(channelFilename)
cDict = XMLChannelList.sortByProvider(cList)

nrDays = args.days

xmltv = XMLTV()

for provCode,xmlChannels in cDict.items():

    provXMLTV = None

    start = time.time()
    if provCode == "MEO":
        print("Getting info for MEO: " + str(len(xmlChannels)))
        provXMLTV = providers.pt_meo.getEPG(xmlChannels, nrDays)
    elif provCode == "VODAFONE":
        print("Getting info for VODAFONE: " + str(len(xmlChannels)))
        provXMLTV = providers.pt_vodafone.getEPG(xmlChannels, nrDays)

    elif provCode == "ES":
        print("Getting info for ES: " + str(len(xmlChannels)))
        provXMLTV = providers.pt_elevensports.getEPG(xmlChannels, nrDays)

    elif provCode == "NOS":
        print("Getting info for NOS: " + str(len(xmlChannels)))
        provXMLTV = providers.pt_nos.getEPG(xmlChannels, nrDays)
    else:
        print("No provider found for: ")
        for item in xmlChannels:
            for channelInfo in item.getChannelList():
                c = Channel(channelInfo.getId(), channelInfo.getDisplayName(), channelInfo.getLang(), channelInfo.getIconSrc())
                xmltv.addChannel(c)
                print(channelInfo.getDisplayName())
        print("Got " + str(len(xmltv.getChannels())))

    end = time.time()

    if (provXMLTV is not None):
        print("Got " + str(len(provXMLTV.getChannels())) + " channels and " + str(len(provXMLTV.getProgrammes())) + " programmes in " + str(int(end-start)) + " seconds.")
        xmltv.addFromXMLTV(provXMLTV)

    print("Total: " + str(len(xmltv.getChannels())) + " channels and " + str(len(xmltv.getProgrammes())) + " programmes.")

xmltv.writeXML(args.output)

print("Done")
