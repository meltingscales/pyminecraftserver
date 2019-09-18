# RLCraft-Vagrant

This is a Vagrant-enabled automatic setup for a modded Minecraft server pack
called RLCraft.

## Running

[Install Vagrant](https://www.vagrantup.com/), and run `vagrant up` in this
directory in a terminal.

Because I'm too dumb and lazy to figure out how to automate this, you need to
run `vagrant ssh` after doing this and then you need to run a few commands to
start the server.

The commands are:

`cd /minecraft/scripts/`
`./run-server.sh`

The password is `vagrant`, and the username is `vagrant`.

## Connecting

Connect on port `25565` with RLCraft.

There is also a map running on <http://127.0.0.1:8123>!

## Adding mods

Add mods to `scripts/mods.list` and then run `vagrant provision`.

See the file for the format. It should be somewhat obvious.

Then, restart your server.

Mods will be prefixed with an obvious identifier if you need to remove them.

## Crap! It broke!

If you think the downloads are f*#%ed or missing or corrupted, then delete the
`downloads` folder.

If you break the server somehow (delete a mod, etc), then delete the `server`
folder. It will be recreated.

If you don't want to delete everything, then just back up your world/config and
add it back in once the files are regenerated.

You don't need to necessarily delete the `world` folder or anything else.

### It's still broken!

Back up your `world` folder and config.

Delete this entire folder and all VMs in VirtualBox.

Re-download this repo.

Put the `world` folder and config back in.
