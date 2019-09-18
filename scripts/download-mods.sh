#!/usr/bin/env bash

# Import file lib fns
. file-lib.sh 2>/dev/null || . $SCRIPT_DIR/file-lib.sh

# Mod directory
MOD_DIR="${SERVER_DIR}/mods/"

while read line; do

    echo "line:"
    echo $line

    # Split by pipe into array
    IFS='=' read -a arr <<< "$line"

    # Download file into mods directory
    download_file "$MOD_DIR/vagrant_auto_download_${arr[0]}" "${arr[1]}"

done < $SCRIPT_DIR/mods.list

exit 0