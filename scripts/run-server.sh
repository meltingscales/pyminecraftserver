#!/usr/bin/env bash

# Recommended Java flags for servers.
# From <https://aikar.co/2018/07/02/tuning-the-jvm-g1gc-garbage-collector-flags-for-minecraft/>
JAVA_NONMEM_FLAGS="-XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=100 -XX:+DisableExplicitGC -XX:TargetSurvivorRatio=90 -XX:G1NewSizePercent=50 -XX:G1MaxNewSizePercent=80 -XX:G1MixedGCLiveThresholdPercent=35 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -Dusing.aikars.flags=mcflags.emc.gs"

# KB of mem on this system.
MEM_KB=$(awk '/MemTotal/ {print $2}' /proc/meminfo)

# MB of mem on this system.
MEM_MB=$(echo "$MEM_KB/1024" | bc)

# Max mem to use regardless of system memory.
MEM_CAP=6000

# Use 80% of memory.
MEM_RATIO=0.8

# Memory to use. Split off the dot.
MEM_TO_USE=$(echo "$MEM_MB*$MEM_RATIO" | bc | cut -f1 -d.)

# Cap memory.
if [[ $MEM_TO_USE -gt $MEM_CAP ]] ; then
    MEM_TO_USE=${MEM_CAP}
fi

if sudo netstat -tulpn | grep :25565; then
    echo 'Minecraft server is up because port 25565 is bound. See above command output for PID.'
elif ps -ax | grep "[f]orge-.*-universal.jar"; then
    echo 'Minecraft server is up because a Forge JAR is running but port 25565 is not bound yet.'
else
    echo 'Minecraft server is not running.'

    echo "Using ${MEM_TO_USE}MB of memory out of ${MEM_MB}MB with a ratio of ${MEM_RATIO} for Java."

    echo "Starting server..."

    if [[ -d /minecraft/server/ ]]; then
        pushd /minecraft/server/ #TODO: This should not be hardcoded!

    elif [[ -d ../persistent/server/ ]]; then
        pushd ../persistent/server/
    else
        echo "Could not find server directory!"
        exit 1
    fi

    java ${JAVA_NONMEM_FLAGS} -Xmx${MEM_TO_USE}M -jar "$(ls forge-*-universal.jar)"

    popd
fi
