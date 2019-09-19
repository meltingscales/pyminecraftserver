#!/usr/bin/env bash

read -p "Are you sure you want to destroy the downloads, server, and all saves and backups?
(y/n) > " -n 1 -r
echo # (optional) move to a new line
if [[ "$REPLY" =~ ^[Yy] ]]; then

    rm ./persistent/server/ -rf
    rm ./persistent/downloads/ -rf
fi