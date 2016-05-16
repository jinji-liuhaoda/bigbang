#!/bin/bash

echo date
source /home/jinji/envs/temple/bin/activate
export DJANGO_SETTINGS_MODULE=settings
export PYTHONPATH=/home/jinji/workspace/temple/web/temple:/home/jinji/workspace/temple/web:/home/jinji/workspace/temple
python /home/jinji/workspace/temple/scripts/update_user_info.py
echo date, 'done'
