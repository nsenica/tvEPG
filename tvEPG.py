#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################
# tvEPG.py - EPG per channel per EPG provider
# Some logos taken from: https://grelha-tv.blogspot.nl/p/logos.html
# by nsenica
# v1.0 - 2018
#########################################

import utils.XMLChannelList as XMLChannelList
import sys
import time
import argparse
import logging
from classes.xmltv.Channel import Channel
from classes.xmltv.XMLTV import XMLTV
from providers import *


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Specify the input channel list file", default="channelList.xml")
parser.add_argument("-o", "--output", help="Specify the output XMLTV filename", default="guide.xml")
parser.add_argument("-d", "--days", help="Specify the number of days to process", type=int, default=8)
parser.add_argument("-p", "--provider", help="Filter on provider", default=None)
parser.add_argument("-c", "--channel", help="Filter on channel (name)", default=None)
parser.add_argument("--debug", help="Turn debug on", action="store_true")
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

if (args.debug):
    logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', level="DEBUG")
else:
    logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', level="INFO")

cDict = XMLChannelList.load(channelFilename, args.provider, args.channel)

if not cDict:
    exit()

nrDays = args.days

xmltv = XMLTV()

for provCode,xmlChannels in cDict.items():

    provXMLTV = None

    start = time.time()
    if provCode == "MEO":
        logging.info("Getting info for MEO: " + str(len(xmlChannels)))
        provXMLTV = pt_meo.getEPG(xmlChannels, nrDays)

    elif provCode == "MEOGO":
        logging.info("Getting info for MEOGO: " + str(len(xmlChannels)))
        provXMLTV = pt_meo_go.getEPG(xmlChannels, nrDays)

    elif provCode == "VODAFONE":
        logging.info("Getting info for VODAFONE: " + str(len(xmlChannels)))
        provXMLTV = pt_vodafone.getEPG(xmlChannels, nrDays)

    elif provCode == "ES":
        logging.info("Getting info for ES: " + str(len(xmlChannels)))
        provXMLTV = pt_elevensports.getEPG(xmlChannels, nrDays)

    elif provCode == "NOS":
        logging.info("Getting info for NOS: " + str(len(xmlChannels)))
        provXMLTV = pt_nos.getEPG(xmlChannels, nrDays)
    else:
        logging.info("No provider found for: ")
        for item in xmlChannels:
            for channelInfo in item.getChannelList():
                c = Channel(channelInfo.getId(), channelInfo.getDisplayName(), channelInfo.getLang(), channelInfo.getIconSrc())
                xmltv.addChannel(c)
                logging.info("\t" + channelInfo.getDisplayName())
        logging.info("Got " + str(len(xmltv.getChannels())))

    end = time.time()

    if (provXMLTV is not None):
        logging.info("["+provCode+"] Got " + str(len(provXMLTV.getChannels())) + " channels and " + str(len(provXMLTV.getProgrammes())) + " programmes in " + str(int(end-start)) + " seconds.")
        xmltv.addFromXMLTV(provXMLTV)

    logging.info("Total: " + str(len(xmltv.getChannels())) + " channels and " + str(len(xmltv.getProgrammes())) + " programmes.")

xmltv.writeXML(args.output)
