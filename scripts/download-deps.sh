#!/usr/bin/env bash

#echo "given $DOWNLOAD_DIR and $SERVER_DIR"
#exit 1

# Import file lib fns
. file-lib.sh 2>/dev/null || . $SCRIPT_DIR/file-lib.sh

DOWNLOAD_PATH="$DOWNLOAD_DIR"
mkdir -p "$DOWNLOAD_PATH"

SERVER_PATH="$SERVER_DIR"
mkdir -p "$SERVER_PATH"

RLCRAFT_SERVER_PACK_URL="https://www.curseforge.com/minecraft/modpacks/rlcraft/download/2780296/file"
RLCRAFT_SERVER_PACK_PATH="${DOWNLOAD_PATH}/RLCraftServerPack-1.12.2-Beta-v2.5.zip"

FORGE_JAR_INSTALLER_URL="https://files.minecraftforge.net/maven/net/minecraftforge/forge/1.12.2-14.23.5.2803/forge-1.12.2-14.23.5.2803-installer.jar"
FORGE_JAR_INSTALLER_PATH_FILE="${DOWNLOAD_PATH}/forge-1.12.2-14.23.5.2803-installer.jar"

MC_VANILLA_SERVER_JAR_URL="https://launcher.mojang.com/v1/objects/886945bfb2b978778c3a0288fd7fab09d315b25f/server.jar"
MC_VANILLA_SERVER_PATH_FILE="${DOWNLOAD_PATH}/server.jar"


download_file "$RLCRAFT_SERVER_PACK_PATH" "$RLCRAFT_SERVER_PACK_URL"
validate_sha256 "$RLCRAFT_SERVER_PACK_PATH" "2f68b4ff3f8587c163309f6f4b23b8993dcedd79b32f2a828b5421fbc66511b9" || exit 1

download_file "$FORGE_JAR_INSTALLER_PATH_FILE" "$FORGE_JAR_INSTALLER_URL"
validate_sha256 "$FORGE_JAR_INSTALLER_PATH_FILE" "dd9c6134015712186ad3df8d8d79ddf59d9129d5e9b2300191fca46eab05547f" || exit 1

download_file "$MC_VANILLA_SERVER_PATH_FILE" "$MC_VANILLA_SERVER_JAR_URL"
validate_sha256 "$MC_VANILLA_SERVER_PATH_FILE" "fe1f9274e6dad9191bf6e6e8e36ee6ebc737f373603df0946aafcded0d53167e" || exit 1

# If the server installer doesn't exist, set it up.
if [ ! -f "${SERVER_PATH}/installer.jar" ]; then

  echo "Setting up Forge server..."

  cp "$FORGE_JAR_INSTALLER_PATH_FILE" "${SERVER_PATH}/installer.jar"
  pushd "$SERVER_PATH"
  java -jar "${SERVER_PATH}/installer.jar" --installServer

  # Run server for the first time.
  java -jar "$(ls forge-*-universal.jar)"

  # Accept EULA. Is this illegal? Probably. :p
  sed -i 's/false/true/g' eula.txt

  popd

  echo "Copying mods..."

  mkdir -p /tmp/modpack/
  unzip $RLCRAFT_SERVER_PACK_PATH -d /tmp/modpack/

  # The * is because it's a nested folder. Thanks guys.
  pushd /tmp/modpack/*
  cp -r ./* "$SERVER_PATH"
  popd

  rm -r /tmp/modpack/

fi

# Install a zipped modpack (containing mods/, config/, etc) to a server.
# First arg is server path,
# Second is a zip file path.
#
# If the zip file contains loose files (i.e. server-mod.zip!/config/), then
# They will be directly inserted.
#
# If the zip file contains a single folder (i.e. server-mod.zip!/modpack-name/config/) (cough THANKS RLCRAFT cough),
# Then the function will attempt to correct for that and still extract the files.
#
function install_modpack() {
    local SERVERPATH="$1"
    local mybutt="lol"
}