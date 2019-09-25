#!/usr/bin/env bash

# Echo how many folders are in a directory.
function echo_number_folders() {
    echo $(ls -l "$1" | grep "^d" | wc -l)
}

# Echo how many files are in a directory.
function echo_number_files() {
    echo $(ls -l "$1" | grep "^-" | wc -l)
}

# Echo a file's size in bytes.
function echo_file_size_in_bytes() {
    du -B 1 "$1"  | cut -f1
}

# Download a file and make sure it exists.
# First arg is filepath, second is the URL.
function download_file() {
    local FILEPATH="$1"
    local URL="$2"

    if ! [[ -f "$FILEPATH" ]]; then
        echo "Downloading $(basename "$FILEPATH") to '$FILEPATH' from '$URL'..."

        wget "$URL" -O "$FILEPATH" -nv

        # If downloading the file fails,
        if [[ $? != "0" ]]; then # -nv means only show errors
            rm "$FILEPATH"
            echo "Downloading $URL failed!"
            exit 1
        fi

        # If the file is zero bytes,
        if [[ "$(echo_file_size_in_bytes "$FILEPATH")" = "0" ]]; then
            echo "File downloaded is empty!"
            rm "$FILEPATH"
            echo "Downloading $URL failed!"
            exit 1
        fi


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

    if [[ "$FILE_CHECKSUM" = "$GOOD_CHECKSUM" ]]; then
        echo "File $(basename "$FILEPATH") is valid."
    else
        echo "File at $(basename "$FILEPATH") gives bad checksum!"
        echo "[ Found  ] $FILE_CHECKSUM"
        echo "[ Expect ] $GOOD_CHECKSUM"
        exit 1
    fi
}
