#!/usr/bin/env python3

# -*- mode: python -*-
# vi: set ft=python :
# vi: set ts=4 :

import json
import argparse
import importlib

paradiseLibrary = importlib.import_module("paradise-library")

##############################
# Utilities
##############################

# TODO
# - [ ] Refactor this function by splitting it into smaller components
def main(trackIdSpotify, lyricsSyntax):
    urlSpotify = paradiseLibrary.urlGenerateBaseSpotify(trackIdSpotify)
    #print("Requesting the " + urlSpotify + " url...")

    dataJsonResponse = paradiseLibrary.internetRequestMethodGetFormatJson(urlSpotify)
    dataJsonStatusError = dataJsonResponse['error']
    #print(dataJsonResponse)

    if dataJsonStatusError == False:
        dataJsonStatusTypeSynchronized = dataJsonResponse['syncType']

        if dataJsonStatusTypeSynchronized == "LINE_SYNCED":
            #print('Synchronized lyrics are available \o/')
            #print(dataJsonResponse['lines'])
            #print(dataJsonResponse['lines'][2])
            #print(dataJsonResponse['lines'][2]['startTimeMs'])

            # Initialize the array variables
            startTimeMs = []
            words = []
            #syllables = []
            endTimeMs = []

            # Store the lines contents into an array
            for i in dataJsonResponse['lines']:
                startTimeMs.append(i['startTimeMs'])
                words.append(i['words'])
                #syllables.append(i['syllables'])
                endTimeMs.append(i['endTimeMs'])

            paradiseLibrary.infoPrintHeader()
            paradiseLibrary.infoPrintFormatSyntax(lyricsSyntax)

            # Generate the lyrics content
            for i in range(len(words)):
                lyricsSyntaxPrefix = ''
                timeMilliseconds = int(paradiseLibrary.primitiveConvertStringToNumber(startTimeMs[i]))

                if lyricsSyntax == 'hh:mm:ss:ms':
                    lyricsSyntaxPrefix = f'[{paradiseLibrary.formatSyntaxLyricsAsHoursMinutesSecondsMilliseconds(timeMilliseconds)}]'
                elif lyricsSyntax == 'hh:mm:ss':
                    lyricsSyntaxPrefix = f'[{paradiseLibrary.formatSyntaxLyricsAsHoursMinutesSeconds(timeMilliseconds)}]'
                elif lyricsSyntax == 'mm:ss:ms':
                    lyricsSyntaxPrefix = f'[{paradiseLibrary.formatSyntaxLyricsAsMinutesSecondsMilliseconds(timeMilliseconds)}]'
                elif lyricsSyntax == 'mm:ss':
                    lyricsSyntaxPrefix = f'[{paradiseLibrary.formatSyntaxLyricsAsMinutesSeconds(timeMilliseconds)}]'
                else:
                    lyricsSyntaxPrefix = ''

                print(f'{lyricsSyntaxPrefix}{words[i]}')
        else:
            print('Only static lyrics are available')
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