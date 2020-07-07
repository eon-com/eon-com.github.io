#!/bin/bash

echo "updating runner"
sudo apt update && sudo apt upgrade -y

echo "installing python3"
sudo apt install python3 -y
