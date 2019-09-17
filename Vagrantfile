MEMORY = 2048
CORES = 4


Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise64"

  config.vm.provision 'shell', run: 'once', path: 'download-deps.sh'

  config.vm.provider "virtualbox" do |v|
    v.memory = MEMORY
    v.cpus = CORES
  end

end
