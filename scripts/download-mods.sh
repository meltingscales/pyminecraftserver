#!/usr/bin/env bash

# Import file lib fns
. file-lib.sh 2>/dev/null || . $SCRIPT_DIR/file-lib.sh

echo "hi lol"

echo "I download mods...im not DONE YET >:("

echo $DOWNLOAD_DIR
echo $SERVER_DIR
echo $SERVER_DIR/mods/

echo "oh look at you using env vars wow so portable :>)"

exit 0