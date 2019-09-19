#!/usr/bin/env bash

read -p "Are you sure you want to destroy the downloads, server, and all saves and backups?
(yes/n) > " -r
echo # (optional) move to a new line
if [[ "$REPLY" =~ ^yes$ ]]; then

    rm ./persistent/server/ -rf
    rm ./persistent/downloads/ -rf
else
    echo "Aborting."
fi