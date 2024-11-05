#!/bin/sh

cd /home/nikkasouza/i2i
source bin/activate
git stash
git pull
sudo $(which python) main.py