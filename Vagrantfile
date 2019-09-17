# frozen_string_literal: true

MEMORY = 2048
CORES = 4

Vagrant.configure('2') do |config|
  config.vm.box = 'hashicorp/precise64'

  config.ssh.username = 'vagrant'
  config.ssh.password = 'vagrant'
  config.ssh.insert_key = false

  # Disable default synced folder
  config.vm.synced_folder '.', '/vagrant', disabled: true

  config.vm.synced_folder './persistent', '/minecraft/persistent/'

  config.vm.provision 'shell', path: 'download-deps.sh'

  config.vm.provider 'virtualbox' do |v|
    v.memory = MEMORY
    v.cpus = CORES
  end
end
