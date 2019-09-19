#!/usr/bin/env bash

read -p "Are you sure you want to destroy the VM, server, and all saves and backups?
(y/n) > " -n 1 -r
echo # (optional) move to a new line
if [[ "$REPLY" =~ ^[Yy] ]]; then
    vagrant destroy -f

    rm ./persistent/downloads/ -rf
    rm ./persistent/server/ -rf
fi