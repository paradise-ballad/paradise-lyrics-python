# -*- mode: python -*-
# vi: set ft=python :
# vi: set ts=4 :

import json
import requests

def dataLyricsBuild(trackIdSpotify, lyricsSyntax, urlSpotify):
    dataJsonResponse = internetRequestMethodGetFormatJson(urlSpotify)
    dataJsonStatusError = dataJsonResponse['error']
    #print(dataJsonResponse)

    if dataJsonStatusError == False:
        result = ''
        lyricsArray = dataLyricsGenerateMain(dataJsonResponse, lyricsSyntax)

        # Build all the lyrics content inside a single variable
        for i in range(len(lyricsArray)):
            result += lyricsArray[i]

            if i < len(lyricsArray) - 1:
                result += '\n'

        return result
    else:
        return 'Could not be found lyrics for this track!'
        #exit(3)

def dataLyricsGenerateMain(dataJsonResponse, lyricsSyntax):
    dataJsonStatusTypeSynchronized = dataJsonResponse['syncType']

    if dataJsonStatusTypeSynchronized == "LINE_SYNCED":
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
    resultContent = []
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
        #print(i, words[i])

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
            pass

        
        # Remove empty content from the last line
        if words[i] == '' and i == len(words) - 1:
            pass
        else:
            resultLineCurrent = f'{lyricsSyntaxPrefix}{words[i]}'

            resultContent.append(f'{resultLineCurrent}')


    return resultContent

def formatSyntaxLyricsAsHoursMinutesSecondsMilliseconds(durationMilliseconds):
    timeMilliseconds = timeConvertFromMillisecondsToHundredth(durationMilliseconds)
    timeSeconds = timeConvertFromMillisecondsToSeconds(durationMilliseconds)
    timeMinutes = timeConvertFromMillisecondsToMinutes(durationMilliseconds)
    timeHours = timeConvertFromMillisecondsToHours(durationMilliseconds)

    timeMilliseconds = timeClockDigitsInsertIfNeeds(timeMilliseconds)
    timeSeconds = timeClockDigitsInsertIfNeeds(timeSeconds)
    timeMinutes = timeClockDigitsInsertIfNeeds(timeMinutes)
    timeHours = timeClockDigitsInsertIfNeeds(timeHours)

    return f'{timeHours}:{timeMinutes}:{timeSeconds}:{timeMilliseconds}'

def formatSyntaxLyricsAsHoursMinutesSeconds(durationMilliseconds):
    timeMilliseconds = timeConvertFromMillisecondsToHundredth(durationMilliseconds)
    timeSeconds = timeConvertFromMillisecondsToSeconds(durationMilliseconds)
    timeMinutes = timeConvertFromMillisecondsToMinutes(durationMilliseconds)
    timeHours = timeConvertFromMillisecondsToHours(durationMilliseconds)

    timeSeconds = timeClockDigitsInsertIfNeeds(timeSeconds)
    timeMinutes = timeClockDigitsInsertIfNeeds(timeMinutes)
    timeHours = timeClockDigitsInsertIfNeeds(timeHours)

    return f'{timeHours}:{timeMinutes}:{timeSeconds}'

def formatSyntaxLyricsAsMinutesSecondsMilliseconds(durationMilliseconds):
    timeMilliseconds = timeConvertFromMillisecondsToHundredth(durationMilliseconds)
    timeSeconds = timeConvertFromMillisecondsToSeconds(durationMilliseconds)
    timeMinutes = timeConvertFromMillisecondsToMinutes(durationMilliseconds)
    timeHours = timeConvertFromMillisecondsToHours(durationMilliseconds)

    timeSeconds = timeClockDigitsInsertIfNeeds(timeSeconds)
    timeMinutes = timeClockDigitsInsertIfNeeds(timeMinutes)

    return f'{timeMinutes}:{timeSeconds}:{timeMilliseconds}'

def formatSyntaxLyricsAsMinutesSeconds(durationMilliseconds):
    timeMilliseconds = timeConvertFromMillisecondsToHundredth(durationMilliseconds)
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
    result = ''

    if lyricsSyntax == 'hh:mm:ss:ms' \
        or lyricsSyntax == 'hh:mm:ss' \
        or lyricsSyntax == 'mm:ss:ms' \
        or lyricsSyntax == 'mm:ss':
        result = f'\n[{lyricsSyntax}]'

    return result

def infoPrintHeader():
    result = '[Credit:Generated by Lyrics Paradise]'
    result += '\n[Source:https://github.com/henrikbeck95/paradise-lyrics]'
    result += '\n[ApiUrl:https://spotify-lyric-api.herokuapp.com/]'
    #result += '\n[length:mm:ss.mmm]'

    return result

def internetRequestMethodGetFormatJson(url):
    headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=headers)

    return r.json()

def primitiveConvertStringToNumber(numberString):
    if isinstance(numberString, str):
        numberString = float(numberString)

    return numberString

def timeClockDigitsInsertIfNeeds(digits):
    if digits < 10:
        digits = f"0{digits}"

    return digits

def timeConvertFromMillisecondsToHours(milliseconds):
    return int((milliseconds / (1000 * 60 * 60)) % 24)

def timeConvertFromMillisecondsToHundredth(milliseconds):
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