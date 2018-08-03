#!/bin/bash

gcloud compute instances create healthcheck-instance --tags http-server \
--metadata startup-script='#! /bin/bash
# Installs apache and a custom homepage
sudo su -
apt-get update
apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common python3-pip
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
apt-get update
apt-get install -y docker-ce

git clone https://github.com/samiracho/HealthChecker.git
cd HealthChecker
pip3 install -r src/resources/requirements.txt

echo "Your system is ready to run HealthChecker"

EOF'