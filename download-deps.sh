#!/usr/bin/env bash

DOWNLOAD_PATH="/minecraft/persistent/downloads/"
mkdir -p "$DOWNLOAD_PATH"

RLCRAFT_SERVER_PACK_URL="https://www.curseforge.com/minecraft/modpacks/rlcraft/download/2780296/file"
RLCRAFT_SERVER_PACK_PATH="${DOWNLOAD_PATH}/RLCraftServerPack-1.12.2-Beta-v2.5.zip"

FORGE_JAR_URL="http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.12.2-14.23.5.2803/forge-1.12.2-14.23.5.2803-universal.jar"
FORGE_JAR_PATH_FILE="${DOWNLOAD_PATH}/forge-1.12.2-14.23.5.2803-universal.jar"

MC_SERVER_JAR_URL="https://launcher.mojang.com/v1/objects/886945bfb2b978778c3a0288fd7fab09d315b25f/server.jar"
MC_SERVER_PATH_FILE="${DOWNLOAD_PATH}/server.jar"

# Download a file and make sure it exists.
# First arg is filepath, second is the URL.
function download_file() {
  FILEPATH="$1"
  URL="$2"

  if ! [ -f "$FILEPATH" ]; then
    echo "Downloading $(basename "$FILEPATH") to '$FILEPATH' from '$URL'..."
    wget "$URL" -O "$FILEPATH"
  else
    echo "File $(basename "$FILEPATH") already exists."
  fi

}

# Validate a SHA256 check file.
# First arg is the filepath, second is the checksum.
function validate_sha256() {
  FILEPATH="$1"
  GOOD_CHECKSUM="$2"

  FILE_CHECKSUM="$(sha256sum "$FILEPATH" | cut -f1 -d' ')"

  if [ "$FILE_CHECKSUM" = "$GOOD_CHECKSUM" ]; then
    echo "File $(basename $FILEPATH) is valid."
  else
    echo "File at $(basename $FILEPATH) gives bad checksum!"
    echo "[ Found  ] $FILE_CHECKSUM"
    echo "[ Expect ] $GOOD_CHECKSUM"
    exit 1
  fi
}

download_file "$RLCRAFT_SERVER_PACK_PATH" "$RLCRAFT_SERVER_PACK_URL"
validate_sha256 "$RLCRAFT_SERVER_PACK_PATH" "2f68b4ff3f8587c163309f6f4b23b8993dcedd79b32f2a828b5421fbc66511b9" || exit 1

download_file "$FORGE_JAR_PATH_FILE" "$FORGE_JAR_URL"
validate_sha256 "$FORGE_JAR_PATH_FILE" "a495a7fbcbde2cb34e6d2db108b4091f910e097ad38b94bef038cfc65c77f0a6" || exit 1

download_file "$MC_SERVER_PATH_FILE" "$MC_SERVER_JAR_URL"
validate_sha256 "$MC_SERVER_PATH_FILE" "fe1f9274e6dad9191bf6e6e8e36ee6ebc737f373603df0946aafcded0d53167e" || exit 1
