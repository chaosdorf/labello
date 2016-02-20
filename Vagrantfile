# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision :shell, path: "bootstrap.sh", run: "always"
  config.vm.network :forwarded_port, host: 8000, guest: 8000

  config.vm.provider :virtualbox do |vb|
    vb.gui = true
    vb.memory = "256"
  end

end
