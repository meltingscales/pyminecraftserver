#!/usr/bin/env bash

# Echo how many folders are in a directory.
function echo_number_folders() {
    echo $(ls -l "$1" | grep "^d" | wc -l)
}

# Echo how many files are in a directory.
function echo_number_files() {
    echo $(ls -l "$1" | grep "^-" | wc -l)
}

# Download a file and make sure it exists.
# First arg is filepath, second is the URL.
function download_file() {
    local FILEPATH="$1"
    local URL="$2"

    if ! [ -f "$FILEPATH" ]; then
        echo "Downloading $(basename "$FILEPATH") to '$FILEPATH' from '$URL'..."
        wget "$URL" -O "$FILEPATH" -sS # -sS means silent but show errors
    else
        echo "File $(basename "$FILEPATH") already exists at '$FILEPATH'"
    fi

}

# Validate a SHA256 check file.
# First arg is the filepath, second is the checksum.
function validate_sha256() {
    local FILEPATH="$1"
    local GOOD_CHECKSUM="$2"

    local FILE_CHECKSUM="$(sha256sum "$FILEPATH" | cut -f1 -d' ')"

    if [ "$FILE_CHECKSUM" = "$GOOD_CHECKSUM" ]; then
        echo "File $(basename $FILEPATH) is valid."
    else
        echo "File at $(basename $FILEPATH) gives bad checksum!"
        echo "[ Found  ] $FILE_CHECKSUM"
        echo "[ Expect ] $GOOD_CHECKSUM"
        exit 1
    fi
}