#!/usr/bin/env bash

# Import file lib fns
. file-lib.sh 2>/dev/null || . $SCRIPT_DIR/file-lib.sh

echo "hi lol"

echo "I download mods...im not DONE YET >:("

echo $DOWNLOAD_DIR
echo $SERVER_DIR
echo $SERVER_DIR/mods/

MOD_DIR="${SERVER_DIR}/mods/"

echo "oh look at you using env vars wow so portable :>)"

while read line; do

    echo "line:"
    echo $line

    # Split by pipe into array
    IFS='=' read -a arr <<< "$line"

    # Download file into mods directory
    download_file "$MOD_DIR/vagrant_auto_download_${arr[0]}" "${arr[1]}"

done < $SCRIPT_DIR/mods.list

exit 0