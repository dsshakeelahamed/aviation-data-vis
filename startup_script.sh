#!/bin/bash
sudo apt install git -y
sudo apt install python3-pip -y
cd /tmp
git clone https://github.com/dsshakeelahamed/aviation-data-vis.git
cd aviation-data-vis
pip3 install -r requirements.txt

#python3 start.py