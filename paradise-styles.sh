#!/bin/sh

PATH_OUTPUT_DIRECTORY="./dist"
TRACK_ID="0nLiqZ6A27jJri2VCalIUs"

lyrics_download() {
    TRACK="$1"
    SYNTAX="$2"
    PATH_OUTPUT_FILE="$3"

    echo "Generating the $PATH_OUTPUT_FILE file..."

    ./paradise-lyrics.py --track "$TRACK" --syntax "$SYNTAX" > "$PATH_OUTPUT_FILE"
}

mkdir -p "$PATH_OUTPUT_DIRECTORY"

lyrics_download "$TRACK_ID" "" "${PATH_OUTPUT_DIRECTORY}/nothing_else_matters_raw.lrc"
lyrics_download "$TRACK_ID" "hhmmssmmm" "${PATH_OUTPUT_DIRECTORY}/nothing_else_matters_hhmmssmmm.lrc"
lyrics_download "$TRACK_ID" "hhmmss" "${PATH_OUTPUT_DIRECTORY}/nothing_else_matters_hhmmss.lrc"
lyrics_download "$TRACK_ID" "mmssmmm" "${PATH_OUTPUT_DIRECTORY}/nothing_else_matters_mmssmmm.lrc"
lyrics_download "$TRACK_ID" "mmss" "${PATH_OUTPUT_DIRECTORY}/nothing_else_matters_mmss.lrc"