#!/usr/bin/env bash

DOWNLOAD_PATH="/minecraft/persistent/downloads/"
mkdir -p "$DOWNLOAD_PATH"

RLCRAFT_SERVER_PACK_URL="https://www.curseforge.com/minecraft/modpacks/rlcraft/download/2780296/file"
RLCRAFT_SERVER_PACK_PATH="${DOWNLOAD_PATH}/RLCraftServerPack-1.12.2-Beta-v2.5.zip"
RLCRAFT_SERVER_CHECKSUM_FILE="${DOWNLOAD_PATH}/RLCraftServerPack-1.12.2-Beta-v2.5.chk"

# Download server path if it does not exist
if ! [ -f "$RLCRAFT_SERVER_PACK_PATH" ]; then
  echo "Downloading server pack..."
  wget "$RLCRAFT_SERVER_PACK_URL" -O "$RLCRAFT_SERVER_PACK_PATH"
fi

pushd $DOWNLOAD_PATH
if sha256sum --check "$RLCRAFT_SERVER_CHECKSUM_FILE"; then
  echo 'Server pack file is valid.'
else
  echo "Server pack file at '$RLCRAFT_SERVER_PACK_PATH' is invalid. Re-download it!"
fi
popd
