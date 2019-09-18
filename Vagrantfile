# frozen_string_literal: true

require 'fileutils'

# Hardware settings
MEMORY = (3 * 1024) # 5 GB in megabytes
CORES = 4

# Host directories to mount to guest vm
HOST_DIRS = {
    :DOWNLOAD_DIR => './persistent/downloads/',
    :SERVER_DIR => './persistent/server/',
    :SCRIPT_DIR => './scripts/',
}

# Guest directories to be mounted
GUEST_DIRS = {
    :DOWNLOAD_DIR => '/minecraft/downloads/',
    :SERVER_DIR => '/minecraft/server/',
    :SCRIPT_DIR => '/minecraft/scripts/',
}

# There must be the same amount of keys in these hashes.
raise "Must have identical directory names!
#{HOST_DIRS.keys} != #{GUEST_DIRS.keys}" unless (HOST_DIRS.keys == GUEST_DIRS.keys)

# Make sure host directories exist.
for tuple in HOST_DIRS
  dir = tuple[1]

  FileUtils.mkdir_p(dir)
end


Vagrant.configure('2') do |config|
  config.vm.box = 'alonsodomin/ubuntu-trusty64-java8'

  # Port for Minecraft.
  config.vm.network "forwarded_port", guest: 25565, host: 25565

  # Port for DynMap. See "mods.list" in scripts/.
  config.vm.network "forwarded_port", guest: 8123, host: 8123

  config.ssh.username = 'vagrant'
  config.ssh.password = 'vagrant'
  config.ssh.insert_key = false

  config.vm.provider 'virtualbox' do |v|
    v.memory = MEMORY
    v.cpus = CORES
  end


  # Disable default synced folder
  config.vm.synced_folder '.', '/vagrant', disabled: true

  # Mount all folders specified in hashes
  for folder_name in HOST_DIRS.keys

    # puts("LINK #{folder_name}...")

    # puts("#{HOST_DIRS[folder_name]} <---> #{GUEST_DIRS[folder_name]}")

    config.vm.synced_folder HOST_DIRS[folder_name], GUEST_DIRS[folder_name]
  end

  config.vm.provision 'shell', path: 'scripts/install-tools.sh', run: 'always'

  config.vm.provision 'shell', path: 'scripts/download-deps.sh', run: 'always', env: GUEST_DIRS

  config.vm.provision 'shell', path: 'scripts/download-mods.sh', run: 'always', env: GUEST_DIRS

  config.vm.provision 'shell', path: 'scripts/advice.sh', run: 'always', env: GUEST_DIRS


end
