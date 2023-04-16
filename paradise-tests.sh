#!/bin/sh

# -*- mode: sh -*-
# vi: set ft=sh :
# vi: set ts=4 :

##############################
# Instructions
##############################
#
# For running this script tool it is recomended
# to be inside the root of this project
#
##############################

##############################
# Declaring the variables
##############################

PATH_OUTPUT_DIRECTORY="./dist"
#TRACK_ID="0nLiqZ6A27jJri2VCalIUz" # Invalid
TRACK_ID="0nLiqZ6A27jJri2VCalIUs" # Valid
TRACK_NAME="nothing_else_matters"
EXTENSION="lrc"

##############################
# Functions
##############################

# TODO
# [ ] Implement colorized text according to the status message
display_message() {
	STATUS="$1"
	MESSAGE="$2"

	if [ "$STATUS" == "fail" ]; then
		printf " %s" "$MESSAGE"
	elif [ "$STATUS" == "success" ]; then
		printf " %s" "$MESSAGE"
	elif [ "$STATUS" == "warning" ]; then
		printf "\n%s" "$MESSAGE"
	else
		printf "This an invalid option!\n"
	fi
}

lyrics_download() {
    TRACK="$1"
    SYNTAX="$2"
    PATH_OUTPUT_FILE="$3"

    display_message "warning" "Generating the '$PATH_OUTPUT_FILE' file..."

    ./paradise-lyrics.py --track "$TRACK" --syntax "$SYNTAX" > "$PATH_OUTPUT_FILE" && \
    	display_message "success" "Download successed :)" || \
	display_message "fail" "Something wrong happened :("
}

##############################
# Calling the functions
##############################

mkdir -p "$PATH_OUTPUT_DIRECTORY"/

lyrics_download "$TRACK_ID" "" "${PATH_OUTPUT_DIRECTORY}/${TRACK_NAME}_raw.${EXTENSION}"
lyrics_download "$TRACK_ID" "hh:mm:ss:ms" "${PATH_OUTPUT_DIRECTORY}/${TRACK_NAME}_hh_mm_ss_ms.${EXTENSION}"
lyrics_download "$TRACK_ID" "hh:mm:ss" "${PATH_OUTPUT_DIRECTORY}/${TRACK_NAME}_hh_mm_ss.${EXTENSION}"
lyrics_download "$TRACK_ID" "mm:ss:ms" "${PATH_OUTPUT_DIRECTORY}/${TRACK_NAME}_mm_ss_ms.${EXTENSION}"
lyrics_download "$TRACK_ID" "mm:ss" "${PATH_OUTPUT_DIRECTORY}/${TRACK_NAME}_mm_ss.${EXTENSION}"