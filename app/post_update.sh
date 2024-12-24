#!/bin/bash

# Copy custom settings file
if [ ! -f settings.py ]; then
    echo "Restoring settings.py..."
    cp /home/ubuntu/settings_backup/settings.py settings.py
fi

source /home/ubuntu/yt_translator/venv/bin/activate
python manage.py migrate


