# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = nil
  config.vm.define "swap" do |swap|
    swap.vm.provider "docker" do |docker|
        docker.name = "swap"
        docker.image = "ezamriy/centos-7-vagrant-supervisor-ssh"
        docker.has_ssh = true
        docker.ports = ["9090:8080", "9000:8000"]
    end

    swap.vm.provision 'ansible' do |ansible|
        ansible.compatibility_mode = '2.0'
        ansible.playbook = 'playbook.yml'
        #ansible.verbose = true
    end

  end
end
