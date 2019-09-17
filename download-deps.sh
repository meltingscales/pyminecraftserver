#!/usr/bin/env bash

DOWNLOAD_PATH="/minecraft/persistent/downloads/"

RLCRAFT_SERVER_PACK_URL="https://www.curseforge.com/minecraft/modpacks/rlcraft/download/2780296/file"
RLCRAFT_SERVER_PACK_FILENAME="RLCraftServerPack-1.12.2-Beta-v2.5.zip"
RLCRAFT_SERVER_PACK_PATH="${DOWNLOAD_PATH}/${RLCRAFT_SERVER_PACK_FILENAME}"

# Download server path if it does not exist
if ! [ -f "$RLCRAFT_SERVER_PACK_PATH" ]; then
    wget "$RLCRAFT_SERVER_PACK_URL" -O "$RLCRAFT_SERVER_PACK_PATH"
fi