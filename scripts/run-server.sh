#!/usr/bin/env bash

# KB of mem on this system.
MEM_KB=$(awk '/MemTotal/ {print $2}' /proc/meminfo)

# MB of mem on this system.
MEM_MB=$(echo "$MEM_KB/1024" | bc)

# Use 80% of memory.
MEM_RATIO=0.8

# Memory to use. Split off the dot.
MEM_TO_USE=$(echo "$MEM_MB*$MEM_RATIO" | bc | cut -f1 -d.)

if sudo netstat -tulpn | grep :25565; then
  echo 'Minecraft server is up because port 25565 is bound. See above command output for PID.'
elif ps -ax | grep "[f]orge-.*-universal.jar"; then
  echo 'Minecraft server is up because a Forge JAR is running but port 25565 is not bound yet.'
else
  echo 'Minecraft server is not running.'

  echo "Using ${MEM_TO_USE}MB of memory out of ${MEM_MB}MB with a ratio of ${MEM_RATIO} for Java."

  echo "Starting server..."

  pushd /minecraft/server/ #TODO: This should not be hardcoded!

  java -Xmx${MEM_TO_USE}M -Xms1G -jar "$(ls forge-*-universal.jar)" -XX:+UseConcMarkSweepGC -XX:+CMSIncrementalMode -XX:-UseAdaptiveSizePolicy -Xmn128M

  popd
fi
