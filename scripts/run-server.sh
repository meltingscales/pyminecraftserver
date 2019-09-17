#!/usr/bin/env bash

if sudo netstat -tulpn | grep :25565; then
  echo 'Minecraft server is up because port 25565 is bound. See above command output for PID.'
elif ps -ax | grep "[f]orge-.*-universal.jar"; then
  echo 'Minecraft server is up because a Forge JAR is running but port 25565 is not bound yet.'
else
  echo 'Minecraft server is not running.'

  echo "Starting server..."

  pushd /minecraft/server/

  java -Xmx3G -Xms1G -jar "$(ls forge-*-universal.jar)"

  popd
fi
