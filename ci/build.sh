#!/bin/bash

# comment cause reasons...
# echo "updating runner"
# sudo apt update && sudo apt upgrade -y

echo "installing python3"
sudo apt install python3 -y

echo "install python3-pip"
sudo apt install python3-pip -y

echo "install 'SchnüffelStück' dependencies"
sudo pip3 install -r requirements.txt

echo "build meta data"
python3 meta.py

echo "collected meta data"
cat meta.json

echo "adding meta data to git"

git config --local user.email "eon_action@github.com"
git config --local user.name "EON GitHub Action"
git commit -m "adding new meta data" -a
