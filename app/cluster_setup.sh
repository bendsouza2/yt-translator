#!/bin/bash
set -e

# Install Build Dependencies
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.10 python3.10-venv
sudo apt install -y libmysqlclient-dev default-libmysqlclient-dev build-essential pkg-config

#Clone the repo
git clone --no-checkout --branch main https://github.com/bendsouza2/yt-translator.git yt_translator
cd yt_translator

python3.10 -m venv venv

git sparse-checkout init --cone
echo "app/" >> .git/info/sparse-checkout
echo "requirements.txt" >> .git/info/sparse-checkout
git checkout main

# Copy post-merge hook
if [ ! -f .git/hooks/post-merge ]; then
    cp hooks/post-merge .git/hooks/post-merge
    chmod +x .git/hooks/post-merge
else
    echo "post-merge hook already exists, skipping copy."
fi


if [ ! -f venv ]; then
	python3.10 -m venv venv
else
	echo "venv already exists, skipping venv creation"	
fi
