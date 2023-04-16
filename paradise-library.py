# -*- mode: python -*-
# vi: set ft=python :
# vi: set ts=4 :

import json
import requests

def dataLyricsBuild(trackIdSpotify, lyricsSyntax):
    urlSpotify = urlGenerateBaseSpotify(trackIdSpotify)
    #print("Requesting the " + urlSpotify + " url...")

    dataJsonResponse = internetRequestMethodGetFormatJson(urlSpotify)
    dataJsonStatusError = dataJsonResponse['error']
    #print(dataJsonResponse)

    if dataJsonStatusError == False:
        return dataLyricsGenerateMain(dataJsonResponse, lyricsSyntax)
    else:
        return 'Could not be found lyrics for this track!'
        #exit(3)

def dataLyricsGenerateMain(dataJsonResponse, lyricsSyntax):
    dataJsonStatusTypeSynchronized = dataJsonResponse['syncType']

    if dataJsonStatusTypeSynchronized == "LINE_SYNCED":
        infoPrintHeader()
        infoPrintFormatSyntax(lyricsSyntax)

        return dataLyricsGenerateSynchronized(dataJsonResponse, lyricsSyntax)
    else:
        return dataLyricsGenerateStatic(dataJsonResponse, lyricsSyntax)

def dataLyricsGenerateStatic(dataJsonResponse, lyricsSyntax):
    return 'There is only static lyrics available.\nWe are working to implementing this function soon!'

def dataLyricsGenerateSynchronized(dataJsonResponse, lyricsSyntax):
    #print('Synchronized lyrics are available \o/')
    #print(dataJsonResponse['lines'])
    #print(dataJsonResponse['lines'][2])
    #print(dataJsonResponse['lines'][2]['startTimeMs'])

    # Initialize the variables
    lyricsSyntaxPrefix = ''
    resultContent = ''
    resultLineCurrent = ''

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

    # Generate the lyrics content
    for i in range(len(words)):
        timeMilliseconds = int(primitiveConvertStringToNumber(startTimeMs[i]))

        if lyricsSyntax == 'hh:mm:ss:ms':
            lyricsSyntaxPrefix = f'[{formatSyntaxLyricsAsHoursMinutesSecondsMilliseconds(timeMilliseconds)}]'
        elif lyricsSyntax == 'hh:mm:ss':
            lyricsSyntaxPrefix = f'[{formatSyntaxLyricsAsHoursMinutesSeconds(timeMilliseconds)}]'
        elif lyricsSyntax == 'mm:ss:ms':
            lyricsSyntaxPrefix = f'[{formatSyntaxLyricsAsMinutesSecondsMilliseconds(timeMilliseconds)}]'
        elif lyricsSyntax == 'mm:ss':
            lyricsSyntaxPrefix = f'[{formatSyntaxLyricsAsMinutesSeconds(timeMilliseconds)}]'
        else:
            lyricsSyntaxPrefix = ''

        resultLineCurrent = f'{lyricsSyntaxPrefix}{words[i]}'

        #print(resultLineCurrent)
        resultContent += (f'{resultLineCurrent}\n')
    
    return resultContent

def formatSyntaxLyricsAsHoursMinutesSecondsMilliseconds(durationMilliseconds):
    timeMilliseconds = timeConvertFromMillisecondsToMilliseconds(durationMilliseconds)
    timeSeconds = timeConvertFromMillisecondsToSeconds(durationMilliseconds)
    timeMinutes = timeConvertFromMillisecondsToMinutes(durationMilliseconds)
    timeHours = timeConvertFromMillisecondsToHours(durationMilliseconds)

    timeMilliseconds = timeClockDigitsInsertIfNeeds(timeMilliseconds)
    timeSeconds = timeClockDigitsInsertIfNeeds(timeSeconds)
    timeMinutes = timeClockDigitsInsertIfNeeds(timeMinutes)
    timeHours = timeClockDigitsInsertIfNeeds(timeHours)

    return f'{timeHours}:{timeMinutes}:{timeSeconds}:{timeMilliseconds}'

def formatSyntaxLyricsAsHoursMinutesSeconds(durationMilliseconds):
    timeMilliseconds = timeConvertFromMillisecondsToMilliseconds(durationMilliseconds)
    timeSeconds = timeConvertFromMillisecondsToSeconds(durationMilliseconds)
    timeMinutes = timeConvertFromMillisecondsToMinutes(durationMilliseconds)
    timeHours = timeConvertFromMillisecondsToHours(durationMilliseconds)

    timeSeconds = timeClockDigitsInsertIfNeeds(timeSeconds)
    timeMinutes = timeClockDigitsInsertIfNeeds(timeMinutes)
    timeHours = timeClockDigitsInsertIfNeeds(timeHours)

    return f'{timeHours}:{timeMinutes}:{timeSeconds}'

def formatSyntaxLyricsAsMinutesSecondsMilliseconds(durationMilliseconds):
    timeMilliseconds = timeConvertFromMillisecondsToMilliseconds(durationMilliseconds)
    timeSeconds = timeConvertFromMillisecondsToSeconds(durationMilliseconds)
    timeMinutes = timeConvertFromMillisecondsToMinutes(durationMilliseconds)
    timeHours = timeConvertFromMillisecondsToHours(durationMilliseconds)

    timeSeconds = timeClockDigitsInsertIfNeeds(timeSeconds)
    timeMinutes = timeClockDigitsInsertIfNeeds(timeMinutes)

    return f'{timeMinutes}:{timeSeconds}:{timeMilliseconds}'

def formatSyntaxLyricsAsMinutesSeconds(durationMilliseconds):
    timeMilliseconds = timeConvertFromMillisecondsToMilliseconds(durationMilliseconds)
    timeSeconds = timeConvertFromMillisecondsToSeconds(durationMilliseconds)
    timeMinutes = timeConvertFromMillisecondsToMinutes(durationMilliseconds)
    timeHours = timeConvertFromMillisecondsToHours(durationMilliseconds)

    timeSeconds = timeClockDigitsInsertIfNeeds(timeSeconds)
    timeMinutes = timeClockDigitsInsertIfNeeds(timeMinutes)

    return f'{timeMinutes}:{timeSeconds}'

def infoPrintCredits():
    print('Author: Henrik Beck')
    print('E-mail: henrikbeck95@gmail.com')
    print('Project: https://github.com/henrikbeck95/paradise-lyrics')
    print('License: GPL3')
    print('Version: v0.0.1')
    print('Warning: All the data is provide from a third API.')
    print('Lyrics source: https://spotify-lyric-api.herokuapp.com')

def infoPrintFormatSyntax(lyricsSyntax):
    if lyricsSyntax == 'hh:mm:ss:ms' \
        or lyricsSyntax == 'hh:mm:ss' \
        or lyricsSyntax == 'mm:ss:ms' \
        or lyricsSyntax == 'mm:ss':
        print(f'[{lyricsSyntax}]')

def infoPrintHeader():
    print('[Credit:Generated by Lyrics Paradise]')
    print('[Source:https://github.com/henrikbeck95/paradise-lyrics]')
    print('[ApiUrl:https://spotify-lyric-api.herokuapp.com/]')
    #print('[length:mm:ss.mmm]')
    print('')

def internetRequestMethodGetFormatJson(url):
    headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=headers)

    return r.json()

def primitiveConvertStringToNumber(number):
    if isinstance(number, str):
        number = float(number)
    
    return number

def timeClockDigitsInsertIfNeeds(digits):
    if digits < 10:
        digits = f"0{digits}"

    return digits

def timeConvertFromMillisecondsToHours(milliseconds):
    return int((milliseconds / (1000 * 60 * 60)) % 24)

def timeConvertFromMillisecondsToMilliseconds(milliseconds):
    return int((milliseconds % 1000) / 10)

def timeConvertFromMillisecondsToMinutes(milliseconds):
    return int((milliseconds / (1000 * 60)) % 60)

def timeConvertFromMillisecondsToSeconds(milliseconds):
    return int((milliseconds / 1000) % 60)

def urlGenerateBaseSpotify(trackId):
    urlBase = 'https://spotify-lyric-api.herokuapp.com/?url='
    urlSpotify = 'https://open.spotify.com/track/'
    urlSuffix='?autoplay=true'

    return urlBase + urlSpotify + trackId + urlSuffix