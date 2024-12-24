#!/bin/bash

# Install Build Dependencies
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.10 python3.10-venv
sudo apt install -y libmysqlclient-dev default-libmysqlclient-dev build-essential pkg-config

#Clone the repo
git clone --branch main https://github.com/bendsouza2/yt-translator.git yt_translator
cd yt_translator

python3.10 -m venv venv

git config core.sparseCheckout true
echo "app/" >> .git/info/sparse-checkout
echo "requirements.txt" >> .git/info/sparse-checkout
git pull origin main

# Copy post-merge hook
cp hooks/post-merge .git/hooks/post-merge
chmod +x .git/hooks/post-merge
