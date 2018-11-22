#!/bin/bash

[ ! -d ~/eth-net-intelligence-api ] && mkdir ~/eth-net-intelligence-api
cd ~/eth-net-intelligence-api

[ ! -d "bin" ] && mkdir bin
[ ! -d "logs" ] && mkdir logs

# update packages
sudo update-alternatives --config python3
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y software-properties-common

# add ethereum repos
sudo add-apt-repository -y ppa:ethereum/ethereum-dev
sudo apt-get update -y

# install ethereum & install dependencies
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get -y install curl git build-essential

if [ ! -f /usr/bin/node ]; then
        curl -sL https://deb.nodesource.com/setup_8.x | sudo bash -
        sudo apt-get install -y build-essential git unzip wget nodejs ntp
fi
# add node symlink if it doesn't exist
# [[ ! -f /usr/bin/node ]] && sudo ln -s /usr/bin/nodejs /usr/bin/node

# set up time update cronjob
sudo bash -c "cat > /etc/cron.hourly/ntpdate << EOF
#!/bin/sh
pm2 flush
sudo service ntp stop
sudo ntpdate -s ntp.ubuntu.com
sudo service ntp start
EOF"

sudo chmod 755 /etc/cron.hourly/ntpdate

# add node service
cd ~/eth-net-intelligence-api/bin

[ ! -d "www" ] && git clone https://github.com/cubedro/eth-net-intelligence-api www
cd www
git pull

[[ ! -f ~/bin/processes.json ]] && cp -b ./processes-ec2.json ./../processes.json

#sudo npm install
sudo npm install pm2 -g

### fix npm modules depence
npm install chalk
npm install web3
npm install each-async
npm install async
npm install lodash
npm install debounce
npm install primus
npm install primus-emit
npm install primus-spark-latency
npm install websockets
npm install --save ws
sudo update-alternatives --config python3

echo "pm2 start processes.json"

