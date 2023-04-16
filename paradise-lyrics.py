#!/usr/bin/env python3

# -*- mode: python -*-
# vi: set ft=python :
# vi: set ts=4 :

#import json
import argparse
import importlib

paradiseLibrary = importlib.import_module("paradise-library")

def main(trackIdSpotify, lyricsSyntax):
    urlSpotify = paradiseLibrary.urlGenerateBaseSpotify(trackIdSpotify)
    #print("Requesting the " + urlSpotify + " url...")

    # Implement header info
    lyricsContent = ''
    lyricsContent += paradiseLibrary.infoPrintHeader()
    lyricsContent += '\n'
    lyricsContent += paradiseLibrary.infoPrintFormatSyntax(lyricsSyntax)
    lyricsContent += '\n'

    # Implement the lyrics
    lyricsContent += paradiseLibrary.dataLyricsBuild(trackIdSpotify, lyricsSyntax, urlSpotify)
    
    print(lyricsContent)

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