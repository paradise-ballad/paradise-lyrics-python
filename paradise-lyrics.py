#!/usr/bin/env python3

# -*- mode: python -*-
# vi: set ft=python :
# vi: set ts=4 :

import json
import argparse
import importlib

paradiseLibrary = importlib.import_module("paradise-library")

def main(trackIdSpotify, lyricsSyntax):
    urlSpotify = paradiseLibrary.urlGenerateBaseSpotify(trackIdSpotify)
    #print("Requesting the " + urlSpotify + " url...")

    dataJsonResponse = paradiseLibrary.internetRequestMethodGetFormatJson(urlSpotify)
    dataJsonStatusError = dataJsonResponse['error']
    #print(dataJsonResponse)

    if dataJsonStatusError == False:
        dataJsonStatusTypeSynchronized = dataJsonResponse['syncType']

        if dataJsonStatusTypeSynchronized == "LINE_SYNCED":
            paradiseLibrary.infoPrintHeader()
            paradiseLibrary.infoPrintFormatSyntax(lyricsSyntax)
            
            lyrics = paradiseLibrary.dataGenerateLyricsSynchronized(dataJsonResponse, lyricsSyntax)

            print(lyrics)

            exit(0)
            
        else:
            paradiseLibrary.dataGenerateLyricsStatic(dataJsonResponse, lyricsSyntax)

            exit(0)

    else:
        print('Could not be found lyrics for this track!')
        exit(3)

##############################
# Arguments treatment
##############################

# Command line interface (CLI) interaction
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--syntax', help='Inform the syntax format')
parser.add_argument('-t', '--track', help='Inform the track id value')
parser.add_argument('-v', '--version', help='Display Lyrics From Paradise version')
args = parser.parse_args()

# Initialize variables
lyricsSyntax = ""
trackIdSpotify = ""

if args.version:
    paradiseLibrary.infoPrintCredits()
    exit(0)

if args.syntax:
    #print(f'Syntax value: {args.syntax}')
    lyricsSyntax = args.syntax

if args.track:
    #print(f'Track value: {args.track}')
    trackIdSpotify = args.track
else:
    print('Track id value must be informed')
    exit(1)

##############################
# Calling the functions
##############################

main(trackIdSpotify, lyricsSyntax)