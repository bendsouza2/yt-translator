#!/bin/bash

cd ~/yt_translator
git pull origin main

# Copy custom settings file
if [ ! -f video_host/settings.py ]; then
    echo "Restoring settings.py..."
    cp /home/ubuntu/settings_backup/settings.py video_host/settings.py
fi

source /home/ubuntu/yt_translator/venv/bin/activate
python manage.py migrate

sudo systemctl stop gunicorn
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn


