#!/usr/bin/env bash

# Import file lib fns
. file-lib.sh 2 > /dev/null || . $SCRIPT_DIR/file-lib.sh

# Mod directory
MOD_DIR="${SERVER_DIR}/mods/"

while read line; do

    # Split by equals sign into array
    IFS='=' read -a arr <<<"$line"

    # Download file into mods directory, make it obvious that it's automatically downloaded
    download_file "$MOD_DIR/_vagrant_auto_download_${arr[0]}" "${arr[1]}"

done < ${SCRIPT_DIR}/config/mods.list

exit 0