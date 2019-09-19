#!/usr/bin/env bash

read -p "Are you sure you want to destroy the VM, downloads, server, and all saves and backups?
(yes/n) > " -r
echo # (optional) move to a new line
if [[ "$REPLY" =~ ^yes$ ]]; then
    vagrant destroy -f

    rm ./persistent/downloads/ -rf
    rm ./persistent/server/ -rf
else
    echo "Aborting."
fi
