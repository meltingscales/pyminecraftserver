MEMORY = 2048
CORES = 4


Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise64"

  # Disable default synced folder
  config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.synced_folder "./persistent", "/minecraft/persistent/"

  config.vm.provision 'shell', run: 'once', path: 'download-deps.sh'

  config.vm.provider "virtualbox" do |v|
    v.memory = MEMORY
    v.cpus = CORES
  end

end
